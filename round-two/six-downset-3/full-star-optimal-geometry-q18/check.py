"""Exact q18 optimal-set geometry verifier, standard library only.

All actual entries, perturbation coordinates and the incidence determinant
are checked anew. PSD uses the EXPLICIT published same-carrier theorem
10296 through a fully checked norm bridge, not new factors. Its proof is
an ordinary external mathematical dependency; it is not rechecked here.
The producer is never imported. See PROOF.md for the unformalized bridges.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json

BASE=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok:raise ValueError(msg)


def carrier():
    # A separate core/outside census, followed by complete downclosure checks.
    X=[]
    for c in range(8):
        allowed=range(1,3) if c==0 else (0,1) if c.bit_count() in (1,2) else (0,)
        for r in allowed:
            for T in combinations(range(18),r):
                if c==6 and r==1 and T[0]<9:continue
                X.append(c+sum(1<<(t+3) for t in T))
    X.sort();require(len(X)==277 and X[0]==1,'fresh proper carrier N278')
    require(all(B in X or B==0 for A in X for B in (A^(1<<j) for j in range(21) if A&(1<<j))),
            'entire fresh downward closure')
    O=[(A&7,((A>>3)&511).bit_count(),(A>>12).bit_count()) for A in X]
    K=sorted(set(O));require(len(K)==23,'all fresh physical member orbits')
    return X,O,K


def original_matrix(data,X,O):
    n=len(X);D=data['free_original_entry_denominator']
    require(type(D) is int and D>0,'exact positive original matrix denominator')
    keys=sorted({tuple(sorted((O[i],O[j]))) for i in range(n) for j in range(i+1,n)
                 if not X[i]&X[j] and X[i]!=1 and X[j]!=1})
    require(data['free_original_entry_orbit_keys']==[[list(x) for x in key] for key in keys]
            and len(keys)==143,'EVERY actual free orbit in canonical order, no missing/extras')
    values=data['free_original_entry_numerators']
    require(len(values)==143 and all(type(x) is int for x in values),'all143 exact original coefficients')
    weights=dict(zip(keys,values));a=X.index(1);S=[i for i,A in enumerate(X) if A&1]
    C=[[0]*n for _ in X]
    for i,A in enumerate(X):
        for j,B in enumerate(X):
            C[i][j]=(57*D if A==B else -D if A&B else
                     0 if A==1 or B==1 else weights[tuple(sorted((O[i],O[j])))])
    for i,A in enumerate(X):
        if A&1:continue
        C[i][a]=C[a][i]=-sum(C[i][j] for j in S if j!=a)
    require(all(C[i][j]==C[j][i] and (A!=B or C[i][j]==57*D)
                and (A==B or not A&B or C[i][j]==-D)
                for i,A in enumerate(X) for j,B in enumerate(X)), 'ALL original symmetry/diagonal/support positions')
    require(all(sum(C[i][j] for j in S)==0 for i in range(n)), 'ALL original maximum-star kernel rows')
    U=[[278*D*int(i==j)-D-C[i][j] for j in range(n)] for i in range(n)]
    return C,U,D,S


def actual_completion(C,D,X,S,tau):
    """Return every actual entry of 220M, represented over D."""
    rows=list(map(sum,C));n=len(X);actual=[0]+X
    L=[[D+sum(rows)]+[D-r for r in rows]]+[
        [D-rows[i]]+[D+x for x in C[i]] for i in range(n)]
    M=[[v-58*D*int(i==j) for j,v in enumerate(row)] for i,row in enumerate(L)]
    require(all(sum(row)==220*D for row in M),'EVERY actual stochastic row')
    require(all(M[i][j]==M[j][i] and (not A&B or M[i][j]==0)
                for i,A in enumerate(actual) for j,B in enumerate(actual)),
            'ENTIRE actual symmetry and disjointness support, including empty loop')
    require(all(M[i][j]>=tau*D for i,A in enumerate(actual) for j,B in enumerate(actual)
                if not A&B),'EVERY allowed actual entry floor')
    h=[0]+[int(A&1!=0) for A in X]
    f=[278*v-58 for v in h]
    require(all(sum(L[i][j]*f[j] for j in range(278))==0 for i in range(278)),
            'ALL actual centered-star lower-kernel rows')
    U=[[278*D*int(i==j)-D-C[i][j] for j in range(277)] for i in range(277)]
    ur=list(map(sum,U))
    lifted=[[sum(ur)]+[-r for r in ur]]+[[-ur[i]]+U[i] for i in range(277)]
    require(all(lifted[i][j]==278*D*int(i==j)-L[i][j]
                for i in range(278) for j in range(278)),
            'ALL actual upper-congruence positions')
    return M


def bareiss_determinant(A):
    """Exact fraction-free determinant; no floating rank inference."""
    A=[row[:] for row in A];n=len(A);sign=1;previous=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        require(pivot is not None,'nonzero incidence pivot')
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=p*A[i][j]-A[i][k]*A[k][j]
                require(v%previous==0,'EVERY exact Bareiss division')
                A[i][j]=v//previous
            A[i][k]=0
        previous=p
    return sign*A[-1][-1]


def verify(data,parent,comparison):
    require((data['actual_agent'],data['role'],data['q'],data['k'],data['actual_empty_N'],data['s'])==
            ('six-downset-3','researcher',18,9,278,58),'exact original carrier and actual authorship')
    require(data['real_tau_interval']==parent['parent_real_tau_interval']==['0','1/128'],
            'fixed closed REAL interval')
    require(parent['parent_source_commit']=='40c0527d02729a26498418bcbdf273ca9b2c1a95'
            and parent['parent_graph_ref']=='bafkreia6zoi2ypjf2xs2jsdzsoz43vbk6ujexvpagj6x32cryqbthrashq'
            and parent['PSD_statement_is_an_explicit_published_mathematical_dependency_not_rechecked_here'] is True
            and data['PSD_proof_uses_explicit_published_10296_dependency_not_new_factors'] is True,
            'explicit same-carrier PUBLISHED theorem dependency, not a new PSD proof')
    old=comparison['comparison_free_numerators']
    require(comparison['comparison_free_denominator']==16384 and len(old)==143
            and hashlib.sha256(json.dumps(old,separators=(',',':')).encode()).hexdigest()==
            '14cca17e8c9dcf4be01d7abe5700745fc120ea782e84bcc73d25b7df176a4e7d',
            'entire fixed old signed comparison table')
    X,O,_=carrier();C1,_,D,S=original_matrix(parent,X,O)
    require(D==148635648,'fixed common parent endpoint denominator')
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(21)]
    require(stars==[58,49,49]+[23]*9+[24]*9,'EVERY original point-star count')
    keys=[tuple(map(tuple,key)) for key in parent['free_original_entry_orbit_keys']]
    require(data['free_original_entry_orbit_keys']==parent['free_original_entry_orbit_keys'],
            'ALL143 perturbation orbits in independently reconstructed original order')
    require(len(data['free_original_perturbation_numerators'])==143
            and all(type(v) is int for v in data['free_original_perturbation_numerators']),
            'all143 exact integer perturbation coefficients')
    old_data=dict(parent,free_original_entry_numerators=[x*(D//16384) for x in old])
    Cold,_,_,_=original_matrix(old_data,X,O)
    # Independently expanded published affine recipe; no producer imports.
    terms={tuple(sorted((u,v))):(c,k) for u,v,c,k in [
        ((0,2,0),(0,0,2),-F(43503,786432),-F(1,48)),
        ((0,2,0),(6,0,1),-F(999,589824),-F(1,36)),
        ((0,0,2),(0,0,2),-F(14527,1376256),-F(1,84)),
        ((0,1,0),(0,0,1),F(476335,2654208),F(41,81)),
        ((0,1,0),(7,0,0),-F(20819,147456),-F(1,9))]}
    start=[];end=[]
    for key,v in zip(keys,old):
        c,k=terms.get(key,(F(0),F(0)))
        start.append(F(v,16384)+c);end.append(F(v,16384)+c+k/128)
    require(all((v*D).denominator==1 for v in start+end)
            and [int(v*D) for v in end]==parent['free_original_entry_numerators'],
            'EVERY parent endpoint coefficient bound to its explicit published line')
    C0,_,_,_=original_matrix(dict(parent,free_original_entry_numerators=[int(v*D) for v in start]),X,O)
    emptyold=[D-sum(row) for row in Cold]
    bad=[i for i,A in enumerate(X) if not A&1 and emptyold[i]<0];B=set(bad)
    require(len(bad)==81 and {O[i] for i in bad}=={(0,2,0),(0,0,2),(6,0,1)},
            'ALL81 bad original nonstar rows')
    d=-sum(emptyold[i] for i in bad);ell=D+sum(map(sum,Cold))-58*D
    require(F(d,D)==F(2497887,16384) and F(ell,D)==F(2021552,16384),
            'actual original deficit and empty-loop capacity')
    free=[(i,j) for i,A in enumerate(X) for j in range(i+1,277)
          if not A&X[j] and A!=1 and X[j]!=1]
    NN=[(i,j) for i,j in free if not X[i]&1 and not X[j]&1]
    NS=[(i,j) for i,j in free if (X[i]&1)!=(X[j]&1)]
    classes={k:[(i,j) for i,j in NN if int(i in B)+int(j in B)==k] for k in range(3)}
    require(len(free)==29802 and len(NS)==10280 and len(NN)==19522
            and {k:len(v) for k,v in classes.items()}=={0:7885,1:9009,2:2628},
            'full independent REAL coordinates and every NN boundary class')

    # Build the perturbation from individual physical pairs, then bind ALL
    # submitted orbit coefficients; the compact table is untrusted data.
    eta=F(data['eta']);HD=data['perturbation_denominator']
    require(eta==F(1,2**60) and HD==162,'fixed exact interior scale and common coefficient denominator')
    H=[[0]*277 for _ in X];expected={}
    for i,j in free:
        if not X[i]&1 and not X[j]&1:
            k=int(i in B)+int(j in B)
            if k==2:
                if {O[i],O[j]}=={(0,2,0),(0,0,2)}:v=F(7,18)
                elif {O[i],O[j]}=={(0,2,0),(6,0,1)}:v=F(7,9)
                elif O[i]==O[j]==(0,0,2):v=-F(1,3)
                else:v=-F(1)
            elif k==0:v=-F(7804,81) if {O[i],O[j]}=={(0,1,0),(0,0,1)} else F(1)
            else:v=F(0)
        else:v=-F(1) if {O[i],O[j]}=={(0,1,0),(7,0,0)} else F(0)
        require((v*HD).denominator==1,'exact denominator of each original free coefficient')
        H[i][j]=H[j][i]=int(v*HD)
        key=tuple(sorted((O[i],O[j])))
        require(key not in expected or expected[key]==H[i][j],'literal orbit constancy')
        expected[key]=H[i][j]
    require([expected[key] for key in keys]==data['free_original_perturbation_numerators'],
            'EVERY submitted perturbation coefficient equals the independent physical recipe')
    a=X.index(1)
    for i,A in enumerate(X):
        if not A&1:H[i][a]=H[a][i]=-sum(H[i][j] for j in S if j!=a)
    require(all(H[i][j]==H[j][i] and (i!=j or H[i][j]==0)
                and (not A&X[j] or H[i][j]==0) for i,A in enumerate(X) for j in range(277))
            and all(sum(H[i][j] for j in S)==0 for i in range(277)),
            'EVERY perturbation symmetry, support, diagonal and star-kernel position')
    require(all(sum(H[i][j] for j in range(277))==0 for i in bad)
            and sum(H[i][j] for i,j in classes[0])==0 and sum(map(sum,H))==0
            and all(H[i][j]==0 for i,j in classes[1]),
            'ALL81 bad-degree equalities, good mass, loop and cross-boundary conservation')
    l1bad=F(sum(abs(H[i][j]) for i,j in classes[2]),HD)
    l1good=F(sum(abs(H[i][j]) for i,j in classes[0]),HD)
    l1anchored=F(sum(abs(H[i][j]) for i,j in NS),HD)
    require([l1bad,l1good,l1anchored]==[F(1512),F(15608),F(9)]
            and [l1bad,l1good,l1anchored]==[F(data['claimed_bad_bad_free_l1']),
            F(data['claimed_good_good_free_l1']),F(data['claimed_anchored_free_l1'])],
            'ENTIRE original independent-coordinate absolute masses')
    norm=l1bad+l1good+2*l1anchored;entry=2*(l1bad+l1good)+l1anchored
    require(norm==F(data['claimed_proper_operator_coefficient_bound'])==17138
            and entry==F(data['claimed_actual_entry_coefficient_bound'])==34249,
            'proper operator and actual-entry bounds from ALL original generators')
    # Check every literal actual generator used by the analytic norm/entry
    # estimate, with no quotient-only scaling or unexamined lift position.
    actual=[0]+X;generator_count=0
    NNset=set(NN)
    for i,j in free:
        if (i,j) in NNset:
            pos={(i+1,j+1):1,(j+1,i+1):1,(0,i+1):-1,(i+1,0):-1,
                 (0,j+1):-1,(j+1,0):-1,(0,0):2};maximum=2
        else:
            n=j if X[i]&1 else i;s=i if X[i]&1 else j
            pos={(n+1,s+1):1,(s+1,n+1):1,(n+1,a+1):-1,(a+1,n+1):-1,
                 (0,s+1):-1,(s+1,0):-1,(0,a+1):1,(a+1,0):1};maximum=1
        require(max(map(abs,pos.values()))==maximum
                and all(not actual[r]&actual[c] for r,c in pos)
                and all(sum(v for (r,c),v in pos.items() if r==row)==0
                        for row in {r for r,c in pos}),
                'EVERY literal original generator actual support, rows and entry bound')
        generator_count+=1
    rowsH=list(map(sum,H))
    AH=[[sum(rowsH)]+[-r for r in rowsH]]+[[-rowsH[i]]+H[i] for i in range(277)]
    require(all(abs(v)<=entry*HD for row in AH for v in row),
            'FULL actual perturbation satisfies the coordinate entry estimate')
    require(F(sum(v*v for row in H for v in row),HD**2)<=norm**2,
            'second FULL-original Frobenius check of the operator estimate')
    require(F(parent['parent_proper_C_starperp_and_U_floor_for_ALL_real_tau'])==
            F(data['published_parent_C_starperp_and_U_uniform_floor'])==F(1,128)
            and F(data['derived_C_starperp_and_U_uniform_floor'])==F(1,256)
            and norm*eta<F(1,256),'explicit paid SAME-carrier spectral-norm transfer inequality')
    require(entry*eta<F(1,2*D) and 9*eta<F(1,2*D),
            'uniform exact entry protection inequalities')

    common=lcm(D,(eta/HD).denominator);scale=common//D;hscale=int((eta/HD)*common)
    forced={(0,0)}|{(0,i+1) for i in bad}|{(i+1,0) for i in bad}
    abc=X.index(7);optional={(0,abc+1),(abc+1,0)}
    require(len(forced)==data['claimed_forced_ordered_entry_positions']==163,
            'ALL and ONLY optimality-forced original ordered entry positions')
    require(AH[0][abc+1]==AH[abc+1][0]==9*HD and AH[0][a+1]==-9*HD
            and all(AH[i][j]==0 for i,j in forced),'literal newly strict abc entry and preserved forced entries')
    endpoint_records={};hashes={}
    for tau,C in ((F(0),C0),(F(1,128),C1)):
        M=actual_completion(C,D,X,S,tau)
        equality={(i,j) for i,A in enumerate(actual) for j,Bmask in enumerate(actual)
                  if not A&Bmask and M[i][j]==tau*D}
        require(equality==forced|optional,'ENTIRE published endpoint equality-position classification')
        others=[M[i][j]-tau*D for i,A in enumerate(actual) for j,Bmask in enumerate(actual)
                if not A&Bmask and (i,j) not in equality]
        require(min(others)>=1,'EVERY other original parent entry has C-unit surplus at least1/D')
        newC=[[scale*C[i][j]+hscale*H[i][j] for j in range(277)] for i in range(277)]
        newM=actual_completion(newC,common,X,S,tau)
        require(all(newM[i][j]-scale*M[i][j]==hscale*AH[i][j]
                    for i in range(278) for j in range(278)),
                'ENTIRE original new actual matrix equals the literal lifted perturbation')
        neweq={(i,j) for i,A in enumerate(actual) for j,Bmask in enumerate(actual)
               if not A&Bmask and newM[i][j]==tau*common}
        require(neweq==forced,'ALL remaining equality entries are forced, exactly163')
        surplus=min(F(newM[i][j],common)-tau for i,A in enumerate(actual) for j,Bmask in enumerate(actual)
                    if not A&Bmask and (i,j) not in forced)
        require(surplus==9*eta,'EVERY unforced actual entry has exact uniform C-unit surplus9eta')
        repair={(i,j):F(newC[i][j],common)-F(Cold[i][j],D) for i,j in NN}
        require(all(repair[i,j]<=-eta for i,j in classes[2])
                and all(repair[i,j]>=eta for i,j in classes[0])
                and all(repair[i,j]==0 for i,j in classes[1]),
                'ALL2628 bad repairs strictly negative, ALL7885 good repairs strictly positive, no cross changes')
        P=sum(max(v,F(0)) for v in repair.values());T=sum(max(-v,F(0)) for v in repair.values())
        require(P==F(476335,32768)+41*tau and T==F(d,2*D)+F(81,2)*tau,
                'ENTIRE original NN mass and universal dual equality accounting')
        require(all(sum(repair[min(i,j),max(i,j)] for j in range(277)
                        if (min(i,j),max(i,j)) in repair)==F(emptyold[i],D)-tau for i in bad),
                'EACH original affine-hull bad-degree equation')
        endpoint_records[str(tau)]={'all_actual_positions':278**2,
            'allowed_ordered_positions':sum(not A&Bmask for A in actual for Bmask in actual),
            'parent_nonforced_nonabc_C_surplus_at_least':str(F(1,D)),
            'forced_ordered_entries':len(neweq),'unforced_C_surplus_minimum':str(surplus),
            'unforced_M_surplus_minimum':str(surplus/220),'NN_positive_edges':7885,
            'NN_negative_edges':2628,'NN_zero_edges':9009,'optimal_mass':str(P),'decreasing_mass':str(T)}
        hashes[str(tau)+'_interior_actual_220M_integer_matrix']=hashlib.sha256(
            json.dumps(newM,separators=(',',':')).encode()).hexdigest()

    # A determinant witness is checked on the ENTIRE original81-row
    # unsigned incidence matrix, not on a three-orbit quotient.
    witness=data['bad_incidence_rank_witness_edges'];masks=[X[i] for i in bad]
    require(len(witness)==81 and len({tuple(e) for e in witness})==81
            and all(len(e)==2 and e[0]<e[1] and e[0] in masks and e[1] in masks
                    and not e[0]&e[1] for e in witness),'ALL81 distinct selected original bad/bad edges')
    incidence=[[int(A in e) for e in witness] for A in masks]
    det=bareiss_determinant(incidence)
    require(abs(det)==data['bad_incidence_absolute_determinant']==2,
            'exact determinant2 proves FULL81 independent degree equations')
    triangle=data['odd_triangle_masks'];tree={tuple(e) for e in witness[:80]};reach={masks[0]}
    for _ in range(81):
        reach|={v for u,v in tree if u in reach}|{u for u,v in tree if v in reach}
    require(reach==set(masks) and len(triangle)==3 and len(set(triangle))==3
            and all(tuple(sorted((triangle[i],triangle[j]))) in {tuple(e) for e in witness}
                    for i in range(3) for j in range(i+1,3)),
            'original connected spanning tree and odd triangle, independent structural rank argument')
    dimension=(len(classes[2])-81)+(len(classes[0])-1)+len(NS)
    require(dimension==data['claimed_affine_dimension']==20711,
            'full REAL optimal equality affine-space dimension')
    return {'actual_agent':'six-downset-3','role':'researcher','actual_empty_N':278,'s':58,
        'all21_original_star_counts':stars,'real_tau_interval':['0','1/128'],
        'eta':str(eta),'perturbation_denominator':HD,'new_common_endpoint_denominator':common,
        'full_affine_star_coordinates':generator_count,'all_original_NN_class_counts':{str(k):len(v) for k,v in classes.items()},
        'anchored_trade_coordinates':len(NS),'bad_incidence_rows':81,'bad_incidence_exact_determinant':det,
        'optimal_equality_affine_dimension':dimension,'endpoint_original_position_checks':endpoint_records,
        'perturbation_original_free_absolute_masses':{'bad_bad':str(l1bad),'good_good':str(l1good),'anchored':str(l1anchored)},
        'proper_operator_perturbation_upper_bound':str(norm*eta),
        'actual_C_unit_entry_perturbation_upper_bound':str(entry*eta),
        'all_real_tau_unforced_M_entry_surplus_at_least':str(9*eta/220),
        'all_real_tau_NN_repair_sign_margin_at_least':str(eta),
        'PSD_statement_is_CONDITIONAL_on_exact_published_parent_theorem':True,
        'published_parent_graph_ref':parent['parent_graph_ref'],'published_parent_source_commit':parent['parent_source_commit'],
        'parent_uniform_proper_floor':'1/128','derived_uniform_proper_floor':'1/256',
        'ordinary_affine_hull_relative_interior_and_spectral_transfer_bridges_unformalized':True,
        'independent_reviewer_verdict':'UNREVIEWED','whole_original_new_matrix_SHA256':hashes}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--geometry',type=Path,default=BASE/'GEOMETRY.json')
    ap.add_argument('--parent-data',type=Path,default=BASE/'BASE-DATA.json')
    ap.add_argument('--comparison',type=Path,default=BASE/'COMPARISON.json');ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();result=verify(json.loads(args.geometry.read_bytes()),
        json.loads(args.parent_data.read_bytes()),json.loads(args.comparison.read_bytes()))
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode();args.out.write_bytes(raw)
    print(json.dumps({'completed':True,'dimension':result['optimal_equality_affine_dimension'],
        'exact_incidence_determinant':result['bad_incidence_exact_determinant'],
        'record_SHA256':hashlib.sha256(raw).hexdigest(),'PSD_dependency_not_rechecked':True},sort_keys=True))


if __name__=='__main__':main()
