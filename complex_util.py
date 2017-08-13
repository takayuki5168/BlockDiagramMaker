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

def withinEpsilon(num):
    if abs(num) <= 1e-3:
        return 0
    else:
        return num

class ComplexPolynominal:

    def __init__(self, is_zero, a, b = 1):
        if is_zero: # ゼロ点で初期化
            self.zero = a
            self.first_coef = b
        else: # 係数で初期化
            self.transCoefToZero(a)
        #print('Initialize done')
        #print('first coef : {}'.format(self.first_coef))
        #print('zero : {}'.format(self.zero))

    def transCoefToZero(self, coef):
        f = Polynomial([x * -1 for x in coef])
        self.zero = f.roots()
        self.first_coef = coef[-1]


    def transZeroToCoef(self):
        coef = []
        for i in range(len(self.zero) + 1):
            c = mulZero([x * -1 for x in self.zero], i)
            coef.append(c)
        
        print('Trans Zero to Coef {}'.format(coef))
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
        print('added coef : {}'.format(added_coef))
        return ComplexPolynominal(False, added_coef)

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
        print('subbed coef : {}'.format(subbed_coef))
        return ComplexPolynominal(False, subbed_coef)

    def __mul__(self, other):
        return ComplexPolynominal(True, self.zero + self.other)
    #def __div__(self, other):

#a = [1,2,3]
#po1 = ComplexPolynominal(False, a)
#b = [10,20]
#po2 = ComplexPolynominal(False, b)
#po1 - po2

#a = [1, 1, 1, 1, 1]
#po = ComplexPolynominal(True, a, 2)
#po.transZeroToCoef()

#b = [1, 5, 10, 10, 5, 1]
#b = [x for x in b]
#po = ComplexPolynominal(False, b)

#b = [2, -3, 1]
#b = [x * 2 for x in b]
#po = ComplexPolynominal(False, b)


class ComplexPolynominalFraction:

    def __init__(self, init_mode, deno, nume, a = 1):
        if init_mode == 0: # ゼロ点で初期化
            self.deno = ComplexPolynominal(True, deno)
            self.nume = ComplexPolynominal(True, nume, a)
        elif init_mode == 1: # 係数で初期化
            self.deno = ComplexPolynominal(False, deno)
            self.nume = ComplexPolynominal(False, nume)
        elif init_mode == 2: # 分子分母の値で初期化
            self.deno = deno
            self.nume = nume
        print('Initialize done')
        print('first coef : {}'.format(self.nume.first_coef / self.deno.first_coef))
        print('deno zero : {}'.format(self.deno.zero))
        print('nume zero : {}'.format(self.nume.zero))

    #def transCoefToZero():
    #    self.deno_zero = self.deno_coef
    #    self.nume_zero = self.nume_coef

    #def transZeroToCoef():
    #    self.deno_coef = self.deno_zero
    #    self.nume_coef = self.nume_zero

    def reduce(self):
        for i in self.deno_zero:
            if i in self.nume_zero:
                index = self.deno_zero.index(i)
                self.deno_zero.pop(i)
                self.nume_zero.pop(i)

    def __add__(self, other):
        a = sorted(self.deno.zero)
        b = sorted(other.deno.zero)

        i = 0
        j = 0
        added_deno = [] # 分母の極
        while True:
            if i == len(a):
                if j == len(b):
                    break
                else: # bのみ残っている
                    added_deno.append(b[j])
                    j += 1
            elif j == len(b): # aのみ残っている
                added_deno.append(a[i])
                i += 1
            else: # aもbも残っている
                if withinEpsilon(a[i] - b[j]) == 0:
                    added_deno.append(a[i])
                    i += 1
                    j += 1
                elif a[i] > b[j]:
                    added_deno.append(b[j])
                    j += 1
                else:
                    added_deno.append(a[i])
                    i += 1
        i = 0
        j = 0
        while True:
            if i == len(added_deno): # aのみ残っている
                break
            elif j == len(a): # added_denoのみ残っている
                self.nume.zero.append(added_deno[i])
                i += 1
            else: # added_denoもaも残っている
                if withinEpsilon(added_deno[i] - a[j]) == 0:
                    i += 1
                    j += 1
                elif added_deno[i] > a[j]:
                    j += 1
                else:
                    self.nume.zero.append(added_deno[i])
                    i += 1
        i = 0
        j = 0
        while True:
            if i == len(added_deno): # bのみ残っている
                break
            elif j == len(b): # added_denoのみ残っている
                other.nume.zero.append(added_deno[i])
                i += 1
            else: # added_denoもbも残っている
                if withinEpsilon(added_deno[i] - b[j]) == 0:
                    i += 1
                    j += 1
                elif added_deno[i] > b[j]:
                    j += 1
                else:
                    other.nume.zero.append(added_deno[i])
                    i += 1

        return ComplexPolynominalFraction(2, ComplexPolynominal(True, added_deno),
                self.nume + other.nume)
        
    def __sub__(self, other):
        a = sorted(self.deno.zero)
        b = sorted(other.deno.zero)

        i = 0
        j = 0
        added_deno = [] # 分母の極
        while True:
            if i == len(a):
                if j == len(b):
                    break
                else: # bのみ残っている
                    added_deno.append(b[j])
                    j += 1
            elif j == len(b): # aのみ残っている
                added_deno.append(a[i])
                i += 1
            else: # aもbも残っている
                if withinEpsilon(a[i] - b[j]) == 0:
                    added_deno.append(a[i])
                    i += 1
                    j += 1
                elif a[i] > b[j]:
                    added_deno.append(b[j])
                    j += 1
                else:
                    added_deno.append(a[i])
                    i += 1
        i = 0
        j = 0
        while True:
            if i == len(added_deno): # aのみ残っている
                break
            elif j == len(a): # added_denoのみ残っている
                self.nume.zero.append(added_deno[i])
                i += 1
            else: # added_denoもaも残っている
                if withinEpsilon(added_deno[i] - a[j]) == 0:
                    i += 1
                    j += 1
                elif added_deno[i] > a[j]:
                    j += 1
                else:
                    self.nume.zero.append(added_deno[i])
                    i += 1
        i = 0
        j = 0
        while True:
            if i == len(added_deno): # bのみ残っている
                break
            elif j == len(b): # added_denoのみ残っている
                other.nume.zero.append(added_deno[i])
                i += 1
            else: # added_denoもbも残っている
                if withinEpsilon(added_deno[i] - b[j]) == 0:
                    i += 1
                    j += 1
                elif added_deno[i] > b[j]:
                    j += 1
                else:
                    other.nume.zero.append(added_deno[i])
                    i += 1
        return ComplexPolynominalFraction(2, ComplexPolynominal(True, added_deno),
                self.nume - other.nume)

    def __mul__(self, other):
        return ComplexPolynominalFraction(0, self.deno.zero + other.deno.zero, self.nume.zero + other.nume.zero, self.nume.first_coef * other.nume.first_coef / self.deno.first_coef / other.deno.first_coef)

    def __div__(self, other):
        return ComplexPolynominalFraction(0, self.deno.zero + other.nume.zero, self.nume.zero + other.deno.zero, self.nume.first_coef / self.deno.first_coef * other.deno.first_coef / other.nume.first_coef)

a = ComplexPolynominalFraction(0, [1,2,3],[1])
b = ComplexPolynominalFraction(0, [1,2,6,7],[3])
a + b
