import sys, ast

class SECD:

    def __init__(self):
        self.s = []
        self.e = []
        self.c = []
        self.d = []
        self.running = True

    def runProgram(self,code,stack=[]):
        self.running = True
        self.loadProgram(code,stack)
        self.run()

    def loadProgram(self, code, stack=[]):
        self.s = stack
        self.e = []
        self.c = code
        self.d = []

    def readout(self):
        print('S: ', self.s)
        print('E: ', self.e)
        print('C: ', self.c)
        print('D: ', self.d)
        print()

    def run(self):
        self.readout()
        while self.running:
            self.execute()
            self.readout()

    def execute(self):
        cmd = self.c.pop().upper()
        op = {'ADD':   self.perform_add,
              'MUL':   self.perform_mul,
              'SUB':   self.perform_sub,
              'DIV':   self.perform_div,
              'CAR':   self.perform_car,
              'CDR':   self.perform_cdr,
              'NIL':   self.perform_nil,
              'ATOM':  self.perform_atom,
              'CONS':  self.perform_cons,
              'LDC':   self.perform_ldc,
              'LDF':   self.perform_ldf,
              'AP':    self.perform_ap,
              'LD':    self.perform_ld,
              'DUM':   self.perform_dum,
              'RAP':   self.perform_rap,
              'JOIN':  self.perform_join,
              'RTN':   self.perform_rtn,
              'SEL':   self.perform_sel,
              'ZERO':  self.perform_zero,
              'EQ':    self.perform_eq,
              'LEQ':   self.perform_leq,
              'STOP':  self.perform_stop,
            }[cmd]

        op()

    def perform_stop(self):
        self.running = False

    def perform_add(self):
        a = self.s.pop()
        b = self.s.pop()
        self.s.append(a + b)

    def perform_sub(self):
        a = self.s.pop()
        b = self.s.pop()
        self.s.append(a - b)

    def perform_mul(self):
        a = self.s.pop()
        b = self.s.pop()
        self.s.append(a * b)

    def perform_div(self):
        a = self.s.pop()
        b = self.s.pop()
        self.s.append(a / b)

    def perform_nil(self):
        self.s.append([])

    def perform_ldc(self):
        a = self.c.pop()
        self.s.append(a)

    def perform_ldf(self):
        fn  = self.c.pop()
        env = self.e[:]
        self.s.append([env,fn])

    def perform_ap(self):
        self.d.append(self.c)
        self.d.append(self.e)
        self.d.append(self.s)
        ce = self.s.pop()
        self.c = ce.pop()
        self.e = ce.pop()
        self.e.append(self.s.pop())
        self.s = []

    def perform_rtn(self):
        retval = self.s.pop()
        self.s = self.d.pop()
        self.s.append(retval)
        self.e = self.d.pop()
        self.c = self.d.pop()

    def perform_join(self):
        self.c = []
        self.c.append(self.d.pop())

    def perform_sel(self):
        x = self.s.pop()
        ct = self.c.pop()
        cf = self.c.pop()
        self.d.append(self.c)
        self.c = []
        if x:
            self.c.append(ct)
        else:
            self.c.append(cf)

    def perform_ld(self):
        loc = self.c.pop()
        x,y = loc.pop(),loc.pop()
        val = self.e[-x][-y] # index from end
        self.s.append(val)

    def perform_dum(self):
        """ create a dummy env """
        self.e.append([])

    def perform_rap(self):
        closure = self.s.pop()
        fn = closure.pop()
        env = closure.pop()
        env.pop()
        v = self.s.pop()
        self.e.pop()
        self.d.append(self.c)
        self.d.append(self.e)
        self.d.append(self.s)
        self.e = env
        self.e.append(v)
        self.c = fn
        self.s = []

    def perform_atom(self):
        self.s.append(self.s[-1] == [])

    def perform_cons(self):
        car = self.s.pop()
        cdr = self.s.pop()
        cdr.append(car)
        self.s.append(cdr)

    def perform_car(self):
        xs = self.s.pop()
        car = xs.pop()
        self.s.append(car)

    def perform_cdr(self):
        xs = self.s.pop()
        xs.pop()
        self.s.append(xs)

    def perform_zero(self):
        self.s.append(self.s[-1] == 0)

    def perform_eq(self):
        self.s.append(self.s[-1] == self.s[-2])

    def perform_leq(self):
        self.s.append(self.s[-1] <= self.s[-2])

if __name__ == "__main__":
    code = ast.literal_eval(sys.stdin.read())
    machine = SECD()
    machine.runProgram(code)
