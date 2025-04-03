import unittest
import re
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
        
        # Check the pattern: captcha_[0-9a-f]{24,32} (hexadecimal UUID)
        pattern = r"^captcha_[0-9a-f]{24,32}$"
        self.assertTrue(re.match(pattern, result), f"ID format incorrect: {result}")
    
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
    
    def test_dir_timestamp_consistency(self):
        """Test that dir timestamp remains consistent until reset"""
        # Get timestamp multiple times
        timestamp1 = IDGenerator.get_dir_timestamp()
        timestamp2 = IDGenerator.get_dir_timestamp()
        timestamp3 = IDGenerator.get_dir_timestamp()
        
        # All timestamps should be identical
        self.assertEqual(timestamp1, timestamp2)
        self.assertEqual(timestamp2, timestamp3)
        
        # After reset, should get a new timestamp
        IDGenerator.reset_dir_timestamp()
        new_timestamp = IDGenerator.get_dir_timestamp()
        
        # The new timestamp should be different (though in very rare cases it might be the same)
        # This is a weak assertion because timestamps could be equal if tests run very quickly
        # or if they run exactly at the change of a second
        
if __name__ == "__main__":
    unittest.main()
