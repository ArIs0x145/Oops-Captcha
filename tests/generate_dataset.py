from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType
from oopscaptcha.config.settings import get_settings
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description='Generate CAPTCHA dataset')
    parser.add_argument('--type', type=str, choices=['image'], default='image',
                        help='CAPTCHA type to generate')
    parser.add_argument('--size', type=int, default=100,
                        help='Total number of samples to generate')
    parser.add_argument('--train-ratio', type=float, default=None,
                        help='Ratio of samples for training (optional, uses config if not specified)')
    parser.add_argument('--val-ratio', type=float, default=None,
                        help='Ratio of samples for validation (optional, uses config if not specified)')
    parser.add_argument('--test-ratio', type=float, default=None,
                        help='Ratio of samples for testing (optional, uses config if not specified)')
    parser.add_argument('--parallel', action='store_true',
                        help='Generate samples in parallel (overrides config)')
    parser.add_argument('--max-workers', type=int, default=None,
                        help='Maximum number of worker processes (optional, uses config if not specified)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducibility (optional, uses config if not specified)')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Output directory for dataset (optional, uses config if not specified)')
    parser.add_argument('--length', type=int, default=None,
                        help='Length of CAPTCHA text (optional, uses config if not specified)')
    parser.add_argument('--width', type=int, default=None,
                        help='Width of CAPTCHA image (optional, uses config if not specified)')
    parser.add_argument('--height', type=int, default=None,
                        help='Height of CAPTCHA image (optional, uses config if not specified)')
    
    args = parser.parse_args()
    
    # Load settings
    settings = get_settings()
    
    # Map string type to CaptchaType enum
    captcha_type_map = {
        'image': CaptchaType.IMAGE,
        # Add more types as they are implemented
    }
    
    captcha_type = captcha_type_map.get(args.type.lower())
    if captcha_type is None:
        raise ValueError(f"Unsupported CAPTCHA type: {args.type}")
    
    # Get captcha config
    captcha_config = settings.get_captcha_config(captcha_type.value)
    
    # Collect generator params
    generator_params = {}
    if args.length is not None:
        generator_params['length'] = args.length
    elif 'length' in captcha_config:
        generator_params['length'] = captcha_config['length']
        
    if args.width is not None:
        generator_params['width'] = args.width
    elif 'width' in captcha_config:
        generator_params['width'] = captcha_config['width']
        
    if args.height is not None:
        generator_params['height'] = args.height
    elif 'height' in captcha_config:
        generator_params['height'] = captcha_config['height']
    
    print(f"Generating {args.size} {args.type} CAPTCHA samples...")
    start_time = time.time()
    
    # Create generator
    generator = CaptchaFactory.create(captcha_type, **generator_params)
    
    # Generate dataset
    result = generator.generate_dataset(
        size=args.size,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        parallel=args.parallel,
        max_workers=args.max_workers,
        seed=args.seed,
        output_dir=args.output_dir
    )
    
    # Print summary
    elapsed_time = time.time() - start_time
    total_generated = sum(len(samples) for samples in result.values())
    
    print(f"Dataset generation completed in {elapsed_time:.2f} seconds")
    print(f"Total samples generated: {total_generated}")
    for split, samples in result.items():
        print(f"  {split}: {len(samples)} samples")
    
if __name__ == "__main__":
    main() 