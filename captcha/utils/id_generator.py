import uuid
import time
import random
from typing import Optional

class IDGenerator:
    
    @staticmethod
    def generate_captcha_id() -> str:
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        uuid_hex = uuid.uuid4().hex[:12]
        
        return f"captcha_{timestamp_str}_{uuid_hex}" 