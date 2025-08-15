"""
This script reads the chain rules file for validators and partners.
It checks whether a given account is a known validator on a specified chain.
"""

from typing import Tuple

# Assuming console_colors.py exists in the repo
from console_colors import Console_Colors as cli


def known_validator(account_info: Tuple[str, str], chain: Tuple[int, int]) -> bool:
    """
    Returns True if the validator is recognized for the specified chain, else False.

    Parameters:
        account_info (Tuple[str, str]): Validator account information (e.g., name, address)
        chain (Tuple[int, int]): Chain identifiers (e.g., mainnet/testnet IDs)

    Returns:
        bool: True if known validator, False otherwise
    """
    print(f"Checking chain ID: {chain} for known validator. Account info: {account_info}")
    print(f"{cli.RED}[Known Validator]: Function needs full implementation! "
          f"Currently returns True only if on main chain testnet.{cli.RESET}")

    # Placeholder logic: only True if chain is (0, 0)
    if chain == (0, 0):
        return True
    else:
        return False


# Example usage
if __name__ == "__main__":
    example_account = ("ValidatorName", "0x123456")
    example_chain = (0, 0)
    result = known_validator(example_account, example_chain)
    print(f"Is known validator? {result}")
