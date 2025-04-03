# API 參考

## CaptchaGenerator

所有驗證碼生成器的抽象基類。

```python
class CaptchaGenerator(Generic[SampleType, LabelType], ABC):
    def generate_label() -> LabelType: ...
    def generate_sample(label: LabelType) -> SampleType: ...
    def generate() -> Tuple[SampleType, LabelType]: ...
    def save(sample: SampleType, label: LabelType, output_dir=None, use_timestamp_dir=True) -> Tuple[Path, Path]: ...
    def export(output_dir=None) -> Tuple[Path, Path]: ...
    def generate_dataset(size, train_ratio=None, val_ratio=None, test_ratio=None, parallel=False, max_workers=None, seed=None, output_dir=None) -> Dict[str, List[Tuple[Path, Path]]]: ...
```

## CaptchaFactory

創建驗證碼生成器的工廠類。

```python
class CaptchaFactory:
    @classmethod
    def create(cls, type_: CaptchaType, **kwargs) -> CaptchaGenerator: ...
```

## ImageCaptchaGenerator

圖像驗證碼生成器的實現。

```python
class ImageCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    # 繼承 CaptchaGenerator 的所有方法
    # 並為圖像驗證碼提供特定實現
```

## Settings

配置管理類。

```python
class Settings:
    def __init__(self, config_path: str = "configs/default.yaml"): ...
    def get_captcha_config(self, type_: str) -> Dict[str, Any]: ...
```

## IDGenerator

唯一 ID 和時間戳生成器。

```python
class IDGenerator:
    @staticmethod
    def generate_captcha_id() -> str: ...
    @staticmethod
    def get_dir_timestamp() -> str: ...
    @staticmethod
    def reset_dir_timestamp(): ...
``` 