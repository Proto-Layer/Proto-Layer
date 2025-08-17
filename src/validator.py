from typing import Any, Dict, LiteralString
from enum import Enum
import asyncio
from abstract_communication import AbstractCommunication
from communication_factory import CommunicationFactory
from run_rules import RunRules
from packet_generator import PacketGenerator, PacketType
from packet_handler import PacketHandler
from logging import Logger
from logger_util import setup_logger

# Set up logger
logger: Logger = setup_logger('Validator', 'validator.log')


class ValidatorState(Enum):
    DISCOVERY = 1
    SYNC = 2
    PENDING = 3
    REDIRECT = 4
    ACTIVE = 5
    ERROR = 6


class Validator:
    def __init__(self, public_key: bytearray, rules_file: str) -> None:
        """
        Initializes a validator instance.
        Loads run rules, prepares packet handler and generator,
        and determines if this validator is known.
        """
        logger.info("Initializing Validator")

        self.state = ValidatorState.DISCOVERY
        self.public_key: bytearray = public_key
        self.run_rules = RunRules(rules_file)
        logger.info(f"Rules from {rules_file} loaded successfully")

        self.run = False
        self.is_known_validator: bool = self.check_if_known_validator()

        self.comm: AbstractCommunication  # Will be initialized later

        # Packet system
        self.packet_generator = PacketGenerator("2024.09.30.1")  # TODO: Pull version from run rules
        self.packet_handler = PacketHandler(self.packet_generator)

    async def start_listener(self) -> None:
        """
        Starts the validator listener asynchronously. Continuously receives
        messages and delegates handling to the packet handler.
        """
        logger.info("Starting validator listener...")

        try:
            self.comm = CommunicationFactory.create_communication("TCP")
        except ValueError as e:
            logger.error(f'Unknown communication type: {e}')
            self.state = ValidatorState.ERROR
            raise

        # Start listener in the background
        asyncio.create_task(self.comm.start_listener("127.0.0.1", 4446))
        self.run = True

        while self.run:
            message: bytes = await self.comm.receive_message()
            await self.handle_message(message)

    async def stop(self) -> None:
        """
        Stops the validator and disconnects communication gracefully.
        """
        self.run = False
        logger.info("Shutting down validator...")

        try:
            await self.comm.disconnect()  # type: ignore
            logger.info("Successfully stopped listening")
        except Exception as e:
            logger.error(f"Failed to stop validator listener: {e}")

    def set_state(self, new_state: ValidatorState) -> None:
        """
        Transitions the validator to a new state.
        """
        logger.info(f"Transitioning to {new_state.name} state.")
        self.state = new_state

    async def handle_message(self, message: bytes) -> None:
        """
        Delegates incoming messages to the packet handler
        and sends a response if necessary.
        """
        logger.info(f"Handling message: {message}")

        try:
            response: bytes | None = self.packet_handler.handle_packet(message)
            if response:
                # TODO: Get real recipient public key
                await self.comm.send_message(response, bytearray(b'recipient_public_key'))
                logger.info("Response sent back to sender")
            else:
                logger.warning("No response generated for this packet")
        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    def send_state_update(self, recipient: bytearray) -> None:
        """
        Sends validator state information to a recipient.
        """
        state_info: LiteralString = f"State: {self.state.name}"
        logger.info(f"Sending state update to {recipient.decode('utf-8')}: {state_info}")
        # TODO: Implement actual sending logic
        ...

    def handle_error(self, error_message: str) -> None:
        """
        Handles errors by logging and transitioning to ERROR state.
        """
        logger.error(f"Error occurred: {error_message}")
        self.set_state(ValidatorState.ERROR)
        # TODO: Recovery or peer notification
        ...

    async def discover_validators(self) -> None:
        """
        Discovers other validators asynchronously and attempts connections.
        """
        logger.info("Discovering validators asynchronously...")

        known_keys: list[str] = self.run_rules.get_known_validator_keys()
        tasks = []

        for key in known_keys:
            if key == self.public_key.decode("utf-8"):
                logger.info(f"Skipping self validator {key}")
                continue

            logger.info(f"Attempting to connect to validator: {key}")
            contact_info = self.get_contact_info(key)
            if contact_info:
                try:
                    comm = CommunicationFactory.create_communication(contact_info["method"])
                    tasks.append(self.connect_to_validator(comm, key, contact_info))
                except ValueError as e:
                    logger.error(f"Unknown communication type for {key}: {contact_info['method']}")
                    self.state = ValidatorState.ERROR
                    raise
                except Exception as e:
                    logger.error(f"Failed to connect to validator {key}: {e}")
            else:
                logger.error(f"No contact info found for {key}")

        if tasks:
            await asyncio.gather(*tasks)
        else:
            logger.info("No validators to connect to.")

    async def connect_to_validator(self, comm: AbstractCommunication, validator_key: str, contact_info: dict) -> None:
        try:
            await comm.connect(bytearray(validator_key, "utf-8"), contact_info)  # type: ignore
        except Exception as e:
            logger.error(f"Failed to connect to validator {validator_key}: {e}")

    def get_contact_info(self, public_key: str) -> dict:
        """
        Returns the contact info for a given validator public key.
        """
        known_validators = self.run_rules.get_known_validators()
        for validator in known_validators:
            if validator['public_key'] == public_key:
                logger.info(f"Found contact info for {public_key}: {validator['contact']}")
                return validator['contact']
        raise ValueError(f"Validator {public_key} not found in run rules.")

    def check_if_known_validator(self) -> bool:
        """
        Checks if this validator is listed in the known validators.
        """
        known_keys: list[str] = self.run_rules.get_known_validator_keys()
        return self.public_key.decode("utf-8") in known_keys


if __name__ == "__main__":
    async def main() -> None:
        public_key = bytearray("validator_pub_key_3", "utf-8")
        run_rules_file = "UndChain.toml"
        validator = Validator(public_key, run_rules_file)

        try:
            await validator.start_listener()
            await validator.discover_validators()

            while validator.run:
                await asyncio.sleep(1)

        except ValueError as e:
            logger.error(f"Run rules file may be misconfigured: {e}")
        finally:
            print("System listening for new connections...")
            await validator.stop()

    asyncio.run(main())
