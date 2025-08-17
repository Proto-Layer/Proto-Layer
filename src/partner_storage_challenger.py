import random
import hashlib
from typing import List, Dict

class PartnerStorageChallenger:
    """
    Simulates a storage challenger among partners. 
    Issues deterministic challenges, verifies responses, 
    and escalates mismatches to a validator.
    """

    def __init__(self, sector_size: int = 4 * 1024 ** 3):
        self.sector_size = sector_size
        self.challenge_log = []      # All issued challenges
        self.escalation_log = []     # Escalation records for failures

    def issue_challenge(self, sector_id: str, partners: List[str], seed: int) -> dict:
        """
        Issues a challenge request for a sector using a deterministic seed.
        Returns the challenge specification and expected responders.
        """
        if len(partners) < 2:
            raise ValueError("At least two distinct partners required.")

        rng = random.Random(seed)
        offset = rng.randint(0, self.sector_size - 256)
        length = 25  # Fixed slice size

        challenger = rng.choice(partners)
        responders = [p for p in partners if p != challenger]

        challenge = {
            "challenge_id": f"challenge-{seed}-{sector_id}",
            "sector_id": sector_id,
            "issued_by": challenger,
            "target_offset": offset,
            "target_length": length,
            "expected_responses": responders
        }

        self.challenge_log.append(challenge)
        return challenge

    def simulate_partner_response(self, partner_id: str, offset: int, length: int, sector_content: str, corrupt: bool = False) -> str:
        """
        Simulates a partner hashing a segment of the sector.
        Corrupt partners can return incorrect data for testing.
        """
        data = sector_content[offset:offset + length]
        if corrupt:
            data = "INVALID" + data[7:]
        return hashlib.sha256(data.encode()).hexdigest()

    def compare_responses(self, response_dict: Dict[str, str]) -> Dict:
        """
        Detects mismatches among partner responses.
        Returns agreement status, hash groups, and suspected faulty partners.
        """
        hash_counts = {}
        for partner, result in response_dict.items():
            hash_counts.setdefault(result, []).append(partner)

        if len(hash_counts) == 1:
            return {
                "status": "valid",
                "matching_hash": next(iter(hash_counts)),
                "responders": list(response_dict.keys())
            }

        return {
            "status": "mismatch",
            "groups": hash_counts,
            "suspected_faulty": [p for h, ids in hash_counts.items() if len(ids) == 1 for p in ids]
        }

    def escalate_to_validator(self, challenge: dict, result: dict) -> None:
        """
        Reports failed challenge to validator. Logs and prints event.
        """
        escalation = {
            "sector_id": challenge["sector_id"],
            "challenge_id": challenge["challenge_id"],
            "challenger": challenge["issued_by"],
            "target_offset": challenge["target_offset"],
            "suspected_faulty": result.get("suspected_faulty", []),
            "hash_groups": result.get("groups", {}),
        }

        self.escalation_log.append(escalation)

        print("\n🚨 ESCALATION TO VALIDATOR 🚨")
        print(f"Sector: {escalation['sector_id']}")
        print(f"Challenge: {escalation['challenge_id']}")
        print(f"Issued By: {escalation['challenger']}")
        print(f"Offset: {escalation['target_offset']}")
        print("Hash Disagreement:")
        for hash_val, responders in escalation["hash_groups"].items():
            print(f"  Hash: {hash_val[:16]}... from: {responders}")
        print(f"Suspected Faulty Partners: {escalation['suspected_faulty']}")

if __name__ == "__main__":
    # Self-test and demonstration
    psc = PartnerStorageChallenger()
    partners = ["A", "B", "C"]
    seed = 12345
    sector_id = "sector_X1"

    challenge = psc.issue_challenge(sector_id, partners, seed)
    print("\nChallenge Issued:")
    print(challenge)

    fake_sector_data = "A" * (4 * 1024 ** 3)
    responses = {
        p: psc.simulate_partner_response(p, challenge["target_offset"], challenge["target_length"], fake_sector_data)
        for p in challenge["expected_responses"]
    }

    # Introduce corruption for testing
    responses["B"] = psc.simulate_partner_response("B", challenge["target_offset"], challenge["target_length"], fake_sector_data, corrupt=True)
    print("\nSimulated Responses:")
    print(responses)

    result = psc.compare_responses(responses)
    print("\nChallenge Outcome:")
    print(result)

    if result["status"] == "mismatch":
        psc.escalate_to_validator(challenge, result)

    print("\n--- Escalation Log ---")
    for e in psc.escalation_log:
        print(e)
