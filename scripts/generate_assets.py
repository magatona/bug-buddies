import os
import json
import sys
import time
from typing import Dict, List, Any
import torch
from PIL import Image, ImageDraw
import io

try:
    from diffusers import StableDiffusionPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False
    print("⚠️ diffusers not available, falling back to alternative methods")

class BugBuddiesAssetGenerator:
    """Free AI-powered pixel art generator for Bug Buddies insects using Hugging Face Diffusers."""
    
    def __init__(self):
        self.use_huggingface = DIFFUSERS_AVAILABLE and os.environ.get("USE_HUGGINGFACE", "true").lower() == "true"
        self.leonardo_api_key = os.environ.get("LEONARDO_API_KEY")  # Optional
        self.replicate_api_key = os.environ.get("REPLICATE_API_KEY")  # Optional
        
        self.agent_id = int(os.environ.get("AGENT_ID", "1"))
        self.insect_type = os.environ.get("INSECT_TYPE", "beetle")
        self.asset_variants = json.loads(os.environ.get("ASSET_VARIANTS", "[]"))
        self.quality_level = os.environ.get("QUALITY_LEVEL", "standard")
        
        self.output_dir = f"temp_assets/agent_{self.agent_id}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.base_prompt_templates = self.get_prompt_templates()
        
        self.pipeline = None
        if self.use_huggingface:
            self.init_huggingface_pipeline()
        
        print(f"🎨 Agent {self.agent_id} initialized for {self.insect_type}")
        print(f"🔧 Generation method: {'Hugging Face Diffusers' if self.use_huggingface else 'Alternative APIs'}")
    
    def init_huggingface_pipeline(self):
        """Initialize Hugging Face Stable Diffusion pipeline."""
        try:
            print("🤖 Loading Hugging Face Stable Diffusion pipeline...")
            
            model_id = os.environ.get("HF_MODEL_ID", "runwayml/stable-diffusion-v1-5")
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if device == "cuda" else torch.float32
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                use_safetensors=True,
                safety_checker=None,  # Disable for faster generation
                requires_safety_checker=False
            )
            
            self.pipeline = self.pipeline.to(device)
            
            if device == "cuda":
                self.pipeline.enable_memory_efficient_attention()
                self.pipeline.enable_xformers_memory_efficient_attention()
            
            print(f"✅ Pipeline loaded on {device}")
            
        except Exception as e:
            print(f"❌ Failed to initialize Hugging Face pipeline: {e}")
            self.use_huggingface = False
            self.pipeline = None
        
    def get_prompt_templates(self) -> Dict[str, str]:
        """Get optimized pixel art prompts for each insect type."""
        templates = {
            "beetle": {
                "base": "pixel art, 8bit style, cute beetle character, game sprite, brown and dark brown colors, simple design, clear outlines, retro gaming, detailed pixels, 16bit game character",
                "idle": "pixel art, 8bit style, cute beetle character standing still, game sprite, brown body with darker brown head, retro gaming, detailed pixels, desktop pet",
                "walk_1": "pixel art, 8bit style, cute beetle character walking pose 1, game sprite, brown body, legs positioned for walking, retro gaming, detailed pixels",
                "walk_2": "pixel art, 8bit style, cute beetle character walking pose 2, game sprite, brown body, legs in different walking position, retro gaming, detailed pixels",
                "level_2": "pixel art, 8bit style, cute beetle character level 2, game sprite, slightly larger brown beetle with small sparkles, retro gaming, detailed pixels",
                "level_3": "pixel art, 8bit style, cute beetle character level 3, game sprite, larger brown beetle with golden highlights, retro gaming, detailed pixels"
            },
            "butterfly": {
                "base": "pixel art, 8bit style, cute butterfly character, game sprite, pink and light pink wings, colorful, simple design, clear outlines, retro gaming, detailed pixels",
                "idle": "pixel art, 8bit style, cute butterfly character with wings spread, game sprite, pink and light pink wings, retro gaming, detailed pixels, desktop pet",
                "fly_1": "pixel art, 8bit style, cute butterfly character flying pose 1, game sprite, wings up position, pink colors, retro gaming, detailed pixels",
                "fly_2": "pixel art, 8bit style, cute butterfly character flying pose 2, game sprite, wings middle position, pink colors, retro gaming, detailed pixels",
                "fly_3": "pixel art, 8bit style, cute butterfly character flying pose 3, game sprite, wings down position, pink colors, retro gaming, detailed pixels",
                "fly_4": "pixel art, 8bit style, cute butterfly character flying pose 4, game sprite, wings up again, pink colors, retro gaming, detailed pixels"
            },
            "ladybug": {
                "base": "pixel art, 8bit style, cute ladybug character, game sprite, red body with black spots, simple design, clear outlines, retro gaming, detailed pixels",
                "idle": "pixel art, 8bit style, cute ladybug character standing still, game sprite, red body with black spots and head, retro gaming, detailed pixels, desktop pet",
                "walk_1": "pixel art, 8bit style, cute ladybug character walking pose 1, game sprite, red body with black spots, legs in walking position, retro gaming, detailed pixels",
                "walk_2": "pixel art, 8bit style, cute ladybug character walking pose 2, game sprite, red body with black spots, legs in different walking position, retro gaming, detailed pixels",
                "level_2": "pixel art, 8bit style, cute ladybug character level 2, game sprite, slightly larger red ladybug with more spots, retro gaming, detailed pixels",
                "level_3": "pixel art, 8bit style, cute ladybug character level 3, game sprite, larger red ladybug with golden spots, retro gaming, detailed pixels"
            },
            "caterpillar": {
                "base": "pixel art, 8bit style, cute caterpillar character, game sprite, green segmented body, simple design, clear outlines, retro gaming, detailed pixels",
                "idle": "pixel art, 8bit style, cute caterpillar character resting, game sprite, green segmented body with cute face, retro gaming, detailed pixels, desktop pet",
                "crawl_1": "pixel art, 8bit style, cute caterpillar character crawling pose 1, game sprite, green segmented body in S-curve, retro gaming, detailed pixels",
                "crawl_2": "pixel art, 8bit style, cute caterpillar character crawling pose 2, game sprite, green segmented body in different curve, retro gaming, detailed pixels",
                "crawl_3": "pixel art, 8bit style, cute caterpillar character crawling pose 3, game sprite, green segmented body stretched out, retro gaming, detailed pixels"
            },
            "ui_elements": {
                "base": "pixel art, 8bit style, cute UI elements for desktop pet insect game, simple design, clear outlines, retro gaming, detailed pixels",
                "food_pellet": "pixel art, 8bit style, cute food pellet for insects, golden yellow color, round shape, retro gaming, detailed pixels, game item",
                "sparkle_effect": "pixel art, 8bit style, cute sparkle effect, white and yellow sparkles, retro gaming, detailed pixels, game effect",
                "level_up_effect": "pixel art, 8bit style, cute level up effect, golden stars and sparkles, retro gaming, detailed pixels, game effect",
                "heart_icon": "pixel art, 8bit style, cute heart icon, red heart shape, retro gaming, detailed pixels, game UI",
                "star_icon": "pixel art, 8bit style, cute star icon, golden yellow star, retro gaming, detailed pixels, game UI"
            }
        }
        return templates.get(self.insect_type, templates["beetle"])
    
    def generate_single_asset(self, variant: str) -> bool:
        """Generate a single asset variant using free AI methods."""
        try:
            prompt = self.base_prompt_templates.get(variant, self.base_prompt_templates["base"])
            
            if self.quality_level == "high":
                prompt += ", highly detailed pixel art, professional game sprite quality, sharp pixels"
            elif self.quality_level == "draft":
                prompt += ", simple pixel art, basic game sprite"
            else:
                prompt += ", clean pixel art, game ready sprite"
            
            print(f"🎨 Agent {self.agent_id}: Generating {self.insect_type} - {variant}")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            original_image = None
            
            if self.use_huggingface and self.pipeline:
                original_image = self.generate_with_huggingface(prompt)
            elif self.leonardo_api_key:
                original_image = self.generate_with_leonardo(prompt)
            elif self.replicate_api_key:
                original_image = self.generate_with_replicate(prompt)
            else:
                original_image = self.generate_programmatic_fallback(variant)
            
            if original_image is None:
                print(f"❌ All generation methods failed for {variant}")
                return False
            
            processed_image = self.process_to_pixel_art(original_image, variant)
            
            output_path = os.path.join(self.output_dir, f"{self.insect_type}_{variant}.png")
            processed_image.save(output_path, "PNG")
            
            print(f"✅ Agent {self.agent_id}: Generated {variant} -> {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Agent {self.agent_id}: Failed to generate {variant}: {e}")
            return False
    
    def generate_with_huggingface(self, prompt: str) -> Image.Image:
        """Generate image using Hugging Face Diffusers (completely free)."""
        try:
            print("🤖 Generating with Hugging Face Diffusers...")
            
            negative_prompt = "blurry, low quality, distorted, realistic, photographic, 3d render, smooth, antialiased"
            
            with torch.no_grad():
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=25,  # Good balance of quality/speed
                    guidance_scale=7.5,      # Standard guidance
                    width=512,
                    height=512,
                    num_images_per_prompt=1
                )
            
            return result.images[0]
            
        except Exception as e:
            print(f"❌ Hugging Face generation failed: {e}")
            return None
    
    def generate_with_leonardo(self, prompt: str) -> Image.Image:
        """Generate image using Leonardo.AI (150 free credits/day)."""
        try:
            print("🎨 Generating with Leonardo.AI...")
            
            import requests
            
            response = requests.post(
                'https://cloud.leonardo.ai/api/rest/v1/generations',
                headers={
                    'Authorization': f'Bearer {self.leonardo_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'prompt': prompt,
                    'modelId': '6bef9f1b-29cb-40c7-b9df-32b51c1f67d3',  # Pixel Art model
                    'num_images': 1,
                    'width': 512,
                    'height': 512,
                    'guidance_scale': 7,
                    'num_inference_steps': 25
                }
            )
            
            if response.status_code != 200:
                print(f"❌ Leonardo API Error: {response.status_code}")
                return None
            
            result = response.json()
            image_url = result['sdGenerationJob']['generatedImages'][0]['url']
            
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                return Image.open(io.BytesIO(img_response.content))
            
            return None
            
        except Exception as e:
            print(f"❌ Leonardo generation failed: {e}")
            return None
    
    def generate_with_replicate(self, prompt: str) -> Image.Image:
        """Generate image using Replicate API (low cost ~$0.01-0.05/image)."""
        try:
            print("🔥 Generating with Replicate...")
            
            import replicate
            
            output = replicate.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "num_inference_steps": 25,
                    "guidance_scale": 7.5,
                    "num_outputs": 1
                }
            )
            
            if output and len(output) > 0:
                import requests
                img_response = requests.get(output[0])
                if img_response.status_code == 200:
                    return Image.open(io.BytesIO(img_response.content))
            
            return None
            
        except Exception as e:
            print(f"❌ Replicate generation failed: {e}")
            return None
    
    def generate_programmatic_fallback(self, variant: str) -> Image.Image:
        """Generate a simple programmatic sprite as fallback."""
        try:
            print("🎮 Using programmatic fallback generation...")
            
            image = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            if self.insect_type == "beetle":
                draw.ellipse([200, 220, 312, 292], fill=(139, 69, 19, 255))
                draw.ellipse([230, 180, 282, 220], fill=(101, 67, 33, 255))
            elif self.insect_type == "butterfly":
                draw.ellipse([180, 200, 240, 260], fill=(255, 192, 203, 255))  # Left wing
                draw.ellipse([272, 200, 332, 260], fill=(255, 192, 203, 255))  # Right wing
                draw.ellipse([248, 220, 264, 280], fill=(139, 69, 19, 255))
            elif self.insect_type == "ladybug":
                draw.ellipse([200, 220, 312, 292], fill=(255, 0, 0, 255))
                draw.ellipse([220, 235, 235, 250], fill=(0, 0, 0, 255))
                draw.ellipse([277, 235, 292, 250], fill=(0, 0, 0, 255))
                draw.ellipse([230, 180, 282, 220], fill=(0, 0, 0, 255))
            elif self.insect_type == "caterpillar":
                for i in range(5):
                    x = 200 + i * 20
                    draw.ellipse([x, 230, x + 25, 255], fill=(34, 139, 34, 255))
            else:  # ui_elements
                draw.ellipse([230, 230, 282, 282], fill=(255, 215, 0, 255))
            
            return image
            
        except Exception as e:
            print(f"❌ Programmatic fallback failed: {e}")
            return None
    
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
