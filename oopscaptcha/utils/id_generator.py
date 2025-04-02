import uuid
import time
import random

class IDGenerator:
    
    _fixed_timestamp = None
    
    @staticmethod
    def generate_captcha_id() -> str:
        """Generate a unique captcha ID using current timestamp and UUID."""
        if IDGenerator._fixed_timestamp:
            timestamp_str = IDGenerator._fixed_timestamp
        else:
            timestamp_str = time.strftime("%Y%m%d_%H%M%S")
            
        # Use random if available, for better reproducibility with seed
        if random.getstate():
            uuid_hex = ''.join(f'{random.randint(0, 15):x}' for _ in range(12))
        else:
            uuid_hex = uuid.uuid4().hex[:12]
        
        return f"captcha_{timestamp_str}_{uuid_hex}"
    
    @staticmethod
    def set_fixed_timestamp(timestamp_str: str = None):
        """Set a fixed timestamp for reproducibility.
        
        Args:
            timestamp_str: A timestamp string, if None, will use current time.
        """
        if timestamp_str is None:
            timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        IDGenerator._fixed_timestamp = timestamp_str
        
    @staticmethod
    def reset_timestamp():
        """Reset the fixed timestamp to None."""
        IDGenerator._fixed_timestamp = None 