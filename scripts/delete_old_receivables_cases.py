#!/usr/bin/env python3
"""
Delete OLD Receivables cases (C43176-C43188) from TestRail Suite 139
These are duplicates - we're keeping the NEW cases (C63962-C63974) with automation
"""

import os
import requests
from base64 import b64encode

class CaseDeleter:
    def __init__(self):
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        
        self.auth = b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
    
    def delete_case(self, case_id):
        """Delete a test case"""
        url = f"{self.url}/index.php?/api/v2/delete_case/{case_id}"
        
        try:
            response = requests.post(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                print(f"  ⚠️ Status {response.status_code}: {response.text[:100]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def delete_old_receivables_cases(self):
        """Delete OLD receivables cases C43176-C43188"""
        old_cases = range(43176, 43189)  # C43176 to C43188
        
        print("=" * 80)
        print("DELETING OLD RECEIVABLES DUPLICATE CASES")
        print("=" * 80)
        print(f"\nDeleting cases C43176-C43188 (13 duplicate cases)")
        print("Keeping NEW cases C63962-C63974 (with automation)\n")
        
        deleted = []
        failed = []
        
        for case_id in old_cases:
            print(f"🗑️  Deleting C{case_id}...", end=" ")
            
            if self.delete_case(case_id):
                deleted.append(case_id)
                print("✅ Deleted")
            else:
                failed.append(case_id)
                print("❌ Failed")
        
        # Summary
        print("\n" + "=" * 80)
        print("DELETION SUMMARY")
        print("=" * 80)
        print(f"✅ Successfully deleted: {len(deleted)} cases")
        print(f"❌ Failed to delete: {len(failed)} cases")
        
        if deleted:
            print(f"\nDeleted cases: C{min(deleted)}-C{max(deleted)}")
        
        if failed:
            print(f"\n⚠️ Failed cases:")
            for case_id in failed:
                print(f"  - C{case_id}")
        
        return len(deleted), len(failed)

if __name__ == "__main__":
    print("\n⚠️  WARNING: This will DELETE old duplicate Receivables cases from TestRail!")
    print("Cases to delete: C43176-C43188 (13 cases)")
    print("Keeping: C63962-C63974 (with automation)\n")
    
    response = input("Do you want to proceed? (yes/no): ")
    
    if response.lower() == 'yes':
        deleter = CaseDeleter()
        deleted, failed = deleter.delete_old_receivables_cases()
        
        if failed == 0:
            print("\n🎉 All duplicate cases successfully removed!")
        else:
            print(f"\n⚠️  {failed} cases failed to delete. Check permissions or case status.")
    else:
        print("\n❌ Operation cancelled")

