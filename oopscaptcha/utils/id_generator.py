import uuid
import random
from datetime import datetime

class IDGenerator:
    _dir_timestamp = None
    
    @staticmethod
    def generate_captcha_id() -> str:
        if random.getstate():
            uuid_hex = ''.join(f'{random.randint(0, 15):x}' for _ in range(24))
        else:
            uuid_hex = uuid.uuid4().hex
        
        return f"captcha_{uuid_hex}"
    
    @staticmethod
    def get_dir_timestamp() -> str:
        if IDGenerator._dir_timestamp is None:
            IDGenerator._dir_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return IDGenerator._dir_timestamp
    
    @staticmethod
    def reset_dir_timestamp():
        IDGenerator._dir_timestamp = None 