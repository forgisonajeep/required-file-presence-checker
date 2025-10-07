# Project Plan – Required File Presence Checker  
*LevelUp Bank Platform Engineering CI/CD Quality Enforcement*

---

## 🧩 Background
LevelUp Bank’s platform engineering team needs to enforce repository consistency across all service repos.  
Each repo must include essential baseline files like:
- `README.md`
- `.gitignore`

Without this consistency, CI/CD pipelines and deployment automation can break.  
To prevent that, the engineering team requested an **automated validation and audit system** using GitHub Actions and AWS CloudWatch.

This project implements that system.

---

## 🎯 Objective
Build a CI/CD-driven **Required File Presence Checker** that:
1. Validates repository structure (required files must exist).  
2. Blocks pull requests if required files are missing.  
3. Logs successful production validations to AWS CloudWatch.  
4. Keeps all credentials stored securely in GitHub Secrets.  

The project evolves in three tiers:
- **Foundational:** Local validation via Python.  
- **Advanced:** Pull request validation using GitHub Actions.  
- **Complex:** CloudWatch logging and environment secrets for audit visibility.

---

## ⚙️ Phase 0 – Repository Setup
### Folder Structure
At the start of the project, the repository was created with:
```
required-file-presence-checker/
├── README.md
├── .gitignore
├── check_required_files.py
└── .github/
    └── workflows/
```

### Key Notes:
- The `.github/workflows` folder stores CI workflow YAML files.
- The root directory holds the Python validation script.
- The `/docs` folder (this file) is for planning and documentation.

---

## 🪜 Phase 1 – Foundational (Local Validation)
**Goal:** Create and test the core validation logic before automating.

**File:** `check_required_files.py`

### Step-by-Step Breakdown
1. **Import modules**
   ```python
   import os
   import sys
   ```
   - `os` is used to check for file existence.
   - `sys` is used for exit codes (0 = success, 1 = failure).

2. **Define required files**
   ```python
   required = ["README.md", ".gitignore"]
   ```
   These are the baseline files every repo must contain.

3. **Check for missing files**
   ```python
   missing = [f for f in required if not os.path.isfile(f)]
   ```
   This list comprehension loops through each required file and checks if it exists.

4. **Handle results**
   ```python
   if missing:
       print("Missing required files:")
       for m in missing:
           print(f"- {m}")
       sys.exit(1)
   else:
       print("All required files are present.")
       sys.exit(0)
   ```

### Validation
**Command:**
```bash
python3 check_required_files.py
```

**Expected output (success):**
```
All required files are present.
```

**Expected output (failure):**
```
Missing required files:
- README.md
- .gitignore
```

---

## 🚀 Phase 2 – Advanced (Pull Request Validation)
**Goal:** Automate the validation process on every pull request.

**File:** `.github/workflows/on_pull_request.yml`

### Purpose
This workflow automatically runs the Python validation script each time a pull request targets the `main` branch.

### Steps
1. Checkout repository files.  
2. Set up Python in the GitHub Actions runner.  
3. Run `check_required_files.py`.  
4. Mark the pull request ✅ or ❌ depending on results.

### Example Workflow
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

### Outcome
- If all required files exist → PR passes.  
- If not → PR fails and cannot be merged until fixed.  

---

## ☁️ Phase 3 – Complex (Merge + AWS CloudWatch Logging)
**Goal:** Log successful production validations to AWS CloudWatch for auditing.

**File:** `.github/workflows/on_merge_to_main.yml`

### What It Does
- Triggers on every **push to main**.  
- Reruns the validation script.  
- If successful, sends a log entry to CloudWatch using the AWS CLI.  

### Key AWS Command Steps
```bash
aws logs create-log-stream \
  --log-group-name "$LOG_GROUP_NAME" \
  --log-stream-name "$TS_ISO" \
  --region "$REGION"

aws logs put-log-events \
  --log-group-name "$LOG_GROUP_NAME" \
  --log-stream-name "$TS_ISO" \
  --log-events "[{\"timestamp\":$(date +%s000),\"message\":\"Prod validation passed at $TS_ISO\"}]"
```

### Example CloudWatch Log
```
Prod validation passed at 2025-10-07T01:15Z
```

---

## 🔐 GitHub Secrets & Environments
**Environments created:**
- `beta` → used for pull requests  
- `prod` → used for main merges  

**Secrets configured per environment:**
| Secret | Description | Example Value |
|--------|--------------|----------------|
| `AWS_ACCESS_KEY_ID` | IAM Access Key ID | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | IAM Secret Key | `wJalrXUtnFEMI/...` |
| `AWS_REGION` | AWS Region | `us-east-1` |
| `LOG_GROUP_NAME` | CloudWatch Log Group | `/github-actions/required-file-presence-check/prod` |

> 💡 *Never hardcode credentials or regions directly into code or workflows.*

---

## 🧪 Testing Strategy
| Test Type | Description | Trigger | Expected Result |
|------------|--------------|----------|----------------|
| Local Test | Run Python script manually | Terminal | Prints missing files or passes |
| Beta Workflow | Open a PR | GitHub Actions | Fails if files missing |
| Prod Workflow | Merge to main | GitHub Actions | Logs success to CloudWatch |

---

## 📈 Validation Results
| Tier | Verified Outcome |
|------|------------------|
| Foundational | Script runs locally and detects missing files correctly. |
| Advanced | Pull request validation runs and blocks merges with missing files. |
| Complex | Successful merges trigger CloudWatch logging with proper secrets. |

---

## 🧠 Lessons Learned
- Small scripts can enforce strong structural policies.  
- GitHub Actions is a simple but powerful CI/CD entry point.  
- AWS CloudWatch is ideal for audit trails and long-term tracking.  
- Secrets management is essential for security and compliance.  

---

## 👤 Author
**Cameron A. Parker**  
LevelUp Bank – Platform Engineering CI/CD Enforcement Project  
GitHub: [forgisonajeep](https://github.com/forgisonajeep)