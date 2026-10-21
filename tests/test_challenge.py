import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest

import challenge


class ChallengeTests(unittest.TestCase):
    def test_exactly_200_nonblank_lines(self):
        lines = Path(challenge.__file__).read_text().splitlines()
        self.assertEqual(len(lines), 200)
        self.assertTrue(all(line.strip() for line in lines))

    def test_fixed_seeds_are_deterministic_integers_in_range(self):
        for seed in (0, 1, 0x123456789ABCDEF0, (1 << 64) - 1):
            with self.subTest(seed=seed), contextlib.redirect_stdout(io.StringIO()) as output:
                first = challenge.generate_number(seed)
                self.assertIs(type(first), int)
                self.assertTrue(1 <= first <= 100)
                self.assertEqual(first, challenge.generate_number(seed))
                self.assertEqual(output.getvalue(), "")

    def test_seed_is_required_for_direct_invocation(self):
        environment = {key: value for key, value in os.environ.items() if key != "CHALLENGE_SEED"}
        result = subprocess.run([sys.executable, challenge.__file__], env=environment,
                                capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("Fork the repository", result.stderr)

    def test_supplied_seed_prints_only_one_integer(self):
        environment = dict(os.environ, CHALLENGE_SEED="123456789abcdef0")
        result = subprocess.run([sys.executable, challenge.__file__], env=environment,
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\A(?:[1-9][0-9]?|100)\n\Z")


if __name__ == "__main__":
    unittest.main()
