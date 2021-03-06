//
//  ImageToMatrix.metal
//  Corgy
//
//  Created by buqian zheng on 5/3/18.
//

#include <metal_stdlib>
using namespace metal;
#include "KernelParamType.h"

kernel void ImageToMatrix(const device float *input [[ buffer(0) ]],
                          device float *output [[ buffer(1) ]],
                          constant ImageToMatParam *param [[ buffer(2) ]],
                          uint id [[thread_position_in_grid]]
                          ) {
    int i = id / param->outputParam.width;
    int j = id % param->outputParam.width;
    
    int channel = j / param->kernelSizeSquared;
    int num = j % param->kernelSizeSquared;
    // directly computed row and col are coordinate in padded input
    // so real row and col should be row - padding or col - padding
    int padding = param->padding;
    int row = i / param->kernelPerRow + num / param->kernelSize - padding;
    int col = i % param->kernelPerRow + num % param->kernelSize - padding;
    
    if (row < 0 || row >= param->inputParam.height || col < 0 || col >= param->inputParam.width) {
        output[id] = 0;
    } else {
        output[id] = input[channel * param->inputParam.sizePerChannel + row * param->inputParam.width + col];
    }
}

kernel void WeightToMatrix(const device float *input [[ buffer(0) ]],
                           device float *output [[ buffer(1) ]],
                           constant WeightToMatParam *param [[ buffer(2) ]],
                           uint id [[thread_position_in_grid]]) {
    int kernelSize = param->inputParam.width;
    int kernelSizeSquared = kernelSize * kernelSize;
    int i = id / param->outputParam.width;
    int tmp = i % kernelSizeSquared;
    int j = id % param->outputParam.width;
    int h = tmp / kernelSize;
    int w = tmp % kernelSize;
    output[id] =
        input[j * param->inputParam.sizePerBatch + i / kernelSizeSquared * param->inputParam.sizePerChannel + h * kernelSize + w];
}

