"""Data-only checker: independent determinants times AUTHOR72 witness coefficients.

Also compares every exposed polynomial coefficient against the late author
fixture if --native-json is supplied. Never imports producer source.
"""
import json,hashlib,copy,argparse
from pathlib import Path
from fractions import Fraction as Q
from core import run,decode
from owned_algebra import P,var,ZERO
from validate_primary import same


def witness_polys(w):
    if type(w) is not list or len(w)!=10:raise ValueError('ten witness rows')
    out=[]
    for row in w:
        if type(row) is not list:raise ValueError('witness row')
        d={}
        for item in row:
            if type(item)is not list or len(item)!=2:raise ValueError('witness item')
            ex,c=item
            if type(ex)is not list or len(ex)!=2 or any(type(v)is not int or v<0 for v in ex) or sum(ex)>4:raise ValueError('witness exponent')
            if type(c)is not str:raise ValueError('witness rational type')
            value=Q(c)
            if not value:raise ValueError('zero witness coefficient')
            k=(0,0,ex[0],ex[1],0,0,0,0)
            if k in d:raise ValueError('duplicate witness coefficient')
            d[k]=value
        out.append(P(d))
    if sum(len(a.d) for a in out)!=72:raise ValueError('whole72 witness coefficient count')
    return out


def verify_unit(record,witness,damage=None):
    multipliers=witness_polys(witness)
    minors=list(map(decode,record['primitive_minors']))
    raw=list(map(decode,record['raw_minors']))
    contents=list(map(Q,record['minor_contents']))
    if damage=='minor':minors[7]=minors[7]+1
    if damage=='raw-normalization':contents[3]+=1
    x=var(3)
    unit=sum((a*b for a,b in zip(multipliers,minors)),P())
    if unit!=x:raise ValueError('entire primitive-minor unit')
    U=[a/c for a,c in zip(multipliers,contents)]
    rawunit=sum((a*b for a,b in zip(U,raw)),P())
    if rawunit!=x:raise ValueError('entire raw-determinant unit')
    S=sum(sum(abs(c) for c in a.d.values()) for a in U)
    if S<=0 or S>Q(1,10**13):raise ValueError('retained positive witness norm bound')
    q=Q(record['Qstar'])
    return {'primitive_unit':unit.serial(),'raw_unit':rawunit.serial(),
            'exact_S':str(S),'strict_rounded_S_lt_1e13_inverse':S<Q(1,10**13),
            'Q':str(q),'exact_SQ':str(S*q),'rounded_gain_over_author':10**13,
            'whole72_coefficients':True,'complete10_minors':True}


def decode_native(rows):
    if type(rows)is not list:raise ValueError('native polynomial row')
    d={}
    for item in rows:
        if type(item)is not list or len(item)!=2:raise ValueError('native polynomial item')
        k,c=item
        if type(k)is not list or len(k)!=10 or any(type(v)is not int for v in k) or any(k[8:]) or type(c)is not str:raise ValueError('native polynomial typed exponent/coefficient')
        key=tuple(k[:8]);v=Q(c)
        if not v or key in d:raise ValueError('native duplicate/zero coefficient')
        d[key]=v
    return P(d)


def compare_native(a,n,w,unit):
    comparisons={}
    def compare(key,ours):
        if decode_native(n[key])!=decode(ours):raise ValueError('whole native '+key)
        comparisons[key]=len(decode(ours).d)
    for key,ours in [('whole_Fstar_over_s_q0',a['Fstar_over_s']),('whole_E_recovery',a['E_recovery'])]:compare(key,ours)
    counts={}
    for key,ours in [('whole_transformed_original_residuals',a['switched']),('whole_Fstar_zero_primitive_quadratics',a['P']),('whole_primitive_three_by_three_minors',a['primitive_minors'])]:
        if len(n[key])!=len(ours):raise ValueError('native entire row count '+key)
        for i,(row,our) in enumerate(zip(n[key],ours)):
            if decode_native(row)!=decode(our):raise ValueError('native whole row '+key+str(i))
        counts[key]={'polynomials':len(ours),'coefficients':sum(len(decode(z).d) for z in ours)}
    if type(n['whole_five_by_three_matrix'])is not list or len(n['whole_five_by_three_matrix'])!=5:raise ValueError('native5matrix')
    matrix_coeffs=0
    for row,own in zip(n['whole_five_by_three_matrix'],a['matrix']):
        if type(row)is not list or len(row)!=3:raise ValueError('native3matrix')
        for z,p in zip(row,own):
            if decode_native(z)!=decode(p):raise ValueError('entire native matrix entry')
            matrix_coeffs+=len(decode(p).d)
    fs=decode(a['source_input_9550']['reconstruction']['h'][2]);B=var(0)
    if decode_native(n['whole_original_moment3'])!=-Q(24,5)*B or decode_native(n['whole_original_moment5'])!=-4*B-Q(40,3)*fs:raise ValueError('whole native Newton moments')
    for key,our in [('whole_specialized_positive_contents',a['contents']),('whole_positive_integer_determinant_contents',a['minor_contents']),('minor_row_triples',a['triples']),('whole_primitive_minor_x_unit_multipliers',w['multipliers'])]:
        if not same(n[key],our):raise ValueError('whole native scalar stream '+key)
    if decode_native(n['whole_unit_target'])!=var(3) or Q(n['exact_raw_unit_coefficient_norm'])!=Q(unit['exact_S']) or n['exact_matrix_Frobenius_coefficient_bound_Q']!=a['Qstar']:raise ValueError('entire native norm/unit stream')
    return {'scalar_polynomial_comparisons':2+5+5+10+15+2+1,'complete_native_maps':40,'native_matrix_entries':15,'native_matrix_coefficients':matrix_coeffs,'selected_map_coefficients':sum(v['coefficients'] for v in counts.values())+sum(comparisons.values())+matrix_coeffs,'all40_map_coefficients':sum(v['coefficients'] for v in counts.values())+sum(comparisons.values())+matrix_coeffs+len(decode_native(n['whole_original_moment3']).d)+len(decode_native(n['whole_original_moment5']).d)+len(decode_native(n['whole_unit_target']).d),'whole72_author_witness_equality':True,'whole_all10_minors_equality':True,'trust':'All exposed mathematical maps compared; native bool identity/control rows and native replay damage receipts are not independent proofs. No producer imports.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native-json',type=Path);args=ap.parse_args()
    root=Path(__file__).resolve().parent;record=run();expected=json.loads((root/'EXPECTED.json').read_text())
    if not same(record,expected):raise ValueError('whole primary typed record')
    w=json.loads((root/'UNIT.json').read_text())
    if not same(w['triples'],record['triples']):raise ValueError('ordered witness triples')
    unit=verify_unit(record,w['multipliers'])
    rejects=[]
    for name in ['last-witness-coefficient','minor','raw-normalization','missing-row','duplicate-exponent','bool-exponent']:
        bad=copy.deepcopy(w['multipliers'])
        if name=='last-witness-coefficient':bad[7][-1][1]=str(Q(bad[7][-1][1])+1)
        if name=='missing-row':bad.pop()
        if name=='duplicate-exponent':bad[0].append(bad[0][-1].copy())
        if name=='bool-exponent':bad[0][0][0][0]=False
        try:verify_unit(record,bad,damage=name)
        except ValueError:rejects.append(name)
        else:raise ValueError('damaged unit survived '+name)
    n=None
    if args.native_json:
        native=json.loads(args.native_json.read_text());n=compare_native(record,native,w,unit)
        # Change remote data, verify fail without using producer code.
        for key in ['whole_Fstar_zero_primitive_quadratics','whole_primitive_three_by_three_minors']:
            bad=copy.deepcopy(native);bad[key][-1][-1][1]=str(Q(bad[key][-1][-1][1])+1)
            try:compare_native(record,bad,w,unit)
            except ValueError:rejects.append('native-last-coefficient-'+key)
            else:raise ValueError('native damage survived')
    output={'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','primary_record_sha256':hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'unit':unit,'certificate_semantic_rejections':rejects,'late_data_only':n,'no_producer_imports':True}
    print(json.dumps(output,sort_keys=True))

if __name__=='__main__':main()
