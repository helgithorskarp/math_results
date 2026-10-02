"""Own original three-vector data from defining set counts; no target imports."""
from fractions import Fraction as F
from linear import need,canonical

def domain(q,k):need(type(q)is int and type(k)is int and q>=4 and 1<=k<=q,'original integer domain')
def data(q,k):
 domain(q,k);N=(q*q+13*q+16)//2-k;s=3*q+4;ell=5*q+4-k;gap=N-s;h=F(1,3*q+5)
 e=F(q*q+(13-6*k)*q+2*k*k-10*k+14,2);A=(2*k+1)*q+k-F(2*k,q);C=ell*(1-k);T=q*gap;B=-(q-k)*s-k*(3+F(2,q));V=ell*gap-4*q*s;S=F(q*(q+1),2)+(3*(q+1)-2*k)*h
 den=T*V-B*B;a=(V*A-B*C)/den;b=(T*C-B*A)/den;Q=e-a*A-b*C;d=S-2*h*(a*q+b*(2*q-k))
 return {'q':q,'k':k,'N':N,'s':s,'ell':ell,'e':e,'A':A,'C':C,'T':T,'B':B,'V':V,'S':S,'h':h,'D':den,'a':a,'b':b,'Q':Q,'d':d,'U0':[[e,A,C],[A,T,B],[C,B,V]],'Delta':[[S,q*h,(2*q-k)*h],[q*h,F(0),F(0)],[(2*q-k)*h,F(0),F(0)]],'R':[[F(0)]*3 for _ in range(3)]}
