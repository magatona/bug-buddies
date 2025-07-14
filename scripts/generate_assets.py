import os
import json
import sys
import time
from typing import Dict, List, Any
import requests
from PIL import Image, ImageDraw
import io

class BugBuddiesAssetGenerator:
    """DALL-E 3 powered pixel art generator for Bug Buddies insects."""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.agent_id = int(os.environ.get("AGENT_ID", "1"))
        self.insect_type = os.environ.get("INSECT_TYPE", "beetle")
        self.asset_variants = json.loads(os.environ.get("ASSET_VARIANTS", "[]"))
        self.quality_level = os.environ.get("QUALITY_LEVEL", "standard")
        
        self.output_dir = f"temp_assets/agent_{self.agent_id}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.base_prompt_templates = self.get_prompt_templates()
        
    def get_prompt_templates(self) -> Dict[str, str]:
        """Get optimized DALL-E 3 prompts for each insect type."""
        templates = {
            "beetle": {
                "base": "A cute pixel art beetle character for a desktop pet game, 32x32 pixels, brown and dark brown colors, simple design with clear outlines, transparent background, top-down view, game sprite style",
                "idle": "A cute pixel art beetle character standing still, 32x32 pixels, brown body with darker brown head, simple pixel art style, transparent background, desktop pet game sprite",
                "walk_1": "A cute pixel art beetle character in walking pose 1, 32x32 pixels, brown body, legs positioned for walking animation, simple pixel art style, transparent background",
                "walk_2": "A cute pixel art beetle character in walking pose 2, 32x32 pixels, brown body, legs in different walking position, simple pixel art style, transparent background",
                "level_2": "A cute pixel art beetle character level 2, 32x32 pixels, slightly larger brown beetle with small sparkles, simple pixel art style, transparent background",
                "level_3": "A cute pixel art beetle character level 3, 32x32 pixels, larger brown beetle with golden highlights, simple pixel art style, transparent background"
            },
            "butterfly": {
                "base": "A cute pixel art butterfly character for a desktop pet game, 32x32 pixels, pink and light pink wings, simple design with clear outlines, transparent background, top-down view",
                "idle": "A cute pixel art butterfly character with wings spread, 32x32 pixels, pink and light pink wings, simple pixel art style, transparent background",
                "fly_1": "A cute pixel art butterfly character flying pose 1, 32x32 pixels, wings up position, pink colors, simple pixel art style, transparent background",
                "fly_2": "A cute pixel art butterfly character flying pose 2, 32x32 pixels, wings middle position, pink colors, simple pixel art style, transparent background",
                "fly_3": "A cute pixel art butterfly character flying pose 3, 32x32 pixels, wings down position, pink colors, simple pixel art style, transparent background",
                "fly_4": "A cute pixel art butterfly character flying pose 4, 32x32 pixels, wings up again, pink colors, simple pixel art style, transparent background"
            },
            "ladybug": {
                "base": "A cute pixel art ladybug character for a desktop pet game, 32x32 pixels, red body with black spots, simple design with clear outlines, transparent background",
                "idle": "A cute pixel art ladybug character standing still, 32x32 pixels, red body with black spots and head, simple pixel art style, transparent background",
                "walk_1": "A cute pixel art ladybug character walking pose 1, 32x32 pixels, red body with black spots, legs in walking position, simple pixel art style, transparent background",
                "walk_2": "A cute pixel art ladybug character walking pose 2, 32x32 pixels, red body with black spots, legs in different walking position, simple pixel art style, transparent background",
                "level_2": "A cute pixel art ladybug character level 2, 32x32 pixels, slightly larger red ladybug with more spots, simple pixel art style, transparent background",
                "level_3": "A cute pixel art ladybug character level 3, 32x32 pixels, larger red ladybug with golden spots, simple pixel art style, transparent background"
            },
            "caterpillar": {
                "base": "A cute pixel art caterpillar character for a desktop pet game, 32x32 pixels, green segmented body, simple design with clear outlines, transparent background",
                "idle": "A cute pixel art caterpillar character resting, 32x32 pixels, green segmented body with cute face, simple pixel art style, transparent background",
                "crawl_1": "A cute pixel art caterpillar character crawling pose 1, 32x32 pixels, green segmented body in S-curve, simple pixel art style, transparent background",
                "crawl_2": "A cute pixel art caterpillar character crawling pose 2, 32x32 pixels, green segmented body in different curve, simple pixel art style, transparent background",
                "crawl_3": "A cute pixel art caterpillar character crawling pose 3, 32x32 pixels, green segmented body stretched out, simple pixel art style, transparent background"
            },
            "ui_elements": {
                "base": "Cute pixel art UI elements for a desktop pet insect game, 32x32 pixels each, simple design with clear outlines, transparent background",
                "food_pellet": "A cute pixel art food pellet for insects, 16x16 pixels, golden yellow color, round shape, simple pixel art style, transparent background",
                "sparkle_effect": "A cute pixel art sparkle effect, 24x24 pixels, white and yellow sparkles, simple pixel art style, transparent background",
                "level_up_effect": "A cute pixel art level up effect, 32x32 pixels, golden stars and sparkles, simple pixel art style, transparent background",
                "heart_icon": "A cute pixel art heart icon, 16x16 pixels, red heart shape, simple pixel art style, transparent background",
                "star_icon": "A cute pixel art star icon, 16x16 pixels, golden yellow star, simple pixel art style, transparent background"
            }
        }
        return templates.get(self.insect_type, templates["beetle"])
    
    def generate_single_asset(self, variant: str) -> bool:
        """Generate a single asset variant using DALL-E 3."""
        try:
            prompt = self.base_prompt_templates.get(variant, self.base_prompt_templates["base"])
            
            if self.quality_level == "high":
                prompt += ", highly detailed pixel art, professional game sprite quality"
            elif self.quality_level == "draft":
                prompt += ", simple pixel art, basic game sprite"
            
            print(f"🎨 Agent {self.agent_id}: Generating {self.insect_type} - {variant}")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "standard" if self.quality_level != "high" else "hd",
                    "style": "natural"
                }
            )
            
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return False
            
            result = response.json()
            image_url = result["data"][0]["url"]
            
            img_response = requests.get(image_url)
            if img_response.status_code != 200:
                print(f"❌ Failed to download image: {img_response.status_code}")
                return False
            
            original_image = Image.open(io.BytesIO(img_response.content))
            processed_image = self.process_to_pixel_art(original_image, variant)
            
            output_path = os.path.join(self.output_dir, f"{self.insect_type}_{variant}.png")
            processed_image.save(output_path, "PNG")
            
            print(f"✅ Agent {self.agent_id}: Generated {variant} -> {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Agent {self.agent_id}: Failed to generate {variant}: {e}")
            return False
    
    def process_to_pixel_art(self, image: Image.Image, variant: str) -> Image.Image:
        """Process the generated image to proper 32x32 pixel art with transparency."""
        
        if "food" in variant or "heart" in variant or "star" in variant:
            target_size = (16, 16)
        elif "sparkle" in variant:
            target_size = (24, 24)
        else:
            target_size = (32, 32)
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        temp_size = (target_size[0] * 4, target_size[1] * 4)
        image = image.resize(temp_size, Image.Resampling.LANCZOS)
        
        image = image.quantize(colors=16, method=Image.Quantize.MEDIANCUT)
        image = image.convert('RGBA')
        
        image = image.resize(target_size, Image.Resampling.NEAREST)
        
        image = self.make_background_transparent(image)
        
        return image
    
    def make_background_transparent(self, image: Image.Image) -> Image.Image:
        """Make the background transparent by removing similar colors to corners."""
        data = image.getdata()
        
        width, height = image.size
        corner_colors = [
            data[0],  # top-left
            data[width-1],  # top-right
            data[width*(height-1)],  # bottom-left
            data[width*height-1]  # bottom-right
        ]
        
        from collections import Counter
        bg_color = Counter(corner_colors).most_common(1)[0][0]
        
        new_data = []
        for item in data:
            if len(item) >= 3:
                r_diff = abs(item[0] - bg_color[0])
                g_diff = abs(item[1] - bg_color[1])
                b_diff = abs(item[2] - bg_color[2])
                
                if r_diff < 30 and g_diff < 30 and b_diff < 30:
                    new_data.append((item[0], item[1], item[2], 0))
                else:
                    new_data.append(item)
            else:
                new_data.append(item)
        
        image.putdata(new_data)
        return image
    
    def generate_all_variants(self) -> Dict[str, Any]:
        """Generate all asset variants for this agent."""
        results = {
            "agent_id": self.agent_id,
            "insect_type": self.insect_type,
            "generated_assets": [],
            "failed_assets": [],
            "total_variants": len(self.asset_variants)
        }
        
        print(f"🚀 Agent {self.agent_id} starting generation for {self.insect_type}")
        print(f"📋 Variants to generate: {self.asset_variants}")
        
        for variant in self.asset_variants:
            success = self.generate_single_asset(variant)
            if success:
                results["generated_assets"].append(variant)
            else:
                results["failed_assets"].append(variant)
            
            time.sleep(2)
        
        report_path = os.path.join(self.output_dir, "generation_report.json")
        with open(report_path, "w") as f:
            json.dump(results, f, indent=2)
        
        success_rate = len(results["generated_assets"]) / results["total_variants"] * 100
        print(f"🎯 Agent {self.agent_id} completed: {success_rate:.1f}% success rate")
        print(f"✅ Generated: {len(results['generated_assets'])}")
        print(f"❌ Failed: {len(results['failed_assets'])}")
        
        return results

def main():
    """Main asset generation function."""
    try:
        generator = BugBuddiesAssetGenerator()
        results = generator.generate_all_variants()
        
        if len(results["failed_assets"]) > 0:
            print(f"⚠️  Some assets failed to generate: {results['failed_assets']}")
            sys.exit(1)
        else:
            print(f"🎉 Agent {generator.agent_id} completed successfully!")
            
    except Exception as e:
        print(f"💥 Agent generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
