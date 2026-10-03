"""Independent cleared-minor zero optimization; every division multiplied back."""
from pathlib import Path
import json
import original_field as O
from stages import load
from polynomial_cap import fieldpoly,RP,Q,K,degree,exquo
from parse_exact import rational
P=Path(__file__).resolve().parent

def ringpoly(p):return RP.from_dict({e:O.FIELD.domain.convert(c) for e,c in p.items()})

def main():
    cap=fieldpoly(load('cap-short-polynomials'));p=cap['numerator'];T=cap['denominator']
    low=json.loads((P/'lower-signs.json').read_text());an,ad=rational(low['a0']);A,B=ringpoly(an),ringpoly(ad)
    minors={}
    for i,j,text in [(0,0,p[1][1]*p[2][2]-p[1][2]**2),(1,1,p[0][0]*p[2][2]-p[0][2]**2),
                     (2,2,p[0][0]*p[1][1]-p[0][1]**2),(0,1,p[0][2]*p[1][2]-p[0][1]*p[2][2]),
                     (0,2,p[0][1]*p[1][2]-p[0][2]*p[1][1]),(1,2,p[0][1]*p[0][2]-p[0][0]*p[1][2])]:
        minors[(i,j)]=exquo(text,T)
    det3=exquo(p[0][0]*minors[(0,0)]+p[0][1]*minors[(0,1)]+p[0][2]*minors[(0,2)],T)
    Dk=B*minors[(2,2)]+A*(p[0][0]+2*p[0][1]+p[1][1])
    h0=B*minors[(0,2)]+A*(p[1][1]+p[0][1]-p[0][2]-p[1][2])
    h1=B*minors[(1,2)]-A*(p[0][0]+p[0][1]+p[0][2]+p[1][2])
    O.require((B*p[0][0]+A*T)*h0+(B*p[0][1]-A*T)*h1==-(B*p[0][2]-A*T)*Dk,'first ENTIRE original optimal stationary equation')
    O.require((B*p[0][1]-A*T)*h0+(B*p[1][1]+A*T)*h1==-(B*p[1][2]+A*T)*Dk,'second ENTIRE original optimal stationary equation')
    vN=Dk-h0+h1
    bn=2*(3*Q+4)*(3*Q**2+3*Q-2);bd=6*Q**2+5*Q-2
    upper=4*bn*B*Dk-vN*(A*bd+bn*B)
    sadj=minors[(0,0)]+minors[(1,1)]+minors[(2,2)]-2*minors[(0,1)]-2*minors[(0,2)]+2*minors[(1,2)]
    Rn=B*det3+A*sadj;Rd=Dk
    O.require(Rn*B*T==(B*p[2][2]+A*T)*Dk+(B*p[0][2]-A*T)*h0+(B*p[1][2]+A*T)*h1,'ENTIRE original residual identity')
    gcd=Rn.gcd(Rd);rawRn,rawRd=Rn,Rd;Rn,Rd=exquo(Rn,gcd),exquo(Rd,gcd)
    O.write('optimization-polynomials',dict(M_denominator=T,H_leading=p[0][0],H_determinant=minors[(2,2)],
        vertex_denominator=Dk,vertex_lower=vN,vertex_upper=upper,h0_numerator=h0,h1_numerator=h1,
        R_numerator=Rn,R_denominator=Rd,raw_R_numerator=rawRn,raw_R_denominator=rawRd,R_common_factor=gcd))
    print('H degrees',degree(p[0][0]),degree(minors[(2,2)]),'vertex degrees',degree(vN),degree(upper),'R degrees',degree(Rn),degree(Rd),flush=True)

if __name__=='__main__':main()
