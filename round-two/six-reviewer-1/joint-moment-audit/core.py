"""Fresh full moment-slice construction, before new producer source/data access.

Uses OWN openly credited 68bf078a Laurent kernel, not a new blind arithmetic
implementation. All new reduction and determinants regenerated from written
9550/9902 defining formulas. No imports of any producer source.
"""
from fractions import Fraction as Q
from itertools import combinations
from owned_algebra import P,var,identity,assembly,chart,det_permutation,ZERO


def decode(rows):
    return P({tuple(k):Q(n,d) for k,n,d in rows})


def run(damage=None):
    log={}
    original,reconstruction=assembly(log)
    B,E,r,s,t=(var(i) for i in range(5))
    q,ee,rr,x,u=(var(i) for i in range(5))
    fstar=decode(reconstruction['h'][2])
    # Division by s AFTER specializing B=0; every resulting even exponent
    # is converted explicitly. Inverse u is legal because t and s nonzero.
    fs_over_s={}
    for k,v in (fstar.sub(0,0)/s).d.items():
        power=k[3]-k[4]
        if power%2 or any(k[j] for j in [0,5,6,7]):
            raise ValueError('Fstar/s parity')
        key=(0,k[1],k[2],power//2,k[4],0,0,0)
        fs_over_s[key]=fs_over_s.get(key,Q(0))+v
    fs= P(fs_over_s)
    if damage=="pivot":fs=fs+ee/60
    displayed=-Q(83,60)*ee-Q(21,4)*rr**2+Q(7,2)*rr*x-Q(49,16)*rr+Q(13,16)*x-Q(663,1792)+(Q(56,3)*rr-14*x+8)/u
    identity(fs,displayed,'complete-Fstar-over-s',log)
    pivot=fs.coeff(1,1)
    identity(pivot,Q(-83,60),'constant-E-pivot',log)
    recover=fs.sub(1,0)*Q(60,83)
    explicit=(-141120*rr**2*u+94080*rr*u*x-82320*rr*u+501760*rr+21840*u*x-9945*u-376320*x+215040)/(37184*u)
    identity(recover,explicit,'complete-E-recovery',log)
    identity(fs.sub(1,recover),0,'Fstar-recovery-zero',log)
    switched=[chart(a.sub(0,0),d) for a,d in zip(original,[2,1,2,1,2])]
    polys=[];contents=[]
    for i,a in enumerate(switched):
        back={}
        for k,v in a.d.items():
            key=(0,k[1],k[2],2*k[3]+k[4]-[2,1,2,1,2][i],k[4],0,0,0)
            back[key]=back.get(key,Q(0))+v
        identity(P(back),original[i].sub(0,0),'full-chart-pullback-'+str(i),log)
        z=a.sub(1,recover)
        if any(k[4]<0 or k[1] or any(k[j] for j in [0,5,6,7]) for k in z.d):
            raise ValueError('non-polynomial E substitution')
        content,p=z.primitive();contents.append(content);polys.append(p)
        identity(content*p,z,'entire-positive-content-'+str(i),log)
        if p.degree(4)>2: raise ValueError('u quadratic')
    if damage=='drop-fifth':polys=polys[:4]
    if len(polys)!=5:raise ValueError('all5 rows retained')
    matrix=[[p.coeff(4,j) for j in [2,1,0]] for p in polys]
    if damage=='matrix':matrix[4][2]=matrix[4][2]+1
    for i,row in enumerate(matrix):
        identity(sum((v*u**j for v,j in zip(row,[2,1,0])),P()),polys[i],'whole-matrix-row-'+str(i),log)
    triples=list(combinations(range(5),3))
    raw=[det_permutation([matrix[i] for i in tri]) for tri in triples]
    minors=[];gcds=[]
    for a in raw:
        cont,p=a.primitive();gcds.append(cont);minors.append(p)
    # Reconstruct Newton moments directly, independent of elimination.
    f=[P(),8*decode(reconstruction['h'][0]),4*decode(reconstruction['h'][1]),Q(8,3)*fstar,2*E,Q(8,5)*B,P(Q(-1,2)),P(),P(1)]
    mu=[P(8)]
    for n in range(1,6):
        mu.append(-sum((f[8-j]*mu[n-j] for j in range(1,n)),P())-n*f[8-n])
    identity(mu[3],-Q(24,5)*B,'whole-original-cubic-moment',log)
    if damage=='moment':mu[5]=mu[5]+B
    identity(mu[5],-4*B-Q(40,3)*fstar,'whole-original-fifth-moment',log)
    # Whole coefficient residue pairing, not numerical root samples.
    max_entry_degree=max(sum(k) for row in matrix for z in row for k in z.d)
    Qstar=sum(sum(abs(v) for v in z.d.values())**2 for row in matrix for z in row)
    boundaries={}
    for point in [Q(-3,8),Q(-3,7),Q(0),Q(1)]:
        values=[[z.sub(3,0).sub(2,point) for z in row] for row in matrix]
        val=[[str(z.d.get(ZERO,0)) for z in row] for row in values]
        all3=[det_permutation([values[i] for i in tri]).d.get(ZERO,0) for tri in triples]
        all2=[det_permutation([[values[i][a],values[i][b]],[values[j][a],values[j][b]]]).d.get(ZERO,0) for i,j in combinations(range(5),2) for a,b in combinations(range(3),2)]
        boundaries[str(point)]={'matrix':val,'rank':3 if any(all3) else 2 if any(all2) else 1 if any(z.d for row in values for z in row) else 0}
    from univariate import stream,many_gcd
    boundary_gcd=many_gcd([stream(a.sub(3,0),2) for a in raw])
    if boundary_gcd['gcd']!=['9/56','45/56','1']:raise ValueError('complete x0 rank-loss locus')
    scalar_gcd={}
    for point,expected in [(Q(-3,8),['224/9','1']),(Q(-3,7),['0','1'])]:
        g=many_gcd([stream(a.sub(3,0).sub(2,point),4) for a in polys])
        if g['gcd']!=expected:raise ValueError('complete finite scalar boundary')
        scalar_gcd[str(point)]=g
    if damage=='boundary':
        bad=boundary_gcd['gcd'].copy();bad[0]='10/56'
        if bad!=boundary_gcd['whole_product']:raise ValueError('altered boundary unit')
    for point,us in [(Q(-3,8),Q(-224,9)),(Q(-3,7),Q(0))]:
        for i,a in enumerate(polys):
            identity(a.sub(3,0).sub(2,point).sub(4,us),0,'boundary-full5-zero-%s-%s'%(point,i),log)
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','schema':1,
            'method':'own68bf078a full Laurent reconstruction; fresh all5 substitution; direct Leibniz determinants; no new producer imports/data',
            'source_input_9550':{'residual':[z.serial() for z in original],'reconstruction':reconstruction},
            'Fstar_over_s':fs.serial(),'E_recovery':recover.serial(),'switched':[z.serial() for z in switched],
            'contents':list(map(str,contents)),'P':[z.serial() for z in polys],
            'matrix':[[z.serial() for z in row] for row in matrix],
            'triples':[list(v) for v in triples],'raw_minors':[z.serial() for z in raw],
            'minor_contents':list(map(str,gcds)),'primitive_minors':[z.serial() for z in minors],
            'term_counts':[len(z.d) for z in polys],'entry_max_total_degree':max_entry_degree,
            'boundary_minor_gcd':boundary_gcd,'boundary_scalar_gcd':scalar_gcd,'Qstar':str(Qstar),'whole_identities':log,'boundary_controls':boundaries}

if __name__=='__main__':
    import json,hashlib,time
    from pathlib import Path
    start=time.monotonic();a=run();data=json.dumps(a,sort_keys=True,separators=(',',':')).encode()
    Path(__file__).with_name('EXPECTED.json').write_bytes(data+b'\n')
    print(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'seconds':time.monotonic()-start,'whole_identities':len(a['whole_identities']),'counts':a['term_counts'],'Q':a['Qstar'],'boundary':a['boundary_controls']}))
