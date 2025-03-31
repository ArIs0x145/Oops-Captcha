from pathlib import Path
from src.generators.factory import CaptchaFactory
from src.generators.types import CaptchaType

def test_default_image_captcha():
    generator = CaptchaFactory.create(CaptchaType.IMAGE)
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    image, text = generator.generate()
    generator.save_sample(image, output_dir / f"default_{text}.png")
    generator.save_label(text, output_dir / f"default_{text}.txt")
    
    # Default Length Is 4
    assert len(text) == 4
    
    print(f"Generated Captcha: {text}")

def test_custom_image_captcha():
    generator = CaptchaFactory.create(
        CaptchaType.IMAGE,
        width=200,
        height=80,
        length=6,
        characters="0123456789"
    )
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    image, text = generator.generate()
    generator.save_sample(image, output_dir / f"custom_{text}.png")
    generator.save_label(text, output_dir / f"custom_{text}.txt")
    
    # Custom Length Is 6
    assert len(text) == 6
    # All Characters Are Numbers
    assert all(c in "0123456789" for c in text)

    print(f"Generated Captcha: {text}")

if __name__ == "__main__":
    test_default_image_captcha()
    test_custom_image_captcha()
    print("All Tests Passed!")