import unittest

from order_instruction import parse_order_instruction


class OrderInstructionTest(unittest.TestCase):
    def test_parses_an_unambiguous_cancel(self) -> None:
        instruction = parse_order_instruction(
            "TRANSCRIPT: Please cancel order EC-2048.\n"
            "ACTION: CANCEL\n"
            "REFERENCE: EC-2048"
        )

        self.assertEqual(instruction.action, "CANCEL")
        self.assertEqual(instruction.reference, "EC-2048")


if __name__ == "__main__":
    unittest.main()
