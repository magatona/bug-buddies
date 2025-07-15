import os
import requests
import time
import json

class PRMonitor:
    """Monitor PR status and auto-merge when ready."""
    
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.game_repo_token = os.environ.get("GAME_REPO_TOKEN") or self.github_token
        self.pr_number = os.environ.get("PR_NUMBER")
        self.target_repo = os.environ.get("TARGET_REPO", "magatona/bug-buddies")
        self.max_wait_time = int(os.environ.get("MAX_WAIT_TIME", "1800"))
        self.check_interval = int(os.environ.get("CHECK_INTERVAL", "60"))
        
        self.headers = {
            "Authorization": f"token {self.game_repo_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if not self.pr_number:
            print("No PR number provided, skipping monitoring")
            return
        
        print(f"Monitoring PR #{self.pr_number} in {self.target_repo}")
    
    def get_pr_status(self):
        """Get current PR status and checks."""
        try:
            pr_url = f"https://api.github.com/repos/{self.target_repo}/pulls/{self.pr_number}"
            response = requests.get(pr_url, headers=self.headers)
            response.raise_for_status()
            
            pr_data = response.json()
            
            checks_url = f"https://api.github.com/repos/{self.target_repo}/commits/{pr_data['head']['sha']}/check-runs"
            checks_response = requests.get(checks_url, headers=self.headers)
            checks_response.raise_for_status()
            
            checks_data = checks_response.json()
            
            return {
                "pr": pr_data,
                "checks": checks_data["check_runs"],
                "mergeable": pr_data.get("mergeable", False),
                "mergeable_state": pr_data.get("mergeable_state", "unknown")
            }
            
        except Exception as e:
            print(f"Error getting PR status: {e}")
            return None
    
    def is_ready_to_merge(self, status):
        """Check if PR is ready to merge."""
        if not status:
            return False, "Unable to get PR status"
        
        pr = status["pr"]
        checks = status["checks"]
        
        if pr["state"] != "open":
            return False, f"PR is {pr['state']}"
        
        if not status["mergeable"]:
            return False, "PR is not mergeable"
        
        if status["mergeable_state"] == "blocked":
            return False, "PR is blocked"
        
        if len(checks) == 0:
            return True, "No checks required"
        
        failed_checks = [check for check in checks if check["conclusion"] == "failure"]
        if failed_checks:
            return False, f"Failed checks: {[check['name'] for check in failed_checks]}"
        
        pending_checks = [check for check in checks if check["status"] in ["queued", "in_progress"]]
        if pending_checks:
            return False, f"Pending checks: {[check['name'] for check in pending_checks]}"
        
        return True, "All checks passed"
    
    def merge_pr(self):
        """Merge the PR."""
        try:
            merge_url = f"https://api.github.com/repos/{self.target_repo}/pulls/{self.pr_number}/merge"
            merge_data = {
                "commit_title": f"Merge PR #{self.pr_number}: AI-Generated Bug Buddies Assets",
                "commit_message": "Automatically merged after successful CI checks",
                "merge_method": "squash"
            }
            
            response = requests.put(merge_url, headers=self.headers, json=merge_data)
            
            if response.status_code == 200:
                merge_result = response.json()
                print(f"✅ Successfully merged PR #{self.pr_number}")
                print(f"Merge SHA: {merge_result['sha']}")
                return True
            else:
                print(f"❌ Failed to merge PR: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error merging PR: {e}")
            return False
    
    def monitor_and_merge(self):
        """Monitor PR and merge when ready."""
        if not self.pr_number:
            print("No PR number provided, skipping monitoring")
            return False
        
        start_time = time.time()
        
        print(f"🔍 Starting to monitor PR #{self.pr_number}")
        print(f"⏰ Max wait time: {self.max_wait_time} seconds")
        print(f"🔄 Check interval: {self.check_interval} seconds")
        
        while time.time() - start_time < self.max_wait_time:
            status = self.get_pr_status()
            ready, reason = self.is_ready_to_merge(status)
            
            print(f"📊 PR Status: {reason}")
            
            if ready:
                print("✅ PR is ready to merge!")
                return self.merge_pr()
            
            if status and status["pr"]["state"] != "open":
                print(f"❌ PR is no longer open: {status['pr']['state']}")
                return False
            
            print(f"⏳ Waiting {self.check_interval} seconds before next check...")
            time.sleep(self.check_interval)
        
        print(f"⏰ Timeout reached after {self.max_wait_time} seconds")
        return False

def main():
    """Main monitoring function."""
    try:
        monitor = PRMonitor()
        success = monitor.monitor_and_merge()
        
        if success:
            print("🎉 PR monitoring and merge completed successfully!")
        else:
            print("⚠️ PR monitoring completed without merge")
            
    except Exception as e:
        print(f"💥 PR monitoring failed: {e}")

if __name__ == "__main__":
    main()
