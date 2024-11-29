import pytest
import git
import pathlib
import shutil
import os
from llvm_ir_reader import extract_instructions
from validate_instruction import validate_instruction, InstructionValidity


def collect_instructions() -> list:
    """
    Uses the llvm-project git submodule to parse the LLVM tests and returns a list of instructions that are to be validated. Currently, only Thumb2 mve-intrinsics tests are parsed.

    outputs:

        - (list) : A list of instructions that are to be validated.
    """
    files = os.listdir(
        f"{pathlib.Path.cwd()}/llvm-project/llvm/test/CodeGen/Thumb2/mve-intrinsics/"
    )
    instructions = []
    for file in files:
        if file == "v2i1-upgrade.ll":
            continue
        file_path = f"{pathlib.Path.cwd()}/llvm-project/llvm/test/CodeGen/Thumb2/mve-intrinsics/{file}"
        file = open(file_path, "r")
        instructions += extract_instructions(file)
        file.close()

    return list(dict.fromkeys(instructions))


@pytest.mark.parametrize("instruction", collect_instructions())
def test_instruction(instruction: str) -> None:
    """
    Tests the instructios using pytest. The function decorator will call `collect_instructions()` and use the returned list to create individual test cases for each instruction.

    inputs:

        - instruction (str) : The instruction that is to be validated in the test case

    outputs:
        None
    """
    result = validate_instruction(instruction)
    if result.get_is_regex() == True:
        pytest.skip(f"{instruction} is in the form of a FileCheck Regular Expression.")
    assert result.get_result() == True
    assert result.get_is_regex() == False


if __name__ == "__main__":
    pytest.main()
