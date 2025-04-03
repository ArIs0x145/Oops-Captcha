# Extending

The system is designed to be extensible, supporting the addition of new CAPTCHA types:

1. Create a new CAPTCHA generator class that inherits from `CaptchaGenerator`
2. Add a new type to the `CaptchaType` enum
3. Register the new generator in `CaptchaFactory._generators`
4. Add corresponding configuration in the config file

Example of extending with a new CAPTCHA type:

```python
# 1. Add to types.py
class CaptchaType(Enum):
    IMAGE = 'image'
    MATH = 'math'  # New type

# 2. Create a new generator class
class MathCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    # Implementation...

# 3. Register in factory.py
class CaptchaFactory:
    _generators: Dict[CaptchaType, Type[CaptchaGenerator]] = {
        CaptchaType.IMAGE: ImageCaptchaGenerator,
        CaptchaType.MATH: MathCaptchaGenerator  # New generator
    } 