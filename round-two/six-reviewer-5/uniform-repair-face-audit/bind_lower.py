"""Stdlib-only whole original-member binding, no CAS or producer evaluator."""
import ast,json
from fractions import Fraction as F
from pathlib import Path
from literal_check import require,members,table,entry,pair,short

P=Path(__file__).resolve().parent

def value(text,env):
    def go(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return F(n.value)
        if isinstance(n,ast.Name) and n.id in env:return F(env[n.id])
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -go(n.operand)
        if isinstance(n,ast.BinOp):
            a,b=go(n.left),go(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
            if isinstance(n.op,ast.Pow) and b.denominator==1 and 0<=b<=128:return a**int(b)
        raise ValueError('nonliteral arithmetic input')
    return go(ast.parse(text,mode='eval').body)

def full_sector(q,standard):
    X=members(q,0);T=table(q)
    C=[];D=[]
    for A in X:
        vals=[entry(A,B,q,T) for B in X]
        C.append([v[0] for v in vals]);D.append([v[1] for v in vals])
    groups=[(0,),(0,),(1,),(2,4),(3,5),(6,)] if standard else [(0,),(0,),(1,),(2,4),(6,),(7,),(3,5),(6,)]
    sizes=[1,2,1,1,1,1] if standard else [1,2,1,1,0,0,1,1]
    V=[]
    for A in X:
        f=int(bool(A&8))-int(bool(A&16))
        V.append([F((A&7) in g and (A>>3).bit_count()==r)*(f if standard else 1) for g,r in zip(groups,sizes)])
    return pair(C,V),pair(D,V),V,C,D

def main():
    data=json.loads((P/'lower-sectors.json').read_text());formulas=json.loads((P/'lower-signs.json').read_text())
    records=[]
    for q in (4,5):
        sector_data=[]
        for standard,name in ((True,'nu'),(False,'tau')):
            C,D,V,actualC,actualD=full_sector(q,standard)
            for key,A in (('Gram0',C),('Delta',D)):
                expected=[[value(x,{'q':q}) for x in row] for row in data[name][key]]
                require(expected==A,'EVERY original '+name+' '+key+' entry')
            target=len(C)-1;norm=2 if standard else q
            zero,W=short(C,[target],[] if standard else [0])
            require(zero[0][0]/norm==value(data[name]['zero'],{'q':q}),'literal zero energy')
            deriv=pair(D,W)[0][0]
            if not standard:
                z=[F(1),F(1),F(0),F(0),F(0),F(-1),F(0),F(0)]
                alpha=sum(z[i]*D[i][j]*z[j] for i in range(8) for j in range(8))
                cross=sum(z[i]*D[i][j]*W[j][0] for i in range(8) for j in range(8))
                require(cross!=0,'singular best-gauge correction actually necessary')
                deriv-=cross*cross/alpha
                require(-cross/alpha==value(data[name]['shift'],{'q':q}),'literal best physical gauge')
            require(deriv/norm==value(data[name]['right_derivative'],{'q':q}),'literal right derivative')
            sector_data.append((V,actualC,actualD))
        # All mixed constant/mean-zero entries are checked, not only diagonal blocks.
        V0,C,D=sector_data[0];V1=sector_data[1][0]
        for A in (C,D):
            for i in range(6):
                for j in range(8):
                    require(sum(V0[a][i]*A[a][b]*V1[b][j] for a in range(len(A)) for b in range(len(A)) if V0[a][i] and A[a][b] and V1[b][j])==0,'all original sector cross entries')
        records.append(dict(q=q,N=len(C)+1,original_pairs=len(C)**2,sector_coefficient_entries=200,cross_entries=96))
    literal=json.loads((P/'literal-original.json').read_text());q,k=literal['q'],literal['k']
    nu,nd,tau,td=[value(formulas[n],{'q':q,'k':k}) for n in ('nu0','nu_prime0','tau0','tau_prime0')]
    a=value(formulas['a0'],{'q':q,'k':k})
    derivative=a*a/F(q)*(F(q-k,k)*nd/(nu*nu)+td/(tau*tau))
    require(a==F(literal['a0']) and derivative==F(literal['a_prime0']),'whole literal deleted-carrier a and best-gauge derivative')
    require(derivative<-F(1,q**4),'new stronger lower derivative on literal carrier')
    records.append(dict(q=q,k=k,N=literal['N'],original_pairs=literal['original_positions'],orbit_entries=literal['all_original_gram_entries'],a0=str(a),a_prime0=str(derivative)))
    record={'status':'EVERY original lower sector entry, all mixed entries and deleted-family short/derivative match','records':records,'producer_code_used':False,'CAS_imported':False}
    (P/'lower-binding.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
