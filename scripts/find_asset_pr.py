import os
import requests
import json

def find_latest_asset_pr():
    """Find the latest asset generation PR."""
    github_token = os.environ.get("GITHUB_TOKEN")
    pr_number = os.environ.get("PR_NUMBER")
    target_repo = os.environ.get("TARGET_REPO", "magatona/bug-buddies")
    
    if pr_number:
        print(f"Using specified PR number: {pr_number}")
        print(f"::set-output name=pr_number::{pr_number}")
        return
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        url = f"https://api.github.com/repos/{target_repo}/pulls"
        params = {
            "state": "open",
            "sort": "created",
            "direction": "desc",
            "per_page": 10
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        pulls = response.json()
        
        for pr in pulls:
            if "generated-assets" in pr["head"]["ref"] or "AI-Generated" in pr["title"]:
                pr_number = pr["number"]
                print(f"Found asset generation PR: #{pr_number} - {pr['title']}")
                print(f"::set-output name=pr_number::{pr_number}")
                return
        
        print("No asset generation PR found")
        print("::set-output name=pr_number::")
        
    except Exception as e:
        print(f"Error finding PR: {e}")
        print("::set-output name=pr_number::")

if __name__ == "__main__":
    find_latest_asset_pr()
