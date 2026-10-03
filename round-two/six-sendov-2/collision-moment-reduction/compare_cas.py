"""Optional same-author whole universal-map comparison using SymPy 1.14.

Uses independent symbolic division and logarithmic/Laurent series. Does not
import verify.py or supply interlacing, feasibility, KKT or review evidence.
"""
from pathlib import Path
import argparse
import json
import time
import sympy as s


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    args=parser.parse_args();start=time.monotonic()
    x,e,g,z=s.symbols('x E G z');variables=(x,e,g)
    h0=z**7-s.Rational(3,8)*z**5+e*z**3+g*z
    j=-h0.subs(z,x);h=s.expand(h0+j)
    f0=s.integrate(8*h,z);c=-f0.subs(z,x);f=s.expand(f0+c)
    r,rem=s.div(h,z-x,z);q,remq=s.div(f,(z-x)**2,z)
    if s.expand(rem)!=0 or s.expand(remq)!=0:raise ValueError('whole symbolic factors')
    def coefficients(p):
        return list(reversed(s.Poly(p,z).all_coeffs()))
    def inverse_series(p,count):
        reverse=list(reversed(coefficients(p)))
        out=[s.Integer(1)]
        for k in range(1,count+1):
            out.append(s.expand(-sum(reverse[i]*out[k-i] for i in range(1,min(k,len(reverse)-1)+1))))
        return reverse,out
    def log_traces(p,count):
        reverse,inv=inverse_series(p,count)
        out=[s.Integer(s.degree(p,z))]
        for k in range(1,count+1):
            out.append(s.expand(-sum(i*reverse[i]*inv[k-i] for i in range(1,min(k,len(reverse)-1)+1))))
        return out
    numerator=s.expand(8*(z*r-(z-x)*q))
    _,inv=inverse_series(r,5);num=list(reversed(coefficients(numerator)))
    nu=[s.expand(sum(num[i]*inv[k-i] for i in range(k+1))) for k in range(6)]
    rt=log_traces(r,10);K=[[rt[i+k] for k in range(6)] for i in range(6)]
    maps={'J':j,'c':c,'Q':coefficients(q),'r':coefficients(r),'f':coefficients(f),'h':coefficients(h),
          'h_traces':log_traces(h,10),'r_traces':rt,'nu':nu,
          'canceled_resolvent_numerator':coefficients(numerator),'K':K,
          'K_derivatives':[[[s.diff(a,t) for a in row] for row in K] for t in variables],
          'nu_derivatives':[[s.diff(a,t) for a in nu] for t in variables],
          'original_moments':log_traces(f,7)}
    expected=json.loads(args.expected.read_text())['universal']
    if set(expected)!=set(maps):raise ValueError('entire universal namespace')
    count=0
    def check(actual,record):
        nonlocal count
        if isinstance(actual,list):
            if len(actual)!=len(record):raise ValueError('whole array length')
            for a,b in zip(actual,record):check(a,b)
        else:
            terms=s.Poly(s.expand(actual),*variables,domain=s.QQ).terms()
            native={tuple(m):s.Rational(a) for m,a in record}
            computed={tuple(m):a for m,a in terms if a}
            if computed!=native:raise ValueError('whole polynomial coefficient mismatch')
            count+=1
    for key in maps:check(maps[key],expected[key])
    print(json.dumps({'verified':True,'all_universal_polynomials':count,'SymPy':s.__version__,
                      'seconds':time.monotonic()-start,'status':'same-author algebra comparison, not independent review'}))


if __name__=='__main__':main()
