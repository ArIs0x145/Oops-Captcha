# 擴展

該系統設計為可擴展的，支持添加新類型的驗證碼：

1. 創建一個新的驗證碼生成器類，繼承 `CaptchaGenerator`
2. 在 `CaptchaType` 枚舉中添加新類型
3. 在 `CaptchaFactory._generators` 中註冊新的生成器
4. 在配置文件中添加相應的配置

擴展新驗證碼類型的示例：

```python
# 1. 在 types.py 中添加
class CaptchaType(Enum):
    IMAGE = 'image'
    MATH = 'math'  # 新類型

# 2. 創建新的生成器類
class MathCaptchaGenerator(CaptchaGenerator[BytesIO, str]):
    # 實現...

# 3. 在 factory.py 中註冊
class CaptchaFactory:
    _generators: Dict[CaptchaType, Type[CaptchaGenerator]] = {
        CaptchaType.IMAGE: ImageCaptchaGenerator,
        CaptchaType.MATH: MathCaptchaGenerator  # 新生成器
    } 