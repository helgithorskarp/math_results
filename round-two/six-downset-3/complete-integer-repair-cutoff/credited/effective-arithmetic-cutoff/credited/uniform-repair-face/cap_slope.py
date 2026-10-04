"""Exact full cap slope and whole-domain combined slope sign proposals.

Small divisor factors regenerate all quotients; every division is multiplied back.
The two independent original trades cancel only in the combined dual.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
import cap_fields as cf
import factors
lower,inputs,z,r,require=cf.lower,cf.inputs,cf.z,cf.r,cf.require
BASE=Path(__file__).resolve().parent
ONE=cf.ONE


def decode(rows):
    result={}
    for power,value in rows:
        power=tuple(power);value=int(value)
        require(len(power)==2 and min(power)>=0 and power not in result, 'ENTIRE unique monomial encoding')
        if value:result[power]=value
    return result


def compact(data,raw=None):
    require(raw is None, 'source-only compact generation accepts no external proposal')
    gt,gs=factors.factor('cap_trivial_vector_gcd'),factors.factor('cap_standard_vector_gcd')
    dt=z.divide(data['full_trivial_vector_denominator'],gt)
    ds=z.divide(data['full_standard_vector_denominator'],gs)
    V=[[z.divide(poly,gt) for poly in row] for row in data['full_trivial_vectors']]
    vs=[z.divide(poly,gs) for poly in data['full_standard_vector']]
    require(z.mul(gt,dt)==data['full_trivial_vector_denominator'] and
            all(z.mul(gt,V[i][j])==data['full_trivial_vectors'][i][j] for i in range(3) for j in range(11)),
            'ALL33 source-only trivial vector divisions multiplied back')
    require(z.mul(gs,ds)==data['full_standard_vector_denominator'] and
            all(z.mul(gs,vs[i])==data['full_standard_vector'][i] for i in range(6)),
            'ALL6 source-only standard vector divisions multiplied back')
    return dt,ds,V,vs


def bilinear(G,x,y):
    # Multiply the sparse affine form first, preserving every coefficient.
    action=[z.add(*(z.mul(G[i][j],y[j]) for j in range(len(G)))) for i in range(len(G))]
    return z.add(*(z.mul(x[i],action[i]) for i in range(len(G))))


def generated():
    data=cf.vectors();dt,ds,V,vs=compact(data)
    et=[[bilinear(data['full_trivial_Delta'],x,y) for y in V] for x in V]
    es=bilinear(data['full_standard_Delta'],vs,vs)
    require(all(et[i][j]==et[j][i] for i in range(3) for j in range(3)), 'ALL complete energy reciprocity coefficients')
    ds2=z.mul(ds,ds)
    # Std target norm squared = k*q/(q-k) times the product of trivial means.
    num=[[z.add(z.scale(z.mul(z.mul(ds2,data['survivors']),et[i][j]),2),
                   z.mul(z.mul(z.mul(cf.K,cf.Q),z.mul(V[i][10],V[j][10])),es))
          for j in range(3)] for i in range(3)]
    den=z.scale(z.mul(z.mul(z.mul(data['delta_clearing'],data['survivors']),z.mul(dt,dt)),ds2),2)
    require(all(num[i][1]==num[i][2] for i in range(3)) and all(num[1][j]==num[2][j] for j in range(3)),
            'ENTIRE original cap Delta depends only on anchor a and b+c+ab+ac')
    return data,{'trivial_vector_denominator':dt,'standard_vector_denominator':ds,
                 'trivial_vectors':V,'standard_vector':vs,
                 'trivial_energies':et,'standard_energy':es,'numerator':num,'denominator':den}


def controls(data,field):
    from cap_controls import control
    fields=(lower.generated('nu'),lower.generated('tau'))
    rows=[]
    for q,k in ((9,3),(21,7),(26,7),(27,7),(32,8),(100,20)):
        original=control(q,k,fields)
        den=z.evaluate(field['denominator'],q,k)
        require(den>0, 'positive original squared cap derivative denominator')
        actual=[[F(z.evaluate(poly,q,k),den) for poly in row] for row in field['numerator']]
        require(actual==original['whole_Delta_compression'],
                'ALL9 complete original23 cap slope positions equal whole polynomial field')
        ss=(-1,1,1);margin=F(1,2*q**4)
        conservative=[[actual[i][j]+margin*ss[i]*ss[j] for j in range(3)] for i in range(3)]
        require(r.schur_psd(conservative)==2 and r.polynomial_psd(conservative)[0]==2,
                'TWO exact algorithms confirm conservative cap slope control')
        rows.append({'q':q,'k':k,'whole_original_cap_slope':actual,
                     'whole_conservative_slope':conservative,'whole_original_joint_slope':original['whole_joint_slope_matrix'],
                     'original_cap_not_PSD_principal_minor':original['exact_negative_principal_minor'],
                     'original_a0_derivative':original['a0_derivative'],
                     'all_original_minimizing_vectors':original['whole_minimizing_vectors']})
    return rows


def matrix_record(G):return lower.matrix_record(G)


def reduced_field(field,raw=None):
    require(raw is None, 'source-only field generation accepts no external proposal')
    gg=factors.factor('cap_field_gcd')
    den=z.divide(field['denominator'],gg)
    num=[[z.divide(poly,gg) for poly in row] for row in field['numerator']]
    require(z.mul(gg,den)==field['denominator'] and
            all(z.mul(gg,num[i][j])==field['numerator'][i][j] for i in range(3) for j in range(3)),
            'ALL9 source-only complete cap field divisions multiplied back')
    return gg,num,den


def signs(field):
    num,den=field['numerator'],field['denominator']
    gg,nn,dd=reduced_field(field)
    q4={(4,0):1}
    # Delta_cap + (1/(2q^4)) ss^T on its two original relevant directions.
    A=z.add(z.scale(z.mul(q4,num[0][0]),2),den)
    Ar=z.add(z.scale(z.mul(q4,nn[0][0]),2),dd)
    Br=z.add(z.scale(z.mul(q4,nn[0][1]),2),z.scale(dd,-1))
    Cr=z.add(z.scale(z.mul(q4,nn[1][1]),2),dd)
    require(z.mul(gg,Ar)==A, 'ENTIRE conservative leading principal compact identity')
    determinant=z.add(z.mul(Ar,Cr),z.scale(z.mul(Br,Br),-1))
    output={}
    for name,poly in (('leading00',A),('determinant2',determinant)):
        coeff=lower.quadrant(poly)
        output[name]={'entire_original_polynomial':lower.record(poly),
                      'entire_quadrant_coefficients':lower.record(coeff),
                      'negative_count':sum(v<0 for v in coeff.values()),
                      'positive_constant':coeff.get((0,0),0)>0,
                      'strict_positive_proved':bool(coeff) and all(v>=0 for v in coeff.values())
                                               and coeff.get((0,0),0)>0}
    output['complete_compact_factor_squared_for_determinant']=lower.record(z.mul(gg,gg))
    output['complete_conservative_compact_matrix2']=matrix_record([[Ar,Br],[Br,Cr]])
    output['determinant_sign_uses_nonzero_factor_square_only']=True
    output['raw_positive_denominator_is_twice_4D_times_survivors_times_two_squares']=True
    return output


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('field','signs'))
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    data,field=generated()
    math={'actual_agent':'six-downset-3','role':'researcher','exact_domain':'ALL integers k>=7,q>=3k',
          'complete_field':{key:matrix_record(value) if key in ('trivial_vectors','trivial_energies','numerator')
                            else [lower.record(poly) for poly in value] if key=='standard_vector'
                            else lower.record(value) for key,value in field.items()},
          'all_original_controls':r.encode(controls(data,field)),
          'all_compact_source_divisions_multiplied_back':True,
          'CAS_imported':False,'independent_review':False,'ordinary_mean_removal_and_fullspace_bridges_unformalized':True}
    if args.phase=='signs':math['whole_signs']=signs(field)
    args.out.write_text(json.dumps(math,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase':args.phase,'field_numerator_terms':[[len(poly) for poly in row] for row in field['numerator']],
                      'field_denominator_terms':len(field['denominator']),
                      'signs':{key:{name:value for name,value in sign.items()
                                   if name not in ('entire_original_polynomial','entire_quadrant_coefficients')}
                               for key,sign in math.get('whole_signs',{}).items() if key in ('leading00','determinant2')}}))
