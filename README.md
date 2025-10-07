# Required File Presence Checker
LevelUp Bank – CI/CD automation that validates required repository files and logs successful production runs to AWS CloudWatch.

## Project Overview
This repository enforces a baseline structure policy for LevelUp Bank’s engineering teams. It checks that required files (like README.md and .gitignore) exist in each repository. The validation runs locally and in GitHub Actions. Pull requests are blocked if the requirements are not met (beta). Merges to main re-run the check and log a success event to AWS CloudWatch (prod).

## Objectives
- Enforce repository structure standards automatically.
- Fail pull requests that are missing required files.
- Log successful production validations to AWS CloudWatch.
- Keep all credentials in GitHub Secrets (no hardcoding).

## Project Tiers (Foundational → Advanced → Complex)
FOUNDATIONAL (Python Script)
- File: check_required_files.py
- Purpose: verify required files exist at the repo root; print any missing; exit non-zero on failure.
- Local run and expected output:
  $ python3 check_required_files.py
  # Expected success:
  # All required files are present.

ADVANCED (GitHub Actions on Pull Requests)
- File: .github/workflows/on_pull_request.yml
- Trigger: pull_request → main
- Purpose: checkout repo, set up Python, run check_required_files.py, and block merges if files are missing.
- Minimal workflow (YAML):
  name: Required Files Check (Beta)
  on:
    pull_request:
      branches: [ main ]
  jobs:
    validate:
      runs-on: ubuntu-latest
      environment: beta
      steps:
        - name: Checkout
          uses: actions/checkout@v4
        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.x"
        - name: Run file presence check
          run: python3 check_required_files.py

COMPLEX (GitHub Actions on push to main + CloudWatch logging)
- File: .github/workflows/on_merge_to_main.yml
- Trigger: push → main
- Purpose: re-run validation and, on success, send a log entry to AWS CloudWatch using environment secrets.
- Minimal workflow (YAML):
  name: Required Files Check (Prod)
  on:
    push:
      branches: [ main ]
  jobs:
    validate:
      runs-on: ubuntu-latest
      environment: prod
      steps:
        - name: Checkout
          uses: actions/checkout@v4
        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.x"
        - name: Run file presence check
          run: python3 check_required_files.py
        - name: Log success to CloudWatch (prod)
          if: success()
          env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_REGION: ${{ secrets.AWS_REGION }}
            LOG_GROUP_NAME: ${{ secrets.LOG_GROUP_NAME }}
          run: |
            REGION="${AWS_REGION:-us-east-1}"
            echo "Using region: $REGION"
            echo "Using log group: $LOG_GROUP_NAME"
            TS_ISO=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
            aws logs create-log-stream \
              --log-group-name "$LOG_GROUP_NAME" \
              --log-stream-name "$TS_ISO" \
              --region "$REGION" || true
            aws logs put-log-events \
              --log-group-name "$LOG_GROUP_NAME" \
              --log-stream-name "$TS_ISO" \
              --log-events "[{\"timestamp\":$(date +%s000),\"message\":\"Prod validation passed at $TS_ISO\"}]" \
              --region "$REGION"
- Example CloudWatch message:
  Prod validation passed at 2025-10-07T01:15Z

## Environment Secrets (kept in GitHub → Settings → Environments)
Create an environment named prod (and optionally beta). Add the following secrets (names must match exactly). Do NOT hardcode these in code or workflows; they are read at runtime as ${{ secrets.NAME }}.
- AWS_ACCESS_KEY_ID → IAM access key ID (from your AWS IAM user)
- AWS_SECRET_ACCESS_KEY → IAM secret access key (from your AWS IAM user)
- AWS_REGION → e.g., us-east-1
- LOG_GROUP_NAME → e.g., /github-actions/required-file-presence-check/prod

## How to Run Locally
1) From repo root (same level as README.md and .gitignore), run:
   $ python3 check_required_files.py
2) To test failure: temporarily rename README.md and run again; the script should list missing files and exit non-zero.

## How to Trigger in CI
- Beta validation: open a pull request to main (on_pull_request.yml runs).
- Prod validation + logging: push/merge to main (on_merge_to_main.yml runs and logs to CloudWatch).

## Technologies Used
Python 3.x, GitHub Actions, AWS CloudWatch, IAM, GitHub Secrets.

## Validation Summary
- Foundational: local script passes when required files are present.
- Advanced: PR workflow blocks merges if required files are missing.
- Complex: production workflow logs success to CloudWatch using environment secrets.

## Author
Cameron A. Parker — LevelUp Bank, Platform Engineering CI/CD Enforcement Project — https://github.com/forgisonajeep