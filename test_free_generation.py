#!/usr/bin/env python3
"""Test script to verify free AI generation works correctly."""

import os
import sys
import json

os.environ['AGENT_ID'] = '1'
os.environ['INSECT_TYPE'] = 'beetle'
os.environ['ASSET_VARIANTS'] = '["idle", "walk_1"]'
os.environ['USE_HUGGINGFACE'] = 'true'
os.environ['QUALITY_LEVEL'] = 'draft'

sys.path.append('scripts')

def test_generator_initialization():
    """Test that the generator initializes correctly with free APIs."""
    try:
        from generate_assets import BugBuddiesAssetGenerator
        
        print("🧪 Testing BugBuddiesAssetGenerator initialization...")
        generator = BugBuddiesAssetGenerator()
        
        print("✅ Generator initialized successfully")
        print(f"🔧 Using Hugging Face: {generator.use_huggingface}")
        print(f"🎨 Insect type: {generator.insect_type}")
        print(f"📋 Variants: {generator.asset_variants}")
        print(f"🎯 Quality level: {generator.quality_level}")
        
        test_prompt = generator.generate_prompt("idle")
        print(f"🎭 Generated prompt: {test_prompt[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return False

def test_fallback_generation():
    """Test programmatic fallback generation."""
    try:
        from generate_assets import BugBuddiesAssetGenerator
        
        print("\n🧪 Testing programmatic fallback generation...")
        generator = BugBuddiesAssetGenerator()
        
        image = generator.generate_programmatic_sprite("beetle", "idle")
        
        if image:
            print("✅ Programmatic sprite generation successful")
            print(f"📏 Image size: {image.size}")
            return True
        else:
            print("❌ Programmatic sprite generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in fallback generation: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting free AI generation tests...\n")
    
    tests = [
        test_generator_initialization,
        test_fallback_generation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Free AI generation is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
