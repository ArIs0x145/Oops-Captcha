#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType
from oopscaptcha.config.settings import get_settings


def generate_single(args):
    """Generate a single CAPTCHA"""
    # Collect parameters
    params = {}
    if args.width:
        params['width'] = args.width
    if args.height:
        params['height'] = args.height
    if args.length:
        params['length'] = args.length
    if args.characters:
        params['characters'] = args.characters
    if args.output_dir:
        params['output_dir'] = args.output_dir
    
    generator = CaptchaFactory.create(CaptchaType(args.type), **params)
    
    sample_path, label_path = generator.export(args.output_dir)
    print(f"CAPTCHA image saved to: {sample_path}")
    print(f"CAPTCHA label saved to: {label_path}")


def generate_dataset(args):
    """Generate a CAPTCHA dataset"""
    # Collect parameters
    params = {}
    if args.width:
        params['width'] = args.width
    if args.height:
        params['height'] = args.height
    if args.length:
        params['length'] = args.length
    if args.characters:
        params['characters'] = args.characters
    
    generator = CaptchaFactory.create(CaptchaType(args.type), **params)
    
    # Get config values
    settings = get_settings()
    captcha_config = settings.get_captcha_config(args.type)
    
    # Use args values or fall back to config values
    train_ratio = args.train_ratio if args.train_ratio is not None else captcha_config.get('train_ratio')
    val_ratio = args.val_ratio if args.val_ratio is not None else captcha_config.get('val_ratio')
    test_ratio = args.test_ratio if args.test_ratio is not None else captcha_config.get('test_ratio')
    
    # Check if ratios sum to 1
    total_ratio = train_ratio + val_ratio + test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        print(f"Error: Ratios must sum to 1.0, got {total_ratio}")
        sys.exit(1)
    
    # Generate dataset
    dataset_params = {}
    dataset_params['size'] = args.size if args.size is not None else captcha_config.get('size')
    dataset_params['train_ratio'] = train_ratio
    dataset_params['val_ratio'] = val_ratio 
    dataset_params['test_ratio'] = test_ratio
    dataset_params['parallel'] = args.parallel
    dataset_params['max_workers'] = args.max_workers if args.max_workers is not None else captcha_config.get('max_workers')
    dataset_params['seed'] = args.seed if args.seed is not None else captcha_config.get('seed')
    dataset_params['output_dir'] = args.output_dir if args.output_dir is not None else captcha_config.get('dataset_output_dir')
    
    # Generate dataset
    result = generator.generate_dataset(**dataset_params)
    
    # Output statistics
    print(f"Dataset generated successfully! Saved to {dataset_params['output_dir']}")
    for split, samples in result.items():
        print(f"{split}: {len(samples)} samples")


def main(argv: Optional[List[str]] = None):
    """Entry point function"""
    # Get default values from config
    settings = get_settings()
    
    parser = argparse.ArgumentParser(
        description='Oops-Captcha - A flexible and extensible CAPTCHA generation library',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='sub-commands'
    )
    
    # Single CAPTCHA generation sub-command
    single_parser = subparsers.add_parser(
        'single',
        help='Generate a single CAPTCHA'
    )
    single_parser.add_argument('--type', required=True, choices=['image'], help='CAPTCHA type (required)')
    
    # Get config based on the type
    def add_single_args(parser):
        parser.add_argument('--width', type=int, help='CAPTCHA width')
        parser.add_argument('--height', type=int, help='CAPTCHA height')
        parser.add_argument('--length', type=int, help='Number of characters')
        parser.add_argument('--characters', help='Character set for CAPTCHA')
        parser.add_argument('--output-dir', type=str, help='Output directory')
    
    add_single_args(single_parser)
    single_parser.set_defaults(func=generate_single)
    
    # Dataset generation sub-command
    dataset_parser = subparsers.add_parser(
        'dataset',
        help='Generate a CAPTCHA dataset'
    )
    dataset_parser.add_argument('--type', required=True, choices=['image'], help='CAPTCHA type (required)')
    dataset_parser.add_argument('--size', type=int, help='Dataset size')
    
    # Add same image params to dataset command
    add_single_args(dataset_parser)
    
    # Add dataset specific params
    dataset_parser.add_argument('--train-ratio', type=float, help='Training set ratio')
    dataset_parser.add_argument('--val-ratio', type=float, help='Validation set ratio')
    dataset_parser.add_argument('--test-ratio', type=float, help='Test set ratio')
    dataset_parser.add_argument('--parallel', action='store_true', help='Enable parallel generation')
    dataset_parser.add_argument('--max-workers', type=int, help='Maximum number of workers')
    dataset_parser.add_argument('--seed', type=int, help='Random seed')
    dataset_parser.set_defaults(func=generate_dataset)
    
    # Parse command line arguments
    args = parser.parse_args(argv)
    
    # Dynamic help text update based on type selection (for future use)
    args.func(args)


if __name__ == "__main__":
    main() 