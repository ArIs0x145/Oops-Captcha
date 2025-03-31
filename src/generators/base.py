from abc import ABC, abstractmethod
from typing import TypeVar, Tuple, Any, Dict, Generic, Union
from dataclasses import dataclass
from pathlib import Path
from .types import CaptchaType

DataType = TypeVar('DataType')  # Captcha Data
LabelType = TypeVar('LabelType')  # Captcha Label

@dataclass(frozen=True)
class CaptchaConfig:
    type: CaptchaType
    params: Dict[str, Any]

class CaptchaGenerator(Generic[DataType, LabelType], ABC):
    
    def __init__(self, config: CaptchaConfig):
        self.config = config
    
    @abstractmethod
    def generate(self) -> Tuple[DataType, LabelType]:
        pass
    
    @abstractmethod
    def save(self, data: DataType, path: Union[str, Path]) -> None:
        pass