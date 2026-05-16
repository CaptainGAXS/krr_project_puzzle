#!/usr/bin/env python3
"""
Run an ASP program with clingo and categorize the execution time.
Usage: python classifier.py <clingo_command>
Example: python classifier.py "clingo myprogram.lp"
"""

import subprocess
import sys
import time


def categorize_time(seconds: float) -> str:
    """
    Categorize the execution time into difficulty levels.
    Adjust the thresholds below to fit your needs.
    """
    if seconds <= 60.0:
        return "Very Easy"
    elif seconds <= 600.0:
        return "Easy"
    elif seconds < 1800.0:
        return "Medium"
    elif 5400.0 >= seconds >= 1800.0:
        return "Hard"
    else:
        return "Harder"


def run_clingo(command: str) -> dict:
    """
    Run the given clingo command and measure its execution time.
    """
    print(f"Running: {command}\n")

    start = time.perf_counter()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        print("Error: clingo not found. Make sure it is installed and in your PATH.")
        sys.exit(1)

    end = time.perf_counter()
    duration = end - start

    return {
        "duration": duration,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def print_results(result: dict) -> None:
    category = categorize_time(result["duration"])

    print("=" * 50)
    print("CLINGO OUTPUT")
    print("=" * 50)
    if result["stdout"]:
        print(result["stdout"])
    if result["stderr"]:
        print("[stderr]")
        print(result["stderr"])

    print("=" * 50)
    print(f"Return code : {result['returncode']}")
    print(f"Duration    : {result['duration']:.4f} seconds")
    print(f"Difficulty  : {category}")
    print("=" * 50)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_clingo.py <clingo_command>")
        print('Example: python run_clingo.py "clingo myprogram.lp"')
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    result = run_clingo(command)
    print_results(result)


if __name__ == "__main__":
    main()