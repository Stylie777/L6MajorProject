import pathlib


class SupportedEarlyClobberInstructions:
    _instructions = [
        {"name": "vhcadd", "size": "s32", "constraint": "qd == qm"},
        {"name": "vcadd", "size": "i32", "constraint": "qd == qm"},
        {"name": "vcadd", "size": "f32", "constraint": "qd == qm"},
        {"name": "vcmla", "size": "f32", "constraint": "qda == qm || qda == qn"},
    ]

    def find_instructions(self):
        return [inst["name"] for inst in self._instructions]

    def get_instructions_dict(self):
        return self._instructions

    def is_instruction_earlyclobber(self, inst_name: str, inst_size: str) -> bool:
        for inst in self._instructions:
            if inst["name"] == inst_name and inst["size"] == inst_size:
                return True

        return False


def extract_instructions(file) -> str:
    instructions = []
    supported_instructions = SupportedEarlyClobberInstructions().find_instructions()
    for line in file:
        line_contents = line.split(":")
        for inst in supported_instructions:
            (
                instructions.append(line_contents[1].split("\n")[0].lstrip())
                if inst in line
                and line_contents[0] == "; CHECK-NEXT"
                and line_contents[0] != "; CHECK-NOT"
                else None
            )

    return instructions


if __name__ == "__main__":
    print("Running LLVM IR Reader Demo")
    file_path = f"{pathlib.Path.cwd()}/llvm-project-copy/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"

    file = open(file_path, "r")

    print(extract_instructions(file))

    file.close()
