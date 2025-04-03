import unittest
import tempfile
import shutil
from pathlib import Path
import json
import os
import time
import glob

from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType
from oopscaptcha.utils.id_generator import IDGenerator

class TestDatasetGeneration(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "test_dataset"
        self.generator = CaptchaFactory.create(CaptchaType.IMAGE)
        # Reset directory timestamp to ensure clean state for each test
        IDGenerator.reset_dir_timestamp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def _get_timestamp_dir(self, base_dir):
        """Helper method to get the timestamped directory"""
        timestamp_dirs = list(base_dir.glob("*"))
        self.assertTrue(len(timestamp_dirs) > 0, "No timestamp directory found")
        return timestamp_dirs[0]
    
    def test_basic_generation(self):
        size = 5
        dataset = self.generator.generate_dataset(
            size=size,
            output_dir=self.output_dir
        )
        
        # Get the timestamp directory
        timestamp_dir = self._get_timestamp_dir(self.output_dir)
        
        # Verify that all split directories were created
        self.assertTrue((timestamp_dir / "train").exists())
        self.assertTrue((timestamp_dir / "val").exists())
        self.assertTrue((timestamp_dir / "test").exists())
        
        # Verify metadata file was generated
        self.assertTrue((timestamp_dir / "metadata.json").exists())
        
        # Verify correct number of samples
        total_samples = sum(len(samples) for samples in dataset.values())
        self.assertEqual(total_samples, size)
        
        # Check if default ratios are correct
        self.assertEqual(len(dataset['train']), 4)  # 0.8 * 5 = 4
        self.assertEqual(len(dataset['val']), 0)    # 0.1 * 5 = 0 (rounded down)
        self.assertEqual(len(dataset['test']), 1)   # remainder
        
        # Verify all files exist
        for split, samples in dataset.items():
            for sample_path, label_path in samples:
                self.assertTrue(sample_path.exists())
                self.assertTrue(label_path.exists())
    
    def test_custom_ratios(self):
        size = 10
        dataset = self.generator.generate_dataset(
            size=size,
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.1,
            output_dir=self.output_dir
        )
        
        # Verify correct number of samples
        self.assertEqual(len(dataset['train']), 7)  # 0.7 * 10 = 7
        self.assertEqual(len(dataset['val']), 2)    # 0.2 * 10 = 2
        self.assertEqual(len(dataset['test']), 1)   # 0.1 * 10 = 1
    
    def test_metadata(self):
        size = 10
        seed = 42
        train_ratio = 0.7
        val_ratio = 0.2
        test_ratio = 0.1
        
        dataset = self.generator.generate_dataset(
            size=size,
            train_ratio=train_ratio,
            val_ratio=val_ratio,
            test_ratio=test_ratio,
            seed=seed,
            output_dir=self.output_dir
        )
        
        # Get the timestamp directory
        timestamp_dir = self._get_timestamp_dir(self.output_dir)
        
        # Read metadata file
        with open(timestamp_dir / "metadata.json", 'r') as f:
            metadata = json.load(f)
        
        # Verify metadata content
        self.assertEqual(metadata['captcha_type'], 'image')
        self.assertEqual(metadata['dataset_config']['size'], size)
        self.assertEqual(metadata['dataset_config']['train_ratio'], train_ratio)
        self.assertEqual(metadata['dataset_config']['val_ratio'], val_ratio)
        self.assertEqual(metadata['dataset_config']['test_ratio'], test_ratio)
        self.assertEqual(metadata['dataset_config']['seed'], seed)
        self.assertEqual(metadata['split_sizes']['train'], len(dataset['train']))
        self.assertEqual(metadata['split_sizes']['val'], len(dataset['val']))
        self.assertEqual(metadata['split_sizes']['test'], len(dataset['test']))
    
    def test_reproducibility(self):
        size = 5
        seed = 12345
        
        # Generate two datasets with the same configuration
        dataset1 = self.generator.generate_dataset(
            size=size,
            seed=seed,
            output_dir=self.output_dir / "dataset1"
        )
        
        # Reset directory timestamp to ensure we get a new directory
        IDGenerator.reset_dir_timestamp()
        
        dataset2 = self.generator.generate_dataset(
            size=size,
            seed=seed,
            output_dir=self.output_dir / "dataset2"
        )
        
        # Check if sample labels are identical
        for split in ['train', 'val', 'test']:
            labels1 = [label_path.stem for _, label_path in dataset1[split]]
            labels2 = [label_path.stem for _, label_path in dataset2[split]]
            self.assertEqual(labels1, labels2)
    
    def test_parallel_generation(self):
        if os.cpu_count() < 2:
            self.skipTest("Need at least 2 CPU cores for parallel test")
        
        size = 10
        # Serial generation
        serial_start = time.time()
        serial_dataset = self.generator.generate_dataset(
            size=size,
            parallel=False,
            output_dir=self.output_dir / "serial"
        )
        serial_time = time.time() - serial_start
        
        # Reset directory timestamp to ensure we get a new directory
        IDGenerator.reset_dir_timestamp()
        
        # Parallel generation
        parallel_start = time.time()
        parallel_dataset = self.generator.generate_dataset(
            size=size,
            parallel=True,
            max_workers=2,
            output_dir=self.output_dir / "parallel"
        )
        parallel_time = time.time() - parallel_start
        
        # Check if both methods generated correct number of samples
        serial_train_files = len(serial_dataset['train'])
        parallel_train_files = len(parallel_dataset['train'])
        
        self.assertEqual(serial_train_files, 8)  # 0.8 * 10 = 8
        self.assertEqual(parallel_train_files, 8)  # 0.8 * 10 = 8
        
        # Ensure both methods have total of 10 samples
        serial_total = sum(len(samples) for samples in serial_dataset.values())
        parallel_total = sum(len(samples) for samples in parallel_dataset.values())
        
        self.assertEqual(serial_total, size)
        self.assertEqual(parallel_total, size)
    
    def test_invalid_ratios(self):
        with self.assertRaises(ValueError):
            # Sum of ratios not equal to 1
            self.generator.generate_dataset(
                size=10,
                train_ratio=0.7,
                val_ratio=0.2,
                test_ratio=0.2,  # Total sum is 1.1
                output_dir=self.output_dir
            )
    
    def test_empty_split(self):
        size = 10
        dataset = self.generator.generate_dataset(
            size=size,
            train_ratio=1.0,  # All samples in training set
            val_ratio=0.0,
            test_ratio=0.0,
            output_dir=self.output_dir
        )
        
        # Get the timestamp directory
        timestamp_dir = self._get_timestamp_dir(self.output_dir)
        
        # Verify correct split
        self.assertEqual(len(dataset['train']), 10)
        self.assertEqual(len(dataset['val']), 0)
        self.assertEqual(len(dataset['test']), 0)
        
        # Verify all split directories were created, even if some are empty
        self.assertTrue((timestamp_dir / "train").exists())
        self.assertTrue((timestamp_dir / "val").exists())
        self.assertTrue((timestamp_dir / "test").exists())

if __name__ == '__main__':
    unittest.main() 