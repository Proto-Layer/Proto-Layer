from run_rules import RunRules
from typing import Any, Dict, List, Optional, TypedDict

from logging import Logger
from logger_util import setup_logger

logger: Logger = setup_logger("ValidatorCore", "validator_core.log")


class PartnerSubscription(TypedDict):
    utility: str
    busy: bool


class ValidatorCore:
    """
    Core logic class for managing validator operations, partner subscriptions,
    perception scores, the ledger, and UnaS.
    """

    def __init__(self, run_rules: RunRules) -> None:
        """
        Initialize the core structures used by validators, including the validator queue,
        partner subscription list, perception scores, ledger (blockchain), and UnaS.
        """
        self.validator_queue: List[Dict[str, Any]] = []  # Queue of validator public keys waiting for tasks
        self.partner_subscription_list: Dict[str, PartnerSubscription] = {}  # {partner_key: {utility, busy}}
        self.perception_scores: Dict[str, int] = {}  # Maps user public keys to perception scores
        self.ledger: List[Dict[str, str]] = []  # Placeholder for blockchain structure (linked list-like)
        self.unas: Dict[str, str] = {}  # UnaS mapping usernames to public keys (UndChain Naming Service)
        self.minimum_perception_score: int = run_rules.get_min_validator_score()

    def add_validator_to_queue(
        self,
        public_key: str,
        latency: float,
        capacity: int,
        uptime: float,
        perception_score: float,
    ) -> Optional[int]:
        """
        Adds a validator to the queue with its metrics and returns its 1-based position.
        Returns None if the validator's perception score is below the threshold.
        """
        if perception_score < self.minimum_perception_score:
            logger.warning(
                f"Validator {public_key} was not added. Perception score ({perception_score}) is below the minimum threshold ({self.minimum_perception_score})."
            )
            return None

        validator_data: dict[str, Any] = {
            "public_key": public_key,
            "latency": latency,
            "capacity": capacity,
            "uptime": uptime,
            "perception_score": perception_score,
        }

        self.validator_queue.append(validator_data)
        return len(self.validator_queue)

    def return_validator_queue(self, start: int) -> List[dict[str, Any]]:
        """
        This method returns the validator queue starting at position
        """
        if start < 0 or start >= len(self.validator_queue):
            return []
        return self.validator_queue[start:]

    def validator_test(self) -> None:
        """
        This method is meant to handle stress testing between validators so
        that we can confirm if this validator is capable of handling network
        loads prior to being active on the network.
        """
        ...

    def subscribe_partner(self, partner_key: str, utility: str) -> None:
        """
        Subscribe a partner to a utility service and mark them as available.
        :param partner_key: Partner's public key.
