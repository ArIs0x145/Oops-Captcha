from typing import Tuple, Union, Optional
from captcha.image import ImageCaptcha  # type: ignore
from .base import CaptchaGenerator, CaptchaConfig
import random
from io import BytesIO
from PIL import Image  # type: ignore
from pathlib import Path
from ..utils.id_generator import IDGenerator

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
        self.output_dir = Path(params.get('output_dir', f"datasets/{config.type.value}"))
        
        # Create Image Generator
        self.generator = ImageCaptcha(
            width=self.width,
            height=self.height,
            fonts=self.fonts
        )
    
    def generate(self) -> Tuple[BytesIO, str]:
        text = self._generate_random_text()
        image = self.generator.generate(str(text))
        return image, text
    
    def _save_sample(self, sample: BytesIO, path: Union[str, Path]) -> Path:
        
        # Convert to Path object
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with BytesIO(sample.getvalue()) as image_data:
                with Image.open(image_data) as img:
                    img.save(path_obj)
            return path_obj
        except Exception as e:
            raise IOError(f"Failed to save captcha image to {path}: {e}")
    
    def _save_label(self, label: str, path: Union[str, Path]) -> Path:
       
        # Convert to Path object
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path_obj, 'w') as f:
                f.write(label)
            return path_obj
        except Exception as e:
            raise IOError(f"Failed to save captcha label to {path}: {e}")
    
    # Generate Random Text
    def _generate_random_text(self) -> str:
        return ''.join(random.choice(self.characters) 
                      for _ in range(self.length))
                      
    def save(self, sample: BytesIO, label: str, output_dir: Optional[Union[str, Path]] = None) -> Tuple[Path, Path]:

        if output_dir is None:
            base_dir = self.output_dir
        else:
            base_dir = Path(output_dir)
        
        # Create Directories
        images_dir = base_dir / "samples"
        labels_dir = base_dir / "labels"
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Unique Filename
        base_filename = IDGenerator.generate_captcha_id()
        
        # Save Sample and Label
        sample_path = self._save_sample(sample, images_dir / f"{base_filename}.png")
        label_path = self._save_label(label, labels_dir / f"{base_filename}.txt")
        
        return sample_path, label_path