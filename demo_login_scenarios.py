#!/usr/bin/env python3
"""
🎯 Quick Demo: Viewz Login Scenarios

This is a simple demo script that shows how to run the login scenarios.
Run this script to see the automation in action!

Usage:
    python demo_login_scenarios.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the login scenarios demo"""
    print("🎯 Viewz Login Scenarios Demo")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("scripts/run_login_scenarios.py").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    print("🚀 Starting login scenarios automation...")
    print("📍 This will:")
    print("   1. Navigate to https://new.viewz.co/login")
    print("   2. Analyze the page structure")
    print("   3. Execute login and logout scenarios")
    print("   4. Generate screenshots and reports")
    print()
    
    # Ask for confirmation
    response = input("🤔 Continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Demo cancelled")
        return
    
    print("\n🎬 Running demo...")
    print("=" * 40)
    
    try:
        # Run the login scenarios script
        result = subprocess.run([
            sys.executable, 
            "scripts/run_login_scenarios.py"
        ], capture_output=False, text=True)
        
        print("\n" + "=" * 40)
        if result.returncode == 0:
            print("✅ Demo completed successfully!")
            print("\n📁 Check these files for results:")
            print("   📸 screenshots/ - All screenshots")
            print("   📊 fixtures/test_report.json - Test results")
            print("   🎯 fixtures/generated_assertions.txt - Generated assertions")
            print("   🔧 fixtures/discovered_selectors.json - Found selectors")
        else:
            print("❌ Demo completed with some issues")
            print("   Check the output above for details")
            
    except Exception as e:
        print(f"❌ Error running demo: {str(e)}")
        print("💡 Try running directly: python scripts/run_login_scenarios.py")

if __name__ == "__main__":
    main() 