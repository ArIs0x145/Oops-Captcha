import unittest
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image # type: ignore

from captcha.generators.types import CaptchaType
from captcha.generators.base import CaptchaConfig
from captcha.generators.image import ImageCaptchaGenerator

class TestImageCaptchaGenerator(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.config = CaptchaConfig(
            type=CaptchaType.IMAGE, 
            params={
                'width': 160,
                'height': 60,
                'length': 6,
                'characters': 'abcdefgh12345',
                'output_dir': tempfile.mkdtemp()  # Use temporary directory
            }
        )
        self.generator = ImageCaptchaGenerator(self.config)
    
    def tearDown(self):
        """Clean up test environment"""
        # Delete temporary files
        output_dir = Path(self.config.params['output_dir'])
        if output_dir.exists():
            import shutil
            shutil.rmtree(output_dir)
    
    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.generator.width, 160)
        self.assertEqual(self.generator.height, 60)
        self.assertEqual(self.generator.length, 6)
        self.assertEqual(self.generator.characters, 'abcdefgh12345')
    
    def test_generate_random_text(self):
        """Test random text generation"""
        text = self.generator._generate_random_text()
        self.assertEqual(len(text), 6)
        for char in text:
            self.assertIn(char, 'abcdefgh12345')
    
    def test_generate(self):
        """Test captcha generation"""
        image, text = self.generator.generate()
        
        # Check if image is a BytesIO object
        self.assertIsInstance(image, BytesIO)
        
        # Check if text is a string with correct length
        self.assertIsInstance(text, str)
        self.assertEqual(len(text), 6)
        
        # Check if the image can be opened
        img = Image.open(BytesIO(image.getvalue()))
        self.assertEqual(img.size, (160, 60))
    
    def test_export(self):
        """Test exporting captcha (generate and save)"""
        sample_path, label_path = self.generator.export()
        
        # Check if files exist
        self.assertTrue(sample_path.exists())
        self.assertTrue(label_path.exists())
        
        # Check if the image can be opened
        img = Image.open(sample_path)
        self.assertEqual(img.size, (160, 60))
        
        # Check label file content
        with open(label_path, 'r') as f:
            label = f.read()
        
        # Label length should be 6
        self.assertEqual(len(label), 6)
        
        # Each character in the label should be in the allowed character set
        for char in label:
            self.assertIn(char, 'abcdefgh12345')
    
    def test_save(self):
        """Test save method with provided sample and label"""
        # Generate a sample first
        image, text = self.generator.generate()
        
        # Save the generated sample and label
        sample_path, label_path = self.generator.save(image, text)
        
        # Check if files exist
        self.assertTrue(sample_path.exists())
        self.assertTrue(label_path.exists())
        
        # Check if the image can be opened
        img = Image.open(sample_path)
        self.assertEqual(img.size, (160, 60))
        
        # Check label file content
        with open(label_path, 'r') as f:
            label = f.read()
        
        # Label should match the original text
        self.assertEqual(label, text)

if __name__ == '__main__':
    unittest.main() 