from abc import ABC, abstractmethod
from typing import TypeVar, Tuple, Any, Dict, Generic, Union, Optional
from dataclasses import dataclass
from pathlib import Path
from .types import CaptchaType

SampleType = TypeVar('SampleType')  # Captcha Sample
LabelType = TypeVar('LabelType')  # Captcha Label

@dataclass(frozen=True)
class CaptchaConfig:
    type: CaptchaType
    params: Dict[str, Any]

class CaptchaGenerator(Generic[SampleType, LabelType], ABC):
    
    def __init__(self, config: CaptchaConfig):
        self.config = config
    
    @abstractmethod
    def generate(self) -> Tuple[SampleType, LabelType]:
        pass
    
    @abstractmethod
    def _save_sample(self, sample: SampleType, path: Union[str, Path]) -> Path:
        pass
    
    @abstractmethod
    def _save_label(self, label: LabelType, path: Union[str, Path]) -> Path:
        pass
    
    @abstractmethod
    def save(self, sample: SampleType, label: LabelType, output_dir: Optional[Union[str, Path]] = None) -> Tuple[Path, Path]:
        pass
    
    def export(self, output_dir: Optional[Union[str, Path]] = None) -> Tuple[Path, Path]:
        sample, label = self.generate()
        return self.save(sample, label, output_dir)