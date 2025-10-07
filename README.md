# Required File Presence Checker
### Automated CI/CD Validation and CloudWatch Logging for LevelUp Bank

##  Project Overview
This project simulates **LevelUp Bank’s internal platform engineering policy enforcement system.** It automatically checks whether every service repository contains the required baseline files before code merges into production and logs all successful validation runs to **AWS CloudWatch** for audit visibility.

##  Objective
Implement a CI/CD-driven quality gate that:
-  Enforces repository structure standards  
-  Fails pull requests missing required files  
-  Logs successful validation results to **AWS CloudWatch**  
-  Uses environment-specific secrets for **beta** (PRs) and **prod** (merges)

##  Project Breakdown
This project was built in three tiers — **Foundational**, **Advanced**, and **Complex** — each layer expanding on the previous one until full CI/CD automation with AWS CloudWatch logging was achieved.

**Foundational Tier:** Focused on creating a simple Python validation script named `check_required_files.py`. This script checks for the presence of required baseline files (e.g., `README.md`, `.gitignore`) and exits with an error if any are missing. Example command and output: `$ python3 check_required_files.py` → `All required files are present.`  

**Advanced Tier:** Introduced GitHub Actions to automate the validation process. The workflow file `.github/workflows/on_pull_request.yml` runs automatically whenever a pull request is opened. It sets up Python, executes the file presence check, and blocks merges if required files are missing. This ensures every pull request meets repository structure requirements before approval.  

**Complex Tier:** Added AWS CloudWatch logging on successful merges to `main`. The second workflow, `.github/workflows/on_merge_to_main.yml`, runs automatically on `push` to `main`. It validates files again and logs a success event to **AWS CloudWatch** using securely stored GitHub Secrets:
- `${{ secrets.AWS_ACCESS_KEY_ID }}`
- `${{ secrets.AWS_SECRET_ACCESS_KEY }}`
- `${{ secrets.AWS_REGION }}`
- `${{ secrets.LOG_GROUP_NAME }}`  

Example CloudWatch log entry: `Prod validation passed at 2025-10-07T01:15Z`  

##  Technologies Used
- **Python 3.x**
- **GitHub Actions**
- **AWS CloudWatch**
- **IAM + Secrets Management**
- **Bash scripting**

##  Validation Summary
| Tier | Description | Verification |
|------|--------------|---------------|
| Foundational | Local Python script to verify required files | Ran locally → “All required files are present.” |
| Advanced | GitHub Actions PR validation | Triggered on pull requests to `demo/pr-1` |
| Complex | Prod logging to CloudWatch | Triggered on merge to `main`, logs success event to AWS CloudWatch |

##  Final Results
 **All three tiers completed and validated successfully:** Foundational Python script functional, Advanced PR automation working, and Complex CloudWatch logging confirmed (prod environment).  

**CloudWatch Log Group:** `/github-actions/required-file-presence-check/prod`  

**Validation Workflow Runs (GitHub Actions):**
-  `Fix CloudWatch JSON formatting for prod logging` — success  
-  `Required Files Check (Prod)` — passing on merge to main  
-  `Required Files Check (Beta)` — passing on pull request  

##  Author
**Cameron A. Parker**  
_LevelUp Bank – Platform Engineering CI/CD Enforcement Project_  
GitHub: [forgisonajeep](https://github.com/forgisonajeep)