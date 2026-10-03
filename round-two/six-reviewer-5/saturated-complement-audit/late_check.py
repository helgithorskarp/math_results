"""Post-seal DATA-only correspondence and a separate incidence lift of 8154."""
import argparse,copy,hashlib,json,pathlib,sys
from fractions import Fraction as F
S=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(S/'primary' if (S/'primary').is_dir() else S))
P=S
from algebra import require,psd,dot
from independent import pair_matrix

def fingerprint(obj):
    b=json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def ordinary_control():
    # From the defining8154 incidence lift, not the author's direct B-entry formula.
    middle=[x for x in range(1,64) if 2<=x.bit_count()<=4]
    members=[0]+[x for x in range(1,64) if x.bit_count()<=4];nonempty=members[1:]
    Q=[[F(26*(a==b)-1)+(F(26-int(a.bit_count()==3)) if a!=b and a^b==63 else 0) for b in middle] for a in middle]
    R=[[int(bool(x&(1<<i))) for x in middle] for i in range(6)]
    projection=[]
    for x in nonempty:
        if x.bit_count()==1:projection.append([-F(v) for v in R[x.bit_length()-1]])
        else:projection.append([F(a==x) for a in middle])
    PQ=[[sum(v*Q[k][j] for k,v in enumerate(row)) for j in range(len(middle))] for row in projection]
    C=[[sum(PQ[i][k]*projection[j][k] for k in range(len(middle))) for j in range(len(nonempty))] for i in range(len(nonempty))]
    # E=[-1^T;I], L=J+ECE^T. Every original member and empty entry retained.
    sums=[sum(row) for row in C];L=[[1+sum(sums)]+[1-x for x in sums]]
    L.extend([[1-sums[i]]+[1+x for x in row] for i,row in enumerate(C)])
    require(all(sum(row)==57 for row in L),'all actual rows')
    require(all(L[i][j]==0 for i,a in enumerate(members) for j,b in enumerate(members) if i!=j and a&b),'all supported distinct entries')
    require(all(L[i][i]==26 for i in range(1,57)),'all original nonempty diagonals')
    require(all(sum(C[i][j] for j,x in enumerate(nonempty) if x&(1<<a))==0 for i in range(56) for a in range(6)),'all336 star rows')
    good,piv=psd(L);require(good and sum(v!=0 for v in piv)==36,'full lower PSD/rank')
    good,piv=psd(C);require(good and sum(v!=0 for v in piv)==35,'core PSD/rank')
    pairs=[(a,b) for i,a in enumerate(nonempty) for b in nonempty[i+1:] if a^b==63 and L[members.index(a)][members.index(b)]==26]
    require(len(pairs)==15,'literal saturation')
    w=[F(0)]+[F(1) if x.bit_count()==1 else F(1,2) if x.bit_count()==3 else F(0) for x in nonempty]
    upper=[[F(57*(i==j))-L[i][j] for j in range(57)] for i in range(57)]
    energy=dot(w,upper,w);require(energy==-444,'literal upper witness')
    v=[F(15*5,26)]+[F(any(x in pair for pair in pairs)) for x in nonempty]
    norm=sum(t*t for t in v);eig=F(52)+F(375,26)
    require(dot(v,L,v)-eig*norm==(L[0][0]-F(375,26))*F(15**2*25,26**2),'original control spectral refinement')
    return L,dict(credited_family_height=8154,n=6,actual_original_vertices=57,original_lower_rank=36,complete_original_entries=3249,all_original_star_rows=336,saturated_pairs=15,cap_budget=5,actual_empty_L00=str(L[0][0]),original_cap_witness_energy=str(energy),complete_L=fingerprint(L),new_ordinary_H=False,scope='Valid credited ordinary H violates count because cap is absent')

def check(native,primary):
    cases=native['principal_controls']
    for row in cases:
        s,r,q,lam=F(row['s']),F(row['r']),row['q'],F(row['ell']);N=2*s+r
        L=pair_matrix(s,r,q,lam);U=[[N*(i==j)-L[i][j] for j in range(len(L))] for i in range(len(L))]
        require(fingerprint([L,U])==row['whole_matrices'],'entire literal matrix fingerprint')
        for A,k,rk in [(L,'lower_psd','lower_rank'),(U,'upper_psd','upper_rank')]:
            yes,piv=psd(A);rank=sum(x!=0 for x in piv) if yes else None
            require(yes==row[k] and rank==row[rk],'literal rank/full PSD')
        require(F(row['lo'])==q*r*r/s and F(row['hi'])==N-2*q*r,'both original endpoints')
    polys=primary['recurrences'][:4];rec=native['recurrence_coefficient_certificate']
    require(list(map(str,polys[0]['difference']))==rec['first_den_minus_num'] and list(map(str,polys[1]['difference']))==rec['second_den_minus_num'],'whole recurrence coefficient streams')
    nodes={x['m']:x for x in primary['recurrences'][4:]}
    from algebra import evaluate
    for row in rec['definition_level_controls']:
        k=row['m'];src=nodes[k]
        require(src['evenA']==row['A'] and src['evenB']==row['B'],'entire native recurrence values')
        require(F(row['first_ratio'])==F(evaluate(polys[0]['numerator'],k),evaluate(polys[0]['denominator'],k)) and F(row['second_ratio'])==F(evaluate(polys[1]['numerator'],k),evaluate(polys[1]['denominator'],k)),'both original ratio fields')
    counts={x['n']:x for x in primary['near_cube']}
    for row in native['original_near_cube_counts']:
        own=counts[row['n']]
        require(own['s']-1==row['total_original_complementary_pairs'] and own['budget']==row['maximum_saturated_pairs'] and own['s']-1-own['budget']==row['minimum_attenuated_original_pairs'],'entire original counts')
        if 'literal_pair_census' in row:require(row['literal_pair_census']==own['s']-1,'literal pair count')
        if 'least_noncentral_deficit_classes_necessary' in row:
            q=own['minimum_classes'];require(row['least_noncentral_deficit_classes_necessary']==q,'class lower bound')
            prior=own['necessary'][q-1]['remaining_saturated'] if q else None
            require(prior==row['saturated_population_at_next_smaller_class_count'],'entire original preceding threshold')
    _,control=ordinary_control();require(control==native['credited_original_ordinary_control'],'entire original57 control including all-entry fingerprint')
    return dict(principal_cases=len(cases),complete_literal_matrix_fingerprints=len(cases),recurrence_nodes=len(rec['definition_level_controls']),whole_count_records=len(native['original_near_cube_counts']),ordinary_control=control,data_only_no_producer_import=True,original_control_is_8154_prior_art=True)

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,default=S);args=ap.parse_args();P=args.work
    native=json.loads((P/'native-normal.json').read_text());primary=json.loads((P/'primary-normal.json').read_text());out=check(native,primary)
    damage=[]
    for name,mutate in [('principal full-matrix digest',lambda x:x['principal_controls'][0]['whole_matrices'].update(sha256='0'*64)),('principal rank',lambda x:x['principal_controls'][0].update(lower_rank=999)),('recurrence coefficient',lambda x:x['recurrence_coefficient_certificate']['first_den_minus_num'].__setitem__(0,'13')),('recurrence value',lambda x:x['recurrence_coefficient_certificate']['definition_level_controls'][0].update(A='0')),('whole original count',lambda x:x['original_near_cube_counts'][0].update(total_original_complementary_pairs=99)),('ordinary original matrix fingerprint',lambda x:x['credited_original_ordinary_control']['complete_L'].update(sha256='0'*64))]:
        wrong=copy.deepcopy(native);mutate(wrong)
        try:check(wrong,primary)
        except ValueError:damage.append(name)
        else:raise ValueError('semantic correspondence damage accepted')
    out['rejected_correspondence_damages']=damage
    (P/'late-comparison.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
