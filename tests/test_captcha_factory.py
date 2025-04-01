import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generators.types import CaptchaType
from src.generators.factory import CaptchaFactory
from src.generators.image import ImageCaptchaGenerator
from src.generators.base import CaptchaGenerator
from src.config.settings import Settings

class TestCaptchaFactory(unittest.TestCase):
    
    @patch('src.generators.factory.get_settings')
    def test_create_image_captcha(self, mock_get_settings):
        """Test creating image captcha generator"""
        # Set up mock
        mock_settings = MagicMock(spec=Settings)
        mock_settings.get_captcha_config.return_value = {
            'width': 160, 
            'height': 60
        }
        mock_get_settings.return_value = mock_settings
        
        # Create generator
        generator = CaptchaFactory.create(CaptchaType.IMAGE)
        
        # Verify generator type
        self.assertIsInstance(generator, ImageCaptchaGenerator)
        self.assertEqual(generator.width, 160)
        self.assertEqual(generator.height, 60)
        
        # Verify mock was called correctly
        mock_get_settings.assert_called_once()
        mock_settings.get_captcha_config.assert_called_once_with('image')
    
    @patch('src.generators.factory.get_settings')
    def test_create_with_custom_params(self, mock_get_settings):
        """Test creating generator with custom parameters"""
        # Set up mock
        mock_settings = MagicMock(spec=Settings)
        mock_settings.get_captcha_config.return_value = {
            'width': 160, 
            'height': 60,
            'length': 4
        }
        mock_get_settings.return_value = mock_settings
        
        # Create generator with parameter overrides
        generator = CaptchaFactory.create(
            CaptchaType.IMAGE,
            width=200,
            length=8
        )
        
        # Verify parameters were correctly overridden
        self.assertEqual(generator.width, 200)  # Custom parameter
        self.assertEqual(generator.height, 60)  # From configuration
        self.assertEqual(generator.length, 8)   # Custom parameter overriding configuration
    
    def test_unsupported_type(self):
        """Test unsupported captcha type"""
        # Create a non-existent enum value
        class FakeCaptchaType:
            value = 'fake'
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            CaptchaFactory.create(FakeCaptchaType())
        
        # Verify error message
        self.assertIn('Unsupported captcha type', str(context.exception))

if __name__ == '__main__':
    unittest.main() 