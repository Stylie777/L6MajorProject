import unittest
import sys

sys.path.append("src/")
from llvm_ir_reader import extract_instructions


class TestStringMethods(unittest.TestCase):
    def test_extract_instructions_with_valid_vhcadd_instructions(self):
        file = open("tests/mocks/fake_test_valid.ll")
        instructions = extract_instructions(file)
        file.close()

        self.assertEqual(
            instructions, ["vhcadd.s32 q2, q1, q0, #270", "vhcadd.s8 q2, q1, q0, #90"]
        )

    def test_extract_instruction_without_supported_instructions(self):
        file = open("tests/mocks/fake_test_no_supported_instructions.ll")
        instructions = extract_instructions(file)
        file.close()

        self.assertEqual(instructions, [])


if __name__ == "__main__":
    unittest.main()
