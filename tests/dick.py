from src.generators.factory import CaptchaFactory
from src.generators.types import CaptchaType

def main():
    generator = CaptchaFactory.create(CaptchaType.IMAGE)
    generator.export()
    
if __name__ == "__main__":
    main()

