"""Whole variable-count original cap slope, separated before target removal.

The original minimizing vectors and polynomial solves are retained in full.
Finite controls bind both physical frames; they do not prove uniform signs.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import lower
inputs=lower.inputs
z,r,require=lower.z,lower.r,lower.require
BASE=Path(__file__).resolve().parent
Q,K,ONE={(1,0):1},{(0,1):1},{(0,0):1}


def integral(poly):
    require(all(v.denominator==1 for v in poly.values()), 'ALL source coefficients integral')
    return {power:int(v) for power,v in poly.items()}


def multiply(A,B):
    return [[z.add(*(z.mul(A[i][t],B[t][j]) for t in range(len(B))))
             for j in range(len(B[0]))] for i in range(len(A))]


def full_trivial_slope():
    D,table=inputs.portable_zero.clearing()
    table={key:lower.extract(poly,1) for key,poly in table.items()}
    f=inputs.portable_frame;p=f.p
    G=[]
    for i,t in enumerate(inputs.cap.TYPES):
        row=[]
        for j,tt in enumerate(inputs.cap.TYPES):
            count=sum(not(a&b) for a in inputs.cap.GROUPS[i] for b in inputs.cap.GROUPS[j])
            choices=p.mul(f.choose(p.Q,t[1]),f.choose(p.add(p.Q,p.constant(-t[1])),tt[1]))
            row.append(integral(p.scale(p.mul(choices,table[tuple(sorted((t,tt)))]),4*count)) if count else {})
        G.append(row)
    require(all(G[i][j]==G[j][i] for i in range(11) for j in range(11)),
            'ALL complete affine full11 original slope reciprocity coefficients')
    leaf=[3,4]
    require(all(not G[i][j] for i in range(11) for j in range(11) if i not in leaf and j not in leaf),
            'ENTIRE original Delta has only two leaf rows and columns')
    return z.scale(integral(D),4),G


def vectors():
    raw=inputs.portable_frame.generated()|inputs.portable_fields.generated()
    frame=inputs.portable_frame.verify(raw);fields=inputs.portable_fields.fields(raw)
    d=integral(inputs.portable_frame.decode(raw['complete_seven_determinant']))
    Y=[[integral(poly) for poly in row] for row in inputs.portable_frame.matrix_decode(raw['complete_seven_solve_adjugate_action'])]
    H=[[integral(poly) for poly in row] for row in inputs.portable_frame.matrix_decode(raw['complete_four_short_numerator'])]
    nn,nd=(integral(inputs.portable_frame.decode(raw['nu_U'][side])) for side in ('numerator','denominator'))
    survivors=z.add(Q,z.scale(K,-1))
    T=z.add(z.scale(z.mul(z.mul(z.mul(Q,d),K),nn),4),z.mul(z.mul(survivors,H[3][3]),nd))
    delta_clear,delta=full_trivial_slope()
    # Full standard cap zero Gram is a different clearing from Delta.
    G,L,np,dp=inputs.portable_fields.standard_polynomial()
    G=[[integral(poly) for poly in row] for row in G];L=integral(L)
    ds,Ys=lower.solve_adjugate(lower.submatrix(G,list(range(5))),lower.submatrix(G,list(range(5)),[5]))
    vs=[z.scale(row[0],-1) for row in Ys]+[ds]
    short=z.add(z.mul(ds,G[5][5]),*(z.scale(z.mul(G[5][j],Ys[j][0]),-1) for j in range(5)))
    require(z.mul(short,nd)==z.scale(z.mul(z.mul(L,ds),nn),2),
            'ENTIRE full6 standard cap zero target equals the credited compact field')
    _,_,_,standard=inputs.portable_zero.cleared_grams()
    std_delta=[[lower.extract(poly,1) for poly in row] for row in standard]
    # For cap anchor e_i, remaining-bcx value is -q nd H_i3/T.
    # Its full-q trivial mean is -(q-k) nd H_i3/T.
    # The full mean-zero target norm squared is k(q-k)q nd^2 H_i3 H_j3/T^2.
    R=list(range(3,10));retained=[0,1,2,10]
    V=[]
    for i in range(3):
        xx=[{} for _ in range(4)];xx[i]=T;xx[3]=z.scale(z.mul(z.mul(survivors,nd),H[i][3]),-1)
        vv=[{} for _ in range(11)]
        for j,poly in zip(retained,xx):vv[j]=z.mul(d,poly)
        for j in range(7):vv[R[j]]=z.scale(z.add(*(z.mul(Y[j][c],xx[c]) for c in range(4))),-1)
        V.append(vv)
    return {'complete_original_frame_receipt':frame,'complete_original_fields_receipt':fields,
            'delta_clearing':delta_clear,'full_trivial_Delta':delta,'full_standard_Delta':std_delta,
            'full_trivial_vector_denominator':z.mul(d,T),'full_trivial_vectors':V,
            'full_standard_vector_denominator':ds,'full_standard_vector':vs,
            'full_standard_zero_Gram':G,'full_standard_zero_clearing':L,
            'original_d':d,'cap_target_denominator':T,'nu_U_numerator':nn,'nu_U_denominator':nd,
            'four_short_numerator':H,'survivors':survivors}


def all_polynomials_record(data):
    matrices={'full_trivial_Delta','full_standard_Delta','full_trivial_vectors',
              'full_standard_zero_Gram','four_short_numerator'}
    receipts={'complete_original_frame_receipt','complete_original_fields_receipt'}
    return {key:value if key in receipts else lower.matrix_record(value) if key in matrices
            else [lower.record(poly) for poly in value] if key=='full_standard_vector'
            else lower.record(value) for key,value in data.items()}


def controls(data):
    # Every physical original Gram position, independently counted source.
    rows=[]
    for q,k in ((9,3),(21,7),(27,7),(32,8),(100,20)):
        D=lower.z.evaluate(data['delta_clearing'],q,k)
        # Build original k=0 family, with the CURRENT original N in its cap.
        ordinary=r.forms(q,0)
        # The full trivial Delta does not depend on the deletion count.
        coordinate=[]
        for gs,typ in zip(inputs.cap.GROUPS,inputs.cap.TYPES):
            coordinate.append([F(int(core in gs and z0+w0==typ[1]))
                               for core,z0,w0 in ordinary['keys']])
        actual=[[r.pair(ordinary['Delta'],x,y) for y in coordinate] for x in coordinate]
        supplied=[[F(z.evaluate(poly,q,k),D) for poly in row] for row in data['full_trivial_Delta']]
        require(actual==supplied, 'ALL121 original counted full11 Delta positions')
        std0=inputs.cap.standard(q,k)[1]['standard_gram']
        supplied_std=[[F(z.evaluate(poly,q,k),z.evaluate(data['full_standard_zero_clearing'],q,k))
                       for poly in row] for row in data['full_standard_zero_Gram']]
        require(std0==supplied_std, 'ALL36 full original standard cap zero Gram positions')
        vv=[F(z.evaluate(poly,q,k),z.evaluate(data['full_standard_vector_denominator'],q,k))
            for poly in data['full_standard_vector']]
        require(all(r.action(std0,vv)[i]==0 for i in range(5)) and vv[5]==1,
                'ALL original standard conditional vector equations')
        rows.append({'q':q,'k':k,'full_original_trivial_Delta_positions':121,
                     'full_original_standard_positions':36,'standard_vector':vv})
    return rows


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    data=vectors();checks=controls(data)
    value={'actual_agent':'six-downset-3','role':'researcher',
           'complete_original_cap_vector_polynomials':all_polynomials_record(data),
           'complete_original_controls':r.encode(checks),
           'uniform_Delta_sign_proved':False,'ordinary_removal_and_fullspace_bridge_unformalized':True}
    args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'all_original_polynomial_vectors_generated':True,
                      'standard_vector_denominator_terms':len(data['full_standard_vector_denominator']),
                      'trivial_vector_denominator_terms':len(data['full_trivial_vector_denominator']),
                      'trivial_vector_terms':[[len(poly) for poly in row] for row in data['full_trivial_vectors']],
                      'all_controls':len(checks)}))
