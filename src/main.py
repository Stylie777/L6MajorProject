import pytest
import git
import pathlib
import shutil
from llvm_ir_reader import extract_instructions
from validate_instruction import validate_instruction, InstructionValidity


def clone_llvm(path: str = "llvm-project/") -> None:
    """
    Clones the LLVM Project as a shallow clone with a depth of 1\n
    inputs:
        path (str): The path where the llvm-project will be located. By default this is 'llvm-project/'.
    """
    print("Cloning latest LLVM Project")

    git.Repo.clone_from(
        "https://github.com/llvm/llvm-project.git",
        f"{pathlib.Path.cwd()}/{path}" if path == "llvm-project/" else f"{path}",
        depth=1,
    )

    print("Cloned")


def remove_llvm(path: str = "llvm-project/") -> None:
    """
    Removes the LLVM-Project as it is no longer needed once the testing is complete\n
    inputs:
        path (str): The path where the llvm-project repo is located. By default this is 'llvm-project/'.
    """
    shutil.rmtree(
        f"{pathlib.Path.cwd()}/{path}" if path == "llvm-project/" else f"{path}"
    )
    print(
        "Removed llvm-project repository from your machine, when the tool is run next time, it will pull the latest version of llvm"
    )


def collect_instructions():
    clone_llvm()

    file_path = f"{pathlib.Path.cwd()}/llvm-project/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"
    file = open(file_path, "r")
    instructions = extract_instructions(file)
    file.close()

    remove_llvm()

    return instructions


@pytest.mark.parametrize("instruction", collect_instructions())
def test_instruction(instruction: str):
    result = validate_instruction(instruction)
    if result.get_is_regex() == True:
        pytest.skip(f"{instruction} is in the form of a FileCheck Regular Expression.")
    assert result.get_result() == True
    assert result.get_is_regex() == False


if __name__ == "__main__":
    pytest.main()
