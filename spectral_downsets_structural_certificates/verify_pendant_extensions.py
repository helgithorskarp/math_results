#!/usr/bin/env python3
"""Exact full matrices, complete extension blocks, credited baseline and controls."""
import argparse
from contextlib import redirect_stdout
from fractions import Fraction as F
from io import StringIO
import json
from pathlib import Path

import certificates as base
import clique_centers
import friendship
import pendant_extensions as build
from pendant_extension_identities import certificates as identities
from verify import check, psd_ldl, require
from verify_clique_centers import matvec, basis_rank, core_buffer, fingerprint
from verify_friendship import main as friendship_baseline
from verify_two_centers import maximum_intersecting_families


def relabel(family, core, permutation):
    rename = lambda a: sum(1 << permutation[i] for i in range(len(permutation)) if a >> i & 1)
    result = sorted(rename(a) for a in family)
    positions = {rename(a):i for i,a in enumerate(family[1:])}
    return result, [[core[positions[a]][positions[b]] for b in result[1:]] for a in result[1:]]


def independent_extension(family, core, center):
    """Literal block entries, without the production constructor or parameter helper."""
    n = max(family).bit_length(); bit = 1 << center; new = 1 << n
    old = {a:i for i,a in enumerate(family[1:])}
    result = sorted(family+[new, bit | new])
    a,beta,chi = F(n*(len(family)-1-n)-1,n*(len(family)-1-n)), 1-F(1,len(family)-1-n), 1+F(n,len(family)-1-n)
    tau,h,q = 1+F(1,len(family)-1-n), 1+F(1,n), 1-F(n,len(family)-1-n)
    def entry(x,y):
        if x==y: return F(n)
        if x & y: return F(-1)
        if x==new or y==new:
            other = y if x==new else x
            return (h if other & bit else q)-1
        if x==(bit | new) or y==(bit | new): return tau-1
        if bool(x & bit) != bool(y & bit): return a*(core[old[x]][old[y]]+1)-1
        if x & bit: return F(-1)
        return beta*(core[old[x]][old[y]]+1)-1
    # chi is used only on the diagonal, whose independent value is n.
    require(beta*n+chi==n+1, 'Independent diagonal clearing failed')
    return result, [[entry(x,y) for y in result[1:]] for x in result[1:]]


def extension_blocks(old_family, old_core, family, core, center):
    n = max(old_family).bit_length(); b = len(old_family)-1-n
    m = len(core); old = old_family[1:]; current = family[1:]
    index = {a:i for i,a in enumerate(current)}
    S = [i for i,a in enumerate(old) if a >> center & 1]
    B = [i for i,a in enumerate(old) if not a >> center & 1]
    pairs = [(i,group[-1]) for group in (S,B) for i in group[:-1]]
    def vector(masks): return [F(a in masks) for a in current]
    z_basis = []
    for i,j in pairs:
        v = [F(0)]*m; v[index[old[i]]]=F(1); v[index[old[j]]]=F(-1)
        z_basis.append(v)
    spoke,single = (1 << center) | (1 << n), 1 << n
    constants = [vector([old[i] for i in S]+[spoke]), vector([old[i] for i in B]+[single]),
                 vector([spoke]), vector([single])]
    require(basis_rank(z_basis+constants)==m, 'Extension decomposition incomplete')
    for v in z_basis:
        image = matvec(core,v)
        require(all(sum(w[i]*image[i] for i in range(m))==0 for w in constants),
                'Standard and constant blocks not orthogonal invariant blocks')
    images = [matvec(core,v) for v in constants]
    gram = [[sum(v[i]*w[i] for i in range(m)) for w in images] for v in constants]
    require(gram==[[F(0)]*4,[F(0)]*4,[F(0),F(0),F(n),F(-1)],
                   [F(0),F(0),F(-1),F(n)]], 'Constant quotient differs')
    require(images[:2]==[[F(0)]*m]*2, 'Two raw kernels fail')
    psd_ldl([[F(n),F(-1)],[F(-1),F(n)]])
    def differences(A):
        return [[A[i][k]-A[j][k]-A[i][l]+A[j][l] for k,l in pairs] for i,j in pairs]
    retained = [[core[index[x]][index[y]] for y in old] for x in old]
    require(psd_ldl(differences(retained))==len(pairs), 'Standard block not positive definite')
    alpha = 1-F(1,n*b); margin = min(1+F(1,b), F(1,n)+F(n,b))
    remainder = [[retained[i][j]-alpha*old_core[i][j]-margin*int(i==j)
                  for j in range(len(old))] for i in range(len(old))]
    psd_ldl(differences(remainder))
    Y = [[old_core[i][j]+1 for j in B] for i in B]
    require(all(sum(row)==b and min(row)>=0 for row in Y), 'Outside block is not nonnegative regular')
    psd_ldl([[F(b*int(i==j))-Y[i][j] for j in range(b)] for i in range(b)])
    require(psd_ldl(core)==m-2, 'Raw extension rank failed')
    core_buffer(core,m+1,F(1))
    return dict(old_n=n,old_b=b,new_N=m+1,complete_basis_dimension=m,
                standard_dimension=len(pairs),standard_margin=str(margin),constant_rank=2)


def seed_check(family,core,center):
    C,n,_,_ = build.validate_seed(family,core,center)
    rank = psd_ldl(C); core_buffer(C,len(family),F(1))
    require(check(family,base.lift(C,n),n,upper=True)==rank+1, 'Seed lift rank differs')
    return dict(n=n,N=len(family),center=center,core_rank=rank,core_sha256=fingerprint(C))


def final_check(family,core,center,description):
    repaired,data = build.finish(family,core,center)
    n = max(family).bit_length(); N = len(family); m=N-1; colors=data['colors']
    require(all(colors[i]!=colors[j] for i,a in enumerate(family[1:])
                for j,b in enumerate(family[1:]) if i!=j and a & b), 'Detecting partition not proper')
    star = [F(bool(a & (1 << center))) for a in family[1:]]
    require(sorted(colors[i] for i,x in enumerate(star) if x)==list(range(n)),
            'Center star does not use every color')
    P = [[F(n*int(c==d)-1) for d in colors] for c in colors]
    psd_ldl(P)
    require(matvec(P,star)==[0]*m and data['extra_quotient']>0,
            'Partition does not preserve/detect the required raw kernels')
    require(sum(map(sum,P))==data['extra_quotient'], 'Partition quotient differs')
    counts=[colors.count(c) for c in range(n)]
    beta=max(0,n*max(counts)-N); epsilon=F(1,2*(beta+1))
    independent=[[(1-epsilon)*core[i][j]+epsilon*P[i][j] for j in range(m)] for i in range(m)]
    require(repaired==independent and data['beta']==beta and data['epsilon']==epsilon,
            'Mixture entries or parameters differ')
    require(psd_ldl(repaired)==m-1 and matvec(repaired,star)==[0]*m, 'Final core rank/kernel failed')
    core_buffer(repaired,N,F(1,2))
    matrix=base.lift(repaired,n)
    closed=[[F(0)]*N for _ in range(N)]
    for i in range(m):
        for j in range(m): closed[i+1][j+1]=(independent[i][j]+1-n*int(i==j))/(N-n)
        closed[0][i+1]=closed[i+1][0]=(1-sum(independent[i]))/(N-n)
    closed[0][0]=(1-n+sum(map(sum,independent)))/(N-n)
    require(matrix==closed, 'Full closed lift differs')
    require(check(family,matrix,n)==N-1, 'Final Hoffman rank failed')
    require(psd_ldl([[F(i==j)-matrix[i][j] for j in range(N)] for i in range(N)])==N-1,
            'Final cap/simple top failed')
    require(all(matrix[i][j]>=0 for i in range(N) for j in range(N) if i!=j),
            'Negative off-diagonal weight')
    require(min(matrix[0][1:])>=F(1,2*(N-n)), 'Empty weights below proved margin')
    maximum_stars=[i for i in range(n) if sum(bool(a & (1 << i)) for a in family)==n]
    require(maximum_stars==[center], 'Center star is not unique')
    census=None
    if N<=20:
        maxima=maximum_intersecting_families(family)
        require(maxima=={tuple(a for a in family if a & (1 << center))}, 'Full equality census differs')
        census=len(maxima)
    result=dict(description,N=N,s=n,raw_core_rank=m-2,L_rank=N-1,upper_rank=N-1,
                recolored=data['recolored'],partition_sizes=counts,partition_quotient=data['extra_quotient'],
                beta=beta,epsilon=str(epsilon),maximum_family_census=census,matrix_sha256=fingerprint(matrix))
    return result,(family,matrix,n)


def inherited_triangle(n,family):
    """Independently counted deleted quotient; compare the prior exact cap test."""
    import deletions
    leaf_edges=[(i,j) for i in range(n) for j in range(i+1,n)
                if not ((1 << i)|(1 << j)) in family]
    leaf_edges.sort(key=lambda e:(1 << e[0])|(1 << e[1]))
    edges=len(leaf_edges); p=n-3
    g=deletions.deletion_data(n,leaf_edges)['gram']
    cross=[i for i,e in enumerate(leaf_edges) if bool(1 in e or 2 in e)]
    other=[i for i in range(edges) if i not in cross]
    require(len(cross)==2*p and len(other)==p*(p-1)//2, 'Deleted orbit sizes differ')
    expected=[[F(4*p,p+1),F(-3*(p-1),p+1)],[F(-12,p+1),F(12,p+1)]]
    for i in cross:
        require([sum(g[i][j] for j in group) for group in (cross,other)]==expected[0],
                'Deleted cross-orbit row count differs')
    if other:
        for i in other:
            require([sum(g[i][j] for j in group) for group in (cross,other)]==expected[1],
                    'Deleted other-orbit row count differs')
    _,scalar=deletions.cap_test(n,leaf_edges)
    formula=F(2*p*(p+2)*(p+3)*(p+5),p**4+12*p**3+46*p*p+72*p+49)
    require(scalar==formula and (p<2 or scalar>1), 'All-order inherited failure formula differs')
    return dict(n=n,p=p,inherited_scalar=str(scalar),outside_strict_inherited_domain=scalar>=1)


def controls():
    D,M,s=base.uniform_rank_two_certificate(3); C=base.extract_core(M,s)
    calls=[lambda:build.clique_pendants(2,1),lambda:build.clique_pendants(True,1),
           lambda:build.clique_pendants(3,0),lambda:build.clique_pendants(3,True),
           lambda:build.clique_pendants(3,1,-1),lambda:build.clique_pendants(3,1,True),
           lambda:build.friendship_pendants(0,1),lambda:build.friendship_pendants(2.0,1),
           lambda:build.clique_center_pendants(2,3,1),lambda:build.clique_center_pendants(3,1,1),
           lambda:build.certificate(D,C,3,1),lambda:build.certificate(D,C,False,1),
           lambda:build.certificate(D,C,0,1.5),lambda:build.certificate(tuple(reversed(D)),C,0,1),
           lambda:build.certificate(D[:-1],C,0,1),lambda:build.certificate([0,1,2,4],[[F(0)]*3]*3,0,1),
           lambda:build.certificate([a << 1 for a in D],C,1,1)]
    for label in ('diagonal','symmetry','floating','centering','sign'):
        bad=[row[:] for row in C]
        if label=='diagonal': bad[0][0]+=1
        if label=='symmetry': bad[0][1]+=1
        if label=='floating': bad[0][0]=float(bad[0][0])
        if label=='centering': bad[0][1]+=1; bad[1][0]+=1
        if label=='sign': bad[0][1]=bad[1][0]=F(-2)
        calls.append(lambda bad=bad:build.certificate(D,bad,0,1))
    for call in calls:
        try: call()
        except ValueError: pass
        else: raise ValueError('Malformed or out-of-domain input accepted')
    for A in ([[F(-1)]],[[F(0),F(1)],[F(1),F(1)]]):
        try: psd_ldl(A)
        except ValueError: pass
        else: raise ValueError('Invalid PSD control accepted')
    require(build.validate_seed(tuple(D),tuple(tuple(row) for row in C),0)[1]==3,
            'Valid tuple input rejected')
    unshifted=build.clique_pendants(3,2); shifted=build.clique_pendants(3,2,7)
    require(shifted==([a << 7 for a in unshifted[0]],unshifted[1],unshifted[2]), 'Shift API differs')
    return dict(domain_inputs_rejected=len(calls),PSD_controls=2,tuple_and_shift_checked=True,
                seed_PSD_is_caller_hypothesis=True,nonexistence_claim=False)


def run():
    symbolic=identities()
    stream=StringIO()
    with redirect_stdout(stream): friendship_baseline()
    reproduced=json.loads(stream.getvalue())
    published=json.loads(Path(__file__).with_name('friendship_expected.json').read_text())
    require(reproduced==published, 'Complete published friendship baseline differs')
    inputs=[]
    for t in range(3,7):
        D,M,s=base.uniform_rank_two_certificate(t)
        inputs.append((dict(kind='clique',seed=[t]),D,base.extract_core(M,s),0,range(1,4),build.clique_pendants))
    for k in range(1,4):
        D,M,s=friendship.certificate(k)
        inputs.append((dict(kind='friendship',seed=[k]),D,base.extract_core(M,s),2*k,range(1,4),build.friendship_pendants))
    for r,t in ((3,2),(3,4),(4,2),(4,4),(5,2),(5,6)):
        inputs.append((dict(kind='clique_center',seed=[r,t]),clique_centers.family(r,t),
                       clique_centers.core(r,t),0,range(1,3) if (r,t)!=(5,6) else [2],build.clique_center_pendants))
    seeds=[]; stages=[]; cases=[]; triangle=[]
    for description,D,C,center,counts,wrapper in inputs:
        seeds.append(dict(description,**seed_check(D,C,center)))
        for u in range(1,max(counts)+1):
            oldD,oldC=D,C
            D,C,_=build.extend_once(D,C,center)
            require((D,C)==independent_extension(oldD,oldC,center), 'Literal extension entries differ')
            stages.append(dict(description,pendants=u,**extension_blocks(oldD,oldC,D,C,center)))
            if u in counts:
                item,certificate=final_check(D,C,center,dict(description,pendants=u)); cases.append(item)
                require(wrapper(*description['seed'],u)==certificate, 'Seed wrapper differs')
                if description==dict(kind='clique',seed=[3]): triangle.append(inherited_triangle(max(D).bit_length(),D))
    # A relabelled positive seed forces every original color class to have size two.
    seedD,seedM,seedS=base.uniform_rank_two_certificate(3)
    seedD,seedC,_=build.raw_extensions(seedD,base.extract_core(seedM,seedS),0,1)
    seedD,seedC=relabel(seedD,seedC,[0,2,3,1])
    description=dict(kind='generic_relabelled_balanced_partition',seed=[4])
    seeds.append(dict(description,**seed_check(seedD,seedC,0)))
    D,C,_=build.extend_once(seedD,seedC,0)
    require((D,C)==independent_extension(seedD,seedC,0), 'Relabelled literal entries differ')
    stages.append(dict(description,pendants=1,**extension_blocks(seedD,seedC,D,C,0)))
    item,_=final_check(D,C,0,dict(description,pendants=1)); cases.append(item)
    require(item['recolored'] and sorted(item['partition_sizes'])==[1,2,2,2,3],
            'Balanced partition recoloring branch not exercised')
    products=[]
    auxiliary=([0,1 << 5,1 << 6],[[F(0),F(1,2),F(1,2)],
              [F(1,2),F(0),F(1,2)],[F(1,2),F(1,2),F(0)]],1)
    for left,right,d in ((build.clique_pendants(3,1),build.clique_pendants(3,1,4),2),
                         (build.clique_pendants(3,2),auxiliary,1)):
        check(*left,upper=True); check(*right,upper=True)
        D,M,s=base.product_certificate([left,right]); N=len(D)
        require(check(D,M,s)==N-d, 'Tensor lower rank differs')
        require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,
                'Tensor cap/simple top differs')
        products.append(dict(N=N,s=s,L_rank=N-d,eligible_stars=d,matrix_sha256=fingerprint(M)))
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,
                reproduced_friendship_baseline=published,seeds=seeds,extension_stages=stages,literal_cases=cases,
                products=products,triangle_inherited_comparison=triangle,input_controls=controls(),
                base_N_max=max(item['N'] for item in cases),full_census_cases=sum(item['maximum_family_census'] is not None for item in cases))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('pendant_extensions_expected.json').read_text())
        require(result==expected, 'Complete expected result differs')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__': main()
