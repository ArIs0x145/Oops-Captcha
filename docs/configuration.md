# Configuration

The default configuration is in `configs/default.yaml`:

```yaml
captcha:
  image:
    width: 160              # CAPTCHA width
    height: 60              # CAPTCHA height
    length: 4               # Number of characters
    fonts: []               # Custom fonts
    characters: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    output_dir: "data/image" # Output directory for single CAPTCHAs
    
    # Dataset generation parameters
    train_ratio: 0.8        # Training set ratio
    val_ratio: 0.1          # Validation set ratio
    test_ratio: 0.1         # Test set ratio
    parallel: false         # Enable parallel generation
    max_workers: null       # Max number of workers
    seed: null              # Random seed
    dataset_output_dir: "data/image_dataset" # Dataset output directory
```

You can override any of these parameters programmatically or via command-line arguments. 