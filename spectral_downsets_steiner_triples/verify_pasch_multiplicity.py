"""Exact finite local certificates and complete cyclic/complement checks.

The universal theorem also needs the ordinary proof, including the pair
quota and Schur bridges. No finite enumeration proves its unbounded scope.
All 729 T patterns, 4096 four-set controls, 762 complementary cyclic bases,
and every 572 legal neighbour of one fixed base. six-downset-2, researcher.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations,product
import json
from math import lcm
from pathlib import Path
from cyclic13_gram import balanced_masks,blocks_from_mask
from pasch_defect import all_trades,point_defect
from pasch_multiplicity import ALPHA,degree_certificate,degree_update,sharp_fixture
from cyclic13_spectral import comparison_data
from verify_cyclic13_spectral import determinant,leading_minors,tuple_defect
from verify_defect_gram import independent_signatures,independent_count
from verify import rejects,exact_psd_rank,matrix_hash
from verify_pasch_neighbourhood import literal_defect


def record(hash_object,value):
    hash_object.update(json.dumps(value,separators=(',',':')).encode()+b'\n')


def minors(M):
    out=[]
    for bits in range(1,8):
        ids=[i for i in range(3)if bits>>i&1]
        H=[[F(M[i][j])for j in ids]for i in ids];scale=1
        for row in H:
            for z in row:scale=lcm(scale,z.denominator)
        out.append(F(determinant([[int(z*scale)for z in row]for row in H]),scale**len(ids)))
    return out


def literal_norm(T,G,kappa):
    return [[[F(kappa*kappa*int(i==j)-2*G[i][j])+sign*2*kappa*(T[i][j]+T[j][i])
              for j in range(3)]for i in range(3)]for sign in (-1,1)]


def local_checks():
    transcript=sha256();shapes=set();inside_minors=0;mu2_patterns=0
    for values in product((-1,0,1),repeat=6):
        T=[[0]*3 for _ in range(3)]
        for (i,j),z in zip(((i,j)for i in range(3)for j in range(3)if i!=j),values):T[i][j]=z
        c=[sum(abs(T[j][k])for j in range(3))for k in range(3)]
        e=sum(c);p=sum(z>0 for z in c);shapes.add((e,p))
        ds=[]
        for sign in (-1,1):
            H=[[ALPHA[e]*int(i==j)+sign*2*(T[i][j]+T[j][i])for j in range(3)]for i in range(3)]
            ds.extend(minors(H));assert min(ds)>=0;inside_minors+=7
        # The envelope is linear in kappa, with nonnegative coefficient,
        # so checking its value at ten covers every real kappa>=10.
        assert 8-ALPHA[e]>=0 and (8-ALPHA[e])*10+8*e+4*p-60>=0
        margins={}
        for mu,k in ((2,F(22,3)),(3,F(34,3)),(4,F(14))):
            if mu==2 and max(c)>1:continue
            if mu==2:mu2_patterns+=1;assert p==e
            M=24*(mu-1)-4*e-2*p;margin=k*(k-ALPHA[e])-2*M
            assert k>=ALPHA[e] and margin>=0;margins[str(mu)]=str(margin)
        record(transcript,[values,e,p,list(map(str,ds)),margins])
    capacity=0;capacity_hash=sha256();mu1=0
    for bits in product(range(2),repeat=4):
        u=bits[:2];z=bits[2:];n=sum(bits);c=abs(u[0]-u[1])+abs(z[0]-z[1])
        assert c<=n<=4-c
        comp=tuple(1-b for b in bits)
        assert sum(comp)==4-n and abs(comp[0]-comp[1])+abs(comp[2]-comp[3])==c
        for mu in range(1,6):
            h=[mu-1-u[b]-z[a]for a,b in product(range(2),repeat=2)]
            if min(h)<0:continue
            pos=[h[1],h[2]];neg=[h[0],h[3]]
            bound=sum(h)+2*min(pos)+2*min(neg)
            assert sum(h)==4*(mu-1)-2*n
            assert bound==8*(mu-1)-4*n-2*int(c>0)
            if mu==1:mu1+=1;assert n==c==sum(h)==0
            if mu==2:assert c<=1
            record(capacity_hash,[bits,mu,h,bound]);capacity+=1
    set_hash=sha256();set_cases=0
    for masks in product(range(8),repeat=4):
        h=[m.bit_count()for m in masks]
        column=[sum((1 if j in (1,2)else -1)*int(masks[j]>>x&1)for j in range(4))for x in range(3)]
        square=sum(z*z for z in column)
        upper=sum(h)+2*min(h[1],h[2])+2*min(h[0],h[3])
        assert square<=upper and sum(map(abs,column))<=sum(h)
        record(set_hash,[masks,column,square,upper]);set_cases+=1
    return {'all_directed_T_patterns':729,'inside_signed_principal_minors':inside_minors,
        'mu2_admissible_column_patterns':mu2_patterns,'e_p_shapes':[list(z)for z in sorted(shapes)],
        'inside_and_scalar_transcript_sha256':transcript.hexdigest(),
        'boolean_capacity_patterns_checked':capacity,'mu1_feasible_boolean_patterns':mu1,
        'boolean_capacity_sha256':capacity_hash.hexdigest(),
        'four_outside_sets_on_three_points':set_cases,'outside_set_inequality_sha256':set_hash.hexdigest(),
        'general_real_kappa_envelope':'kappa >= 10; kappa*(kappa-8) >= 48*mu-108; mu >= 3'}


def base_checks():
    orbit,_,families=balanced_masks((4,));signatures=independent_signatures()
    count,states=independent_count(4,signatures);assert count==len(families[4])==762
    triples={sum(1<<x for x in t)for t in combinations(range(13),3)}
    transcript=sha256();point_forms={};entries=0
    for mask in families[4]:
        a=blocks_from_mask(mask,orbit);b=sorted(triples-set(a))
        A=tuple_defect(4,a);B=tuple_defect(7,b)
        _,_,author=point_defect(13,7,b)
        assert A==B==author;entries+=169
        M=[[20*(13*int(i==j)-1)-13*B[i][j]for j in range(13)]for i in range(13)]
        assert all(sum(row)==0 for row in M)
        key=tuple(tuple(row)for row in M)
        if key not in point_forms:
            ds=leading_minors([row[1:]for row in M[1:]])
            assert min(ds)>0;point_forms[key]=ds
        record(transcript,[mask,A,len(a),len(b)])
    comparisons=[]
    for lam,h,bound in ((4,3,164),(7,5,238)):
        for depth in range(h+1):
            data=comparison_data(13,lam,20+14*depth,bound)
            ds=[minors(data['comparison'])[i]for i in (0,2,6)]
            assert min(ds)>0
            comparisons.append({'lambda':lam,'depth':depth,'gamma':20+14*depth,
                                'B':bound,'positive_leading_minors':list(map(str,ds))})
    return {'lambda4_fixed_shift_bases':count,'lambda7_complementary_bases':count,
        'independent_DP_max_states':states,'literal_complement_point_entries':entries,
        'distinct_12x12_complement_initial_forms':len(point_forms),
        'positive_integer_initial_leading_minors':12*len(point_forms),
        'complement_base_transcript_sha256':transcript.hexdigest(),'shorter_path_comparisons':comparisons}


def seed_checks():
    orbit,_,families=balanced_masks((4,));blocks=blocks_from_mask(23768,orbit);U=set(blocks)
    triples={sum(1<<x for x in t)for t in combinations(range(13),3)}
    complement=sorted(triples-U);old=tuple_defect(4,blocks)
    seen=set();hist=Counter();transcript=sha256();norm_hash=sha256()
    full_minor_count=0;norm_pattern=set()
    for groups,even,odd in all_trades(13):
        if even<=U and odd.isdisjoint(U):reverse=False
        elif odd<=U and even.isdisjoint(U):reverse=True
        else:continue
        new,Z,D,info=degree_update(13,4,blocks,groups,reverse)
        newq,Zq,Dq,iq=degree_update(13,7,complement,groups,not reverse)
        assert set(newq)==triples-set(new) and Zq==Z==tuple_defect(4,new)==tuple_defect(7,newq)
        assert Dq==D and all(D[i][j]==Z[i][j]-old[i][j]for i in range(13)for j in range(13))
        assert info['T']==iq['T'] and info['outside_rows']==iq['outside_rows']
        assert info['outside_Gram']==iq['outside_Gram']
        assert tuple(new)not in seen;seen.add(tuple(new))
        T=info['T'];G=info['outside_Gram'];norm_pattern.add((tuple(z for row in T for z in row),tuple(z for row in G for z in row)))
        least=None
        for k in range(1,15):
            if all(min(minors(H))>=0 for H in literal_norm(T,G,k)):least=k;break
        assert least is not None;hist[least]+=1
        for sign in (-1,1):
            H=[[14*(13*int(i==j)-1)+sign*13*D[i][j]for j in range(13)]for i in range(13)]
            assert all(sum(row)==0 for row in H)
            ds=leading_minors([row[1:]for row in H[1:]])
            assert min(ds)>0;full_minor_count+=12
            record(norm_hash,[groups,reverse,sign,ds])
        n=[z['inside_extra_count']for z in info['local_columns']];c=[z['column_support_count']for z in info['local_columns']]
        record(transcript,[groups,reverse,T,G,n,c,least])
    assert len(seen)==572 and len(norm_pattern)==264
    assert dict(hist)=={6:65,7:221,8:221,9:52,10:13}
    return {'seed_mask':23768,'canonical_trade_candidates':25740,'complete_legal_neighbours':572,
        'complement_legal_neighbours_also_checked':572,'distinct_T_OGram_patterns':264,
        'least_integer_actual_norm_histogram':{str(k):v for k,v in sorted(hist.items())},
        'full_13x13_signed_norm_forms':1144,'positive_integer_norm_leading_minors':full_minor_count,
        'signed_norm_minor_sha256':norm_hash.hexdigest(),'neighbourhood_norm_sha256':transcript.hexdigest()}


def boundary_checks():
    triples={sum(1<<x for x in t)for t in combinations(range(7),3)}
    fano={sum(1<<((x+t)%7)for x in (0,1,3))for t in range(7)}
    inputs=[(7,4,sorted(triples-fano),'complement of cyclic Fano (0,1,3)')]
    orbit,_,family=balanced_masks((2,3))
    for mu in (2,3):inputs.append((13,mu,blocks_from_mask(family[mu][0],orbit),family[mu][0]))
    out=[]
    for v,lam,blocks,seed in inputs:
        U=set(blocks);old=literal_defect(v,lam,blocks)
        for groups,a,b in all_trades(v):
            if a<=U and b.isdisjoint(U):reverse=False
            elif b<=U and a.isdisjoint(U):reverse=True
            else:continue
            new,Z,D,info=degree_update(v,lam,blocks,groups,reverse)
            assert Z==literal_defect(v,lam,new)
            assert all(D[i][j]==Z[i][j]-old[i][j]for i in range(v)for j in range(v))
            kappa=info['degree_certificate']['kappa'];ranks=[];hashes=[]
            for sign in (-1,1):
                H=[[kappa*(int(i==j)-F(1,v))+sign*D[i][j]for j in range(v)]for i in range(v)]
                ranks.append(exact_psd_rank(H));hashes.append(matrix_hash(H))
            assert ranks==([0,0]if kappa==0 else[v-1,v-1])
            out.append({'v':v,'lambda':lam,'mu':info['degree_certificate']['mu'],
                'seed':seed,'groups':[list(g)for g in groups],'reverse':reverse,
                'kappa':str(kappa),'signed_full_Fraction_PSD_ranks':ranks,
                'signed_full_matrix_sha256':hashes});break
        else:raise AssertionError('Boundary fixture has no legal move')
    return out


def sharp_checks():
    blocks,groups,reverse,certificate=sharp_fixture();U=set(blocks)
    # Direct tuple pair degrees and replications do not import design_data.
    pair_degrees=Counter();replication=Counter()
    for code in blocks:
        points=[i for i in range(13)if code>>i&1]
        assert len(points)==3 and code<1<<13
        replication.update(points);pair_degrees.update(combinations(points,2))
    assert len(pair_degrees)==78 and set(pair_degrees.values())=={4}
    assert len(replication)==13 and set(replication.values())=={24}
    sides=[set(),set()]
    for bits in product(range(2),repeat=3):
        sides[sum(bits)%2].add(sum(1<<groups[i][bits[i]]for i in range(3)))
    assert sides[0]<=U and sides[1].isdisjoint(U)
    direct_new=sorted(U-sides[0]|sides[1]);old=literal_defect(13,4,blocks)
    literal=literal_defect(13,4,direct_new)
    Delta=[[literal[i][j]-old[i][j]for j in range(13)]for i in range(13)]
    new,Z,author,info=degree_update(13,4,blocks,groups,reverse)
    assert new==direct_new and Z==literal and author==Delta
    x=certificate['integer_eigenvector'];assert len(x)==13 and sum(x)==0
    assert sum(z*z for z in x)==420
    assert all(sum(Delta[i][j]*x[j]for j in range(13))==14*x[i]for i in range(13))
    norm_ranks=[];hashes=[]
    for sign in (-1,1):
        H=[[F(14)*(int(i==j)-F(1,13))+sign*Delta[i][j]for j in range(13)]for i in range(13)]
        norm_ranks.append(exact_psd_rank(H));hashes.append(matrix_hash(H))
    assert norm_ranks==[11,12]
    assert info['T']==[[0,1,1],[1,0,1],[1,1,0]]
    assert info['outside_Gram']==[[14]*3 for _ in range(3)] and info['outside_trace']==42
    assert info['signed_three_by_three_norm_ranks']==[2,3] and info['scalar_comparison_margin']==0
    lower=[[F(13)*(int(i==j)-F(1,13))-Delta[i][j]for j in range(13)]for i in range(13)]
    negative=sum(x[i]*lower[i][j]*x[j]for i in range(13)for j in range(13))
    assert negative==-420
    rejects(lambda:exact_psd_rank(lower))
    return {'v':13,'lambda':4,'mu':4,'simple_blocks':104,'pair_degrees_checked':78,
        'pair_degree':4,'point_replications_checked':13,'replication':24,
        'blocks':blocks,'groups':[list(g)for g in groups],'reverse':reverse,**certificate,
        'integer_eigenvector_squared_norm':420,'Delta_eigenvalue':14,
        'signed_14K_norm_Fraction_PSD_ranks':norm_ranks,'signed_14K_norm_matrix_sha256':hashes,
        'three_by_three_norm_ranks':[2,3],'outside_trace':42,'scalar_comparison_margin':0,
        'budget13_negative_quadratic':str(negative),
        'all_real_budget_k_less14_quadratic':'420*(k-14) < 0',
        'meaning':'14 is the least possible uniform symmetric Pasch norm budget at mu=4, already sharp at v=13. This is not a counterexample to H or an optimal cap/radius.'}


def run():
    out={'agent':'six-downset-2','role':'researcher','local':local_checks(),
         'bases':base_checks(),'seed':seed_checks(),'boundary':boundary_checks(),'sharp':sharp_checks()}
    controls=[]
    for name,call in [('full_design_no_move',lambda:degree_certificate(13,11)),
                      ('mu2_insufficient_budget',lambda:degree_certificate(13,2,7)),
                      ('mu3_insufficient_budget',lambda:degree_certificate(13,3,11)),
                      ('mu4_insufficient_budget',lambda:degree_certificate(13,4,13))]:
        rejects(call);controls.append(name)
    out.update(rejection_controls=controls,whole_dense_slack_eliminations=0,
        trust_boundary='CPython exact integers/Fractions. Universal claims require the ordinary proof; finite validation is explicitly bounded. No solver, floating point, whole-slack elimination or design-isomorphism census.')
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('pasch_multiplicity_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
