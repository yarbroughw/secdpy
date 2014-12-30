import sys

def lex(stream):
    stream = stream.replace('(',' ( ')
    stream = stream.replace(')',' ) ')
    return stream.split()

def parse(program):
    tokens = lex(program)
    return buildast(tokens)

def buildast(tokens):
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(buildast(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('mismatched parens.')
    else:
        return atom(token)

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)

operators = {
                '+': 'add',
                '*': 'mul',
                '-': 'sub',
                '/': 'div',
            }

builtins = ['if','null','nil','lambda','let','letrec','list','and2']

def index(e, n):
    def indx2(e, n, j):
        if len(n) == 0:
            return []
        elif n[0] == e:
            return j
        else:
            return indx2(e, n[1:], j + 1)

    def indx(e, n, i):
        if len(n) == 0:
            return []

        j = indx2(e, n[0], 1)

        if j == []:
            return indx(e, n[1:], i + 1)
        else:
            return [j, i]

    rval = indx(e, n, 1)

    if rval == []:
        return rval
    else:
        assert len(rval) == 2
        assert type(rval[0]) == int
        assert type(rval[1]) == int
        return rval

def isAtom(e):
    return e == [] or type(e) == int or type(e) == str

def isBuiltin(e):
    return e in ['+','-','*','/','car','cdr','zero','atom','eq','leq']

def isOperator(e):
    return e in operators

def codegen(expr,names,code):
    # print("expr =", expr, ", names =", names, ", code =", code)

    if isAtom(expr):
        if expr == []:
            # print("1 appending nil to", code)
            code.append('nil')
            return code
        else:
            ij = index(expr,names)
            if ij == []:
                code.append(expr)
                code.append('ldc')
            else:
                code.append(ij)
                code.append('ld')
            return code
    else:
        fn   = expr[0]
        args = expr[1:]
        if isAtom(fn):
            if isBuiltin(fn):
                if isOperator(fn):
                    fn = operators[fn]
                code.append(fn)
                return genBuiltin(args, names, code)
            elif fn == "list":
                xs = []
                # print("looping through", args)
                for item in args:
                    x = codegen(item,names,['cons'])
                    xs.extend(x[::-1])
                xs = xs[::-1]
                code.extend(xs)
                # print("2 appending nil to", code)
                code.append('nil')
                return code
            elif fn == "lambda":
                # print("generating lambda w/",args[1],args[0],code)
                return genLambda(args[1], [args[0]]+names, code)
            elif fn == "if":
                return genIf(args[0],args[1],args[2],n,code)
            elif fn == 'let' or fn == 'letrec':
                new  = [args[0]] + names
                vals = args[1]
                body = args[2]

                if fn == 'let':
                    code.append('ap')
                    lamb = genLambda(body,new,code)
                    app = genApp(vals,names,lamb)
                    # print("3 appending nil to", code)
                    app.append('nil')
                    return app
                elif fn == 'letrec':
                    code.append('rap')
                    lamb = genLambda(body,new,code)
                    app = genApp(vals,new,lamb)
                    # print("4 appending nil to", code)
                    app.append('nil')
                    app.append('dum')
                    return app
            else:
                code.append('ap')
                code.append(index(fn,names))
                code.append('ld')
                app = genApp(args,names,code)
                # print("5 appending nil to", code)
                app.append('nil')
                return app
        else:
            code.append('ap')
            code = codegen(fn,names,code)
            app  = genApp(args,names,code)
            # print("6 appending nil to", code)
            app.append('nil')
            return app


def genBuiltin(args,names,code):
    if args == []:
        return code
    else:
        return genBuiltin(args[1:], names, codegen(args[0],names,code))

def genLambda(body,names,code):
    code.append(codegen(body,names,['rtn']))
    code.append('ldf')
    # print("generated lambda:",code)
    return code

def genIf(test,trueExpr,falseExpr,names,code):
    code.append(codegen(falseExpr,names,['join']))
    code.append(codegen(trueExpr, names,['join']))
    code.append('sel')
    return codegen(test,names,code)

def genApp(args, names, code):
    if args == []:
        return code
    else:
        code.append('cons')
        return genApp(args[1:], names,
            codegen(args[0], names, code))

def main():
    code = sys.stdin.read()
    print(codegen(parse(code), [], ['stop']))

if __name__ == '__main__':
    main()

