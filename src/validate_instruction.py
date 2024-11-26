import re


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
    _dt = ""
    _qd = ""
    _qn = ""
    _qm = ""
    _rot = ""
    _register_regex = False

    def __init__(self, inst: str) -> None:
        self._inst = inst
        if r"{{" in inst:
            self._register_regex = True
            return
        self._name = inst.split(".")[0]
        self._dt = inst.split(".")[1].split(" ")[0]
        self._qd = inst.split(" ")[1].split(",")[0]
        self._qn = inst.split(" ")[2].split(",")[0]
        self._qm = inst.split(" ")[3].split(",")[0]
        self._rot = inst.split(" ")[4].split(",")[0]
        return

    def is_earlyclobber(self) -> bool:
        return True if self._dt == "s32" else False

    def is_instruction_regex(self) -> bool:
        return self._register_regex

    def is_register_allocation_valid(self) -> bool:

        if self.is_earlyclobber() and self._qd == self._qm:
            return False

        if not (re.search(r"q[0-7], q[0-7], q[0-7]", self._inst)):
            return False

        return True

    def is_instruction_rot_valid(self) -> bool:
        if self._rot != "#90" and self._rot != "#270":
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
