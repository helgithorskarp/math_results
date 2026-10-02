"""Reconstruct shared complete finite/dual/scalar records, no author imports.

Written AFTER the independent normal record was frozen. The layout and
parameter formulas are credited to the published author record. This is
corroboration, not the independent PSD proof engine.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys
import core as c
from audit import strict_json

def scalar(q,k,own):
    N=(q*q+13*q+16)//2-k;s=3*q+4
    out={'q':q,'k':k,'N':N,'s':s}
    key='continue'+str(q)
    if (k==2 and q in [4,5,6]) or (k==3 and q in [9,10,11]):
        z=own[key]
        return {**out,'kappa':F(z['kappa']),'tau':F(z['tau']),
          'seed_gamma':F(1,8192),'gap':F(1,16384),'eta':F(1,4096),
          'delta_norm':F(z['derivative_absolute_row_norm']),'method':'finite cap continuity'}
    if (q,k)==(8,3):return {**out,'kappa':F(1,4096),'tau':F(1,2),
                                  'gap':F(1,1 << 20),'method':'finite affine rectangle'}
    g=N-2*s;h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h;B=N-s-k
    if k==2:
        kap=F(1,8)
        chi=2*g*(N-kap+kap*h)**2-((N-kap)+kap*alpha)*(N-kap)*(N-s-2)
        gamma=g*chi/(N*(N-kap)**2*(N-s-2))
        return {**out,'kappa':kap,'chi':chi,'gamma':gamma,'seed_gamma':gamma,
                'gap':gamma/2,'tau':min(F(1,192),gamma/4),'method':'credited9145 tail'}
    c.need(k==3 and q>=12,'credited three-deletion scalar branch')
    B0=F(q*q-11*q-10,2);D=2*k*g*(1-h)+(alpha-2*k+2)*B
    E=k*g*(1-h)**2+(alpha-k+1)*B;kap=min(F(1,8),N*B0/(2*D))
    chi=N*N*B0-kap*N*D+kap*kap*E
    gamma=g*chi/(N*(N-kap)**2*B)
    c.need(min(B0,D,E,chi,gamma)>0,'credited scalar positivity at this parameter')
    return {**out,'g':g,'B0':B0,'h':h,'alpha':alpha,'D':D,'E':E,'kappa':kap,
         'chi':chi,'gamma':gamma,'seed_gamma':gamma,'gap':gamma/2,
         'tau':min(kap/24,gamma/4),'minimum_q':12,'method':'credited9195 tail'}

def negative(q,own):
    r=own['neg'+str(q)]
    return {'q':q,'N':r['N'],'alpha':r['negative_kappa_energy'],'C0_z':'0','R_z':'0'}

def reconstruct(own):
    finite=[]
    pairs=[(4,2),(5,2),(6,2),(8,3),(9,3),(10,3),(11,3)]
    def row(q,k,kap,t):
        sets,C,D,R,U=c.matrices(q,k);end=c.affine(c.affine(C,D,kap),R,t)
        return {'q':q,'k':k,'N':len(sets),'s':3*q+4,'kappa':str(kap),'t':str(t),
                'domain_sha256':c.digest([c.mask(A) for A in sets]),'core_sha256':c.digest(end)}
    for q,k in pairs:
        if q==8:continue
        p=scalar(q,k,own);r=row(q,k,p['kappa'],F(0))
        r.update(phase='continuity',rank=own['continue'+str(q)]['zero_cap_floor']['rank'],
            eta=str(p['eta']),delta_norm=str(p['delta_norm']),tau=str(p['tau']),
            seed_gamma=str(p['seed_gamma']),gap=str(p['gap']))
        finite.append(r)
    for positive in [False,True]:
        for high in [False,True]:
            key='corner'+str(int(positive))+('b' if high else 'a');z=own[key]
            r=row(8,3,F(z['kappa']),F(z['t']))
            for phase,rank in [('corner-lower',z['lower']['rank']),('corner-upper',z['upper_floor']['rank'])]:
                finite.append({**r,'phase':phase,'rank':rank,'eta':str(F(1,1 << 20))})
    for q,k in pairs:
        p=scalar(q,k,own);r=row(q,k,p['kappa'],p['tau'])
        z=own['corner1b' if q==8 else 'continue'+str(q)]['original_whole_control']
        r.update(whole_sha256=z['L_sha256'],actual_empty_M_loop=z['empty_M_loop'],gap=str(p['gap']))
        for phase in ['whole-lower','whole-gap']:
            finite.append({**r,'phase':phase,'rank':r['N']-1,
                          'normalized_gap':str(p['gap']/(p['N']-p['s']))})
    n=own['neg4'];dual={'q4':{'q':4,'N':n['N'],'zero_upper':n['dual']['pairing']['a'],
       'delta':n['dual']['pairing']['d'],'repair':n['dual']['pairing']['r'],
       'lower_negative_kappa':negative(4,own)},'rank_two':[],
       'fixture_sha256':hashlib.sha256((c.ROOT/'INPUT-DUALS.json').read_bytes()).hexdigest(),
       'scope':'all real kappa,t infeasible only in the specified affine-table/four-edge ansatz'}
    for q in [5,6,7]:
        n=own['neg'+str(q)];z=n['dual']
        dual['rank_two'].append({'q':q,'N':n['N'],'weight':z['weight'],
            'pairings':z['separate_pairings'],'combined':z['combined_pairings'],
            'lower_negative_kappa':negative(q,own)})
    parameters={'samples':[scalar(q,k,own) for q,k in pairs+[(7,2),(12,3),(1000000,2),(1000000,3)]]}
    q=1000000;k=3;p=scalar(q,k,own);kap=p['kappa'];t=p['tau'];h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h;deleted=[frozenset([1,2,x]) for x in range(3,6)]
    def unpack(m):return frozenset(i for i in range(m.bit_length()) if m >> i & 1)
    def rho(A):
        a=len(A&{0,1,2});r=F(1) if a==0 else h if a<3 else -3*(q+1)*h
        return kap*r-sum(c.primitive(q,A,B,kap) for B in deleted)+t*(2 if A=={0} else -1 if A in [{0,1},{0,2}] else 0)
    def entry(a,b):
        A=unpack(a);B=unpack(b)
        if a==b==0:L=1+kap*(alpha-2*k*h)+k*(p['s']-k)
        elif a==0:L=1-rho(B)
        elif b==0:L=1-rho(A)
        else:L=1+c.primitive(q,A,B,kap)+t*c.repair(A,B)
        return str((L-p['s']*int(a==b))/(p['N']-p['s']))
    parameters['large_scalar_only_entries']=[entry(a,b) for a,b in [(0,0),(0,1),(1,0),(1,2),(3,4),(8,16),(11,21)]]
    return c.canonical({'finite':finite,'duals':dual,'parameters':parameters})

def main():
    c.need(len(sys.argv)==2,'supply public hash-pinned author EXPECTED.json')
    data=Path(sys.argv[1]).read_bytes()
    c.need(hashlib.sha256(data).hexdigest()=='259d37a58e9a5780fea1d66f39f6c39b15c1570fd4930b9d7e8ebcf149e8def1','entire author record pin')
    author=strict_json(data.decode());own=strict_json((c.ROOT/'EXPECTED.json').read_text())
    r=reconstruct(own)
    for name in r:
        c.need(json.dumps(r[name],sort_keys=True,separators=(',',':'))==
               json.dumps(author[name],sort_keys=True,separators=(',',':')),
               'entire typed shared '+name+' record')
    c.need(len(r['finite'])==28,'complete finite phase census')
    print(json.dumps({'ok':True,'finite_records':28,'entire_duals':True,'entire_scalar_records':True,
        'record_sha256':c.digest(r),'scope':'Shared finite,dual,scalar fields; author26 damage names and author record self-digest are native corroboration only.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
