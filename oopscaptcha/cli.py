#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType


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
    
    # Check if ratios sum to 1
    total_ratio = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        print(f"Error: Ratios must sum to 1.0, got {total_ratio}")
        sys.exit(1)
    
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
    
    # Output statistics
    print(f"Dataset generated successfully! Saved to {args.output_dir}")
    for split, samples in result.items():
        print(f"{split}: {len(samples)} samples")


def main(argv: Optional[List[str]] = None):
    """Entry point function"""
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
    single_parser.add_argument('--type', default='image', choices=['image'], help='CAPTCHA type')
    single_parser.add_argument('--width', type=int, help='CAPTCHA width')
    single_parser.add_argument('--height', type=int, help='CAPTCHA height')
    single_parser.add_argument('--length', type=int, help='Number of characters')
    single_parser.add_argument('--characters', help='Character set for CAPTCHA')
    single_parser.add_argument('--output-dir', type=str, help='Output directory')
    single_parser.set_defaults(func=generate_single)
    
    # Dataset generation sub-command
    dataset_parser = subparsers.add_parser(
        'dataset',
        help='Generate a CAPTCHA dataset'
    )
    dataset_parser.add_argument('--type', default='image', choices=['image'], help='CAPTCHA type')
    dataset_parser.add_argument('--size', type=int, required=True, help='Dataset size')
    dataset_parser.add_argument('--width', type=int, help='CAPTCHA width')
    dataset_parser.add_argument('--height', type=int, help='CAPTCHA height')
    dataset_parser.add_argument('--length', type=int, help='Number of characters')
    dataset_parser.add_argument('--characters', help='Character set for CAPTCHA')
    dataset_parser.add_argument('--train-ratio', type=float, default=0.8, help='Training set ratio')
    dataset_parser.add_argument('--val-ratio', type=float, default=0.1, help='Validation set ratio')
    dataset_parser.add_argument('--test-ratio', type=float, default=0.1, help='Test set ratio')
    dataset_parser.add_argument('--parallel', action='store_true', help='Enable parallel generation')
    dataset_parser.add_argument('--max-workers', type=int, help='Maximum number of workers')
    dataset_parser.add_argument('--seed', type=int, help='Random seed')
    dataset_parser.add_argument('--output-dir', type=str, required=True, help='Output directory')
    dataset_parser.set_defaults(func=generate_dataset)
    
    # Parse command line arguments
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main() 