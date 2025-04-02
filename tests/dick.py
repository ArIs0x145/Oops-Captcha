from captcha.generators.factory import CaptchaFactory
from captcha.generators.types import CaptchaType

def main():
    generator = CaptchaFactory.create(CaptchaType.IMAGE)
    generator.export()
    
if __name__ == "__main__":
    main()

