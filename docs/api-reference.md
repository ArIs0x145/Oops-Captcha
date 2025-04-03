# API Reference

## CaptchaGenerator

Base abstract class for all CAPTCHA generators.

```python
class CaptchaGenerator(Generic[SampleType, LabelType], ABC):
    def generate_label() -> LabelType: ...
    def generate_sample(label: LabelType) -> SampleType: ...
    def generate() -> Tuple[SampleType, LabelType]: ...
    def save(sample: SampleType, label: LabelType, output_dir=None, use_timestamp_dir=True) -> Tuple[Path, Path]: ...
    def export(output_dir=None) -> Tuple[Path, Path]: ...
    def generate_dataset(size, train_ratio=None, val_ratio=None, test_ratio=None, parallel=None, max_workers=None, seed=None, output_dir=None) -> Dict[str, List[Tuple[Path, Path]]]: ...
```

## CaptchaFactory

Factory class to create appropriate CAPTCHA generators.

```python
class CaptchaFactory:
    @classmethod
    def create(cls, type_: CaptchaType, **kwargs) -> CaptchaGenerator: ...
```

## ImageCaptchaGenerator

Implementation of image-based CAPTCHA generator.

```python
class ImageCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    # Inherits all methods from CaptchaGenerator
    # with specific implementation for image CAPTCHAs
```

## Settings

Configuration management class.

```python
class Settings:
    def __init__(self, config_path: str = "configs/default.yaml"): ...
    def get_captcha_config(self, type_: str) -> Dict[str, Any]: ...
```

## IDGenerator

Unique ID and timestamp generator.

```python
class IDGenerator:
    @staticmethod
    def generate_captcha_id() -> str: ...
    @staticmethod
    def get_dir_timestamp() -> str: ...
    @staticmethod
    def reset_dir_timestamp(): ...
``` 
