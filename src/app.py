"""Demo CLI for the password validator.

Five sample passwords picked to hit every band. Runs by default when the
Docker image starts.
"""

from src.component import check_password


SAMPLES = [
    "abc",
    "password",
    "abcdefghij",
    "Hello12!",
    "Tr0ub4dor&3xK!",
]


def main() -> None:
    print("Password strength validator - sample run")
    print("-" * 50)
    for pwd in SAMPLES:
        result = check_password(pwd)
        reasons = ", ".join(result["reasons"]) if result["reasons"] else "(none)"
        print(f"{pwd:<20} -> {result['band']:<10} "
              f"score={result['score']:<3} entropy={result['entropy']:.2f}")
        print(f"{'':<20}    reasons: {reasons}")
    print("-" * 50)


if __name__ == "__main__":
    main()
