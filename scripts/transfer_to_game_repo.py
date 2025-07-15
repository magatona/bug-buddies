import os
import json
import base64
import requests
from typing import Dict, List, Any
import time

class GameRepoTransfer:
    """Transfer generated assets to the Bug Buddies game repository."""
    
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.game_repo_token = os.environ.get("GAME_REPO_TOKEN") or self.github_token
        self.target_repo = os.environ.get("TARGET_REPO", "magatona/bug-buddies")
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.game_repo_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Bug-Buddies-Asset-Generator"
        }
        
        self.assets_dir = "assets"
        self.branch_name = f"devin/{int(time.time())}-generated-assets"
        
        print(f"🔄 Initializing transfer to {self.target_repo}")
    
    def create_feature_branch(self) -> bool:
        """Create a new feature branch for the asset transfer."""
        try:
            main_branch_url = f"{self.api_base}/repos/{self.target_repo}/git/refs/heads/main"
            response = requests.get(main_branch_url, headers=self.headers)
            
            if response.status_code == 404:
                main_branch_url = f"{self.api_base}/repos/{self.target_repo}/git/refs/heads/clean-implementation"
                response = requests.get(main_branch_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ Failed to get main branch: {response.status_code}")
                return False
            
            main_sha = response.json()["object"]["sha"]
            
            create_branch_url = f"{self.api_base}/repos/{self.target_repo}/git/refs"
            branch_data = {
                "ref": f"refs/heads/{self.branch_name}",
                "sha": main_sha
            }
            
            response = requests.post(create_branch_url, headers=self.headers, json=branch_data)
            
            if response.status_code == 201:
                print(f"✅ Created feature branch: {self.branch_name}")
                return True
            elif response.status_code == 422:
                print(f"⚠️  Branch {self.branch_name} already exists, using existing branch")
                return True
            else:
                print(f"❌ Failed to create branch: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating feature branch: {e}")
            return False
    
    def upload_file_to_repo(self, local_path: str, repo_path: str) -> bool:
        """Upload a single file to the repository."""
        try:
            with open(local_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
            
            file_url = f"{self.api_base}/repos/{self.target_repo}/contents/{repo_path}"
            
            get_response = requests.get(file_url, headers=self.headers, params={"ref": self.branch_name})
            
            file_data = {
                "message": f"Add generated asset: {os.path.basename(repo_path)}",
                "content": content,
                "branch": self.branch_name
            }
            
            if get_response.status_code == 200:
                file_data["sha"] = get_response.json()["sha"]
                print(f"🔄 Updating existing file: {repo_path}")
            else:
                print(f"📁 Creating new file: {repo_path}")
            
            response = requests.put(file_url, headers=self.headers, json=file_data)
            
            if response.status_code in [200, 201]:
                print(f"✅ Uploaded: {repo_path}")
                return True
            else:
                print(f"❌ Failed to upload {repo_path}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading {local_path}: {e}")
            return False
    
    def transfer_all_assets(self) -> Dict[str, Any]:
        """Transfer all generated assets to the game repository."""
        transfer_results = {
            "successful_uploads": [],
            "failed_uploads": [],
            "total_files": 0,
            "success_rate": 0
        }
        
        if not os.path.exists(self.assets_dir):
            print(f"❌ Assets directory not found: {self.assets_dir}")
            return transfer_results
        
        print(f"📦 Starting asset transfer from {self.assets_dir}")
        
        for root, dirs, files in os.walk(self.assets_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, ".")
                
                transfer_results["total_files"] += 1
                
                if self.upload_file_to_repo(local_path, relative_path):
                    transfer_results["successful_uploads"].append(relative_path)
                else:
                    transfer_results["failed_uploads"].append(relative_path)
                
                time.sleep(0.1)
        
        if transfer_results["total_files"] > 0:
            transfer_results["success_rate"] = len(transfer_results["successful_uploads"]) / transfer_results["total_files"] * 100
        
        print(f"📊 Transfer completed: {len(transfer_results['successful_uploads'])}/{transfer_results['total_files']} files")
        return transfer_results
    
    def create_pull_request(self, transfer_results: Dict[str, Any]) -> bool:
        """Create a pull request with the transferred assets."""
        try:
            manifest_path = f"{self.assets_dir}/manifest.json"
            manifest_data = {}
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest_data = json.load(f)
            
            pr_title = f"🎨 Add AI-Generated Bug Buddies Assets ({manifest_data.get('total_assets', 'Multiple')} assets)"
            
            pr_body = f"""# 🎨 AI-Generated Bug Buddies Assets

- **Total Assets**: {manifest_data.get('total_assets', 'N/A')}
- **Generated At**: {manifest_data.get('generated_at', 'N/A')}
- **Success Rate**: {transfer_results['success_rate']:.1f}%

"""
            
            for insect_type, assets in manifest_data.get('characters', {}).items():
                pr_body += f"- **{insect_type.title()}**: {len(assets)} sprites\n"
            
            pr_body += f"""
"""
            
            for insect_type, animations in manifest_data.get('animations', {}).items():
                pr_body += f"- **{insect_type.title()}**: {len(animations)} animations\n"
            
            pr_body += f"""
- **Count**: {len(manifest_data.get('ui_elements', []))}

- **Asset Size**: 32x32 pixels
- **Format**: PNG (sprites), GIF (animations)
- **Background**: Transparent
- **Generated via**: OpenAI DALL-E 3 API
- **Parallel Agents**: 5 agents (beetle, butterfly, ladybug, caterpillar, UI)

```
assets/
├── characters/
│   ├── beetle/
│   ├── butterfly/
│   ├── ladybug/
│   └── caterpillar/
├── animations/
│   ├── beetle/
│   ├── butterfly/
│   ├── ladybug/
│   └── caterpillar/
├── ui/
└── manifest.json
```

This PR includes the AssetManager.js system that will automatically load these assets into the game while maintaining backward compatibility with the existing programmatic drawing system.

- **Link to Devin run**: https://app.devin.ai/sessions/76d1afdeaadc4fa796872adca009def2
- **Requested by**: @magatona

- [ ] Assets generated successfully
- [ ] All files transferred to repository
- [ ] AssetManager integration complete
- [ ] Backward compatibility maintained
"""
            
            pr_url = f"{self.api_base}/repos/{self.target_repo}/pulls"
            pr_data = {
                "title": pr_title,
                "body": pr_body,
                "head": self.branch_name,
                "base": "clean-implementation"
            }
            
            response = requests.post(pr_url, headers=self.headers, json=pr_data)
            
            if response.status_code == 201:
                pr_info = response.json()
                print(f"✅ Created pull request: {pr_info['html_url']}")
                print(f"📋 PR #{pr_info['number']}: {pr_title}")
                return True
            else:
                print(f"❌ Failed to create PR: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating pull request: {e}")
            return False
    
    def execute_transfer(self) -> bool:
        """Execute the complete transfer process."""
        print("🚀 Starting Bug Buddies asset transfer process...")
        
        if not self.create_feature_branch():
            return False
        
        transfer_results = self.transfer_all_assets()
        
        if len(transfer_results["successful_uploads"]) == 0:
            print("❌ No assets were successfully transferred")
            return False
        
        if not self.create_pull_request(transfer_results):
            return False
        
        print("🎉 Asset transfer completed successfully!")
        return True

def main():
    """Main transfer function."""
    try:
        transfer = GameRepoTransfer()
        success = transfer.execute_transfer()
        
        if not success:
            print("💥 Asset transfer failed")
            exit(1)
            
    except Exception as e:
        print(f"💥 Transfer process failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
