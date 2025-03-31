from abc import ABC, abstractmethod
from typing import TypeVar, Tuple, Any, Dict, Generic, Union
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
    def save_sample(self, sample: SampleType, path: Union[str, Path]) -> None:
        pass
    
    @abstractmethod
    def save_label(self, label: LabelType, path: Union[str, Path]) -> None:
        pass