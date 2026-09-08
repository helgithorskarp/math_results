#!/usr/bin/env python3
"""Independent audit of the uniform mod-7 colouring certificate."""
from __future__ import annotations
import argparse,hashlib,json,math,sys,time
from pathlib import Path

def require(ok,msg):
    if not ok:raise ValueError(msg)

def factor_kernel(n):
    require(isinstance(n,int) and n>0,'positive factor input')
    m=n;c=1;s=1;p=2
    while p*p<=m:
        e=0
        while m%p==0:m//=p;e+=1
        c*=p**(e//2)
        if e&1:s*=p
        p+=1
    if m>1:s*=m
    require(c*c*s==n,'factor reconstruction')
    return c,s

def audit(data,controls=False):
    require(set(data)=={'prime','quadratic_residue_roots','weights','colour_pairs_in_r_units','residue_conic_rows','distance24_factor_rows','distance24_triangle'},'top keys')
    p=data['prime'];require(p==7,'prime')
    roots={int(k):v for k,v in data['quadratic_residue_roots'].items()}
    require(set(roots)=={1,2,4} and all(q*q%p==s for s,q in roots.items()),'residue roots')
    weights=data['weights'];require(weights==[0,3,2,0,6,0,0],'weight rule')
    require(data['colour_pairs_in_r_units']==[[0,1],[2,3],[4,5],[6]],'colour partition')
    def col(D,t):
        r=2*D%p;j=t*pow(r,-1,p)%p
        return next(i for i,B in enumerate(data['colour_pairs_in_r_units']) if j in B)
    expected=[];direction_checks=0;colour_checks=0
    for D in range(1,p):
        r=2*D%p;bad={0,r,-r%p}
        require(D%p not in bad,'vertical displacement')
        for s in range(p):
            # This is reconstructed from the declared square/nonsquare rule,
            # independently of the producer's table traversal.
            a=3*roots[s]%p if s in roots else 0
            require(a==weights[s],'weight reconstruction')
            for k in range(p):
                for c in range(p):
                    if (k*k+s*c*c-D*D)%p:continue
                    ds=sorted({(k+a*c)%p,(k-a*c)%p})
                    require(not set(ds)&bad,'conic displacement')
                    expected.append([D,s,c,k,ds])
                    for d in ds:
                        for t in range(p):
                            require(col(D,t)!=col(D,(t+d)%p),'edge colour')
                            colour_checks+=1
                    direction_checks+=len(ds)
    # Producer uses c-major order; compare canonically so traversal is independent.
    got=data['residue_conic_rows']
    require(len(got)==len(expected) and sorted(got)==sorted(expected),'complete conic table')
    rows=[];D=24;rad=set();physical_direction_checks=2
    for k in range(D):
        c,s=factor_kernel(D*D-k*k);a=weights[s%p]
        ds=sorted({(k+a*c)%p,(k-a*c)%p})
        rows.append([k,c,s,a,ds]);rad.add(s)
        mult=2 if k==0 else 4
        physical_direction_checks+=mult
        require(not set(ds)&{0,2*(D%p)%p,-2*(D%p)%p},'distance24 residue')
    require(rows==data['distance24_factor_rows'],'distance24 factors')
    require(physical_direction_checks==96,'physical directions')
    tri=data['distance24_triangle'];require(tri==[[[0,1],0],[[0,1],24],[[12,3],12]],'triangle data')
    # [coefficient, squarefree radicand] represents coefficient*sqrt(radicand).
    triangle_norm_checks=0
    for i in range(3):
        for j in range(i):
            dx1,s1=tri[i][0];dx2,s2=tri[j][0]
            # Only the third point has a nonzero horizontal coordinate.
            if s1==s2:hsq=(dx1-dx2)**2*s1
            else:
                require(dx1==0 or dx2==0,'triangle sparse basis')
                hsq=dx1*dx1*s1+dx2*dx2*s2
            dy=tri[i][1]-tri[j][1]
            require(hsq+dy*dy==576,'triangle unit edge');triangle_norm_checks+=1
    report={'status':'PASS','prime':p,'quadratic_residues':len(roots),'residue_conic_rows':len(got),'residue_direction_checks':direction_checks,'quotient_colour_checks':colour_checks,'distance24_factor_rows':len(rows),'distance24_squarefree_classes':len(rad),'distance24_physical_directions':physical_direction_checks,'triangle_norm_checks':triangle_norm_checks,'malformed_certificate_rejections':0,'native_solver_calls':0}
    if controls:
        bad=[]
        def reject(label,mut):
            try:audit(mut,False)
            except (ValueError,KeyError,TypeError,ZeroDivisionError):bad.append(label)
            else:raise ValueError('accepted malformed '+label)
        import copy
        z=copy.deepcopy(data);z['prime']=5;reject('wrong prime',z)
        z=copy.deepcopy(data);z['weights'][2]=0;reject('wrong radical weight',z)
        z=copy.deepcopy(data);z['colour_pairs_in_r_units'][0]=[0,2];reject('wrong colour pair',z)
        z=copy.deepcopy(data);z['residue_conic_rows'].pop();reject('missing conic row',z)
        z=copy.deepcopy(data);z['residue_conic_rows'][0][4]=[0];reject('bad conic delta',z)
        z=copy.deepcopy(data);z['distance24_factor_rows'][8][1]+=1;reject('bad square factor',z)
        z=copy.deepcopy(data);z['distance24_triangle'][2][1]=11;reject('nonunit triangle',z)
        z=copy.deepcopy(data);z['extra']=1;reject('extra field',z)
        report['malformed_certificate_rejections']=len(bad)
        require(len(bad)==8,'control count')
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default=str(Path(__file__).with_name('certificate.json')));ap.add_argument('--check-expected',action='store_true');ap.add_argument('--controls',action='store_true');a=ap.parse_args()
    start=time.monotonic();raw=Path(a.certificate).read_bytes();data=json.loads(raw);report=audit(data,a.controls);report['certificate_bytes']=len(raw);report['certificate_sha256']=hashlib.sha256(raw).hexdigest();report['seconds']=time.monotonic()-start
    if a.check_expected:
        expected=json.loads(Path(__file__).with_name('expected.json').read_text())
        stable={k:v for k,v in report.items() if k!='seconds'};require(stable==expected,'expected mismatch')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
