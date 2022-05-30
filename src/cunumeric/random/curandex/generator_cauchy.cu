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

#include "generator.cuh"

template <typename field_t>
struct cauchy_t;

template <>
struct cauchy_t<float> {
  static constexpr float pi = 3.1415926535897932384626433832795f;

  float x0, gamma;

  template <typename gen_t>
  __forceinline__ __host__ __device__ float operator()(gen_t& gen)
  {
    float y = curand_uniform(&gen);  // y cannot be 0
    return x0 + gamma * ::tanf(pi * y + 0.5f);
  }
};

extern "C" curandStatus_t CURANDAPI curandGenerateCauchyEx(
  curandGeneratorEx_t generator, float* outputPtr, size_t num, float x0, float gamma)
{
  curandimpl::basegenerator* gen = (curandimpl::basegenerator*)generator;
  cauchy_t<float> func;
  func.x0    = x0;
  func.gamma = gamma;
  return curandimpl::dispatch_sample<cauchy_t<float>, float>(gen, func, num, outputPtr);
}

template <>
struct cauchy_t<double> {
  static constexpr double pi = 3.1415926535897932384626433832795;

  double x0, gamma;

  template <typename gen_t>
  __forceinline__ __host__ __device__ double operator()(gen_t& gen)
  {
    double y = curand_uniform_double(&gen);  // y cannot be 0
    return x0 + gamma * ::tan(pi * y + 0.5);
  }
};

extern "C" curandStatus_t CURANDAPI curandGenerateCauchyDoubleEx(
  curandGeneratorEx_t generator, double* outputPtr, size_t num, double x0, double gamma)
{
  curandimpl::basegenerator* gen = (curandimpl::basegenerator*)generator;
  cauchy_t<double> func;
  func.x0    = x0;
  func.gamma = gamma;
  return curandimpl::dispatch_sample<cauchy_t<double>, double>(gen, func, num, outputPtr);
}