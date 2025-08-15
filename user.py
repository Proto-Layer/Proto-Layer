"""
ProtoLayer: Unified Python Module

This file contains the core components for ProtoLayer:
- Console colors
- Validator checks
- App configuration loader
- User handling
- Dependencies list
- CLI interface for user types
"""

# ----------------------------
# Console Colors
# ----------------------------
class Console_Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Reset to default color

# ----------------------------
# User Class
# ----------------------------
from typing import Tuple
import hashlib

class User:
    """
    Placeholder class for user-related methods.
    Refactor in future as common user methods expand.
    """
    def __init__(self) -> None:
        self.public_key: str = hashlib.sha256(b'public_key_data').hexdigest()
        self.username: str = '@test'
        self.username = self.username.capitalize()

    def get_account(self) -> Tuple[str, str]:
        """
        Returns account details:
        - Public key hash (str)
        - Username (str)
        """
        return self.public_key, self.username

    def sign(self) -> str:
        """
        Returns the user's signature for transactions.
        """
        return 'My Signature'

# ----------------------------
# Validator Check
# ----------------------------
from typing import Tuple

def known_validator(account_info: Tuple[str, str], chain: Tuple[int, int]) -> bool:
    """
    Returns True if the validator is recognized for the specified chain; else False.
    """
    print(f'Checking chain ID: {chain} for known validator. Account info: {account_info}')
    print(f'{Console_Colors.RED}[Known Validator]: Implementation placeholder! True for main/test chain{Console_Colors.RESET}')
    return chain == (0, 0)

# ----------------------------
# App Config Loader
# ----------------------------
import tomllib
from typing import Dict, Any

class AppConfig:
    _instance: 'AppConfig' = None  # Singleton instance

    def __new__(cls) -> 'AppConfig':
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        file_path = 'Validator/preferences.toml'
        with open(file_path, 'rb') as toml_file:
            self.data = tomllib.load(toml_file)

    def get_config(self) -> Dict[str, Any]:
        return self.data

# ----------------------------
# Dependencies List
# ----------------------------
PROTO_LAYER_DEPENDENCIES = [
    "certifi==2024.8.30",
    "cffi==1.16.0",
    "charset-normalizer==3.4.0",
    "cryptography==42.0.8",
