"""Literal controls for the ordinary matrix/containment equality refinements.

These six graphs are INVALID signed identity controls. The theorem's
universal conditional steps are the ordinary arguments in REVIEW.md.
"""
from itertools import product
import json
import sys
import check as own


def record():
    controls=[]
    for f in json.loads((own.ROOT/'INPUT-controls.json').read_text())['controls']:
        rows=own.adjacency(f['red_masks']);out=own.original(rows)
        L,H=out['low_vertices'],out['high_vertices']
        M=[[int(x in rows[i]) for x in H] for i in L]
        A=[[int(j in rows[i]) for j in L] for i in L]
        Q=[[int(y in rows[x]) for y in H] for x in H]
        K=[[sum(M[i][x]*M[j][x] for x in range(18)) for j in range(4)] for i in range(4)]
        S=out['mixed_slack_matrix']
        T=[[sum(M[i][y]*Q[y][x] for y in range(18)) for x in range(18)] for i in range(4)]
        rhs=[[5-2*M[i][x]-sum(A[i][j]*M[j][x] for j in range(4))-S[i][x]
              for x in range(18)] for i in range(4)]
        own.need(T == rhs,'all72 literal MQ entries, retaining signed invalid slacks')
        B=[[sum(T[i][x]*M[j][x] for x in range(18)) for j in range(4)] for i in range(4)]
        C=[[5*sum(M[j])-2*K[i][j]-sum(A[i][k]*K[k][j] for k in range(4))
            -sum(S[i][x]*M[j][x] for x in range(18)) for j in range(4)] for i in range(4)]
        own.need(B == C and all(B[i][j] == B[j][i] for i in range(4) for j in range(4)),
                 'all16 literal MQM transpose and symmetry entries')
        controls.append({'name':f['name'],'MQ':T,'MQMt':B,'K':K,'valid':out['Ramsey_valid']})
    # Under exact-two q1, zero nonnegative slacks at p,r and the unique
    # positive incident slack at isolated s imply K_rs=5+M_p,x_s.
    q1=[]
    for incidence in [0,1]:
        krs=5+incidence
        own.need(45-krs == 40-incidence and krs > 4,'entire q1 symmetry contradiction')
        q1.append({'M_p_xs':incidence,'forced_K_rs':krs,'blue_low_pair_cap':4,'contradiction':True})
    # Every column obeys Q_xu+Q_xv-2Q_xw >=0 in the quad case.
    quad=[list(v) for v in product([0,1],repeat=3) if v[0]+v[1]-2*v[2] >= 0]
    own.need(quad == [[0,0,0],[0,1,0],[1,0,0],[1,1,0],[1,1,1]],'all quad column patterns')
    own.need(all(u == v == 1 for u,v,w in quad if w),'whole containment premise')
    own.need(not any(u == 0 and w == 1 for u,v,w in quad),'x=u makes u,w a blue pair')
    own.need(6+1 > 6,'six high and one actual low common neighbors violate blue cap')
    counts=[v for v in own.profiles()['exact_two_profiles'] if v[0] == 0 and v[3] == 2]
    own.need(counts == [[0,2,14,2,0]],'sole nonexcluded exact-two type profile')
    value={'agent':'six-reviewer-2','role':'independent mathematical reviewer','target':9199,
        'signed_controls':controls,'literal_MQ_entries':432,'literal_MQMt_entries':96,
        'q1_symmetry_contradictions':q1,'quad_nonnegative_column_patterns':quad,
        'quad_common_neighbors':{'high':6,'low':1,'blue_cap':6},
        'only_remaining_exact_two_profile':counts[0],
        'remaining_mixed_slacks':{'all_blue':0,'red_per_low':'one1 and eight0'},
        'remaining_low_neighborhood_degrees':[2]+[3]*8,
        'scope':'Necessary equality conditions, no existence and no n1>=3 proof.'}
    for name in ['wrong q1 forced overlap','omitted quad pattern']:
        changed=json.loads(json.dumps(value))
        if name.startswith('wrong'):changed['q1_symmetry_contradictions'][0]['forced_K_rs']=4
        else:changed['quad_nonnegative_column_patterns'].pop()
        own.reject(lambda:own.exact_record(value,changed))
    value['rejected_damages']=['wrong q1 forced overlap','omitted quad pattern']
    return value


if __name__ == '__main__':
    value=record()
    if '--record' in sys.argv:print(json.dumps(value,sort_keys=True,indent=2))
    else:
        own.exact_record(value,json.loads((own.ROOT/'boundary-expected.json').read_text()))
        print(json.dumps({'status':'PASS','record_sha256':own.digest(value),
            'MQ_entries':432,'MQMt_entries':96,'remaining_profiles':1},sort_keys=True))
