import pytest
import git
import pathlib
import shutil
import os
from llvm_ir_reader import extract_instructions
from validate_instruction import validate_instruction, InstructionValidity


def collect_instructions():
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
def test_instruction(instruction: str):
    result = validate_instruction(instruction)
    if result.get_is_regex() == True:
        pytest.skip(f"{instruction} is in the form of a FileCheck Regular Expression.")
    assert result.get_result() == True
    assert result.get_is_regex() == False


if __name__ == "__main__":
    pytest.main()
