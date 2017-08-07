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
