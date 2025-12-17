#!/usr/bin/env python3
"""
Security Test Runner - OTP Authentication Validation
Runs security tests against the stage environment to verify API endpoints
properly require OTP-based authentication.

Usage:
    python3 run_security_tests.py                    # Run all security tests
    python3 run_security_tests.py --quick            # Run quick security scan
    python3 run_security_tests.py --verbose          # Run with verbose output
    python3 run_security_tests.py --report           # Generate HTML report
    python3 run_security_tests.py --category otp     # Run specific category

Categories:
    unauth  - Test unauthenticated access rejection
    otp     - Test OTP flow validation
    token   - Test invalid/manipulated token rejection
    scan    - Run comprehensive endpoint security scan
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime


def get_python_executable():
    """Get the Python executable, preferring venv if available"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(project_root, 'venv', 'bin', 'python')
    
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


def run_security_tests(args):
    """Run security tests with specified options"""
    
    # Change to project directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    python_exec = get_python_executable()
    
    print("=" * 70)
    print("🔐 SECURITY TEST RUNNER - OTP Authentication Validation")
    print("=" * 70)
    print(f"📅 Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 Environment: Stage (https://app.stage.viewz.co)")
    print(f"🐍 Python: {python_exec}")
    print("=" * 70)
    
    # Build pytest command
    pytest_cmd = [
        python_exec, "-m", "pytest",
        "tests/api/test_security_otp_validation.py",
        "-v",
        "-m", "security",  # Only run tests marked as security
    ]
    
    # Add options based on arguments
    if args.verbose:
        pytest_cmd.extend(["-s", "--tb=long"])
    else:
        pytest_cmd.extend(["--tb=short"])
    
    if args.report:
        report_dir = os.path.join(project_root, "reports", "security")
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_report = os.path.join(report_dir, f"security_test_report_{timestamp}.html")
        
        pytest_cmd.extend([
            f"--html={html_report}",
            "--self-contained-html"
        ])
        print(f"📊 HTML Report will be saved to: {html_report}")
    
    if args.quick:
        # Run only essential security tests
        pytest_cmd.extend([
            "-k", "test_journal_entries_rejects_unauthenticated or test_login_does_not_return_token"
        ])
        print("⚡ Running QUICK security scan (essential tests only)")
    
    if args.category:
        category_mapping = {
            'unauth': 'test_*_rejects_unauthenticated',
            'otp': 'test_login_does_not_return_token or test_otp_validation',
            'token': 'test_*_invalid_token or test_*_manipulated',
            'scan': 'test_all_sensitive_endpoints'
        }
        if args.category in category_mapping:
            pytest_cmd.extend(["-k", category_mapping[args.category]])
            print(f"🎯 Running category: {args.category}")
        else:
            print(f"⚠️ Unknown category: {args.category}")
            print(f"   Available categories: {', '.join(category_mapping.keys())}")
    
    # Add logging
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"security_tests_{timestamp}.log")
    
    print(f"📝 Log file: {log_file}")
    print("=" * 70)
    print()
    
    # Run pytest
    with open(log_file, 'w') as f:
        f.write(f"Security Test Run - {datetime.now().isoformat()}\n")
        f.write(f"Command: {' '.join(pytest_cmd)}\n")
        f.write("=" * 70 + "\n\n")
    
    result = subprocess.run(
        pytest_cmd,
        cwd=project_root,
        capture_output=False
    )
    
    # Print summary
    print()
    print("=" * 70)
    if result.returncode == 0:
        print("✅ SECURITY TESTS PASSED - All authentication checks verified")
    elif result.returncode == 1:
        print("❌ SECURITY TESTS FAILED - Potential vulnerabilities detected!")
        print("   Review the test output above for details.")
    else:
        print(f"⚠️ Tests completed with exit code: {result.returncode}")
    
    print("=" * 70)
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run security tests for OTP authentication validation"
    )
    
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick security scan (essential tests only)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run with verbose output"
    )
    
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate HTML test report"
    )
    
    parser.add_argument(
        "--category", "-c",
        type=str,
        choices=['unauth', 'otp', 'token', 'scan'],
        help="Run specific test category: unauth, otp, token, scan"
    )
    
    args = parser.parse_args()
    
    exit_code = run_security_tests(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

