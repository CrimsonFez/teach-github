# The 200-file challenge

One fixed integer from **1 to 100**, hidden behind a chain of **200 Python files**.
The first person to report the correct number to **Hazel** wins.

## Play

1. [Fork this repository](https://github.com/hazelfjeld/teach-github/fork).
2. Clone your fork, replacing `YOUR-USERNAME` below with your GitHub username:

   ```sh
   git clone https://github.com/YOUR-USERNAME/teach-github.git
   cd teach-github
   ```

3. Run the challenge with **Python 3.8 or newer**:

   ```sh
   python3 challenge.py
   ```

4. Report the number to Hazel.

Python's standard library is all you need. There is nothing to install with pip.

## The puzzle

`challenge.py` follows a shuffled route through every math file in `maze/`.
Each file transforms the previous file's result and points to the next file.
The last result becomes a single integer from 1 to 100, and everyone gets the same number.

Forking is part of the exercise, but public code can also be downloaded and run without a fork.

## Checks

```sh
python3 -m unittest discover -s tests -v
```

The checks verify the result and the complete 200-file route without printing the answer.
