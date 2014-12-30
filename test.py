import secd
import pytest

@pytest.fixture(scope="session")
def machine():
    return secd.SECD()

def test_perform_add(machine):
    machine.loadProgram([],[1,1])
    machine.perform_add()
    assert machine.s.pop() == 2

def test_perform_sub(machine):
    machine.loadProgram([],[8,10])
    machine.perform_sub()
    assert machine.s.pop() == 2

def test_perform_mul(machine):
    machine.loadProgram([],[10,8])
    machine.perform_mul()
    assert machine.s.pop() == 80

def test_perform_div(machine):
    machine.loadProgram([],[100,500])
    machine.perform_div()
    assert machine.s.pop() == 5

def test_perform_nil(machine):
    machine.perform_nil()
    assert machine.s.pop() == []

def test_perform_ldc(machine):
    machine.loadProgram([10],[1,2])
    machine.perform_ldc()
    assert machine.s.pop() == 10

def test_perform_ldf(machine):
    fn = [1,2,3]
    machine.loadProgram([fn],[0])
    machine.e = [10,100]
    machine.perform_ldf()
    loaded = machine.s.pop()
    assert loaded.pop() == fn
    assert loaded.pop() == machine.e

def test_perform_ap(machine):
    machine.s = [500, [4, 3], [[[99,999]],['rtn','add',[1,1],'ld',[2,1],'ld']]]
    machine.e = [[99,999]]
    machine.c = ['lol']
    machine.d = [7]
    machine.perform_ap()
    assert machine.s == []
    assert machine.e == [[99,999],[4,3]]
    assert machine.c == ['rtn','add',[1,1],'ld',[2,1],'ld']
    assert machine.d == [7,['lol'],[[99,999]],[500]]

def test_perform_rtn(machine):
    machine.s = [3,2,1,0]
    machine.c = [10000]
    machine.e = [20000]
    machine.d = [7,[6],[5],[4]]
    machine.perform_rtn()
    assert machine.s == [4,0]
    assert machine.e == [5]
    assert machine.c == [6]
    assert machine.d == [7]

def test_perform_join(machine):
    machine.s = [0]
    machine.e = [1]
    machine.c = [5000]
    machine.d = [3,2]
    machine.perform_join()
    assert machine.s == [0]
    assert machine.e == [1]
    assert machine.c == [2]
    assert machine.d == [3]

def test_perform_sel(machine):
    # case: True
    machine.s = [2,1,True]
    machine.e = [3]
    machine.c = [7,6,5,4]
    machine.d = [9,8]
    machine.perform_sel()
    assert machine.s == [2,1]
    assert machine.e == [3]
    assert machine.c == [4]
    assert machine.d == [9,8,[7,6]]

    # case: False
    machine.s = [2,1,False]
    machine.e = [3]
    machine.c = [7,6,5,4]
    machine.d = [9,8]
    machine.perform_sel()
    assert machine.s == [2,1]
    assert machine.e == [3]
    assert machine.c == [5]
    assert machine.d == [9,8,[7,6]]

def test_perform_ld(machine):
    machine.s = []
    machine.e = [[3,2,1],[[2,2],4],[8]]
    machine.c = [[2,3],[1,3],[2,2],[1,2],[1,1]]
    machine.d = [5000]
    machine.perform_ld()
    assert machine.s == [8]
    assert machine.e == [[3,2,1],[[2,2],4],[8]]
    assert machine.c == [[2,3],[1,3],[2,2],[1,2]]
    assert machine.d == [5000]
    machine.perform_ld()
    assert machine.s == [8,4]
    machine.perform_ld()
    assert machine.s == [8,4,[2,2]]
    machine.perform_ld()
    assert machine.s == [8,4,[2,2],1]
    machine.perform_ld()
    assert machine.s == [8,4,[2,2],1,2]

def test_perform_dum(machine):
    machine.s = [3000]
    machine.e = [3,2,1]
    machine.c = [4000]
    machine.d = [5000]
    machine.perform_dum()
    assert machine.s == [3000]
    assert machine.e == [3,2,1,[]]
    assert machine.c == [4000]
    assert machine.d == [5000]

def test_perform_rap(machine):
    machine.s = [4,3,2,[[1,0,[]],'f']]
    machine.e = [6,5,[]]
    machine.c = [8,7]
    machine.d = [10,9]
    machine.perform_rap()
    assert machine.s == []
    assert machine.e == [1,0,2]
    assert machine.c == 'f'
    assert machine.d == [10,9,[8,7],[6,5],[4,3]]

def test_perform_atom(machine):
    # true case
    machine.s = [3,2,1,[]]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_atom()
    assert machine.s == [3,2,1,[],True]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []
    # false case
    machine.s = [3,2,1]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_atom()
    assert machine.s == [3,2,1,False]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []

def test_perform_cons(machine):
    machine.s = [3,2,1,[],0]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_cons()
    assert machine.s == [3,2,1,[0]]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []

def test_perform_car(machine):
    machine.s = [100,[3,2,1]]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_car()
    assert machine.s == [100,1]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []

def test_perform_cdr(machine):
    machine.s = [100,[3,2,1]]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_cdr()
    assert machine.s == [100,[3,2]]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []

def test_perform_zero(machine):
    machine.s = [100,0]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_zero()
    assert machine.s == [100,0,True]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []
    machine.s = [100,99]
    machine.perform_zero()
    assert machine.s == [100,99,False]

def test_perform_eq(machine):
    machine.s = [100,100]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_eq()
    assert machine.s == [100,100,True]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []
    machine.s = [100,99]
    machine.perform_eq()
    assert machine.s == [100,99,False]

def test_perform_leq(machine):
    machine.s = [100,100]
    machine.e = []
    machine.c = []
    machine.d = []
    machine.perform_leq()
    assert machine.s == [100,100,True]
    assert machine.e == []
    assert machine.c == []
    assert machine.d == []
    machine.s = [100,101]
    machine.perform_leq()
    assert machine.s == [100,101,False]
    machine.s = [100,99]
    machine.perform_leq()
    assert machine.s == [100,99,True]

def test_execute(machine):
    machine.loadProgram(['ADD'],[1,1])
    machine.execute()
    assert machine.s == [2]

    machine.loadProgram([0,'ldc'],[2,1])
    machine.execute()
    assert machine.s == [2,1,0]

    machine.loadProgram([0,'eq'],[2,1])
    machine.execute()
    assert machine.s == [2,1,False]
