from abc import ABC, abstractmethod
from typing import TypeVar, Tuple, Any, Dict, Generic, Union, Optional, List
from dataclasses import dataclass
from pathlib import Path
import random
import os
from .types import CaptchaType
import json
from datetime import datetime
import numpy as np # type: ignore
from ..utils.id_generator import IDGenerator
from ..config.settings import get_settings

SampleType = TypeVar('SampleType')  # Captcha Sample
LabelType = TypeVar('LabelType')  # Captcha Label

@dataclass(frozen=True)
class CaptchaConfig:
    type: CaptchaType
    params: Dict[str, Any]

class CaptchaGenerator(Generic[SampleType, LabelType], ABC):
    
    def __init__(self, config: CaptchaConfig):
        self.config = config
    
    @abstractmethod
    def generate_label(self) -> LabelType:
        pass
    
    @abstractmethod
    def _save_label(self, label: LabelType, path: Union[str, Path]) -> Path:
        pass

    @abstractmethod
    def generate_sample(self, label: LabelType) -> SampleType:
        pass
    
    @abstractmethod
    def _save_sample(self, sample: SampleType, path: Union[str, Path]) -> Path:
        pass

    @abstractmethod
    def generate(self) -> Tuple[SampleType, LabelType]:
        pass
    
    @abstractmethod
    def save(self, sample: SampleType, label: LabelType, output_dir: Optional[Union[str, Path]] = None, use_timestamp_dir: bool = True) -> Tuple[Path, Path]:
        pass
    
    def export(self, output_dir: Optional[Union[str, Path]] = None) -> Tuple[Path, Path]:
        sample, label = self.generate()
        return self.save(sample, label, output_dir)
        
    def generate_dataset(self,
                        size: Optional[int] = None, 
                        train_ratio: Optional[float] = None,
                        val_ratio: Optional[float] = None,
                        test_ratio: Optional[float] = None,
                        parallel: Optional[bool] = None,
                        max_workers: Optional[int] = None,
                        seed: Optional[int] = None,
                        output_dir: Optional[Union[str, Path]] = None) -> Dict[str, List[Tuple[Path, Path]]]:
        
        # Get default values from configuration
        captcha_config = get_settings().get_captcha_config(self.config.type.value)
        
        # Use default values from configuration
        train_ratio = captcha_config.get('train_ratio') if train_ratio is None else train_ratio
        val_ratio = captcha_config.get('val_ratio') if val_ratio is None else val_ratio
        test_ratio = captcha_config.get('test_ratio') if test_ratio is None else test_ratio
        parallel = captcha_config.get('parallel') if parallel is None else parallel
        max_workers = captcha_config.get('max_workers') if max_workers is None else max_workers
        seed = captcha_config.get('seed') if seed is None else seed
        
        # Check if parameters exist or are valid
        if size is None:
            raise ValueError(f"Missing required parameter 'size' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")
        if train_ratio is None:
            raise ValueError(f"Missing required parameter 'train_ratio' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")
        if val_ratio is None:
            raise ValueError(f"Missing required parameter 'val_ratio' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")
        if test_ratio is None:
            raise ValueError(f"Missing required parameter 'test_ratio' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")
        if parallel is None:
            raise ValueError(f"Missing required parameter 'parallel' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")
        if output_dir is None:
            raise ValueError(f"Missing required parameter 'output_dir' and no default value in configuration for CAPTCHA type '{self.config.type.value}'")

        # Validate size is positive
        if size <= 0:
            raise ValueError(f"Invalid size: {size}")
        
        # Validate ratios are non-negative
        if train_ratio < 0 or val_ratio < 0 or test_ratio < 0:
            raise ValueError(f"Ratios must be non-negative, got "
                             f"train_ratio: {train_ratio}, "
                             f"val_ratio: {val_ratio}, "
                             f"test_ratio: {test_ratio}")
        
        # Validate ratios sum to 1
        total_ratio = train_ratio + val_ratio + test_ratio
        if abs(total_ratio - 1.0) > 1e-6:
            raise ValueError(f"Ratios must sum to 1.0, got {total_ratio}")
        
        # Set random seeds for reproducibility if specified
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Create dataset output directory
        base_output_dir = Path(output_dir)
       
        # Use Shared Directory Timestamp
        timestamp = IDGenerator.get_dir_timestamp()
        output_dir = base_output_dir / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Split Directories
        splits = ['train', 'val', 'test']
        split_dirs = {}
        for split in splits:
            split_dir = output_dir / split
            split_dir.mkdir(parents=True, exist_ok=True)
            split_dirs[split] = split_dir
            
        # Calculate sizes for each split
        train_size = int(size * train_ratio)
        val_size = int(size * val_ratio)
        test_size = size - train_size - val_size
        
        split_sizes = {
            'train': train_size,
            'val': val_size,
            'test': test_size
        }
        
        # Generate dataset
        results: Dict[str, List[Tuple[Path, Path]]] = {split: [] for split in splits}
        
        if parallel and max_workers != 0:
            # Parallel generation
            max_workers = max_workers or os.cpu_count() or 1
            
            for split, split_size in split_sizes.items():
                if split_size <= 0:
                    continue
                    
                split_results = self._generate_dataset_parallel(
                    size=split_size,
                    output_dir=split_dirs[split],
                    max_workers=max_workers
                )
                results[split].extend(split_results)
        else:
            # Sequential generation
            for split, split_size in split_sizes.items():
                if split_size <= 0:
                    continue
                    
                split_results = self._generate_dataset_sequential(
                    size=split_size,
                    output_dir=split_dirs[split]
                )
                results[split].extend(split_results)
            
        # Save metadata
        self._save_dataset_metadata(output_dir, size, train_ratio, val_ratio, test_ratio, 
                                  parallel, max_workers, seed, results)
        
        # Reset directory timestamp to ensure new datasets get new timestamps
        IDGenerator.reset_dir_timestamp()
        
        return results
    
    def _generate_dataset_sequential(self, size: int, output_dir: Path) -> List[Tuple[Path, Path]]:
        results = []
        for _ in range(size):
            sample, label = self.generate()
            sample_path, label_path = self.save(sample, label, output_dir, use_timestamp_dir=False)
            results.append((sample_path, label_path))
        return results
    
    def _generate_dataset_parallel(self, size: int, output_dir: Path, max_workers: int) -> List[Tuple[Path, Path]]:
        results = []
        
        # Pre-generate labels for reproducibility
        labels = [self.generate_label() for _ in range(size)]
        
        # Define a serializable processing function
        def _parallel_save(args):
            idx, output_dir_str, label = args
            output_dir_path = Path(output_dir_str)
            
            try:
                # Use a new instance of the generator
                from .factory import CaptchaFactory
                generator = CaptchaFactory.create(self.config.type)
                
                sample = generator.generate_sample(label)
                return generator.save(sample, label, output_dir_path, use_timestamp_dir=False)
            except Exception as e:
                # Error handling: fallback to current instance
                print(f"Parallel generation failed: {e}")
                sample = self.generate_sample(label)
                return self.save(sample, label, output_dir_path, use_timestamp_dir=False)
        
        # Use thread pool to execute parallel tasks
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            args_list = [(i, str(output_dir), label) for i, label in enumerate(labels)]
            futures = executor.map(_parallel_save, args_list)
            results.extend(futures)
        
        return results
    
    def _save_dataset_metadata(self, output_dir: Path, size: int, train_ratio: float, 
                             val_ratio: float, test_ratio: float, parallel: bool,
                             max_workers: Optional[int], seed: Optional[int],
                             results: Dict[str, List[Tuple[Path, Path]]]) -> Path:

        metadata = {
            "timestamp": datetime.now().isoformat(),
            "captcha_type": self.config.type.value,
            "captcha_params": {k: str(v) for k, v in self.config.params.items()},
            "dataset_config": {
                "size": size,
                "train_ratio": train_ratio,
                "val_ratio": val_ratio,
                "test_ratio": test_ratio,
                "parallel": parallel,
                "max_workers": max_workers,
                "seed": seed
            },
            "split_sizes": {
                split: len(paths) for split, paths in results.items()
            }
        }
        
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return metadata_path