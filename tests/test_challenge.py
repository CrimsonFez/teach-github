import contextlib
import io
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest import mock

import challenge


class ChallengeTests(unittest.TestCase):
    def test_result_is_a_deterministic_integer_in_range(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            first = challenge.generate_number()
            second = challenge.generate_number()
        self.assertIs(type(first), int)
        self.assertTrue(1 <= first <= 100, "The number must be between 1 and 100.")
        self.assertTrue(first == second, "Repeated runs must produce the same number.")
        self.assertTrue(output.getvalue() == "", "Importing and calling must be quiet.")

    def test_every_room_is_visited_exactly_once(self):
        maze = Path(challenge.__file__).resolve().parent / "maze"
        expected = {"maze." + path.stem for path in maze.glob("room_*.py")}
        self.assertEqual(len(expected), 200)
        self.assertEqual(challenge.ROOM_COUNT, 200)
        visited = []
        real_import = challenge.import_module

        def record_import(name):
            visited.append(name)
            return real_import(name)

        with mock.patch.object(challenge, "import_module", side_effect=record_import):
            state = challenge.walk()
        self.assertIs(type(state), int)
        self.assertTrue(0 <= state < (1 << 128), "The carried state must remain bounded.")
        self.assertEqual(len(visited), 200)
        self.assertEqual(set(visited), expected)

    def test_cli_prints_only_one_integer(self):
        result = subprocess.run(
            [sys.executable, str(Path(challenge.__file__).resolve())],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stderr == "", "The program must not write to stderr.")
        self.assertTrue(
            re.fullmatch(r"(?:[1-9][0-9]?|100)\n", result.stdout) is not None,
            "The program must print exactly one integer from 1 to 100 and a newline.",
        )


if __name__ == "__main__":
    unittest.main()
