import uuid
import time
import random

class IDGenerator:
    
    _fixed_timestamp = None
    
    @staticmethod
    def generate_captcha_id() -> str:
        
        timestamp_str = IDGenerator._fixed_timestamp or time.strftime("%Y%m%d_%H%M%S")
    
        # Use random if available, for better reproducibility with seed
        if random.getstate():
            uuid_hex = ''.join(f'{random.randint(0, 15):x}' for _ in range(12))
        else:
            uuid_hex = uuid.uuid4().hex[:12]
        
        return f"captcha_{timestamp_str}_{uuid_hex}"
    
    @staticmethod
    def set_fixed_timestamp(timestamp_str: str = None):
        IDGenerator._fixed_timestamp = timestamp_str or time.strftime("%Y%m%d_%H%M%S")
        
    @staticmethod
    def reset_timestamp():
        IDGenerator._fixed_timestamp = None 