# Architecture

The project follows object-oriented design patterns, including the Factory pattern and abstract base classes.

## Core Components

1. **CAPTCHA Generators**: Responsible for generating and saving CAPTCHAs
2. **Configuration Management**: Handles application configuration and parameters
3. **Factory Class**: Creates and configures appropriate CAPTCHA generators
4. **Dataset Generation**: Creates training, validation, and test datasets
5. **ID Generator**: Generates unique identifiers and manages timestamps

## Directory Structure

```
Oops-Captcha/
├── configs/                  # Configuration files
│   └── default.yaml          # Default configuration
├── data/                     # Data storage directory
├── oopscaptcha/              # Main package
│   ├── config/               # Configuration module
│   │   └── settings.py       # Settings management
│   ├── generators/           # CAPTCHA generators
│   │   ├── base.py           # Generator abstract base class
│   │   ├── factory.py        # Generator factory class
│   │   ├── image.py          # Image CAPTCHA generator
│   │   └── types.py          # CAPTCHA type definitions
│   └── utils/                # Utilities
│       └── id_generator.py   # ID generator
└── tests/                    # Tests
    ├── test_*.py             # Various test modules
    └── generate_dataset.py   # Dataset generation tool
```

## Directory Timestamp Feature

For organization, the system uses timestamped directories:
1. Single CAPTCHAs are saved in `output_dir/{timestamp}/samples` and `output_dir/{timestamp}/labels`
2. Datasets are saved in `dataset_output_dir/{timestamp}/<split>` where `<split>` is `train`, `val`, or `test` 