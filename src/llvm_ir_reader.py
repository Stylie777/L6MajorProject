import pathlib
from enum import Enum


class ConstraintType(Enum):
    QdQm = 1
    QdQn = 2


class SupportedEarlyClobberInstructions:
    _instructions = [
        {
            "name": "vhcadd",
            "size": ["s32"],
            "constraint": [ConstraintType.QdQm],
            "has_rot": True,
            "rot_values": ["#90", "#270"],
            "has_Qn": True,
        },
        {
            "name": "vcadd",
            "size": ["i32", "f32"],
            "constraint": [ConstraintType.QdQm],
            "has_rot": True,
            "rot_values": ["#90", "#270"],
            "has_Qn": True,
        },
        {
            "name": "vrev64",
            "size": ["8", "16", "32"],
            "constraint": [ConstraintType.QdQm],
            "has_rot": False,
            "rot_values": [],
            "has_Qn": False,
        },
        {
            "name": "vcmul",
            "size": ["f32"],
            "constraint": [ConstraintType.QdQm, ConstraintType.QdQn],
            "has_rot": True,
            "rot_values": ["#0", "#90", "#180", "#270"],
            "has_Qn": True,
        },
        {
            "name": "vqdmull",
            "size": ["s32"],
            "constraint": [ConstraintType.QdQm, ConstraintType.QdQn],
            "has_rot": False,
            "rot_values": [],
            "has_Qn": True,
        },
    ]

    def find_instructions(self):
        return [inst["name"] for inst in self._instructions]

    def get_instructions_dict(self):
        return self._instructions

    def is_instruction_earlyclobber(self, inst_name: str, inst_size: str) -> bool:
        for inst in self._instructions:
            if inst["name"] == inst_name and inst_size in inst["size"]:
                return True

        return False

    def get_constraint_type(self, inst_name: str, inst_size: str):
        return [
            inst["constraint"]
            for inst in self._instructions
            if inst["name"] == inst_name and inst_size in inst["size"]
        ][0]

    def has_rot(self, inst_name: str) -> bool:
        for inst in self._instructions:
            if inst["name"] == inst_name and inst["has_rot"]:
                return True

        return False

    def get_rot_values(self, inst_name: str):
        return [
            inst["rot_values"]
            for inst in self._instructions
            if inst["name"] == inst_name
        ][0]

    def has_qn(self, inst_name: str) -> bool:
        for inst in self._instructions:
            if inst["name"] == inst_name and inst["has_Qn"]:
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
                and "TMP" not in line
                else None
            )

    return instructions


if __name__ == "__main__":
    print("Running LLVM IR Reader Demo")
    file_path = f"{pathlib.Path.cwd()}/llvm-project-copy/llvm/test/CodeGen/Thumb2/mve-intrinsics/vcaddq.ll"

    file = open(file_path, "r")

    print(extract_instructions(file))

    file.close()
