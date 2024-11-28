import unittest
import sys

sys.path.append("src/")
from llvm_ir_reader import (
    extract_instructions,
    SupportedEarlyClobberInstructions,
    ConstraintType,
)


class TestLlvmIrReader(unittest.TestCase):
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

    def test_SupportedEarlyClobberInstructions_find_instructions_for_instructions_in_list(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        self.assertEqual(
            supported.find_instructions(),
            [inst["name"] for inst in supported._instructions],
        )

    def test_SupportedEarlyClobberInstructions_is_earlyclobber_instruction_with_earlyclobber_instruction(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertTrue(supported.is_instruction_earlyclobber("vhcadd", "s32"))

    def test_SupportedEarlyClobberInstructions_is_earlyclobber_instruction_with_non_earlyclobber_instruction(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertFalse(supported.is_instruction_earlyclobber("vhcadd", "s8"))

    def test_SupportedEarlyClobberInstructions_get_constraint_type_for_QdQm_constraint(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        name = "vhcadd"
        size = "s32"

        self.assertEqual(
            supported.get_constraint_type(name, size),
            [ConstraintType.QdQm],
        )

    def test_SupportedEarlyClobberInstructions_get_constraint_type_for_QdQm_QdQn_constraint(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        name = "vqdmull"
        size = "s32"

        self.assertEqual(
            supported.get_constraint_type(name, size),
            [ConstraintType.QdQm, ConstraintType.QdQn],
        )

    def test_SupportedEarlyClobberInstructions_has_rot_with_instruction_that_uses_rot(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertTrue(supported.has_rot("vcmul"))

    def test_SupportedEarlyClobberInstructions_has_rot_with_instruction_that_does_not_use_rot(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertFalse(supported.has_rot("vqdmull"))

    def test_SupportedEarlyClobberInstructions_get_rot_values_for_instruction_using_90_270_values(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        name = "vhcadd"

        self.assertEqual(supported.get_rot_values(name), ["#90", "#270"])

    def test_SupportedEarlyClobberInstructions_get_rot_values_for_instruction_using_0_90_180_270_values(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        name = "vcmul"

        self.assertEqual(supported.get_rot_values(name), ["#0", "#90", "#180", "#270"])

    def test_SupportedEarlyClobberInstructions_get_rot_values_for_instruction_using_no_values(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()
        name = "vrev64"

        self.assertEqual(supported.get_rot_values(name), [])

    def test_SupportedEarlyClobberInstructions_has_qn_with_instruction_that_uses_qn_register(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertTrue(supported.has_qn("vhcadd"))

    def test_SupportedEarlyClobberInstructions_has_qn_with_instruction_that_does_not_use_qn_register(
        self,
    ):
        supported = SupportedEarlyClobberInstructions()

        self.assertFalse(supported.has_qn("vrev64"))


if __name__ == "__main__":
    unittest.main()
