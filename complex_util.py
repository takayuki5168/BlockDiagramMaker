#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Complex:

    # 係数で初期化
    def __init__(self, coef):
        self.coef = coef

    # ゼロ点で初期化
    def __init__(self, zero):
        self.zero = zero

    def transCoefToZero:
        self.zero = self.coef
        self.zero = self.coef

    def transZeroToCoef:
        self.coef = self.zero
        self.coef = self.zero

    def reduceWhenZero(self):
        for i in self.zero:
            if i in self.zero:
                index = self.zero.index(i)
                self.zero.pop(i)
                self.zero.pop(i)

    def reduceWhenCoef(self):
        self.transCoefToZero
        self.reduceWhenZero

    #def __add__(self, other):
    #def __sub__(self, other):
    #def __mul__(self, other):
    #def __div__(self, other):

class ComplexFraction:

    def __init__(self, deno_coef, nume_coef):
        self.deno_coef = deno_coef
        self.nume_coef = nume_coef

    def __init__(self, coef, deno_zero, nume_zero):
        self.deno_zero = deno_zero
        self.nume_zero = nume_zero
        self.coef = coef

    def transCoefToZero:
        self.deno_zero = self.deno_coef
        self.nume_zero = self.nume_coef

    def transZeroToCoef:
        self.deno_coef = self.deno_zero
        self.nume_coef = self.nume_zero

    def reduceWhenZero(self):
        for i in self.deno_zero:
            if i in self.nume_zero:
                index = self.deno_zero.index(i)
                self.deno_zero.pop(i)
                self.nume_zero.pop(i)

    def reduceWhenCoef(self):
        self.transCoefToZero
        self.reduceWhenZero

    #def __add__(self, other):
    #def __sub__(self, other):
    #def __mul__(self, other):
    #def __div__(self, other):
