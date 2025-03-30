from typing import Dict, Type, Any
from .types import CaptchaType
from .base import CaptchaGenerator, CaptchaConfig
from .image import ImageCaptchaGenerator
from ..config.settings import get_settings

class CaptchaFactory:
    
    # Register Generators
    _generators: Dict[CaptchaType, Type[CaptchaGenerator]] = {
        CaptchaType.IMAGE: ImageCaptchaGenerator
    }
    
    @classmethod
    def create(cls, type_: CaptchaType, **kwargs) -> CaptchaGenerator:
        
        if type_ not in cls._generators:
            raise ValueError(f"Unsupported captcha type: {type_}")
        
        # Get Default Config
        settings = get_settings()
        config_params = settings.get_captcha_config(type_.value)
        
        # Update Custom Config By Args (Override Default Config)
        config_params.update(kwargs)
        
        # Create Config Object
        config = CaptchaConfig(type=type_, params=config_params)
        
        # Create Generator Instance
        return cls._generators[type_](config)