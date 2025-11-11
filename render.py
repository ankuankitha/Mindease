"""
Fix deployment issues for MindEase Streamlit app
Run this before deploying to fix common problems
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Ensure Python version is compatible"""
    version = sys.version_info
    print(f"📍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 8 <= version.minor <= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version must be 3.8-3.11 for TensorFlow 2.15")
        print("   Current version:", sys.version)
        return False

def create_runtime_txt():
    """Create runtime.txt for deployment platforms"""
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    with open("runtime.txt", "w") as f:
        f.write(f"python-{python_version}\n")
    
    print(f"✅ Created runtime.txt with Python {python_version}")

def create_packages_txt():
    """Create packages.txt for system dependencies (Linux deployments)"""
    packages = [
        "libgl1-mesa-glx",
        "libglib2.0-0",
        "libsm6",
        "libxext6",
        "libxrender-dev"
    ]
    
    with open("packages.txt", "w") as f:
        f.write("\n".join(packages))
    
    print("✅ Created packages.txt for system dependencies")

def fix_requirements():
    """Create optimized requirements.txt"""
    requirements = """# Core web framework
streamlit==1.28.0

# Computer vision (headless for server deployment)
opencv-python-headless==4.8.1.78

# Numerical computing
numpy==1.24.3

# Image handling
Pillow==10.0.1

# Deep learning for emotion detection
tensorflow==2.15.0
keras==2.15.0
deepface==0.0.79

# Music API
spotipy==2.23.0

# Supporting libraries
gdown==4.7.1
tqdm==4.66.1
requests==2.31.0
protobuf==3.20.3

# For environment variables (optional)
python-dotenv==1.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print("✅ Created optimized requirements.txt")

def create_streamlit_config():
    """Create .streamlit/config.toml"""
    os.makedirs(".streamlit", exist_ok=True)
    
    config = """[theme]
primaryColor = "#8B5CF6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#1F2937"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config)
    
    print("✅ Created .streamlit/config.toml")

def create_gitignore():
    """Create .gitignore file"""
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Streamlit
.streamlit/secrets.toml

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temp files
temp_*
*.tmp

# Models (optional - uncomment if you want to exclude large model files)
# *.h5
# *.pkl
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore)
    
    print("✅ Created .gitignore")

def create_readme():
    """Create README.md"""
    readme = """# 🎧 MindEase - AI Emotion & Music Companion

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- 🎭 **Emotion Detection**: AI-powered facial emotion recognition
- 🎵 **Music Therapy**: Personalized Spotify recommendations
- 👩‍⚕️ **Women's Health**: Menstrual cycle tracking and wellness tips
- 🔒 **Privacy First**: No data storage, local processing

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd mindease-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Click Deploy!

## 📦 Requirements

- Python 3.8-3.11
- 2GB free disk space
- Stable internet (first run downloads models)

## 🔧 Configuration

### Spotify API (Optional but Recommended)

1. Get free credentials at [developer.spotify.com](https://developer.spotify.com)
2. Create `.streamlit/secrets.toml`:

```toml
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
```

## 📱 Usage

1. **Emotion Detection**: Upload a photo to detect your mood
2. **Music Recommendations**: Get personalized playlists
3. **Women's Health**: Track cycles and get wellness tips

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Emotion AI**: DeepFace + TensorFlow
- **Music API**: Spotipy (Spotify)
- **Computer Vision**: OpenCV

## ⚠️ Disclaimer

This is a supportive wellness tool, NOT medical advice. If experiencing mental health crisis:

- 🆘 US: Call 988 (Suicide & Crisis Lifeline)
- 🆘 International: Contact local emergency services

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push and create Pull Request

## 📄 License

MIT License - Feel free to use for personal/educational purposes.

## 👨‍💻 Author

Built with ❤️ for mental health awareness

---

**Star ⭐ this repo if you found it helpful!**
"""
    
    with open("README.md", "w") as f:
        f.write(readme)
    
    print("✅ Created README.md")

def test_imports():
    """Test if critical libraries can be imported"""
    print("\n🧪 Testing imports...")
    
    imports_to_test = [
        ("streamlit", "Streamlit"),
        ("cv2", "OpenCV"),
        ("deepface", "DeepFace"),
        ("spotipy", "Spotipy"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow")
    ]
    
    all_passed = True
    
    for module_name, display_name in imports_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {display_name}")
        except ImportError as e:
            print(f"  ❌ {display_name}: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Main fix script"""
    print("=" * 60)
    print("🔧 MindEase Deployment Fix Script")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        print("\n⚠️  Please install Python 3.8-3.11 and try again")
        return
    
    print("\n📝 Creating configuration files...")
    create_runtime_txt()
    create_packages_txt()
    fix_requirements()
    create_streamlit_config()
    create_gitignore()
    create_readme()
    
    print("\n" + "=" * 60)
    print("✅ All configuration files created!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Test imports:")
    if test_imports():
        print("\n   ✅ All imports successful!")
    else:
        print("\n   ⚠️  Some imports failed. Run: pip install -r requirements.txt")
    
    print("\n3. Run the app:")
    print("   streamlit run app.py")
    
    print("\n4. Deploy (choose one):")
    print("   • Streamlit Cloud: https://streamlit.io/cloud")
    print("   • Render: https://render.com")
    print("   • Hugging Face: https://huggingface.co/spaces")
    
    print("\n💡 Pro Tip: For Render deployment, you may need to:")
    print("   • Set Python version in dashboard to 3.11")
    print("   • Add environment variables for Spotify credentials")
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete! Happy coding!")
    print("=" * 60)

if __name__ == "__main__":
    main()
