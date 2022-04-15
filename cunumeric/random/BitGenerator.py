# Copyright 2021-2022 NVIDIA Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import numpy as np
from cunumeric.array import ndarray
from cunumeric.config import BitGeneratorType
from cunumeric.runtime import runtime


class BitGenerator:
    def __init__(self, seed=None, generatorType=BitGeneratorType.DEFAULT):
        if type(self) is BitGenerator:
            raise NotImplementedError(
                "BitGenerator is a base class and cannot be instantized"
            )
        self.handle = runtime.bitgenerator_create(generatorType)
        if seed is not None:
            runtime.bitgenerator_set_seed(self.handle, seed)

    def __del__(self):
        runtime.bitgenerator_destroy(self.handle)

    # when output is false => skip ahead
    def random_raw(self, shape=None, output=True):
        if shape is None:
            shape = (1,)
        if not isinstance(shape, tuple):
            shape = (shape,)
        if output:
            res = ndarray(shape, dtype=np.dtype(np.uint32))
            res._thunk.bitgenerator_random_raw(self.handle)
            return res
        else:
            runtime.bitgenerator_random_raw(self.handle, shape)


class XORWOW(BitGenerator):
    def __init__(self, seed=None):
        super().__init__(seed, BitGeneratorType.XORWOW)


class MRG32k3a(BitGenerator):
    def __init__(self, seed=None):
        super().__init__(seed, BitGeneratorType.MRG32K3A)


class MTGP32(BitGenerator):
    def __init__(self, seed=None):
        super().__init__(seed, BitGeneratorType.MTGP32)


class MT19937(BitGenerator):
    def __init__(self, seed=None):
        super().__init__(seed, BitGeneratorType.MT19937)


class PHILOX4_32_10(BitGenerator):
    def __init__(self, seed=None):
        super().__init__(seed, BitGeneratorType.PHILOX4_32_10)