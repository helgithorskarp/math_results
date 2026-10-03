"""Reader of exact certificates, independent of all discovery generators.

Only the pinned published original forms and two exact PSD algorithms are
imported after the complete public source closure has passed its hash gate.
The new dual vectors are treated as untrusted input and fully re-evaluated.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
import sourcecheck
PACKET_SOURCE=sourcecheck.check_bundle(HERE)
BASE=HERE/'ancestral/uniform-zero-cap-cutoff'
PIN='b783ede83b894ba80936d6d11ad25a7be2c437602234e23aa95ebc3d4c454cb5'
if hashlib.sha256((BASE/'SHA256SUMS').read_bytes()).hexdigest()!=PIN:
    raise ValueError('changed published whole-source manifest')
spec=importlib.util.spec_from_file_location('core7_reader_sourcecheck',BASE/'sourcecheck.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
SOURCE=gate.check_bundle(BASE)
sys.path.insert(0,str(BASE))
import reduce as r
require=r.require


def physical_energy(A,v):
    """Separate symmetric upper-triangle evaluation, no generator pair call."""
    n=len(A)
    require(len(v)==n and all(len(row)==n for row in A),'full original physical vector dimensions')
    return sum(A[i][i]*v[i]*v[i] for i in range(n))+2*sum(
        A[i][j]*v[i]*v[j] for i in range(n) for j in range(i+1,n))


def absence(packet):
    require([p['q'] for p in packet['absence']]==list(range(7,27)),
            'COMPLETE finite order coverage, no missing or duplicate q')
    rows=[]
    for row in packet['absence']:
        q,k=row['q'],row['k'];require(type(q) is int and type(k) is int and k==7,'exact intended deletion count')
        D=r.forms(q,k)
        zz=[F(x) for x in row['orientation_vector']]
        expected=[F(1-int(bool(c&1))-int(bool(c&2))-int(bool(c&4))+int(c.bit_count()>=2))
                  for c,_,_ in D['keys']]
        require(zz==expected,'ENTIRE original orientation vector, not a sign convention')
        orient=[physical_energy(D['C0'],zz)]+[physical_energy(D[n],zz) for n in ('Delta','Rb','Rc','B')]
        require(orient[0]==0 and orient[1]==F(row['orientation_delta'])>0 and orient[2:]==[0,0,0],
                'full original necessary kappa orientation, with no upper parameter bound')
        weights=[F(x) for x in row['positive_dual_weights']]
        require(len(weights)==len(row['planes'])>0 and all(x>0 for x in weights),'each dual weight strictly positive')
        decoded=[]
        for plane in row['planes']:
            endpoint=plane['endpoint'];require(endpoint in ('lower','cap'),'actual spectral endpoint')
            vv=[F(x) for x in plane['vector']]
            sign=1 if endpoint=='lower' else -1
            A=D['C0'] if endpoint=='lower' else D['U0']
            coeff=[physical_energy(A,vv)]+[sign*physical_energy(D[n],vv) for n in ('Delta','Rb','Rc','B')]
            require(coeff==[F(x) for x in plane['coefficients_constant_kappa_tb_tc_sigma']],
                    'EVERY original affine endpoint coefficient, both independent trades retained')
            decoded.append(coeff)
        total=[sum(w*c[j] for w,c in zip(weights,decoded)) for j in range(5)]
        require(total==[F(x) for x in row['whole_original_coefficients_sum']],
                'whole positive weighted dual equals all original coefficients')
        require(total[2:]==[0,0,0] and total[0]<0 and total[1]<=0,
                'BOTH independent trades and bc cancel, strict constant and all-kappa slope')
        rows.append({'q':q,'physical_keys':D['keys'],'physical_sizes':D['sizes'],
                     'orientation_coefficients':orient,'decoded_full_planes':decoded,
                     'positive_weights':weights,'entire_weighted_sum':total,
                     'whole_original_six_forms_sha256':r.exact.digest(r.encode({n:D[n] for n in r.NAMES}))})
    return {'all_real_kappa_tb_tc_sigma':True,'all_orders':list(range(7,27)),
            'all_original_cancellations_strict_constants_slopes_checked':True,'rows':rows,
            'scope_only_prescribed_original_face':True}


def psd(A,rank,message):
    first=r.schur_psd(A);second,digest,den=r.polynomial_psd(A)
    require(first==second==rank,message)
    return {'rank_both_algorithms':rank,'whole_matrix_sha256':r.exact.digest(r.encode(A)),
            'full_characteristic_coefficients_sha256':digest,'integral_denominator':den}


def positive(packet):
    row=packet['new_positive'];q,k=row['q'],row['k']
    require((q,k)==(27,7),'new exact boundary order')
    kap,t,sigma=F(row['kappa']),F(row['t']),F(row['sigma'])
    require(0<kap<=F(1,8) and (kap,t,sigma)==(F(1,2**30),F(19),F(-18)),
            'precise rational certificate and credited nonfixed domain')
    D=r.forms(q,k);C,U=r.evaluate(D,kap,t,sigma)
    require((D['N'],D['s'])==(row['N'],row['s'])==(541,85),'original cardinality and greatest star')
    n=len(D['keys']);star=r.vectors(D)['star']
    weighted=[F(D['sizes'][i])*star[i] for i in range(n)]
    require(sum(weighted)==D['s'] and not any(r.action(C,star)),'full actual greatest-star kernel')
    lower=F(1,2**50);upper=F(1,2**19)
    CL=[[C[i][j]-lower*(F(D['sizes'][i]*int(i==j))-weighted[i]*weighted[j]/D['s'])
         for j in range(n)] for i in range(n)]
    UU=[[U[i][j]-upper*D['sizes'][i]*int(i==j) for j in range(n)] for i in range(n)]
    checks={'entire_lower':psd(C,n-1,'ENTIRE positive original fixed lower PSD and rank'),
            'entire_cap':psd(U,n,'ENTIRE positive original fixed cap PSD and rank'),
            'original_weighted_lower_floor':psd(CL,n-1,'ENTIRE original weighted greatest-star lower floor'),
            'original_weighted_cap_floor':psd(UU,n,'ENTIRE original weighted cap floor')}
    require(lower<=kap/2 and upper<=D['N']-2*D['s'],
            'explicit finite floors bounded by all-original nonfixed complementary floors')
    require(row['original_H_lower_rank']==row['original_H_cap_rank']==D['N']-1 and
            F(row['whole_M_unit_gap_lower_bound'])==upper/(D['N']-D['s']),
            'whole actual-empty endpoint ranks and full projected M gap normalization')
    Czero,Uzero=r.evaluate(D,F(0),t,sigma)
    zz=[F(1-int(bool(c&1))-int(bool(c&2))-int(bool(c&4))+int(c.bit_count()>=2))
        for c,_,_ in D['keys']]
    require(not any(r.action(Czero,zz)) and not any(r.action(Czero,star)) and
            r.schur_psd(Czero)==n-2,'zero endpoint has TWO lower kernels and cannot establish greatest rank')
    return {'q':q,'k':k,'N':D['N'],'s':D['s'],'t':t,'sigma':sigma,'kappa':kap,
            'physical_keys':D['keys'],'physical_sizes':D['sizes'],'checks':checks,
            'original_nonempty_lower_floor':lower,'original_nonempty_cap_floor':upper,
            'internal_C_and_LminusJ_rank':D['N']-2,'actual_L_and_NIminusL_ranks':D['N']-1,
            'whole_M_unit_gap_lower_bound':upper/(D['N']-D['s']),
            'ordinary_nonfixed_lift_rank_bridges_credited':True,
            'independent_person_review':False,'formalized':False}


def literal(q):
    D,positions=r.original_forms(q,7)
    return {'q':q,'k':7,'all_ordered_original_nonempty_member_pairs':positions,
            'all_six_complete_original_forms_checked_entry_by_entry':True,
            'physical_keys':D['keys'],'physical_sizes':D['sizes'],
            'entire_forms_sha256':r.exact.digest(r.encode({n:D[n] for n in r.NAMES}))}


def actual_empty_lift(packet):
    """Whole reader-facing M, including an independent empty entry formula."""
    import original_checks as credited
    p=packet['new_positive'];q,k=p['q'],p['k'];D=r.forms(q,k)
    kap,t,sig=F(p['kappa']),F(p['t']),F(p['sigma'])
    X,C,pairs=credited.literal_checks(D,parameters=(kap,t,sig))
    N,s=D['N'],D['s'];n=N-1
    require(X[0]==0 and len(X)==N and len(C)==n,'ACTUAL empty and complete nonempty domains')
    columns=[sum(C[i][j] for i in range(n)) for j in range(n)]
    L=[[1+sum(columns)]+[1-x for x in columns]]
    L.extend([[1-columns[i]]+[1+x for x in C[i]] for i in range(n)])
    M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
    require(all(sum(row)==N for row in L) and all(sum(row)==1 for row in M),
            'EVERY actual original L and M row equation')
    require(all(M[i][j]==M[j][i] and (not(A&B) or M[i][j]==0)
                for i,A in enumerate(X) for j,B in enumerate(X)),
            'EVERY original symmetry and intersecting-support position')
    require(all(M[i][i]==0 for i in range(1,N)),'every nonempty diagonal zero')
    census=[sum(bool(A&(1<<i)) for A in X) for i in range(q+3)]
    require(census[0]==s and all(x<s for x in census[1:]),'actual unique greatest a-star census')
    centered=[F(bool(A&1))-F(s,N) for A in X]
    require(not any(r.action(L,centered)),'ENTIRE actual centered greatest-star lower kernel')
    h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
    require(L[0][0]==1+k*(s-k)+kap*(alpha-2*k*h)+2*sig,
            'independent ACTUAL empty diagonal formula')
    tab=r.table(q)
    for j,A in enumerate(X[1:],1):
        core=(A&7).bit_count();rr=F(1) if core==0 else h if core<3 else -3*(q+1)*h
        intersects=k if A&6 else ((A>>3)&((1<<k)-1)).bit_count()
        if intersects==k:deleted=F(-k)
        else:
            aa,bb=tab[tuple(sorted((r.typ(A),(2,1))))]
            deleted=-intersects+(k-intersects)*(aa-1+kap*bb)
        repair=sum(F(edges.get(tuple(sorted((A,B))),0)) for edges in (r.RB,r.RC) for B in range(1,8))
        expected=1-(kap*rr-deleted+t*repair+sig*int(A in (2,4)))
        require(L[0][j]==expected,'EVERY independent ACTUAL empty off-diagonal formula')
    return {'q':q,'k':k,'N':N,'s':s,'original_nonempty_ordered_pairs':pairs['positions'],
            'all_original_M_ordered_entries':N*N,'every_actual_original_row_support_empty_star_entry_checked':True,
            'every_star_size':census,'original_empty_M_loop':M[0][0],
            'complete_original_C_sha256':r.exact.digest(r.encode(C)),
            'complete_original_L_sha256':r.exact.digest(r.encode(L)),
            'complete_original_M_sha256':r.exact.digest(r.encode(M)),
            'dense_M_spectral_claim_uses_credited_fixed_complement_lift_bridge':True}


def damaged(packet):
    mutations=[]
    def add(name,change,checker):
        p=copy.deepcopy(packet);change(p)
        try:checker(p)
        except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):mutations.append(name);return
        raise ValueError('accepted semantic damage: '+name)
    add('missing covered order',lambda p:p['absence'].pop(),absence)
    add('zero dual weight',lambda p:p['absence'][1]['positive_dual_weights'].__setitem__(0,'0'),absence)
    add('wrong original orientation',lambda p:p['absence'][1]['orientation_vector'].__setitem__(0,'9'),absence)
    add('changed original dual vector',lambda p:p['absence'][1]['planes'][0]['vector'].__setitem__(0,'7'),absence)
    add('uncancelled BC',lambda p:p['absence'][1]['whole_original_coefficients_sum'].__setitem__(4,'1'),absence)
    def trades(p):
        row=p['absence'][1]
        row['planes'][0]['coefficients_constant_kappa_tb_tc_sigma'][2]=str(F(row['planes'][0]['coefficients_constant_kappa_tb_tc_sigma'][2])+1)
        row['planes'][0]['coefficients_constant_kappa_tb_tc_sigma'][3]=str(F(row['planes'][0]['coefficients_constant_kappa_tb_tc_sigma'][3])-1)
    add('decoy preserves combined trade, breaks independent trade',trades,absence)
    add('nonnegative asserted dual constant',lambda p:p['absence'][-1]['whole_original_coefficients_sum'].__setitem__(0,'0'),absence)
    add('false all-kappa dual slope',lambda p:p['absence'][-1]['whole_original_coefficients_sum'].__setitem__(1,'1'),absence)
    add('zero endpoint misrepresented as positive',lambda p:p['new_positive'].__setitem__('kappa','0'),positive)
    add('false original H rank',lambda p:p['new_positive'].__setitem__('original_H_lower_rank',539),positive)
    add('unproved stronger whole unit gap',lambda p:p['new_positive'].__setitem__('whole_M_unit_gap_lower_bound','1'),positive)
    return {'rejected_all_semantic_damages':mutations,'count':len(mutations)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('absence','positive','damage','literal','baseline','empty'))
    ap.add_argument('--q',type=int);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    path=Path(__file__).with_name('CERTIFICATE.json');packet=json.loads(path.read_text())
    if args.phase=='absence':record=absence(packet)
    elif args.phase=='positive':record=positive(packet)
    elif args.phase=='damage':record=damaged(packet)
    elif args.phase=='literal':record=literal(args.q)
    elif args.phase=='empty':record=actual_empty_lift(packet)
    else:
        import recovery
        record={'baseline_only_no_new_mathematics':recovery.verify_positive(28,7)}
    record.update(source_gate=SOURCE,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  actual_agent='six-downset-3',role='researcher',phase=args.phase)
    raw=(json.dumps(r.encode(record),sort_keys=True,indent=2)+'\n').encode()
    args.out.write_bytes(raw)
    print(json.dumps({'phase':args.phase,'q':args.q,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))


if __name__=='__main__':main()
