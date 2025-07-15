import os
import json
import sys

def generate_asset_matrix():
    """Generate matrix for 5 parallel agents with specific insect assignments."""
    
    asset_type = os.environ.get("ASSET_TYPE", "all")
    quality_level = os.environ.get("QUALITY_LEVEL", "standard")
    
    agent_assignments = [
        {
            "agent_id": 1,
            "insect_type": "beetle",
            "description": "Brown beetle, 32x32px, walking animation",
            "asset_variants": ["idle", "walk_1", "walk_2", "level_2", "level_3"],
            "animation_types": ["walking", "idle"],
            "colors": {"primary": "#8B4513", "secondary": "#654321"}
        },
        {
            "agent_id": 2,
            "insect_type": "butterfly",
            "description": "Colorful butterfly, 32x32px, flying animation",
            "asset_variants": ["idle", "fly_1", "fly_2", "fly_3", "fly_4"],
            "animation_types": ["flying", "idle"],
            "colors": {"primary": "#FF69B4", "secondary": "#FFB6C1"}
        },
        {
            "agent_id": 3,
            "insect_type": "ladybug",
            "description": "Red and black ladybug, 32x32px, walking animation",
            "asset_variants": ["idle", "walk_1", "walk_2", "level_2", "level_3"],
            "animation_types": ["walking", "idle"],
            "colors": {"primary": "#FF0000", "secondary": "#000000"}
        },
        {
            "agent_id": 4,
            "insect_type": "caterpillar",
            "description": "Green caterpillar, 32x32px, crawling animation",
            "asset_variants": ["idle", "crawl_1", "crawl_2", "crawl_3"],
            "animation_types": ["crawling", "idle"],
            "colors": {"primary": "#32CD32", "secondary": "#228B22"}
        },
        {
            "agent_id": 5,
            "insect_type": "ui_elements",
            "description": "UI elements: food, effects, icons",
            "asset_variants": ["food_pellet", "sparkle_effect", "level_up_effect", "heart_icon", "star_icon"],
            "animation_types": ["sparkle", "pulse"],
            "colors": {"primary": "#FFD700", "secondary": "#FFA500"}
        }
    ]
    
    if asset_type != "all":
        if asset_type == "characters":
            agent_assignments = [a for a in agent_assignments if a["insect_type"] != "ui_elements"]
        elif asset_type == "ui":
            agent_assignments = [a for a in agent_assignments if a["insect_type"] == "ui_elements"]
    
    for assignment in agent_assignments:
        assignment["quality_level"] = quality_level
    
    matrix = {"include": agent_assignments}
    
    matrix_string = json.dumps(matrix)
    print(f"matrix={matrix_string}")
    
    os.makedirs("temp_assets/config", exist_ok=True)
    with open("temp_assets/config/generation_config.json", "w") as f:
        json.dump({
            "asset_type": asset_type,
            "quality_level": quality_level,
            "agent_count": len(agent_assignments),
            "total_variants": sum(len(a["asset_variants"]) for a in agent_assignments)
        }, f, indent=2)

if __name__ == "__main__":
    generate_asset_matrix()
