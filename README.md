# Password Strength Validator — CSY3056 AS1

A small Python component that classifies a password as **very weak, weak, medium or strong**
based on length, character variety, Shannon entropy, and a blocklist of well-known leaked
passwords. The validator is the thin-slice component of a wider user-authentication system.

## Layout

```
src/        - validator (component.py) and demo CLI (app.py)
tests/      - pytest suite covering normal, edge, invalid, failure and decision-path cases
Dockerfile  - builds a slim Python 3.11 image that runs the demo CLI by default
Jenkinsfile - four-stage pipeline: checkout, build image, run tests, demo run
```

## Running locally

```powershell
python -m pip install -r requirements.txt
python -m pytest -v
python -m src.app
```

## Running via Docker

```powershell
docker build -t password-validator .
docker run --rm password-validator                                # runs the demo CLI
docker run --rm password-validator python -m pytest -v            # runs the tests
```

## Why this component

The brief rewards components that involve decision-making, validation, classification, rule
checking and different outcomes. A password validator hits all five. The deliberate
differentiators from a textbook submission are: Shannon entropy used alongside rule checks,
a leaked-password blocklist that overrides everything else, and a configurable `Policy`
dataclass so the same validator can serve different sites.

See the technical report for the full design rationale, testing strategy, CI/CD reasoning,
evaluation, and ethics discussion.
