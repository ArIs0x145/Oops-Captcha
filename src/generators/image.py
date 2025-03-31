from typing import Tuple, Union
from captcha.image import ImageCaptcha  # type: ignore
from .base import CaptchaGenerator, CaptchaConfig
import random
from io import BytesIO
from PIL import Image  # type: ignore
from pathlib import Path

class ImageCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    
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
    
    def generate(self) -> Tuple[BytesIO, str]:
        text = self._generate_text()
        image = self.generator.generate(str(text))
        return image, text
    
    def save_sample(self, sample: BytesIO, path: Union[str, Path]) -> None:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with BytesIO(sample.getvalue()) as image_data:
                with Image.open(image_data) as img:
                    img.save(path_obj)
        except Exception as e:
            raise IOError(f"Failed to save captcha image to {path}: {e}")
    
    def save_label(self, label: str, path: Union[str, Path]) -> None:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path_obj, 'w') as f:
                f.write(label)
        except Exception as e:
            raise IOError(f"Failed to save captcha label to {path}: {e}")
    
    # Generate Random Text
    def _generate_text(self) -> str:
        return ''.join(random.choice(self.characters) 
                      for _ in range(self.length))