import sys
from collections import defaultdict
from typing import Dict, Callable, List, Final
from dataclasses import dataclass
from types import FrameType

@dataclass
class ConstantValue:
    frame: FrameType
    name: str
    value: object

def _traceFun(frame: FrameType, event: str, arg: object) -> None:
    for constant in constMap[frame]:
        if constant.name in frame.f_locals and frame.f_locals[constant.name] != constant.value:
            frame.f_locals[constant.name] = constant.value 
            raise SyntaxError(f"Cannot assign value to constant {repr(constant.name)}")

class _ConstClass:
    def __setattr__(self, name, value):
        """This is the method called when a new constant is created"""
        targetFrame = sys._getframe(1)
        targetFrame.f_trace_lines = False
        targetFrame.f_trace_opcodes = True
        targetFrame.f_trace = _traceFun 
        targetFrame.f_locals[name] = value
        constMap[targetFrame].append(ConstantValue(targetFrame, name, value))


constMap: Dict[FrameType, List[ConstantValue]] = defaultdict(list) # FIXME
sys.settrace(lambda frame, event, arg: None)
const = _ConstClass()
