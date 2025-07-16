"""
Date Format Validator for API Testing
Validates that all date fields in API requests and responses use YYYY-MM-DD format
"""

import re
import json
from typing import Dict, Any, List, Tuple, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DateFormatValidator:
    """Validates date formats in API payloads"""
    
    # YYYY-MM-DD format regex pattern
    VALID_DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    # Common date field names to check
    DATE_FIELD_PATTERNS = [
        r'.*date.*',
        r'.*_at$',
        r'.*_on$',
        r'created.*',
        r'updated.*', 
        r'modified.*',
        r'timestamp.*',
        r'time.*',
        r'start.*',
        r'end.*',
        r'expir.*',
        r'due.*'
    ]
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize date format validator
        
        Args:
            strict_mode: If True, raises exception on invalid dates. If False, logs warnings.
        """
        self.strict_mode = strict_mode
        self.validation_errors = []
        self.validation_warnings = []
        
    def is_valid_date_format(self, date_string: str) -> bool:
        """
        Check if date string matches YYYY-MM-DD format and is a valid date
        
        Args:
            date_string: Date string to validate
            
        Returns:
            bool: True if valid YYYY-MM-DD format, False otherwise
        """
        if not isinstance(date_string, str):
            return False
            
        # Check pattern match
        if not self.VALID_DATE_PATTERN.match(date_string):
            return False
            
        # Check if it's a valid date
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def is_likely_date_field(self, field_name: str) -> bool:
        """
        Check if field name suggests it contains date data
        
        Args:
            field_name: Field name to check
            
        Returns:
            bool: True if field name suggests date content
        """
        field_lower = field_name.lower()
        
        # Skip metadata fields that contain date format descriptions
        if 'format' in field_lower or 'schema' in field_lower or 'template' in field_lower:
            return False
        
        for pattern in self.DATE_FIELD_PATTERNS:
            if re.match(pattern, field_lower):
                return True
                
        return False
    
    def validate_date_value(self, field_path: str, value: Any) -> bool:
        """
        Validate a single date value
        
        Args:
            field_path: Path to the field (e.g., "data.entry_date")
            value: Value to validate
            
        Returns:
            bool: True if valid, False if invalid
        """
        if not isinstance(value, str):
            # Non-string values in date fields might be acceptable (null, etc.)
            if value is not None:
                warning = f"Non-string value in potential date field '{field_path}': {type(value).__name__}"
                self.validation_warnings.append(warning)
                logger.warning(warning)
            return True
            
        if not self.is_valid_date_format(value):
            error = f"Invalid date format in field '{field_path}': '{value}' (expected YYYY-MM-DD)"
            self.validation_errors.append(error)
            
            if self.strict_mode:
                logger.error(error)
                return False
            else:
                logger.warning(error)
                
        return True
    
    def validate_json_payload(self, payload: Union[Dict[str, Any], List[Any]], 
                            path_prefix: str = "") -> bool:
        """
        Recursively validate date formats in JSON payload
        
        Args:
            payload: JSON payload to validate (dict, list, or primitive)
            path_prefix: Current path in the JSON structure
            
        Returns:
            bool: True if all dates valid, False if any invalid dates found
        """
        if isinstance(payload, dict):
            return self._validate_dict(payload, path_prefix)
        elif isinstance(payload, list):
            return self._validate_list(payload, path_prefix)
        else:
            # Primitive value - no validation needed
            return True
    
    def _validate_dict(self, data: Dict[str, Any], path_prefix: str) -> bool:
        """Validate dictionary/object"""
        all_valid = True
        
        for key, value in data.items():
            current_path = f"{path_prefix}.{key}" if path_prefix else key
            
            # Check if this looks like a date field
            if self.is_likely_date_field(key):
                if not self.validate_date_value(current_path, value):
                    all_valid = False
            
            # Recursively validate nested structures
            if isinstance(value, (dict, list)):
                if not self.validate_json_payload(value, current_path):
                    all_valid = False
                    
        return all_valid
    
    def _validate_list(self, data: List[Any], path_prefix: str) -> bool:
        """Validate list/array"""
        all_valid = True
        
        for index, item in enumerate(data):
            current_path = f"{path_prefix}[{index}]"
            
            if not self.validate_json_payload(item, current_path):
                all_valid = False
                
        return all_valid
    
    def validate_request_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validate request payload for correct date formats
        
        Args:
            payload: Request payload to validate
            
        Returns:
            bool: True if all dates valid, False otherwise
        """
        logger.info("Validating request payload for date formats")
        self.validation_errors.clear()
        self.validation_warnings.clear()
        
        return self.validate_json_payload(payload, "request")
    
    def validate_response_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validate response payload for correct date formats
        
        Args:
            payload: Response payload to validate
            
        Returns:
            bool: True if all dates valid, False otherwise
        """
        logger.info("Validating response payload for date formats")
        self.validation_errors.clear()
        self.validation_warnings.clear()
        
        return self.validate_json_payload(payload, "response")
    
    def get_validation_results(self) -> Dict[str, Any]:
        """
        Get detailed validation results
        
        Returns:
            Dict containing validation errors, warnings, and summary
        """
        return {
            "valid": len(self.validation_errors) == 0,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
            "errors": self.validation_errors.copy(),
            "warnings": self.validation_warnings.copy()
        }
    
    def assert_valid_dates(self, payload: Dict[str, Any], payload_type: str = "payload"):
        """
        Assert that all dates in payload are valid, raising exception if not
        
        Args:
            payload: Payload to validate
            payload_type: Type description for error messages
            
        Raises:
            AssertionError: If invalid dates found
        """
        is_valid = self.validate_json_payload(payload)
        
        if not is_valid:
            error_summary = f"Date format validation failed for {payload_type}:\n"
            error_summary += "\n".join(f"  - {error}" for error in self.validation_errors)
            raise AssertionError(error_summary)


class DateFormatTestHelper:
    """Helper class for date format testing in API tests"""
    
    def __init__(self):
        self.validator = DateFormatValidator(strict_mode=False)
        
    def get_test_dates(self) -> Dict[str, List[str]]:
        """
        Get test date sets for validation testing
        
        Returns:
            Dict with 'valid' and 'invalid' date lists
        """
        return {
            "valid": [
                "2024-01-01",
                "2024-12-31",
                "2023-06-15", 
                "2025-03-10",
                "2020-02-29",  # Valid leap year date
                datetime.now().strftime("%Y-%m-%d")
            ],
            "invalid": [
                "01/01/2024",   # MM/DD/YYYY
                "01-01-2024",   # MM-DD-YYYY  
                "2024/01/01",   # YYYY/MM/DD
                "2024.01.01",   # YYYY.MM.DD
                "Jan 1, 2024",  # Month name format
                "1/1/24",       # M/D/YY
                "2024-1-1",     # YYYY-M-D (no zero padding)
                "24-01-01",     # YY-MM-DD
                "2024-13-01",   # Invalid month
                "2024-12-32",   # Invalid day
                "2021-02-29",   # Invalid leap year date
                "invalid-date",
                "",
                "null",
                "undefined"
            ]
        }
    
    def create_test_payload_with_dates(self, valid_dates: bool = True) -> Dict[str, Any]:
        """
        Create test payload with date fields for testing
        
        Args:
            valid_dates: If True, use valid dates. If False, use invalid dates.
            
        Returns:
            Dict: Test payload with various date fields
        """
        test_dates = self.get_test_dates()
        dates_to_use = test_dates["valid"] if valid_dates else test_dates["invalid"]
        
        return {
            "entry_date": dates_to_use[0] if dates_to_use else "2024-01-01",
            "created_at": dates_to_use[1] if len(dates_to_use) > 1 else "2024-01-02",
            "updated_on": dates_to_use[2] if len(dates_to_use) > 2 else "2024-01-03",
            "start_date": dates_to_use[3] if len(dates_to_use) > 3 else "2024-01-04",
            "end_date": dates_to_use[4] if len(dates_to_use) > 4 else "2024-01-05",
            "metadata": {
                "transaction_date": dates_to_use[0] if dates_to_use else "2024-01-06",
                "due_date": dates_to_use[1] if len(dates_to_use) > 1 else "2024-01-07"
            },
            "items": [
                {
                    "item_date": dates_to_use[2] if len(dates_to_use) > 2 else "2024-01-08",
                    "expiry_date": dates_to_use[3] if len(dates_to_use) > 3 else "2024-01-09"
                }
            ],
            "non_date_field": "This should not be validated",
            "amount": 1000.50,
            "count": 5
        }
    
    def validate_api_response_dates(self, response_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate date formats in API response and return detailed results
        
        Args:
            response_data: API response data to validate
            
        Returns:
            Tuple of (is_valid, validation_results)
        """
        is_valid = self.validator.validate_response_payload(response_data)
        results = self.validator.get_validation_results()
        
        return is_valid, results 