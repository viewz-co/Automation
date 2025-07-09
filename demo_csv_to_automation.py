#!/usr/bin/env python3
"""
Demo Script: CSV to Automation Generator
Demonstrates converting CSV test cases to Python Playwright automation code
"""

import os
import sys
import json
from pathlib import Path
from scripts.csv_to_automation_generator import CSVToAutomationGenerator

def main():
    """Main demo function"""
    print("🚀 CSV to Automation Generator Demo")
    print("=" * 50)
    
    # Check if sample CSV exists
    csv_file = "sample_test_cases.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Sample CSV file not found: {csv_file}")
        print("Please ensure the sample CSV file is in the current directory")
        return
    
    print(f"📁 Using CSV file: {csv_file}")
    print(f"📊 Generating automation tests...")
    
    # Create generator instance
    generator = CSVToAutomationGenerator(csv_file, "demo_generated_tests")
    
    # Generate complete test suite
    generator.generate_all()
    
    # Show summary
    print("\n" + "=" * 50)
    print("📋 Generation Summary:")
    print(f"   • Total Test Cases: {len(generator.test_cases)}")
    print(f"   • Test Sections: {len(generator.sections)}")
    print(f"   • Generated Files: {count_generated_files('demo_generated_tests')}")
    
    # Show section breakdown
    print("\n📁 Section Breakdown:")
    for section_name, test_cases in generator.sections.items():
        print(f"   • {section_name}: {len(test_cases)} test cases")
    
    # Show TestRail mapping
    print("\n🔗 TestRail Integration:")
    mapping_file = Path("demo_generated_tests/fixtures/testrail_csv_mapping.json")
    if mapping_file.exists():
        with open(mapping_file) as f:
            mapping = json.load(f)
        print(f"   • TestRail Cases: {len(mapping)} mapped")
        print(f"   • Case Range: C401 - C{400 + len(mapping)}")
    
    # Show next steps
    print("\n📋 Next Steps:")
    print("1. Review generated code in 'demo_generated_tests' directory")
    print("2. Customize page objects and test methods")
    print("3. Configure environment settings")
    print("4. Run tests with: pytest demo_generated_tests/tests/ -v")
    
    # Show sample files
    print("\n📄 Generated Files:")
    show_generated_files("demo_generated_tests")
    
    print("\n✅ Demo completed successfully!")

def count_generated_files(output_dir: str) -> int:
    """Count generated files"""
    output_path = Path(output_dir)
    if not output_path.exists():
        return 0
    
    count = 0
    for root, dirs, files in os.walk(output_path):
        count += len(files)
    return count

def show_generated_files(output_dir: str):
    """Show generated files structure"""
    output_path = Path(output_dir)
    if not output_path.exists():
        print("   No files generated")
        return
    
    # Show directory structure
    for root, dirs, files in os.walk(output_path):
        level = root.replace(str(output_path), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

def run_sample_test():
    """Run a sample generated test to demonstrate functionality"""
    print("\n🧪 Running Sample Test...")
    
    # Check if pytest is available
    try:
        import pytest
        print("✅ pytest is available")
    except ImportError:
        print("❌ pytest not found. Install with: pip install pytest")
        return
    
    # Check if generated tests exist
    test_dir = Path("demo_generated_tests/tests")
    if not test_dir.exists():
        print("❌ Generated tests not found. Run generation first.")
        return
    
    # Run a sample test
    print("🚀 Running generated tests...")
    os.system("cd demo_generated_tests && python -m pytest tests/ -v --tb=short")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--run-tests":
            run_sample_test()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python demo_csv_to_automation.py           # Generate tests from CSV")
            print("  python demo_csv_to_automation.py --run-tests  # Run generated tests")
            print("  python demo_csv_to_automation.py --help       # Show this help")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        main() 