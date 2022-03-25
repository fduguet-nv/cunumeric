import numpy as np

import cunumeric

from cunumeric.config import CuNumericOpCode
from cunumeric import runtime

# class BitGenerator:
#     DEFAULT = 0
#     XORWOW = 1
#     MRG32K3A = 2
#     MTGP32 = 3
#     MT19937 = 4
#     PHILOX4_32_10 = 5
    
#     __slots__ = [
#         "handle", # handle to the runtime id
#     ]

#     def __init__(self, seed=None, generatorType=DEFAULT):
#         task = runtime.legate_context.create_task(
#             CuNumericOpCode.CUNUMERIC_BITGENERATOR,
#             manual=True,
#             launch_domain=Rect(lo=(0,), hi=(self.num_gpus,)),

#         )
#         self.handle = runtime.get_generator_id()
#         task.add_input(self.handle)
#         task.add_input(generatorID)
        
#         task.execute()
#         runtime.legate_runtime.issue_execution_fence(block=True)

#     def random_raw(self, size=None, output=True):
#         raise NotImplementedError('Not Implemented')

def test_bitgenerator():
    a = cunumeric.random.BitGenerator()
    print("DONE")
    pass

def test_bitgenerator_sub(a):
    print("testing for type = " + str(type(a)))
    a.random_raw(256, False)
    a.random_raw((512,256), False)

def test_bitgenerator_XORWOW():
    a = cunumeric.random.XORWOW()
    test_bitgenerator_sub(a)
    a = None
    runtime.legate_runtime.issue_execution_fence(block=True)
    print("DONE")
    pass

def test_bitgenerator_MRG32k3a():
    a = cunumeric.random.MRG32k3a()
    test_bitgenerator_sub(a)
    a = None
    runtime.legate_runtime.issue_execution_fence(block=True)    
    print("DONE")
    pass

def test_bitgenerator_MTGP32():
    a = cunumeric.random.MTGP32()
    test_bitgenerator_sub(a)
    a = None
    runtime.legate_runtime.issue_execution_fence(block=True)
    print("DONE")
    pass

def test_bitgenerator_MT19937():
    a = cunumeric.random.MT19937()
    test_bitgenerator_sub(a)
    a = None
    runtime.legate_runtime.issue_execution_fence(block=True)    
    print("DONE")
    pass

def test_bitgenerator_PHILOX4_32_10():
    a = cunumeric.random.PHILOX4_32_10()
    test_bitgenerator_sub(a)
    a = None
    runtime.legate_runtime.issue_execution_fence(block=True)    
    print("DONE")
    pass 

if __name__ == "__main__":
    test_bitgenerator()
    test_bitgenerator_XORWOW()
    test_bitgenerator_MRG32k3a()
    test_bitgenerator_MTGP32()
    test_bitgenerator_MT19937()
    test_bitgenerator_PHILOX4_32_10()