from typing import Dict, Optional, List
import time

class FileManager:
    def __init__(self):
        self.user_index: Dict[str, Dict] = {}  # Maps @user to file metadata
        self.sector_map: Dict[str, Dict] = {}  # sector_id -> {file_id: content}
        self.allocation_table: Dict[str, Dict] = {}  # file_id -> allocation info

    def create_file(self, user: str, file_name: str, content: str, *,
                    mutable: bool = True,
                    storage_type: str = "slow",
                    replication: int = 1,
                    ttl: Optional[int] = None) -> str:
        file_id = f"{user}/{file_name}"
        sector_id = f"sector_{len(self.sector_map)+1}"
        offset = 0
        length = len(content)

        # Store metadata
        self.user_index.setdefault(user, {})[file_name] = {
            "file_id": file_id,
            "mutable": mutable,
            "storage_type": storage_type,
            "replication": replication,
            "ttl": ttl,
            "created_at": time.time()
        }

        # Store allocation info
        self.allocation_table[file_id] = {
            "sector_id": sector_id,
            "offset": offset,
            "length": length,
            "replicas": [sector_id]*replication
        }

        # Store actual content
        self.sector_map.setdefault(sector_id, {})[file_id] = content
        return file_id

    def read_file(self, file_id: str) -> Optional[str]:
        loc = self.allocation_table.get(file_id)
        if not loc:
            return None
        return self.sector_map.get(loc["sector_id"], {}).get(file_id)

    def update_file(self, user: str, file_name: str, new_content: str) -> bool:
        file_id = f"{user}/{file_name}"
        meta = self.user_index.get(user, {}).get(file_name)
        if not meta or not meta["mutable"]:
            return False
        loc = self.allocation_table.get(file_id)
        if not loc:
            return False
        loc["length"] = len(new_content)
        self.sector_map[loc["sector_id"]][file_id] = new_content
        return True

    def delete_file(self, user: str, file_name: str) -> bool:
        file_id = f"{user}/{file_name}"
        meta = self.user_index.get(user, {}).get(file_name)
        if not meta or not meta["mutable"]:
            return False
        loc = self.allocation_table.get(file_id)
        if loc:
            self.sector_map[loc["sector_id"]].pop(file_id, None)
            self.allocation_table.pop(file_id, None)
        self.user_index[user].pop(file_name, None)
        return True

    def resolve_allocation(self, file_id: str) -> Optional[Dict]:
        return self.allocation_table.get(file_id)

    def list_files(self, user: str) -> List[str]:
        return list(self.user_index.get(user, {}).keys())


if __name__ == "__main__":
    fm = FileManager()

    # Create file
    file_id = fm.create_file("@Chris", "my_file.txt", "Hello Modulr!", mutable=True, storage_type="fast", replication=2)
    print(f"Created File ID: {file_id}")

    # Read file
    print(f"Read Content: {fm.read_file(file_id)}")

    # Update file
    fm.update_file("@Chris", "my_file.txt", "Updated content.")
    print(f"Updated Content: {fm.read_file(file_id)}")

    # Resolve allocation
    print(f"Allocation Info: {fm.resolve_allocation(file_id)}")

    # Delete file
    fm.delete_file("@Chris", "my_file.txt")
    print(f"Remaining Files: {fm.list_files('@Chris')}")
