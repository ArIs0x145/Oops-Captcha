import unittest
import re
import time
from collections import Counter
from oopscaptcha.utils.id_generator import IDGenerator

class TestIDGenerator(unittest.TestCase):
    
    def test_generate_captcha_id_returns_string(self):
        """Test that the method returns a string"""
        result = IDGenerator.generate_captcha_id()
        self.assertIsInstance(result, str)
    
    def test_generate_captcha_id_format(self):
        """Test that the ID has the correct format"""
        result = IDGenerator.generate_captcha_id()
        
        # Should start with "captcha_"
        self.assertTrue(result.startswith("captcha_"))
        
        # Check the pattern: captcha_YYYYMMDD_HHMMSS_uuid
        pattern = r"^captcha_\d{8}_\d{6}_[0-9a-f]{12}$"
        self.assertTrue(re.match(pattern, result), f"ID format incorrect: {result}")
    
    def test_generate_captcha_id_contains_current_timestamp(self):
        """Test that the ID contains the current timestamp"""
        current_time = time.strftime("%Y%m%d_%H%M")  # Minutes precision for test stability
        result = IDGenerator.generate_captcha_id()
        
        self.assertTrue(current_time in result, 
                       f"Current timestamp {current_time} not in ID {result}")
    
    def test_generate_captcha_id_uniqueness(self):
        """Test that generated IDs are unique"""
        # Generate 100 IDs and check they're all unique
        ids = [IDGenerator.generate_captcha_id() for _ in range(100)]
        id_counts = Counter(ids)
        
        # Check that each ID appears exactly once
        for id_str, count in id_counts.items():
            self.assertEqual(count, 1, f"ID {id_str} was generated {count} times")
        
        # Also check the total number of unique IDs
        self.assertEqual(len(id_counts), 100, 
                        f"Expected 100 unique IDs, got {len(id_counts)}")

if __name__ == "__main__":
    unittest.main()
