"""Exact all-pairs geometry in two independently derived metric formulas."""
from family import *
from math import lcm
import ctypes as ct

class Geometry:
    def __init__(self,path):
        self.lib=ct.CDLL(str(Path(path).resolve()))
        for name in ('contacts','real_contacts'):
            fun=getattr(self.lib,name)
            fun.argtypes=[ct.c_int]+[ct.c_int64]*4+[ct.POINTER(ct.c_int64),ct.POINTER(ct.c_int)]
            fun.restype=ct.c_int
    def graph(self,pp,ss,audit=True):
        require(0<len(pp)<=20000,'geometry vertex range')
        require(len(set(pp))==len(pp),'physical point duplicates')
        require(sign(ss)>0 and K.sqrt_real(ss) is None,'non-basis radicand')
        den=lcm(*(x.denominator for p in pp for q in p for x in q))
        nums=[int(x*den) for p in pp for q in p for x in q]
        sd=lcm(ss[0].denominator,ss[1].denominator); s0=int(ss[0]*sd);s1=int(ss[1]*sd)
        require(max(map(abs,nums+[den,sd,s0,s1]))<=10**9,'integer overflow guard')
        data=(ct.c_int64*len(nums))(*nums); n=len(pp);found=[]
        for name in (('contacts','real_contacts') if audit else ('contacts',)):
            out=(ct.c_int*(n*(n-1)))();m=getattr(self.lib,name)(n,den,sd,s0,s1,data,out)
            require(m>=0,'native geometry rejected input')
            found.append([(out[2*i],out[2*i+1]) for i in range(m)])
        if audit:require(found[0]==found[1],'real-coordinate metric disagreement')
        return found[0]

def three_points(root):
    M=spindle();u=tuple(tuple(map(F,p)) for p in root['u']);v=tuple(tuple(map(F,p)) for p in root['v'])
    um=[ecscale(u,m) for m in M];vm=[ecscale(v,m) for m in M]
    uv=[eadd(b,c) for b,c in product(um,vm)]
    pts=[(add(a,w[0]),w[1]) for a,w in product(M,uv)]
    pp=sorted(set(pts));ii={p:i for i,p in enumerate(pp)}
    return pp,[ii[p] for p in pts]

def descend(word,lm,n):
    require(len(word)==len(lm) and all(c in '0123' for c in word),'malformed colour word')
    cc=[None]*n
    for c,i in zip(word,lm):
        require(0<=i<n,'bad physical label')
        require(cc[i] is None or cc[i]==c,'colour does not descend through collision')
        cc[i]=c
    require(all(c is not None for c in cc),'uncoloured vertex')
    return cc

def proper(cc,es):
    require(all(cc[a]!=cc[b] for a,b in es),'monochromatic strict edge')
