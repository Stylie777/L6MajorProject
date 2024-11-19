import subprocess
import git
import pathlib
import shutil
from llvm_ir_reader import extract_instructions
from validate_instruction import validate_instruction, InstructionValidity

def clone_llvm(path:str = "llvm-project/") -> None:
    """
    Clones the LLVM Project as a shallow clone with a depth of 1\n
    inputs:
        path (str): The path where the llvm-project will be located. By default this is 'llvm-project/'.
    """
    print ("Cloning latest LLVM Project")

    git.Repo.clone_from(
        "https://github.com/llvm/llvm-project.git",
        f"{pathlib.Path.cwd()}/{path}" if path == "llvm-project/" else f"{path}",
        depth = 1
    )

    print("Cloned")

def remove_llvm(path:str = "llvm-project/") -> None:
    """
    Removes the LLVM-Project as it is no longer needed once the testing is complete\n
    inputs:
        path (str): The path where the llvm-project repo is located. By default this is 'llvm-project/'.
    """
    shutil.rmtree(f"{pathlib.Path.cwd()}/{path}" if path == "llvm-project/" else f"{path}")
    print("Removed llvm-project repository from your machine, when the tool is run next time, it will pull the latest version of llvm")

def parse_command_line_options():
    return None

if __name__ == "__main__":
    clone_llvm()

    # file_path = f"{pathlib.Path.cwd()}/llvm-project-copy/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"
    file_path = f"{pathlib.Path.cwd()}/llvm-project/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"
    file = open(file_path, "r")
    instructions = extract_instructions(file)
    file.close()

    for inst in instructions:
        result = validate_instruction(inst)
        if result.get_result() and not result.get_is_regex():
            print(f"{inst} is a valid Arm Assembley Instruction")
        elif result.get_is_regex() == True:
            continue
        else:
            print(f"{inst} is not a valid Arm Assembley instruction")

    remove_llvm()
