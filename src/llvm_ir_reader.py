from io import TextIOWrapper
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

    def find_instructions(self) -> list:
        """
        Returns the names of the available instructions that are supported by the tool.

        Outputs:

            - (list) : List of the names of available instructions
        """
        return [inst["name"] for inst in self._instructions]

    def get_instructions_dict(self) -> dict:
        """
        Returns the full dictionary for available instructions, including all relevant information that can be used

        Outputs:

            - dict : The full dictionary of supported instructions.
        """
        return self._instructions

    def is_instruction_earlyclobber(self, inst_name: str, inst_size: str) -> bool:
        """
        Checks if the instruction being validated has earlyclobber contraints

        inputs:
        
            - inst_name (str) : The name of the instruction being validated.
            - inst_size (str) : The size of the instruction being validated. Only specific size variants of instructions have earlyclobber contraints.
        
        outputs:

            - (bool) : Values determining if the instruction has earlyclobber constraints.
        """
        for inst in self._instructions:
            if inst["name"] == inst_name and inst_size in inst["size"]:
                return True

        return False

    def get_constraint_type(self, inst_name: str, inst_size: str) -> list:
        """
        Returns the contraint type that is related to the instruction being validated. These contraints can the be used to determine how to ensure if the instruction is valid.

        inputs:

            - inst_name (str) : The name of the instruction being validated.
            - inst_size (str) : The size of the instruction being validated. Only specific size variants of instructions have earlyclobber contraints.

        outputs:

            - (list) : A list of contraints that apply to the instruction.
        """
        return [
            inst["constraint"]
            for inst in self._instructions
            if inst["name"] == inst_name and inst_size in inst["size"]
        ][0]

    def has_rot(self, inst_name: str) -> bool:
        """
        Returns boolean value to determine if the instruction uses a rotate value

        inputs:

            - inst_name (str) : The name of the instruction being validated.

        outputs:

            - (bool) : Value to determine if a rotate value is used.
        """
        for inst in self._instructions:
            if inst["name"] == inst_name and inst["has_rot"]:
                return True

        return False

    def get_rot_values(self, inst_name: str) -> list:
        """
        Returns the rotate values that apply to the specific instruction. These are different depending on the instruction being validated

        inputs:

            - inst_name (str) : The name of the instruction being validated.
        
        outputs:
            - (list) : A list of the rotate values that are applicable to the instruction.
        """
        return [
            inst["rot_values"]
            for inst in self._instructions
            if inst["name"] == inst_name
        ][0]

    def has_qn(self, inst_name: str) -> bool:
        """
        Returns if the instruction being validated uses a Qn input register. Not all instructions use two separate input registers, so this needs to be determined when parsing the instruction.

        inputs:

            - inst_name (str) : The name of the instruction being validated.
        
        outputs:

            - (bool) : Value to determine if the instruction uses a Qn input register.
        """
        for inst in self._instructions:
            if inst["name"] == inst_name and inst["has_Qn"]:
                return True

        return False


def extract_instructions(file: TextIOWrapper) -> list:
    """
    Extracts the instructions from a specific file. Each line is parsed and instructions are added to a list which is returned to the user.

    inputs:

        - file (TextIOWrapper) : The file being parsed.
    
    outputs:

        - instructions (list) : A list of strings which represent each instruction that is picked up from the file.
    """
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
