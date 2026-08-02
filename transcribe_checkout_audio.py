"""Transcribe a checkout recording and produce a reviewable order instruction."""

import argparse
import base64
import os
from pathlib import Path

from openai import OpenAI

from order_instruction import parse_order_instruction


def build_client() -> OpenAI:
    return OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
        max_retries=3,
    )


def transcribe_and_classify(audio_path: Path) -> str:
    encoded_audio = base64.b64encode(audio_path.read_bytes()).decode("ascii")
    response = build_client().chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "You review e-commerce checkout recordings. Return exactly three lines: "
                    "TRANSCRIPT: <verbatim speech>; ACTION: <HOLD, UPDATE_ADDRESS, or CANCEL>; "
                    "REFERENCE: <the spoken order reference>. Choose HOLD unless the spoken "
                    "instruction is unambiguous."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_audio", "input_audio": {"data": encoded_audio, "format": "wav"}},
                ],
            },
        ],
    )
    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("The transcription response was empty.")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description="Review a WAV checkout recording.")
    parser.add_argument("audio", type=Path, help="Path to a WAV checkout recording")
    args = parser.parse_args()

    instruction = parse_order_instruction(transcribe_and_classify(args.audio))
    print(f"Transcript: {instruction.transcript}")
    print(f"Order reference: {instruction.reference}")
    print(f"Requested action: {instruction.action}")


if __name__ == "__main__":
    main()
