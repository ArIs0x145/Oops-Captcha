import unittest
from unittest.mock import patch, MagicMock
from oopscaptcha.generators.types import CaptchaType
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.image import ImageCaptchaGenerator
from oopscaptcha.config.settings import Settings

class TestCaptchaFactory(unittest.TestCase):
    
    @patch('oopscaptcha.generators.factory.get_settings')
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
    
    @patch('oopscaptcha.generators.factory.get_settings')
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