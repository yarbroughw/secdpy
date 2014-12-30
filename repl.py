from codegen import *
from secd    import *
import sys

# read eval print loop

machine = SECD()
while True:
    line = input('SECDrepl> ')
    code = codegen(parse(line), [], ['stop'])
    machine.runProgram(code, [])
