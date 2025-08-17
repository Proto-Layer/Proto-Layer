import tomllib
import os
from typing import Dict, Any, List
from logging import Logger
from logger_util import setup_logger

logger: Logger = setup_logger('RunRules', 'run_rules.log')

class RunRules:
    def __init__(self, config_filename: str) -> None:
        # Construct path to the run rules file
        root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        run_rules_path: str = os.path.join(root_dir, 'Run Rules', config_filename)

        # Load the TOML file
        with open(run_rules_path, 'rb') as f:
            self.config: Dict[str, Any] = tomllib.load(f)

    # ----------------- Configuration Accessors -----------------
    def get_job_file_structure(self, co_chain_name: str = "base_job_file") -> Dict[str, Any]:
        """Fetch the job file structure for a co-chain or base job file."""
        job_structure: Dict[str, Any] = {
            "fields": self.config[co_chain_name]["fields"],
            "mandatory": self.config[co_chain_name]["mandatory"],
            "job_types": self.config[co_chain_name]["job_types"],
            "token": self.config[co_chain_name]["token"]
        }
        return job_structure

    def get_validator_info(self) -> Dict[str, Any]:
        """Fetch validator info: max validators and known validators."""
        max_validators = self.config["max_validators"]["max"]
        known_validators = self.config["known_validators"]
        return {"max_validators": max_validators, "known_validators": known_validators}

    def get_utilities(self) -> Dict[str, Any]:
        return self.config.get("utilities", {})

    def get_sub_domain_info(self) -> Dict[str, Any]:
        return self.config.get("sub_domains", {})

    def get_governance_rules(self) -> Dict[str, Any]:
        return self.config.get("governance", {})

    def get_tokenomics_rules(self) -> Dict[str, Any]:
        return self.config.get("tokenomics", {})

    def get_performance_metrics(self) -> Dict[str, Any]:
        return self.config.get("performance", {})

    def get_subscription_services(self) -> Dict[str, Any]:
        return self.config.get("subscription_services", {})

    # ----------------- Validator/Partner Scoring -----------------
    def get_min_validator_score(self) -> int:
        score = self.config.get("min_validator_score", 0)
        if isinstance(score, int):
            return score
        logger.warning(f"'min_validator_score' is not an integer. Returning default of 420.")
        return 420

    def get_min_partner_score(self) -> int:
        score = self.config.get("min_partner_score", 0)
        if isinstance(score, int):
            return score
        logger.warning(f"'min_partner_score' is not an integer. Returning default of 420.")
        return 420

    # ----------------- Known Validators -----------------
    def get_known_validator_keys(self) -> List[str]:
        return [v["public_key"] for v in self.config["known_validators"]]

    def get_known_validators(self) -> List[Dict[str, Any]]:
        return self.config["known_validators"]

    # ----------------- Job Validation -----------------
    def validate_job_file(self, job_data: Dict[str, Any], co_chain_name: str = "base_job_file") -> bool:
        """Validate job file against mandatory fields for a co-chain."""
        mandatory_fields = self.config[co_chain_name]["mandatory"]
        return all(field in job_data and job_data[field] is not None for field in mandatory_fields)


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    run_rules = RunRules("UndChain.toml")

    print("Known Validators:", run_rules.get_known_validators())
    print("Job File Structure:", run_rules.get_job_file_structure())
    print("Validator Info:", run_rules.get_validator_info())
    print("Utilities:", run_rules.get_utilities())
    print("Sub-Domain Info:", run_rules.get_sub_domain_info())
    print("Governance Rules:", run_rules.get_governance_rules())
    print("Tokenomics Rules:", run_rules.get_tokenomics_rules())
    print("Performance Metrics:", run_rules.get_performance_metrics())
    print("Subscription Services:", run_rules.get_subscription_services())

    job_data = {
        "user_id": "user123",
        "job_type": "transfer",
        "block_id": "0001",
        "block_time": "2024-08-30T12:34:56Z",
        "job_priority": "high"
    }

    print("Minimum Validator Score:", run_rules.get_min_validator_score())
    print("Minimum Partner Score:", run_rules.get_min_partner_score())
    print("Is Job File Valid?", run_rules.validate_job_file(job_data))
