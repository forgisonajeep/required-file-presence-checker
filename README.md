# Required File Presence Checker  
*A CI/CD automation project for LevelUp Bank’s engineering team.*

---

##  Project Overview
This project automates a structural validation process for LevelUp Bank’s repositories.  
Each service repository must include certain baseline files—like `README.md` and `.gitignore`—before code is merged into the main branch.  

Using **Python** and **GitHub Actions**, this project:  
- Automatically checks for required files.  
- Blocks pull requests if files are missing.  
- Logs successful production checks to **AWS CloudWatch** for auditing.  
- Stores all credentials securely in **GitHub Secrets** (never hardcoded).  

---

##  How It Works – Three Phases of Automation

### 1️ Local Validation (Python Script)
Before automation, the validation can be tested locally with a simple Python script.

**File:** `check_required_files.py`

**What it does:**  
- Verifies required files (`README.md` and `.gitignore`) exist in the repo root.  
- Prints any missing files and exits with an error code (1) if something is missing.  
- Exits silently (code 0) when everything passes.

**Run locally:**
```bash
python3 check_required_files.py
```

**Expected output when all files exist:**
```bash
All required files are present.
```

**If a required file is missing:**
```bash
Missing required files:
- README.md
- .gitignore
```

---

### 2️ Pull Request Validation (GitHub Actions – Beta Environment)
Once local validation works, automation is added using **GitHub Actions**.  
This workflow runs every time a **pull request** is opened toward the `main` branch.

**Purpose:**  
- Automatically check required files.  
- Prevent merging when files are missing.  
- Run safely in a “beta” environment to test changes.

**Workflow file:** `.github/workflows/on_pull_request.yml`

**What happens under the hood:**  
1. The code is checked out.  
2. Python is set up in the runner.  
3. The script runs automatically.  
4. If validation fails, the pull request shows an ❌ failure.

**Example workflow:**
```yaml
name: Required Files Check (Beta)
on:
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    environment: beta
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Run file presence check
        run: python3 check_required_files.py
```

If all required files are present, GitHub marks the check ✅ **Passed** and the PR can be merged.

---

### 3️ Production Validation (Main Merge + CloudWatch Logging)
After a pull request is merged into the `main` branch, another workflow runs to perform the same check in **production mode** and log success to AWS CloudWatch.

**Workflow file:** `.github/workflows/on_merge_to_main.yml`

**Purpose:**  
- Confirm the repo structure after merge.  
- Log audit details (timestamp, workflow name, commit SHA, actor) to CloudWatch.  
- Use GitHub environment secrets for secure AWS access.

**Workflow example:**
```yaml
name: Required Files Check (Prod)
on:
  push:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    environment: prod

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Run file presence check
        run: python3 check_required_files.py

      - name: Log success to CloudWatch
        if: success()
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.AWS_REGION }}
          LOG_GROUP_NAME: ${{ secrets.LOG_GROUP_NAME }}
        run: |
          REGION="${AWS_REGION:-us-east-1}"
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
```

 **Example CloudWatch message:**
```bash
Prod validation passed at 2025-10-07T01:15Z
```

---

##  Repository Structure
```bash
required-file-presence-checker/
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml       # Validates required files on pull requests (Beta)
│       └── on_merge_to_main.yml      # Logs validation success to CloudWatch (Prod)
│
├── docs/
│   └── project-plan.md               # Full breakdown of project phases and design reasoning
│
├── check_required_files.py           # Python script enforcing required file presence
├── .gitignore                        # Git ignore patterns
└── README.md                         # Main project documentation
```

---

###  How to Navigate the Repo
This repository is organized to mirror real-world DevOps workflow stages — **Foundational → Advanced → Complex** — each tier building on the previous one:

- ** Foundational:**  
  Focuses on the Python validation script (`check_required_files.py`) and basic GitHub repository setup.  
  You’ll see how the script enforces required files and ensures a project’s baseline structure before code review.

- ** Advanced:**  
  Introduces **GitHub Actions automation** through `.github/workflows/on_pull_request.yml`.  
  This workflow automatically runs the validation script whenever a **pull request** is opened to the `main` branch, enforcing structure compliance in the **Beta** environment.

- ** Complex:**  
  Extends the automation to include **AWS CloudWatch logging** via `.github/workflows/on_merge_to_main.yml`.  
  This ensures all successful validations are logged to a CloudWatch group (for **Prod** auditing), providing visibility into repository compliance events.

Each directory and file directly supports one of these tiers:
- `/` → Foundational  
- `.github/workflows/` → Advanced + Complex  
- `/docs/` → Supporting documentation and long-form project plan  

Together, these components demonstrate a **complete CI/CD quality gate system** — from local validation to cloud-based audit logging — all driven by GitHub Actions.

---

###  Quick Start

Follow these steps to explore and test the **Required File Presence Checker** project locally and through GitHub Actions:

#### 1. **Clone the Repository**
```bash
git clone https://github.com/forgisonajeep/required-file-presence-checker.git
cd required-file-presence-checker
```

#### 2. **Run the Validation Script Locally**
Before using GitHub Actions, verify the Python script locally:
```bash
python3 check_required_files.py
```
Expected output (if all required files exist):
```
All required files are present.
```

If any are missing, you’ll see a list like:
```
Missing required files:
- README.md
- .github/workflows/on_pull_request.yml
```

#### 3. **Trigger the GitHub Actions Workflows**
The repository has **two automated workflows**:

| Workflow | Trigger | Purpose |
|-----------|----------|----------|
| `.github/workflows/on_pull_request.yml` | When a pull request is opened | Validates required files in **Beta** environment. |
| `.github/workflows/on_merge_to_main.yml` | When code merges to main | Logs successful validation results to **AWS CloudWatch (Prod)**. |

To test:
1. Create a new branch and make a small change.  
2. Open a **Pull Request** → triggers Beta validation.  
3. Merge into **main** → triggers Prod CloudWatch logging.

#### 4. **View Results**
- Go to the **Actions tab** in GitHub.  
- Select the latest workflow run to view validation results and CloudWatch logging output.  

---

###  Example Success Output
```bash
All required files are present.
Beta validation passed.
Prod validation logged to CloudWatch.
```

---

### Pro Tip
If you’re using AWS CloudWatch for the first time, check your region under **us-east-1 → Log groups → /RequiredFilePresenceChecker** to confirm log delivery.

---

##  Setting Up Environments & Secrets
In GitHub → **Settings → Environments**, create two environments:  
- **beta** (for pull requests)  
- **prod** (for merges to main)  

Each must include these secrets:
- `AWS_ACCESS_KEY_ID` → IAM user access key ID  
- `AWS_SECRET_ACCESS_KEY` → IAM user secret key  
- `AWS_REGION` → region (example: `us-east-1`)  
- `LOG_GROUP_NAME` → CloudWatch log group (example: `/github-actions/required-file-presence-check/prod`)

>  **Note:** No credentials or region names should ever appear directly in your code or YAML files.

---

##  How to Test the Project
**Local test:**
```bash
1. Run python3 check_required_files.py
2. Rename or delete a file to trigger failure.
3. Observe the printed “Missing required files” message.
```

**Pull request test (Beta):**
```bash
1. Create a new branch.
2. Delete .gitignore temporarily.
3. Open a pull request → GitHub Actions runs automatically and fails.
4. Restore .gitignore → push → rerun the workflow → it passes ✅.
```

**Main merge test (Prod):**
```bash
1. Merge your pull request into main.
2. Visit the Actions tab → look for the “Prod Validation” workflow.
3. Once successful, open CloudWatch → Log Groups → confirm the event appears.
```

---

##  Validation Summary
| Phase | Environment | Trigger | Expected Outcome |
|-------|--------------|----------|------------------|
| Local | Local terminal | Manual run | Prints missing files or success |
| Beta | GitHub Actions | Pull request | Blocks merge if missing |
| Prod | GitHub Actions | Push to main | Logs success to CloudWatch |

---

##  Key Takeaways
- Validate repo structure with a single lightweight Python script.  
- Automate checks with GitHub Actions for both pull requests and merges.  
- Keep credentials out of code by using GitHub Secrets.  
- Use AWS CloudWatch for a permanent audit trail of successful runs.  
- Reuse this pattern for any type of repository compliance enforcement.

---

##  Author
**Cameron A. Parker**  
LevelUp Bank – Platform Engineering CI/CD Enforcement Project  
GitHub: [forgisonajeep](https://github.com/forgisonajeep)