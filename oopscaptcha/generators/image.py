from typing import Tuple, Union, Optional
from captcha.image import ImageCaptcha  # type: ignore
from .base import CaptchaGenerator, CaptchaConfig
import random
from io import BytesIO
from PIL import Image  # type: ignore
from pathlib import Path
from ..utils.id_generator import IDGenerator
from ..config.settings import get_settings

class ImageCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    
    def __init__(self, config: CaptchaConfig):
        super().__init__(config)
        # Get or Set Params
        params = config.params
        captcha_config = get_settings().get_captcha_config(config.type.value)
        
        # Use Params First, Then Use Config
        self.width = params.get('width') if 'width' in params else captcha_config.get('width')
        self.height = params.get('height') if 'height' in params else captcha_config.get('height') 
        self.length = params.get('length') if 'length' in params else captcha_config.get('length')
        self.fonts = params.get('fonts') if 'fonts' in params else captcha_config.get('fonts')
        self.characters = params.get('characters') if 'characters' in params else captcha_config.get('characters')
        self.output_dir = params.get('output_dir') if 'output_dir' in params else captcha_config.get('output_dir')

        # Check Required Params
        if self.width is None:
            raise ValueError(f"Missing required parameter 'width' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        if self.height is None:
            raise ValueError(f"Missing required parameter 'height' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        if self.length is None:
            raise ValueError(f"Missing required parameter 'length' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        if self.fonts is None:
            raise ValueError(f"Missing required parameter 'fonts' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        if self.characters is None:
            raise ValueError(f"Missing required parameter 'characters' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        if self.output_dir is None:
            raise ValueError(f"Missing required parameter 'output_dir' and no default value in configuration for CAPTCHA type '{config.type.value}'")
        
        self.output_dir = Path(self.output_dir)
        
        # Create Image Generator
        self.generator = ImageCaptcha(
            width=self.width,
            height=self.height,
            fonts=self.fonts
        )
    
    # Generate Random Text
    def generate_label(self) -> str:
        return ''.join(random.choice(self.characters) 
                      for _ in range(self.length))
    
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
    
    def generate_sample(self, label: str) -> BytesIO:
        return self.generator.generate(str(label))

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
    
    def generate(self) -> Tuple[BytesIO, str]:
        text = self.generate_label()
        image = self.generate_sample(str(text))
        return image, text
                      
    def save(self, sample: BytesIO, label: str, output_dir: Optional[Union[str, Path]] = None, use_timestamp_dir: bool = True) -> Tuple[Path, Path]:
        if output_dir is None:
            base_dir = self.output_dir
        else:
            base_dir = Path(output_dir)
        
        # Only create timestamp directory if specified
        if use_timestamp_dir:
            timestamp = IDGenerator.get_dir_timestamp()
            base_dir = base_dir / timestamp
        
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