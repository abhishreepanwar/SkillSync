"""
SkillSync Configuration

This file helps you configure your SkillSync installation.
"""

import os

def setup_environment():
    """
    Help users set up their environment for SkillSync AI features
    """
    print("🚀 SkillSync AI Configuration Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        create_env_file(env_file)
    else:
        print("✅ .env file already exists")
    
    # Check for Gemini API key
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        print("\n⚠️  Gemini API Key Not Found!")
        print("To enable AI-powered feedback:")
        print("1. Visit: https://makersuite.google.com/app/apikey")
        print("2. Create a free Gemini API key")
        print("3. Add it to your .env file:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("\n💡 SkillSync will work in demo mode without the API key")
    else:
        print("✅ Gemini API key configured!")
    
    print("\n🎯 Setup complete! You can now run:")
    print("   python app.py")

def create_env_file(file_path):
    """Create a .env file with template configuration"""
    template = """# SkillSync AI Configuration
# Get your free Gemini API key from: https://makersuite.google.com/app/apikey

GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Set environment mode
ENVIRONMENT=development

# Note: SkillSync works in demo mode without the API key
# AI features will be simulated with high-quality fallback responses
"""
    
    try:
        with open(file_path, 'w') as f:
            f.write(template)
        print(f"✅ Created {file_path}")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    setup_environment() 