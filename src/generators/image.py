from typing import Any, Tuple
from captcha.image import ImageCaptcha
from .base import CaptchaGenerator, CaptchaConfig
import random

class ImageCaptchaGenerator(CaptchaGenerator[Any, str]):
    
    def __init__(self, config: CaptchaConfig):
        super().__init__(config)
        # Get or Set Params
        params = config.params
        self.width = params.get('width', 160)
        self.height = params.get('height', 60)
        self.fonts = params.get('fonts')
        self.length = params.get('length', 4)
        self.characters = params.get('characters', "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Create Image Generator
        self.generator = ImageCaptcha(
            width=self.width,
            height=self.height,
            fonts=self.fonts
        )
    
    def generate(self) -> Tuple[Any, str]:
        text = self._generate_text()
        image = self.generator.generate(text)
        return image, text
    
    def save(self, image: Any, path: str) -> None:
        self.generator.write(image, path)
    
    # Generate Random Text
    def _generate_text(self) -> str:
        return ''.join(random.choice(self.characters) 
                      for _ in range(self.length))