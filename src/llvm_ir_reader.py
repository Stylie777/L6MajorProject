import pathlib


def extract_instructions(file) -> str:
    instructions = []
    for line in file: 
        line_contents = line.split(":")
        if "vhcadd" in line and line_contents[0] == "; CHECK-NEXT" and line_contents[0] != "; CHECK-NOT":
            instructions.append(line_contents[1].split("\n")[0].lstrip())
    
    return instructions

if __name__ == "__main__":
    print("Running LLVM IR Reader Demo")
    file_path = f"{pathlib.Path.cwd()}/llvm-project/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"

    file = open(file_path, "r")

    file.close()