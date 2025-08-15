"""
ProtoLayer Utility Script

This script includes:
1. ANSI console colors
2. Known validator check
3. User type selection CLI
"""

from typing import Tuple, Optional, Any
import argparse

# ----------------------------
# Console Colors Definition
# ----------------------------
class Console_Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Resets the color to default

# ----------------------------
# Known Validator Function
# ----------------------------
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
    print(f"{Console_Colors.RED}[Known Validator]: Function needs full implementation! "
          f"Currently returns True only if on main chain testnet.{Console_Colors.RESET}")

    # Placeholder logic: only True if chain is (0, 0)
    if chain == (0, 0):
        return True
    else:
        return False

# ----------------------------
# System Key Check
# ----------------------------
def check_system_key() -> bool:
    """
    Checks if a valid system key is present. Currently returns True as a placeholder.

    Returns:
        bool: True if a valid key is found, False otherwise.
    """
    # Placeholder for actual key checking logic
    return True

# ----------------------------
# Main CLI Function
# ----------------------------
def main(user_type: Optional[str] = None, **kwargs: Any) -> None:
    """
    Main function that handles user type selection and additional keyword arguments.
    Continues to prompt for user type until 'exit' is entered.

    Args:
        user_type (Optional[str]): The type of user (Validator, Chain Owner, Partner, Client).
        **kwargs (Any): Additional keyword arguments for future use.
    """
    if not check_system_key():
        print(f"{Console_Colors.RED}No valid system key found.{Console_Colors.RESET}")
        return

    while True:
        if user_type is None:
            user_input = input("Please enter your user type (Validator, Chain Owner, Partner, Client) or type 'exit' to quit: ").upper()

            if user_input == 'EXIT':
                print(f"{Console_Colors.YELLOW}Exiting ProtoLayer.{Console_Colors.RESET}")
                break

            if user_input in ['VALIDATOR', 'CHAIN OWNER', 'PARTNER', 'CLIENT']:
                print(f"{Console_Colors.GREEN}You are a {user_input.title()}. Still developing the role, so nothing happens after this.{Console_Colors.RESET}")
                break
            else:
                print(f"{Console_Colors.RED}Invalid user type.{Console_Colors.RESET}")
        else:
            user_input = user_type.upper()
            if user_input in ['VALIDATOR', 'CHAIN OWNER', 'PARTNER', 'CLIENT']:
                print(f"{Console_Colors.GREEN}You are a {user_input.title()}.{Console_Colors.RESET}")
            break  # Exit loop if user_type is provided as an argument

# ----------------------------
# Example Usage
# ----------------------------
if __name__ == "__main__":
    # Argparse for CLI user_type
    parser = argparse.ArgumentParser(description="User type selection for ProtoLayer")
    parser.add_argument("--user_type", type=str, help="Specify the user type (Validator, Chain Owner, Partner, Client)")

    args = parser.parse_args()

    main(user_type=args.user_type)

    # Example for validator check
    example_account = ("ValidatorName", "0x123456")
    example_chain = (0, 0)
    result = known_validator(example_account, example_chain)
    print(f"{Console_Colors.CYAN}Is known validator? {result}{Console_Colors.RESET}\n")

    # Example for console colors
    print(f"{Console_Colors.RED}This will be red{Console_Colors.RESET}")
    print(f"{Console_Colors.GREEN}This will be green{Console_Colors.RESET}")
    print(f"{Console_Colors.BLUE}This will be blue{Console_Colors.RESET}")
    print(f"{Console_Colors.MAGENTA}This is called magenta, but it's pink 😁{Console_Colors.RESET}")
