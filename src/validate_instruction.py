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


class VhcaddInstruction:
    _name = ""
    _dt = ""
    _qd = ""
    _qn = ""
    _qm = ""
    _rot = ""
    _register_regex = False

    def __init__(self, inst: str) -> None:
        self._name = inst.split(".")[0]
        self._dt = inst.split(".")[1].split(" ")[0]
        if r"{{" in inst:
            self._register_regex = True
        else:
            self._qd = inst.split(" ")[1].split(",")[0]
            self._qn = inst.split(" ")[2].split(",")[0]
            self._qm = inst.split(" ")[3].split(",")[0]
        self._rot = inst.split(" ")[4].split(",")[0]
        return

    def is_earlyclobber(self) -> bool:
        return True if self._dt == "s32" else False

    def is_register_allocation_valid(self) -> InstructionValidity:
        if self._register_regex:
            return InstructionValidity(False, True)

        if self.is_earlyclobber():
            return (
                InstructionValidity(True, False)
                if self._qd != self._qm
                else InstructionValidity(False, False)
            )

        return InstructionValidity(True, False)


def validate_instruction(inst: str) -> InstructionValidity:

    instruction = VhcaddInstruction(inst)

    return instruction.is_register_allocation_valid()
