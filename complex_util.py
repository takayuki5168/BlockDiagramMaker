#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy.polynomial.polynomial import Polynomial

def mulZero(zero, num):
    if num == 0:
        return 1
    if len(zero) >= num + 1:
        return zero[0] * mulZero(zero[1:], num - 1) + mulZero(zero[1:], num)
    else:
        return zero[0] * mulZero(zero[1:], num - 1)

class ComplexPolynominal:

    def __init__(self, is_zero, a, b = 1):
        if is_zero: # ゼロ点で初期化
            self.zero = a
            self.first_coef = b
        else: # 係数で初期化
            self.transCoefToZero(a)

    def transCoefToZero(self, coef):
        f = Polynomial([x * -1 for x in coef])
        self.zero = f.roots()
        self.first_coef = coef[-1]

        print(self.first_coef)
        print(self.zero)

    def transZeroToCoef(self):
        coef = []
        for i in range(len(self.zero) + 1):
            c = mulZero([x * -1 for x in self.zero], i)
            coef.append(c)
        
        print(coef)
        return coef
            

    def __add__(self, other):
        self_coef = self.transZeroToCoef()
        other_coef = other.transZeroToCoef()
        
        added_coef = []
        for i in range(max(len(self_coef), len(other_coef))):
            tmp = 0
            if i < len(self_coef):
                tmp += self_coef[i]
            if i < len(other_coef):
                tmp += other_coef[i]
            added_coef.append(tmp)
        print(added_coef)
        return added_coef

    def __sub__(self, other):
        self_coef = self.transZeroToCoef()
        other_coef = other.transZeroToCoef()
        
        subbed_coef = []
        for i in range(max(len(self_coef), len(other_coef))):
            tmp = 0
            if i < len(self_coef):
                tmp += self_coef[i]
            if i < len(other_coef):
                tmp -= other_coef[i]
            subbed_coef.append(tmp)
        print(subbed_coef)
        return subbed_coef

    def __mul__(self, other):
        return ComplexPolynominal(True, self.zero + self.other)
    #def __div__(self, other):

a = [1,2,3]
po1 = ComplexPolynominal(True, a)
b = [10,20]
po2 = ComplexPolynominal(True, b)
po1 - po2

#a = [1, 1, 1, 1, 1]
#po = ComplexPolynominal(True, a, 2)
#po.transZeroToCoef()

#b = [1, 5, 10, 10, 5, 1]
#b = [x for x in b]
#po = ComplexPolynominal(False, b)

#b = [2, -3, 1]
#b = [x * 2 for x in b]
#po = ComplexPolynominal(False, b)


#class ComplexPolynominalFraction:
#
#    def __init__(self, deno_coef, nume_coef):
#        self.deno_coef = deno_coef
#        self.nume_coef = nume_coef
#
#    def __init__(self, coef, deno_zero, nume_zero):
#        self.deno_zero = deno_zero
#        self.nume_zero = nume_zero
#        self.coef = coef
#
#    def transCoefToZero:
#        self.deno_zero = self.deno_coef
#        self.nume_zero = self.nume_coef
#
#    def transZeroToCoef:
#        self.deno_coef = self.deno_zero
#        self.nume_coef = self.nume_zero
#
#    def reduceWhenZero(self):
#        for i in self.deno_zero:
#            if i in self.nume_zero:
#                index = self.deno_zero.index(i)
#                self.deno_zero.pop(i)
#                self.nume_zero.pop(i)
#
#    def reduceWhenCoef(self):
#        self.transCoefToZero
#        self.reduceWhenZero
#
#    #def __add__(self, other):
#    #def __sub__(self, other):
#    #def __mul__(self, other):
#    #def __div__(self, other):
