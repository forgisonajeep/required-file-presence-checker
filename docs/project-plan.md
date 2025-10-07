# Project Plan – Required File Presence Checker  
*LevelUp Bank | CI/CD Automation Initiative*  

---

##  Project Objective
LevelUp Bank’s engineering leadership requires all internal repositories to include baseline documentation and structure files before merging any code.  
This project builds a **CI/CD quality gate** using **Python** and **GitHub Actions** that automatically validates the presence of key files and logs successful validation results to **AWS CloudWatch**.

The automation ensures:
- Every repository follows consistent structure standards.  
- Missing documentation is caught before merge.  
- Successful checks are logged for compliance and audit visibility.

---

##  Foundational Phase – Local Validation

**Goal:** Build and test a local validation script.  
**File:** `check_required_files.py`  

**Key tasks:**
- Verify that `README.md` and `.gitignore` exist in the repository root.  
- Print missing files with clear messages.  
- Exit with `0` if all files exist or `1` if any are missing.  

**Example command:**
```bash
python3 check_required_files.py
```

**Expected output:**
```bash
All required files are present.
```
or:
```bash
Missing required files:
- README.md
```

This phase proves that the validation logic works independently of automation.

---

##  Advanced Phase – GitHub Actions (Beta)

**Goal:** Automate validation through GitHub Actions on pull requests.  
**File:** `.github/workflows/on_pull_request.yml`  

**Trigger:**  
```yaml
on:
  pull_request:
    branches: [ main ]
```

**Process:**
1. Checkout the repository.  
2. Install and configure Python.  
3. Run the validation script automatically.  
4. Fail the workflow if any required file is missing.  

**Outcome:**  
Pull requests cannot be merged until the repository structure meets baseline requirements.  
This serves as the **“Beta Environment”** to test changes before production.

---

##  Complex Phase – AWS CloudWatch Logging (Prod)

**Goal:** Extend validation to production merges and log successful checks to AWS CloudWatch.  
**File:** `.github/workflows/on_merge_to_main.yml`  

**Trigger:**  
```yaml
on:
  push:
    branches: [ main ]
```

**Steps:**
1. Run the validation script again post-merge.  
2. Use AWS CLI to send an audit log to CloudWatch:
   - Workflow name  
   - Commit SHA  
   - Actor (GitHub user)  
   - Timestamp (UTC ISO format)  

**Example CloudWatch Message:**
```
Prod validation passed at 2025-10-07T01:15Z
```

**Environments & Secrets (via GitHub → Settings → Environments):**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `LOG_GROUP_NAME`

This ensures all credentials remain secure and non-hardcoded.

---

##  Repository Structure
```bash
required-file-presence-checker/
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml
│       └── on_merge_to_main.yml
│
├── docs/
│   └── project-plan.md
│
├── check_required_files.py
├── .gitignore
└── README.md
```

---

##  Testing Plan

**1️ Local Test:**  
Run the script manually:
```bash
python3 check_required_files.py
```

**2️ Beta Test (Pull Request):**  
- Create a branch and remove `.gitignore`.  
- Open a pull request.  
- Confirm the workflow fails until file is restored.

**3️ Prod Test (Main Merge):**  
- Merge into `main`.  
- Confirm CloudWatch log event appears in AWS under `/github-actions/required-file-presence-check/prod`.

---

##  Key Outcomes
- Enforced consistent repository structure across teams.  
- Automated CI/CD checks directly inside GitHub.  
- Secured AWS integration using environment secrets.  
- Established permanent audit logging in CloudWatch.  
- Demonstrated full DevOps workflow lifecycle (local → beta → prod).  

---

##  Author
**Cameron A. Parker**  
LevelUp Bank – Platform Engineering CI/CD Enforcement Project  
GitHub: [forgisonajeep](https://github.com/forgisonajeep)