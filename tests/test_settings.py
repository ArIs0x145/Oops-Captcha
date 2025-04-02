import unittest
import os
import sys
import tempfile
import yaml # type: ignore
from unittest.mock import patch, mock_open

from src.config.settings import Settings, get_settings

class TestSettings(unittest.TestCase):
    
    def test_load_config(self):
        """Test loading configuration file"""
        # Create temporary configuration file
        config_data = {
            'captcha': {
                'image': {
                    'width': 200,
                    'height': 80,
                    'length': 6
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            yaml.dump(config_data, temp)
            temp_path = temp.name
        
        try:
            # Create Settings instance
            settings = Settings(config_path=temp_path)
            
            # Verify configuration was loaded correctly
            self.assertEqual(settings._config, config_data)
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_get_captcha_config(self):
        """Test getting captcha configuration"""
        # Mock configuration
        config_data = {
            'captcha': {
                'image': {
                    'width': 200,
                    'height': 80,
                    'length': 6
                }
            }
        }
        
        # Use mock_open to simulate file reading
        with patch('builtins.open', mock_open(read_data=yaml.dump(config_data))):
            settings = Settings()
            
            # Test getting existing configuration
            image_config = settings.get_captcha_config('image')
            self.assertEqual(image_config, {
                'width': 200,
                'height': 80,
                'length': 6
            })
            
            # Test getting non-existent configuration
            non_existent = settings.get_captcha_config('non_existent')
            self.assertEqual(non_existent, {})
    
    def test_file_not_found(self):
        """Test handling non-existent configuration file"""
        # Use non-existent file path
        non_existent_path = '/path/to/non_existent_file.yaml'
        
        # Should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError) as context:
            Settings(config_path=non_existent_path)
        
        # Verify error message
        self.assertIn('not found', str(context.exception))
    
    @patch('src.config.settings.Settings')
    def test_get_settings_cache(self, mock_settings):
        """Test caching functionality"""
        # Ensure each call returns the same instance
        instance1 = get_settings()
        instance2 = get_settings()
        
        # Verify Settings instance was created only once
        mock_settings.assert_called_once()

if __name__ == '__main__':
    unittest.main() 