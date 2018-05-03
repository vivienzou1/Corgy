//
//  LeakyReLU.swift
//  Corgy
//
//  Created by HOPE on 5/2/18.
//

import Foundation
import Metal

public extension Corgy {
    /// an inplace ReLU layer, it will modify
    /// and return the input
    public static func LeakyReLU(negativeScope: Float = 0.01) -> Layer  {
        return {(_ input) in
            let threadsPerThreadGroup = MTLSizeMake(min(THREAD_PER_GROUP, input.value.count), 1, 1)
            let threadGroups = MTLSizeMake((input.value.count + THREAD_PER_GROUP - 1) / THREAD_PER_GROUP, 1, 1)
            
            let param = WorkParams(threadGroups: threadGroups, threadsPerThreadgroup: threadsPerThreadGroup)
            let leakyReLUParam = LeakyReLUParam(inputParam: input.getParam(), negativeScope: negativeScope)
            let paramBuffer = makeBuffer(leakyReLUParam)
            
            submitWork(name: "LeakyReLU", in: input, param: param, parameterBuffer: paramBuffer)
            return input
        }
    }
}
