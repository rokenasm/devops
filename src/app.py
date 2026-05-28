"""
Small demo CLI for the password strength validator.

This is what the Docker image runs by default. The point is to have something
that produces visible, meaningful output for the "successful Docker run"
screenshot - if the container just printed "Hello World" the marker would
have no evidence that the component itself actually works inside the image.

I picked four sample passwords chosen to hit all four bands so the demo
also doubles as a quick sanity check after building the image.
"""

from src.component import check_password


SAMPLES = [
    "abc",                # expected: very weak (too short, no classes)
    "password",           # expected: very weak (blocklisted)
    "abcdefghij",         # expected: weak (no upper / digit / symbol)
    "Hello12!",           # expected: medium
    "Tr0ub4dor&3xK!",     # expected: strong
]


def main() -> None:
    print("Password strength validator - sample run")
    print("-" * 50)
    for pwd in SAMPLES:
        result = check_password(pwd)
        # Padding the password column makes the output line up neatly in
        # the screenshot, which makes the demo easier to read.
        reasons = ", ".join(result["reasons"]) if result["reasons"] else "(none)"
        print(f"{pwd:<20} -> {result['band']:<10} "
              f"score={result['score']:<3} entropy={result['entropy']:.2f}")
        print(f"{'':<20}    reasons: {reasons}")
    print("-" * 50)


if __name__ == "__main__":
    main()
