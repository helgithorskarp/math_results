"""Literal full-matrix threefold checks; all-orders scope is the written proof.

Integer Schur verifies all four forms on three13/15 inputs. Both centered and
maximal lower forms of cyclic13 also use rational Schur. No orbit reduction.
CPython3.11+, assertions enabled, standard library. six-downset-2, researcher.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from certificates import mask
from integer_psd import integer_psd_rank
from threefold_identities import run as identities
from uniform_threefold import centered_certificate, design_data, fixtures, gap, maximal_certificate, weights
from verify import check_definition, exact_psd_rank, matrix_hash, rejects
from verify_three9 import buffered_upper, gram_rank


def incidence_check(v, blocks):
    pairs, completing, codegrees, outside = design_data(v, blocks)
    r = 3*(v-1)//2
    P = [[int(a >> x & 1) for a in pairs] for x in range(v)]
    C = [[int((1 << x) in completing[a]) for a in pairs] for x in range(v)]
    B = [[int(a >> x & 1) for a in blocks] for x in range(v)]
    H = [[outside[a].get(x, 0) for a in blocks] for x in range(v)]
    for matrix, row_sum, col_sum in ((P,v-1,2),(C,r,3),(B,r,3),(H,2*r,6)):
        assert all(sum(row) == row_sum for row in matrix)
        assert all(sum(row[j] for row in matrix) == col_sum for j in range(len(matrix[0])))
    Z = [[0]*v for _ in range(v)]
    for x in range(v):
        for y in range(v):
            dot = lambda A, T: sum(a*b for a,b in zip(A[x],T[y]))
            assert dot(P,P) == (v-2)*int(x==y)+1
            assert dot(B,B) == (r-3)*int(x==y)+3
            assert dot(P,C) == dot(C,P) == 3*int(x!=y)
            Z[x][y] = dot(C,C)-(r-3)*int(x==y)-3
            assert Z[x][y] == (codegrees[(1<<x)|(1<<y)]-3 if x!=y else 0)
            assert dot(B,H) == dot(H,B) == 9*int(x!=y)+Z[x][y]
    assert all(sum(row)==0 for row in Z)
    for A in blocks:
        contained=[p for p in pairs if p&A==p]
        assert len(contained)==3
        for x in range(v):
            assert sum(int(p>>x&1) for p in contained)==2*int(A>>x&1)
            assert sum(int((1<<x) in completing[p]) for p in contained)==int(A>>x&1)+outside[A].get(x,0)
    for p in pairs:
        containing=[A for A in blocks if A&p==p]
        assert len(containing)==3
        for x in range(v):
            assert sum(int(A>>x&1) for A in containing)==3*int(p>>x&1)+int((1<<x) in completing[p])
    return {'incidence_identities_checked':10, 'Z_offdiagonal_values':sorted({Z[x][y] for x in range(v) for y in range(v) if x!=y}),
            'Z_nonzero':any(any(row) for row in Z),
            'outside_completion_values':sorted({z for row in H for z in row})}


def run():
    out={'agent':'six-downset-2','role':'researcher','arithmetic':'Fraction and integer Schur congruence',
         'identities':identities(),'inputs':[]}
    for name,v,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,blocks)
        Dm,sm,Qm,eta=maximal_certificate(v,blocks,(D,s,Qc))
        assert (Dm,sm)==(D,s)
        check_definition(D,s,Qc,psd=False)
        check_definition(D,s,Qm,psd=False)
        n=len(D)
        forms={'centered':Qc,'centered_buffer':buffered_upper(Qc,gap(v)),
               'maximal':Qm,'maximal_buffer':buffered_upper(Qm,3*gap(v)/4)}
        ranks={key:integer_psd_rank(form) for key,form in forms.items()}
        assert ranks=={'centered':n-v-1,'centered_buffer':n-1,'maximal':n-v,'maximal_buffer':n-1}
        rational=[]
        if name=='cyclic13':
            for key in ('centered','maximal'):
                assert exact_psd_rank(forms[key])==ranks[key]
                rational.append(key)
        stars=[[F(bool(A>>x&1))-F(s,n) for A in D] for x in range(v)]
        empty=[F(j==0)-F(1,n) for j in range(n)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        info=incidence_check(v,blocks)
        tetrahedron=generation.get('tetrahedron_witness')
        if tetrahedron:
            faces=[mask(face) for face in combinations(tetrahedron,3)]
            assert len(set(tetrahedron))==4 and all(face in blocks for face in faces)
            assert all((a&b).bit_count()==2 for a,b in combinations(faces,2))
            # Any STS contains at most one of the four faces; three cannot suffice.
        info['no_three_STS_decomposition_witness']=tetrahedron
        out['inputs'].append({'name':name,'v':v,'N':n,'s':s,'blocks':blocks,'generation':generation,
                              'weights':{k:str(x) for k,x in weights(v).items()},'ranks':ranks,
                              'centered_gap':str(gap(v)),'maximal_gap':str(3*gap(v)/4),
                              'eta':str(eta),'Q00':str(Qm[0][0]),
                              'centered_sha256':matrix_hash(Qc),'maximal_sha256':matrix_hash(Qm),
                              'rational_Schur_also_checked':rational,**info})
        print('validated',name,'N',n,'ranks',ranks,file=sys.stderr,flush=True)
    assert any(item['Z_nonzero'] for item in out['inputs'])
    assert out['inputs'][-1]['Z_nonzero']  # The removed-correction control below.
    rejects(lambda:weights(11))
    rejects(lambda:weights(14))
    rejects(lambda:centered_certificate(v,blocks[:-1]))
    rejects(lambda:centered_certificate(v,blocks+[blocks[0]]))
    damaged=[row[:] for row in Qc]
    _,_,codegrees,_=design_data(v,blocks)
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==1 and a!=b:
                    damaged[i][j]-=weights(v)['t']*(codegrees[a|b]-3)
    rejects(lambda:check_definition(D,s,damaged,psd=False))
    rejects(lambda:integer_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=6
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    assert not(args.check and args.write_expected)
    out=run()
    expected=Path(__file__).with_name('uniform_threefold_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
