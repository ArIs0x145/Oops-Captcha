# Oops-Captcha

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ArIs0x145/Oops-Captcha)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

A flexible and extensible Python library for generating CAPTCHA images and datasets.

## Installation

```bash
# Clone the repository
git clone https://github.com/ArIs0x145/Oops-Captcha.git
cd Oops-Captcha

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

Generate a single CAPTCHA image:

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# Create an image CAPTCHA generator
generator = CaptchaFactory.create(CaptchaType.IMAGE)

# Generate and save a CAPTCHA
sample_path, label_path = generator.export()
print(f"CAPTCHA image saved to: {sample_path}")
print(f"CAPTCHA label saved to: {label_path}")
```

Generate a CAPTCHA dataset:

```bash
python -m tests.generate_dataset --type image --size 1000 --parallel
```

## Usage

### Generating Single CAPTCHA

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# Create an image CAPTCHA generator with custom settings
generator = CaptchaFactory.create(
    CaptchaType.IMAGE,
    width=200,
    height=80,
    length=6,
    characters="0123456789"
)

# Generate and save
sample_path, label_path = generator.export("custom_output_dir")
```

### Generating CAPTCHA Dataset

From the command line:

```bash
python -m tests.generate_dataset --type image --size 1000 --train-ratio 0.7 --val-ratio 0.2 --test-ratio 0.1 --parallel --output-dir custom_dataset
```

Or programmatically:

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# Create an image CAPTCHA generator
generator = CaptchaFactory.create(CaptchaType.IMAGE)

# Generate dataset
dataset = generator.generate_dataset(
    size=1000,
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1,
    parallel=True,
    max_workers=4,
    seed=42,
    output_dir="custom_dataset"
)

# Print statistics
for split, samples in dataset.items():
    print(f"{split}: {len(samples)} samples")
```

## Documentation

For more detailed information, see the [documentation](docs/README.md):

- [API Reference](docs/api-reference.md)
- [Architecture](docs/architecture.md)
- [Configuration](docs/configuration.md)
- [Extending](docs/extending.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.