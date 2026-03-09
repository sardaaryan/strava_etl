import os
import shutil
import subprocess

# Config
METRICS_SOURCE = 'data/metrics.json'
PORTFOLIO_REPO_NAME = "your-portfolio-repo-name" # e.g., "my-nextjs-site"
TARGET_PATH = f"../{PORTFOLIO_REPO_NAME}/public/data/metrics.json"

def export_to_portfolio():
    """
    Copies the metrics.json to your local portfolio folder 
    so you can test the UI before pushing to GitHub.
    """
    if os.path.exists(METRICS_SOURCE):
        # Ensure target directory exists in your other repo
        os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
        
        # Copy the file
        shutil.copy2(METRICS_SOURCE, TARGET_PATH)
        print(f"Exported metrics to {TARGET_PATH}")
    else:
        print("metrics.json not found. Run transform.py first.")

if __name__ == "__main__":
    export_to_portfolio()