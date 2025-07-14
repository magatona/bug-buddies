import os
import json
import shutil
from typing import Dict, List, Any
from PIL import Image

class AssetAggregator:
    """Aggregate and organize assets from all parallel agents."""
    
    def __init__(self):
        self.temp_dir = "temp_assets"
        self.output_dir = "assets"
        self.agent_count = 5
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/characters", exist_ok=True)
        os.makedirs(f"{self.output_dir}/animations", exist_ok=True)
        os.makedirs(f"{self.output_dir}/ui", exist_ok=True)
        
        self.manifest = {
            "version": "1.0.0",
            "generated_at": "",
            "characters": {},
            "animations": {},
            "ui_elements": {},
            "total_assets": 0
        }
    
    def collect_agent_assets(self) -> Dict[str, Any]:
        """Collect assets from all agent directories."""
        collected_assets = {
            "characters": {},
            "animations": {},
            "ui_elements": {},
            "reports": []
        }
        
        print("📦 Collecting assets from all agents...")
        
        for agent_id in range(1, self.agent_count + 1):
            agent_dir = f"{self.temp_dir}/agent-{agent_id}-assets"
            if not os.path.exists(agent_dir):
                print(f"⚠️  Agent {agent_id} assets not found: {agent_dir}")
                continue
            
            self.process_agent_directory(agent_id, agent_dir, collected_assets)
        
        return collected_assets
    
    def process_agent_directory(self, agent_id: int, agent_dir: str, collected_assets: Dict):
        """Process assets from a single agent directory."""
        print(f"🤖 Processing Agent {agent_id} assets...")
        
        agent_base_dir = f"{agent_dir}/agent_{agent_id}"
        if not os.path.exists(agent_base_dir):
            print(f"⚠️  Agent base directory not found: {agent_base_dir}")
            return
        
        report_path = f"{agent_base_dir}/asset_report.json"
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report = json.load(f)
                collected_assets["reports"].append(report)
                insect_type = report.get("insect_type", f"unknown_{agent_id}")
        else:
            insect_type = f"unknown_{agent_id}"
        
        self.collect_character_assets(agent_base_dir, insect_type, collected_assets)
        
        animations_dir = f"{agent_base_dir}/animations"
        if os.path.exists(animations_dir):
            self.collect_animation_assets(animations_dir, insect_type, collected_assets)
    
    def collect_character_assets(self, agent_dir: str, insect_type: str, collected_assets: Dict):
        """Collect character sprite assets."""
        character_dir = f"{self.output_dir}/characters/{insect_type}"
        os.makedirs(character_dir, exist_ok=True)
        
        collected_assets["characters"][insect_type] = []
        
        for file in os.listdir(agent_dir):
            if file.endswith('.png') and not file.startswith('ui_'):
                src_path = os.path.join(agent_dir, file)
                dst_path = os.path.join(character_dir, file)
                
                try:
                    self.optimize_and_copy_image(src_path, dst_path)
                    collected_assets["characters"][insect_type].append(file)
                    print(f"✅ Collected character asset: {file}")
                except Exception as e:
                    print(f"❌ Failed to process {file}: {e}")
    
    def collect_animation_assets(self, animations_dir: str, insect_type: str, collected_assets: Dict):
        """Collect animation GIF assets."""
        animation_output_dir = f"{self.output_dir}/animations/{insect_type}"
        os.makedirs(animation_output_dir, exist_ok=True)
        
        collected_assets["animations"][insect_type] = []
        
        for file in os.listdir(animations_dir):
            if file.endswith('.gif'):
                src_path = os.path.join(animations_dir, file)
                dst_path = os.path.join(animation_output_dir, file)
                
                try:
                    shutil.copy2(src_path, dst_path)
                    collected_assets["animations"][insect_type].append(file)
                    print(f"✅ Collected animation: {file}")
                except Exception as e:
                    print(f"❌ Failed to process animation {file}: {e}")
    
    def optimize_and_copy_image(self, src_path: str, dst_path: str):
        """Optimize image and ensure proper format."""
        with Image.open(src_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            if img.size != (32, 32):
                img = img.resize((32, 32), Image.NEAREST)
            
            img.save(dst_path, 'PNG', optimize=True)
    
    def collect_ui_assets(self, collected_assets: Dict):
        """Collect UI element assets."""
        ui_dir = f"{self.output_dir}/ui"
        
        for agent_id in range(1, self.agent_count + 1):
            agent_dir = f"{self.temp_dir}/agent-{agent_id}-assets/agent_{agent_id}"
            if not os.path.exists(agent_dir):
                continue
            
            for file in os.listdir(agent_dir):
                if file.startswith('ui_') and file.endswith('.png'):
                    src_path = os.path.join(agent_dir, file)
                    dst_path = os.path.join(ui_dir, file)
                    
                    try:
                        self.optimize_and_copy_image(src_path, dst_path)
                        if "ui_elements" not in collected_assets:
                            collected_assets["ui_elements"] = []
                        collected_assets["ui_elements"].append(file)
                        print(f"✅ Collected UI asset: {file}")
                    except Exception as e:
                        print(f"❌ Failed to process UI asset {file}: {e}")
    
    def generate_manifest(self, collected_assets: Dict):
        """Generate asset manifest for dynamic loading."""
        import datetime
        
        self.manifest["generated_at"] = datetime.datetime.utcnow().isoformat()
        self.manifest["characters"] = collected_assets["characters"]
        self.manifest["animations"] = collected_assets["animations"]
        self.manifest["ui_elements"] = collected_assets.get("ui_elements", [])
        
        total_assets = (
            sum(len(assets) for assets in collected_assets["characters"].values()) +
            sum(len(assets) for assets in collected_assets["animations"].values()) +
            len(collected_assets.get("ui_elements", []))
        )
        self.manifest["total_assets"] = total_assets
        
        manifest_path = f"{self.output_dir}/manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        print(f"📋 Generated manifest with {total_assets} total assets")
    
    def generate_summary_report(self, collected_assets: Dict):
        """Generate comprehensive summary report."""
        report = {
            "aggregation_summary": {
                "total_agents": self.agent_count,
                "successful_agents": len(collected_assets["reports"]),
                "total_characters": len(collected_assets["characters"]),
                "total_animations": sum(len(anims) for anims in collected_assets["animations"].values()),
                "total_ui_elements": len(collected_assets.get("ui_elements", [])),
                "total_assets": self.manifest["total_assets"]
            },
            "character_breakdown": {},
            "animation_breakdown": {},
            "agent_reports": collected_assets["reports"]
        }
        
        for insect_type, assets in collected_assets["characters"].items():
            report["character_breakdown"][insect_type] = {
                "asset_count": len(assets),
                "assets": assets
            }
        
        for insect_type, animations in collected_assets["animations"].items():
            report["animation_breakdown"][insect_type] = {
                "animation_count": len(animations),
                "animations": animations
            }
        
        report_path = f"{self.output_dir}/aggregation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("📊 Generated comprehensive aggregation report")
        return report

def main():
    """Main aggregation function."""
    try:
        aggregator = AssetAggregator()
        
        collected_assets = aggregator.collect_agent_assets()
        
        aggregator.collect_ui_assets(collected_assets)
        
        aggregator.generate_manifest(collected_assets)
        
        summary_report = aggregator.generate_summary_report(collected_assets)
        
        print("\n🎉 Asset aggregation completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Total assets: {summary_report['aggregation_summary']['total_assets']}")
        print(f"   - Characters: {summary_report['aggregation_summary']['total_characters']} types")
        print(f"   - Animations: {summary_report['aggregation_summary']['total_animations']} files")
        print(f"   - UI elements: {summary_report['aggregation_summary']['total_ui_elements']} files")
        
    except Exception as e:
        print(f"💥 Asset aggregation failed: {e}")
        raise

if __name__ == "__main__":
    main()
