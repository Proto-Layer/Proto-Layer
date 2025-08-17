import os
import tomllib
import tomli_w
from typing import Dict, Tuple
from crypto_factory import CryptoFactory

class UserAccountHandler:
    """
    Handles the creation, storage, retrieval, and management 
    of user accounts (public/private key pairs) for UndChain.
    """

    def __init__(self, storage_dir: str = "accounts") -> None:
        self.storage_dir: str = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def new_account(self, username: str) -> str:
        """
        Create a brand-new user account. A key pair is generated
        and stored in a dedicated folder for the username.

        Returns:
            str: The filesystem path to the account folder
        """
        path: str = os.path.join(self.storage_dir, username)
        if os.path.exists(path):
            raise ValueError(f"ERROR: Account {username} already exists.")

        os.makedirs(path)

        private_key, public_key = CryptoFactory.generate_keys()
        self.store_keys(username, private_key, public_key, path)

        account_data: Dict[str, str] = {
            "username": username,
            "public_key": CryptoFactory.view_public_key(public_key)
        }

        with open(os.path.join(path, "account_info.toml"), "wb") as file:
            tomli_w.dump(account_data, file)

        return path

    def store_keys(self, username: str, private_key, public_key, directory: str) -> None:
        """
        Save the generated key pair in the user’s folder.
        """
        CryptoFactory.get_crypto_handler().save_keys(
            private_key, public_key, file_name=username, directory=directory
        )

    def load_account(self, username: str) -> Dict[str, str]:
        """
        Retrieve account information for the given username.

        Returns:
            Dict[str, str]: Dictionary containing account details
        """
        path: str = os.path.join(self.storage_dir, username)
        if not os.path.exists(path):
            raise ValueError(f"Account {username} does not exist.")

        with open(os.path.join(path, "account_info.toml"), "rb") as file:
            account_data: Dict[str, str] = tomllib.load(file)

        return account_data

    def list_accounts(self) -> Tuple[str, ...]:
        """
        Get a list of all stored account directories.

        Returns:
            Tuple[str]: Names of all existing accounts
        """
        return tuple(os.listdir(self.storage_dir))

    def remove_account(self, username: str) -> str:
        """
        Delete the specified account folder and its contents.
        WARNING: This action is irreversible unless the keys
        are backed up elsewhere.

        Returns:
            str: Confirmation message
        """
        path: str = os.path.join(self.storage_dir, username)
        if not os.path.exists(path):
            raise ValueError(f"Account {usern
