"""Iterative stdlib AST parser for expanded QQ[q,k] stage records.

No Python evaluation, recursion-limit change, symbolic parser or calls.
The exponent bound244 is the determinant bound2*122 from this cap
certificate, not a solver/memory/thread/time limit.
"""
import ast
from fractions import Fraction as F
from literal_check import require
from check_polynomials import mul,scale,ONE

def polynomial(root):
    todo=[(root,False)];values={}
    while todo:
        node,ready=todo.pop()
        if not ready:
            if isinstance(node,ast.Constant) and type(node.value) is int:
                values[id(node)]={(0,0):F(node.value)} if node.value else {};continue
            if isinstance(node,ast.Name) and node.id in ('q','k'):
                values[id(node)]={(1,0) if node.id=='q' else (0,1):F(1)};continue
            if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):
                todo.extend([(node,True),(node.operand,False)]);continue
            if isinstance(node,ast.BinOp):
                todo.extend([(node,True),(node.right,False),(node.left,False)]);continue
            raise ValueError('nonliteral polynomial AST')
        if isinstance(node,ast.UnaryOp):
            values[id(node)]=scale(values.pop(id(node.operand)),-1);continue
        a=values.pop(id(node.left));b=values.pop(id(node.right))
        if isinstance(node.op,(ast.Add,ast.Sub)):
            sign=1 if isinstance(node.op,ast.Add) else -1
            for e,c in b.items():
                a[e]=a.get(e,F(0))+sign*c
                if not a[e]:del a[e]
            result=a
        elif isinstance(node.op,ast.Mult):result=mul(a,b)
        elif isinstance(node.op,ast.Div):
            require(set(b)=={(0,0)},'only rational constant division inside polynomial')
            result=scale(a,1/b[(0,0)])
        elif isinstance(node.op,ast.Pow):
            require(isinstance(node.right,ast.Constant) and type(node.right.value) is int and 0<=node.right.value<=244,'derived244 determinant degree bound')
            n=node.right.value
            require(len(a)<=1,'expanded polynomial monomial power only')
            if n==0:result=dict(ONE)
            elif not a:result={}
            else:
                (i,j),c=next(iter(a.items()));result={(i*n,j*n):c**n}
        else:raise ValueError('unsupported polynomial operator')
        values[id(node)]=result
    require(len(values)==1,'entire AST consumed')
    result=values[id(root)]
    require(all(sum(e)<=244 for e in result),'derived244 total degree bound')
    return result

def rational(text):
    node=ast.parse(text,mode='eval').body
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):return polynomial(node.left),polynomial(node.right)
    return polynomial(node),ONE
