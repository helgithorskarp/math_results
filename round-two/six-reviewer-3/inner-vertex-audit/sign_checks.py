"""Independent whole closed interval-Horner certificates for current signs."""
import argparse,hashlib,json
from pathlib import Path
from digit import T,Z,coefficients,monomials,prove_zero
from geometry import model
from bindings import decode,divide,require
from signs import complete_sign

BOX=['14/25','593/1000','6/5','7/5']

def tasks(f):
    out={}
    for name,guards in [('bound0',['B+','H+']),('bound1',['A+','B+']),
        ('bound2',['A+','H-']),('delta',['A+','B+']),('C0',['A+','H-']),
        ('C4',['A+','H-']),('C6',['A+','B+']),('margin',['B+','H+'])]:
        p=f[name]
        for guard in guards:
            expr={'A':p.p,'B':p.q,'H':p.q*p.q*p.relation-p.p*p.p}[guard[0]]
            out[name+'_'+guard]=(expr,1 if guard[1]=='+' else -1)
    out['critical_norm99']=(f['critical_norm99'].p,1)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('name');args=ap.parse_args()
    m=model();f=decode(json.loads(Path('FACTORS.json').read_text()),m['R'])
    if args.name=='bound2_factorization':
        p=f['bound2'];h=p.q*p.q*m['R']-p.p*p.p;d=f['bound2_square_factor'].p
        rows=divide(coefficients(h),coefficients(d));q=monomials([(i,j,v) for (i,j),v in rows.items()]);proof=prove_zero(h-q*d)
        print(json.dumps({'identity':proof,'whole_quotient':[[i,j,v] for (i,j),v in sorted(rows.items())]},sort_keys=True,separators=(',',':')));return
    p,sign=tasks(f)[args.name];clearing=None
    if args.name=='bound2_H-':
        Q=m['a']*m['D']*Z*Z-2*m['D']*Z+2*T*T-T+1
        multiplier=-8*m['a']**4*m['b']**4*m['c']**2*m['J']*Q
        clearing={'whole_original_H_binding':prove_zero(p-multiplier*f['bound2_square_factor'].p),
            'strictly_negative_multiplier':'-8 a^4 b^4 c^2 J Q; a,b,c,J,Q>0 on entire closed box',
            'raw_sign':-1,'factor_sign':1}
        p=f['bound2_square_factor'].p;sign=1
    poly=coefficients(p);record=complete_sign(poly,BOX,sign)
    print(json.dumps({'name':args.name,'strict_sign':sign,'closed_box':BOX,
        'whole_coefficients':[[i,j,v] for (i,j),v in sorted(poly.items())],
        'coefficient_source':'independent certified digit decoding','certificate':record,
        'uncancelled_clearing':clearing},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
