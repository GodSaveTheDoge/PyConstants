import sys
from dataclasses import dataclass
from typing import Any
from IPython import embed

@dataclass
class ConstVar:
    frame: Any # too lazy to type hint correctly. Doesn't matter
    name: str
    value: Any

ConstList= []

def checkConsts(*a):
    for cvar in ConstList:
        if cvar.frame.f_locals[cvar.name] != cvar.value:
            cvar.frame.f_locals[cvar.name] = cvar.value
            raise SyntaxError('Cannot assign value to constant')

class ConstSetter:
    def __setattr__(self, key, value):
        target_frame = sys._getframe(1)
        target_frame.f_locals[key] = value
        target_frame.f_trace = checkConsts
        target_frame.f_trace_opcodes = True
        target_frame.f_trace_lines = False
        ConstList.append(ConstVar(target_frame, key, value))

const = ConstSetter()
sys.settrace(lambda *a: None)
