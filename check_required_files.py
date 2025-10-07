import os
import sys

# List of required files
required_files = ["README.md", ".gitignore"]

# Collect missing files
missing = [f for f in required_files if not os.path.exists(f)]

if missing:
    print("Missing required files:")
    for f in missing:
        print(f" - {f}")
    sys.exit(1)  # fail
else:
    print("All required files are present.")
    sys.exit(0)  # pass