/* Copyright 2021-2022 NVIDIA Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#pragma once

#include <curand.h>

#define CHECK_CURAND(expr)                        \
  do {                                            \
    curandStatus_t __result__ = (expr);           \
    check_curand(__result__, __FILE__, __LINE__); \
  } while (false)

static Legion::Logger log_curand("cunumeric.random");

__host__ inline void check_curand(curandStatus_t error, const char* file, int line)
{
  if (error != CURAND_STATUS_SUCCESS) {
    log_curand.fatal() << "Internal CURAND failure with error" << (int)error << " in file " << file
                       << " at line " << line;
    exit((int)error);
  }
}

static inline curandRngType get_curandRngType(cunumeric::BitGeneratorType kind)
{
  switch (kind) {
    case cunumeric::BitGeneratorType::DEFAULT: return curandRngType::CURAND_RNG_PSEUDO_XORWOW;
    case cunumeric::BitGeneratorType::XORWOW: return curandRngType::CURAND_RNG_PSEUDO_XORWOW;
    case cunumeric::BitGeneratorType::MRG32K3A: return curandRngType::CURAND_RNG_PSEUDO_MRG32K3A;
    case cunumeric::BitGeneratorType::MTGP32: return curandRngType::CURAND_RNG_PSEUDO_MTGP32;
    case cunumeric::BitGeneratorType::MT19937: return curandRngType::CURAND_RNG_PSEUDO_MT19937;
    case cunumeric::BitGeneratorType::PHILOX4_32_10:
      return curandRngType::CURAND_RNG_PSEUDO_PHILOX4_32_10;
    default: {
      log_curand.fatal() << "unknown parameter";
      assert(false);
      return curandRngType::CURAND_RNG_TEST;
    }
  }
}

static inline bool supportsSkipAhead(curandRngType gentype)
{
  switch (gentype) {
    case curandRngType::CURAND_RNG_PSEUDO_XORWOW: return true;
    case curandRngType::CURAND_RNG_PSEUDO_MRG32K3A: return true;
    case curandRngType::CURAND_RNG_PSEUDO_MTGP32: return false;
    case curandRngType::CURAND_RNG_PSEUDO_MT19937: return false;
    case curandRngType::CURAND_RNG_PSEUDO_PHILOX4_32_10: return true;
    default: {
      log_curand.fatal() << "unknown parameter";
      assert(false);
      return false;
    }
  }
}

// https://docs.nvidia.com/cuda/curand/host-api-overview.html#thread-safety
template <bool GPUflavor>
static inline bool isThreadSafe(curandRngType gentype)
{
  switch (gentype) {
    case curandRngType::CURAND_RNG_PSEUDO_XORWOW: return true;
    case curandRngType::CURAND_RNG_PSEUDO_MRG32K3A: return true;
    case curandRngType::CURAND_RNG_PSEUDO_MTGP32: return true;
    case curandRngType::CURAND_RNG_PSEUDO_MT19937: return GPUflavor;
    case curandRngType::CURAND_RNG_PSEUDO_PHILOX4_32_10: return true;
    default: {
      ::fprintf(stderr, "[ERROR] : unknown generator");
      assert(false);
      return false;
    }
  }
}