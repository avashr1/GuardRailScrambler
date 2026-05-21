#!/usr/bin/env python
"""
Setup script to create project structure and initialize the application.
Run this before starting the Flask server.
"""

import os
import sys
from pathlib import Path

def setup():
    """Create necessary directories and initialize the project."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Create templates directory
    templates_dir = project_root / 'templates'
    templates_dir.mkdir(exist_ok=True)
    print(f"✓ Created templates directory: {templates_dir}")
    
    # Create static directory (optional, for future CSS/JS files if needed)
    static_dir = project_root / 'static'
    static_dir.mkdir(exist_ok=True)
    print(f"✓ Created static directory: {static_dir}")
    
    # Check if templates/index.html exists
    html_file = templates_dir / 'index.html'
    if html_file.exists():
        print(f"✓ Found templates/index.html")
    else:
        print(f"⚠ Warning: templates/index.html not found")
        print(f"  Please ensure the HTML file is in: {html_file}")
    
    # Check if app.py exists
    app_file = project_root / 'app.py'
    if app_file.exists():
        print(f"✓ Found app.py")
    else:
        print(f"⚠ Warning: app.py not found")
        print(f"  Please ensure it's in: {app_file}")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download spaCy model: python -m spacy download en_core_web_sm")
    print("3. Run the app: python app.py")
    print("4. Open http://localhost:5000 in your browser")

if __name__ == '__main__':
    try:
        setup()
    except Exception as e:
        print(f"❌ Setup failed: {e}", file=sys.stderr)
        sys.exit(1)
