"""Parse the constrained order instruction returned for a checkout recording."""

from dataclasses import dataclass


ALLOWED_ACTIONS = {"HOLD", "UPDATE_ADDRESS", "CANCEL"}


@dataclass(frozen=True)
class OrderInstruction:
    transcript: str
    action: str
    reference: str


def parse_order_instruction(text: str) -> OrderInstruction:
    """Accept the three-line response contract and reject ambiguous instructions."""
    fields = {}
    for line in text.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip().upper()] = value.strip()

    transcript = fields.get("TRANSCRIPT", "")
    action = fields.get("ACTION", "")
    reference = fields.get("REFERENCE", "")
    if not transcript or action not in ALLOWED_ACTIONS or not reference:
        raise ValueError("The model response did not match the order instruction contract.")
    return OrderInstruction(transcript=transcript, action=action, reference=reference)
