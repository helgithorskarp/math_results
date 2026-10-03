"""Data-only binding: every native raw form to sealed independent covariance."""
import argparse,json,pathlib,sys
from fractions import Fraction as F
from functools import lru_cache
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from canonical import K,QQ

def need(ok,why):
    if not ok:raise ValueError(why)

def polynomial(terms,den=1):
    a={}
    for e,c in terms:
        e=tuple(e);need(len(e)==2 and all(type(t) is int and t>=0 for t in e),'polynomial exponents')
        c=F(c)/den;need(e not in a,'distinct polynomial terms');a[e]=QQ(c.numerator,c.denominator)
    return K(K.ring.from_dict(a))

def native(p):
    need(type(p['denominator']) is int and p['denominator']>0,'positive scalar denominator')
    return polynomial(p['terms'],p['denominator'])

def td(p):return max((sum(ex) for ex,c in p.terms()),default=0)

def own(p):return polynomial(p['num'])/polynomial(p['den'])

def maximum(a):
    n=len(a)
    @lru_cache(None)
    def visit(mask):
        i=mask.bit_count()
        if i==n:return 0
        return max((a[i][j]+visit(mask|(1<<j)) for j in range(n) if not(mask>>j)&1 and a[i][j]>=0),default=-100000)
    return visit(0)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('primary',type=pathlib.Path);ap.add_argument('raw',type=pathlib.Path);ap.add_argument('out',type=pathlib.Path);ap.add_argument('--damage');a=ap.parse_args()
    p=json.loads(a.primary.read_text());raw=json.loads(a.raw.read_text())
    ours={name:[[p['scalars'][i]]] for i,name in enumerate(p['scalar_order'])}
    ours.update({{'anti-heavy':'antiH','anti-light':'antiL'}.get(name,name):m for name,m in p['sectors'].items()})
    need(set(ours)==set(raw['forms']),'complete ten form catalogue')
    if a.damage=='original-entry':raw['forms']['fixed']['raw'][0][0]['numerator']['terms'][0][1]='999'
    if a.damage=='negative-factor':raw['forms']['fixed']['positive_row_domains'][0][0]['factor']['terms']=[[[0,0],'-1']]
    if a.damage=='degree':raw['bounds'][-1]['h_degree_bound']=-1
    boundmap={(r['group'],r['order']):r for r in raw['bounds']};forms={};counts=0;factors=0
    expected={(name,k) for name,m in ours.items() for k in range(1,len(m)+1)}
    need(set(boundmap)==expected and len(boundmap)==len(raw['bounds'])==24,'complete 24 obligations')
    for name,matrix in ours.items():
        n=len(matrix);r=raw['forms'][name]
        need(len(r['raw'])==len(r['positive_row_domains'])==n and all(len(row)==n for row in r['raw']),'entire square raw form')
        cleared=[]
        for i,row in enumerate(matrix):
            D=K.one
            for f in r['positive_row_domains'][i]:
                factor=native(f['factor']);e=f['power'];need(type(e) is int and e>0,'positive integer factor power')
                need(td(factor.denom)==0 and td(factor.numer)<=1,'affine factor')
                coeff=dict(factor.numer.terms());den=factor.denom[(0,0)]
                need(coeff.get((1,0),0)/den>=0 and coeff.get((0,1),0)/den>=0,'nonnegative affine slopes')
                need(sum(c*2**ex[0]*4**ex[1] for ex,c in coeff.items())/den>0,'strict affine factor at h2 q4')
                D*=factor**e;factors+=1
            crow=[]
            for j,ind in enumerate(row):
                z=r['raw'][i][j];val=native(z['numerator'])
                for f in z['denominator_factors']:val/=native(f['factor'])**f['power']
                need(val==own(ind),'ENTIRE independent rational-function equality '+name+':'+str((i,j)))
                c=D*val;need(td(c.denom)==0,'entire exact row clearing')
                crow.append([[list(ex),str(co/c.denom[(0,0)])] for ex,co in sorted(c.numer.terms())]);counts+=1
            cleared.append(crow)
        degrees=[[[max((ex[v] for ex,c in z),default=-1) for z in row] for row in cleared] for v in (0,1)]
        for k in range(1,n+1):
            bh,bq=[maximum([row[:k] for row in mat[:k]]) for mat in degrees];claim=boundmap[(name,k)]
            need(0<=bh<=claim['h_degree_bound'] and 0<=bq<=claim['q_degree_bound'],'proved separate original determinant degree bounds')
        forms[name]=dict(cleared=cleared,actual_entry_degrees=degrees)
    out=dict(actual_agent='six-reviewer-5',role='independent reviewer',domain='integer h>=3, real q>=4',forms=forms,bounds=raw['bounds'],rational_entries_bound=counts,positive_affine_factor_occurrences=factors,complete_original_rational_binding=True)
    a.out.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['forms','bounds']}))
if __name__=='__main__':main()
