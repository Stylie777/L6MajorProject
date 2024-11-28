import re
from llvm_ir_reader import SupportedEarlyClobberInstructions, ConstraintType


class InstructionValidity:
    _result = False
    _is_regex = False

    def __init__(self, result: bool, is_regex: bool) -> None:
        self._result = result
        self._is_regex = is_regex

    def get_result(self) -> bool:
        return self._result

    def get_is_regex(self) -> bool:
        return self._is_regex


class VectorInstruction:
    _inst = ""
    _name = ""
    _size = ""
    _qd = ""
    _qn = ""
    _qm = ""
    _rot = ""
    _register_regex = False

    def __init__(self, inst: str) -> None:
        supported_insts = SupportedEarlyClobberInstructions()
        self._inst = inst
        if r"{{" in inst:
            self._register_regex = True
            return
        self._name = inst.split(".")[0]
        self._size = inst.split(".")[1].split(" ")[0]
        self._qd = inst.split(" ")[1].split(",")[0]
        if supported_insts.has_qn(self._name):
            self._qn = inst.split(" ")[2].split(",")[0]
            self._qm = inst.split(" ")[3].split(",")[0]
        else:
            self._qm = inst.split(" ")[2].split(",")[0]
        if supported_insts.has_rot(self._name):
            self._rot = inst.split(" ")[4].split(",")[0]
        return

    def is_earlyclobber(self) -> bool:
        supported_insts = SupportedEarlyClobberInstructions()
        return (
            True
            if supported_insts.is_instruction_earlyclobber(self._name, self._size)
            else False
        )

    def is_instruction_regex(self) -> bool:
        return self._register_regex

    def is_register_allocation_valid(self) -> bool:
        supported_insts = SupportedEarlyClobberInstructions()

        if self.is_earlyclobber():
            for const in supported_insts.get_constraint_type(self._name, self._size):
                if (const == ConstraintType.QdQm and self._qd == self._qn) or (
                    const == ConstraintType.QdQn and self._qd == self._qn
                ):
                    return False

        if supported_insts.has_qn(self._name):
            regex = re.compile(r"q[0-7], q[0-7], q[0-7]")
        else:
            regex = re.compile(r"q[0-7], q[0-7]")
        if not (re.search(regex, self._inst)):
            return False

        return True

    def is_instruction_rot_valid(self) -> bool:
        supported_insts = SupportedEarlyClobberInstructions()
        if supported_insts.has_rot(
            self._name
        ) and self._rot not in supported_insts.get_rot_values(self._name):
            return False

        return True


def validate_instruction(inst: str) -> InstructionValidity:
    instruction = VectorInstruction(inst)

    if instruction.is_instruction_regex():
        return InstructionValidity(False, True)

    if not instruction.is_instruction_rot_valid():
        return InstructionValidity(False, False)

    if not instruction.is_register_allocation_valid():
        return InstructionValidity(False, False)

    return InstructionValidity(True, False)


if __name__ == "__main__":
    print(validate_instruction("vcadd.i32 q2, q0, q1, #90").get_result())
    print(validate_instruction("vcmul.f32 q2, q0, q1, #90").get_result())
    print(validate_instruction("vrev64.16 q0, q1").get_result())
    print(validate_instruction("vqdmul.s32 q2, q0, q1").get_result())
