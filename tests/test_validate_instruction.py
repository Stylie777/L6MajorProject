import unittest
import sys

sys.path.append("src/")
from validate_instruction import (
    validate_instruction,
    VhcaddInstruction,
    InstructionValidity,
)


class TestStringMethods(unittest.TestCase):
    def test_validate_instruction_with_valid_earlyclobber_instruction(self):
        inst = "vhcadd.s32 q2, q1, q0, #270"
        result = validate_instruction(inst)

        self.assertTrue(result.get_result())
        self.assertFalse(result.get_is_regex())

    def test_validate_instruction_with_invalid_earlyclobber_instruction(self):
        inst = "vhcadd.s32 q0, q0, q0, #270"
        result = validate_instruction(inst)

        self.assertFalse(result.get_result())
        self.assertFalse(result.get_is_regex())

    def test_validate_instruction_with_valid_instruction(self):
        inst = "vhcadd.s8 q2, q1, q0, #90"
        result = validate_instruction(inst)

        self.assertTrue(result.get_result())
        self.assertFalse(result.get_is_regex())

    def test_validate_instruction_with_regex_instruction(self):
        inst = r"vhcadd.s8 q{{[0-9]+}}, q{{[0-9]+}}, q{{[0-9]+}}, #90"
        result = validate_instruction(inst)

        self.assertFalse(result.get_result())
        self.assertTrue(result.get_is_regex())

    def test_VhcaddInstruction_is_earlyclobber_with_earlyclobber_instruction(self):
        inst = VhcaddInstruction("vhcadd.s32 q2, q1, q0, #270")

        self.assertTrue(inst.is_earlyclobber())

    def test_VhcaddInstruction_is_earlyclobber_with_non_earlyclobber_instruction(self):
        inst = VhcaddInstruction("vhcadd.s8 q2, q1, q0, #270")

        self.assertFalse(inst.is_earlyclobber())

    def test_InstructionValidity_get_result_with_false_result(self):
        result = InstructionValidity(False, False)
        result._result = False

        self.assertFalse(result.get_result())

    def test_InstructionValidity_get_result_with_true_result(self):
        result = InstructionValidity(False, False)
        result._result = True

    def test_InstructionValidity_get_result_with_false_is_regex(self):
        result = InstructionValidity(False, False)
        result._is_regex = False

        self.assertFalse(result.get_is_regex())

    def test_InstructionValidity_get_result_with_true_is_regex(self):
        result = InstructionValidity(False, False)
        result._is_regex = True

        self.assertTrue(result.get_is_regex())


if __name__ == "__main__":
    unittest.main()
