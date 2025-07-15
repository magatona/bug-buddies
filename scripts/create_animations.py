import os
import json
import sys
from typing import List, Dict, Any
from PIL import Image
import imageio

class BugBuddiesAnimationCreator:
    """Create GIF animations from generated static assets."""
    
    def __init__(self):
        self.agent_id = int(os.environ.get("AGENT_ID", "1"))
        self.insect_type = os.environ.get("INSECT_TYPE", "beetle")
        self.animation_types = json.loads(os.environ.get("ANIMATION_TYPES", "[]"))
        
        self.input_dir = f"temp_assets/agent_{self.agent_id}"
        self.output_dir = f"{self.input_dir}/animations"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.animation_configs = self.get_animation_configs()
    
    def get_animation_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get animation configuration for each insect type."""
        configs = {
            "beetle": {
                "walking": {
                    "frames": ["beetle_walk_1.png", "beetle_idle.png", "beetle_walk_2.png", "beetle_idle.png"],
                    "duration": 0.5,
                    "loop": True
                },
                "idle": {
                    "frames": ["beetle_idle.png", "beetle_idle.png"],
                    "duration": 1.0,
                    "loop": True
                }
            },
            "butterfly": {
                "flying": {
                    "frames": ["butterfly_fly_1.png", "butterfly_fly_2.png", "butterfly_fly_3.png", "butterfly_fly_4.png"],
                    "duration": 0.3,
                    "loop": True
                },
                "idle": {
                    "frames": ["butterfly_idle.png", "butterfly_idle.png"],
                    "duration": 1.5,
                    "loop": True
                }
            },
            "ladybug": {
                "walking": {
                    "frames": ["ladybug_walk_1.png", "ladybug_idle.png", "ladybug_walk_2.png", "ladybug_idle.png"],
                    "duration": 0.5,
                    "loop": True
                },
                "idle": {
                    "frames": ["ladybug_idle.png", "ladybug_idle.png"],
                    "duration": 1.0,
                    "loop": True
                }
            },
            "caterpillar": {
                "crawling": {
                    "frames": ["caterpillar_crawl_1.png", "caterpillar_crawl_2.png", "caterpillar_crawl_3.png"],
                    "duration": 0.6,
                    "loop": True
                },
                "idle": {
                    "frames": ["caterpillar_idle.png", "caterpillar_idle.png"],
                    "duration": 1.2,
                    "loop": True
                }
            },
            "ui_elements": {
                "sparkle": {
                    "frames": ["ui_elements_sparkle_effect.png"],
                    "duration": 0.2,
                    "loop": False
                },
                "pulse": {
                    "frames": ["ui_elements_heart_icon.png", "ui_elements_heart_icon.png"],
                    "duration": 0.8,
                    "loop": True
                }
            }
        }
        return configs.get(self.insect_type, {})
    
    def create_animation(self, animation_type: str) -> bool:
        """Create a single animation GIF."""
        try:
            if animation_type not in self.animation_configs:
                print(f"⚠️  Unknown animation type: {animation_type}")
                return False
            
            config = self.animation_configs[animation_type]
            frames = []
            
            print(f"🎬 Agent {self.agent_id}: Creating {animation_type} animation for {self.insect_type}")
            
            for frame_file in config["frames"]:
                frame_path = os.path.join(self.input_dir, frame_file)
                if os.path.exists(frame_path):
                    frame = Image.open(frame_path)
                    frames.append(frame)
                else:
                    print(f"⚠️  Frame not found: {frame_path}")
                    placeholder = self.create_placeholder_frame()
                    frames.append(placeholder)
            
            if not frames:
                print(f"❌ No frames available for {animation_type}")
                return False
            
            output_path = os.path.join(self.output_dir, f"{self.insect_type}_{animation_type}.gif")
            
            frame_arrays = []
            for frame in frames:
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                frame_arrays.append(frame)
            
            frame_duration = config["duration"]
            
            imageio.mimsave(
                output_path,
                frame_arrays,
                duration=frame_duration,
                loop=0 if config["loop"] else 1,
                disposal=2  # Clear frame before next
            )
            
            print(f"✅ Created animation: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create {animation_type} animation: {e}")
            return False
    
    def create_placeholder_frame(self) -> Image.Image:
        """Create a placeholder frame when assets are missing."""
        size = (32, 32)
        if self.insect_type == "ui_elements":
            size = (16, 16)
        
        image = Image.new('RGBA', size, (255, 0, 255, 128))  # Magenta placeholder
        return image
    
    def optimize_gif(self, gif_path: str) -> None:
        """Optimize GIF file size while maintaining quality."""
        try:
            frames = imageio.mimread(gif_path)
            
            imageio.mimsave(
                gif_path,
                frames,
                duration=0.5,
                optimize=True,
                loop=0
            )
            
            print(f"🔧 Optimized: {gif_path}")
            
        except Exception as e:
            print(f"⚠️  Failed to optimize {gif_path}: {e}")
    
    def create_all_animations(self) -> Dict[str, Any]:
        """Create all animations for this agent."""
        results = {
            "agent_id": self.agent_id,
            "insect_type": self.insect_type,
            "created_animations": [],
            "failed_animations": [],
            "total_animations": len(self.animation_types)
        }
        
        print(f"🎬 Agent {self.agent_id} starting animation creation for {self.insect_type}")
        print(f"📋 Animation types: {self.animation_types}")
        
        for animation_type in self.animation_types:
            success = self.create_animation(animation_type)
            if success:
                results["created_animations"].append(animation_type)
                gif_path = os.path.join(self.output_dir, f"{self.insect_type}_{animation_type}.gif")
                self.optimize_gif(gif_path)
            else:
                results["failed_animations"].append(animation_type)
        
        report_path = os.path.join(self.output_dir, "animation_report.json")
        with open(report_path, "w") as f:
            json.dump(results, f, indent=2)
        
        success_rate = len(results["created_animations"]) / results["total_animations"] * 100 if results["total_animations"] > 0 else 0
        print(f"🎯 Agent {self.agent_id} animation creation: {success_rate:.1f}% success rate")
        print(f"✅ Created: {len(results['created_animations'])}")
        print(f"❌ Failed: {len(results['failed_animations'])}")
        
        return results

def main():
    """Main animation creation function."""
    try:
        creator = BugBuddiesAnimationCreator()
        results = creator.create_all_animations()
        
        if len(results["failed_animations"]) > 0:
            print(f"⚠️  Some animations failed to create: {results['failed_animations']}")
        
        print(f"🎉 Agent {creator.agent_id} animation creation completed!")
        
    except Exception as e:
        print(f"💥 Animation creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
