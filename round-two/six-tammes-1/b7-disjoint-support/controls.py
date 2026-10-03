"""Arithmetic, physical distinctness, and once-verified record controls.

Both baselines run full geometry once. Projection damage tests subsequently
compare with those fresh baselines; they do not rerun geometry per damage.
The shared-self witness additionally goes through the full sparse auditor.
"""
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import argparse,json

import check as dense
import audit as sparse


def need(ok,why):
    if not ok:raise ValueError(why)


def rejected(call,why):
    try:call()
    except (ValueError,KeyError,TypeError,IndexError):return
    raise ValueError('control accepted: '+why)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',default='CERTIFICATE.json');args=parser.parse_args()
    data=json.loads(Path(args.certificate).read_text())
    baseline=dense.build();audited=sparse.audit(data)
    dense.compare_frozen(data,baseline);sparse.compare_frozen(data,audited)
    arithmetic=[]
    def record(name,ok):need(ok,name);arithmetic.append(name)

    vectors=((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1)),(F(1,3),F(2,3),F(2,3)))
    gram=[[sum(a*b for a,b in zip(u,v)) for v in vectors] for u in vectors]
    record('four-vector rank-three Gram vanishes',not dense.det([[[v] for v in row] for row in gram]) and not sparse.determinant([[sparse.P(v) for v in row] for row in gram]))
    eye=[[[F(int(i==j))] for j in range(4)] for i in range(4)]
    record('rank-four identity determinant is one',dense.det(eye)==[F(1)] and sparse.determinant([[sparse.P(int(i==j)) for j in range(4)] for i in range(4)])==sparse.P(1))
    record('Bareiss retains row-exchange orientation',sparse.determinant([[{},sparse.P(1)],[sparse.P(1),{}]])==sparse.P(-1))
    first=([F(1)],[],[F(-1)]);second=([F(1)],[F(-2)],[F(1)])
    to_sparse=lambda p:{i:v for i,v in enumerate(p) if v}
    record('quadratic common root keeps zero resultant',not dense.result(first,second) and not sparse.resultant(tuple(map(to_sparse,first)),tuple(map(to_sparse,second))))
    first=([],[F(1)],[]);second=([],[F(1)],[F(-1)])
    record('padded degree drop is retained even without common root',not dense.result(first,second) and not sparse.resultant(tuple(map(to_sparse,first)),tuple(map(to_sparse,second))))
    z,_=sparse.strip(sparse.P(0,0,1))
    record('sparse zeros remain absent after positive-factor strip',z==sparse.P(1) and sparse.stripped_cached(('0','0','1'))[0]==('1',))
    q,rem=sparse.quotient(sparse.P(0,0,1),sparse.R)
    record('whole sparse division with leading zero coefficients',q==sparse.R and not rem)
    p=[F(1),F(1)];iv=dense.inverse_h(p)
    record('quadratic-field inverse is coefficientwise exact',dense.mod_h(dense.mul(p,iv))==[F(1)] and sparse.mod_h(sparse.times(sparse.P(1,1),sparse.inverse_h(sparse.P(1,1))))==sparse.P(1))
    rejected(lambda:dense.inverse_h(dense.H),'zero quadratic-field denominator, dense')
    rejected(lambda:sparse.inverse_h(sparse.H),'zero quadratic-field denominator, sparse')
    arithmetic.append('both zero field denominators reject')
    record('exceptional parameter retains exact closed-band equation',dense.add([F(0),F(0),F(3)],dense.neg(dense.mul(dense.D,dense.D)))==[2*v for v in dense.H])
    midpoint=(dense.LO+dense.HI)/2
    positive=dense.add([F(1)],dense.mul([-midpoint,F(1)],[-midpoint,F(1)]))
    record('positive polynomial passes both enclosure mechanisms',dense.sign(positive)==1 and sparse.positive(to_sparse(positive)))
    endpoint=[-dense.LO,F(1)]
    record('closed-endpoint zero is never a strict sign',dense.sign(endpoint)==0 and not sparse.positive(to_sparse(endpoint)))
    record('identically zero is not strict nonexistence',dense.sign([])==0 and not sparse.positive({}))
    for eps in (-1,1):
        need(dense.positive_radical([F(-2)],[F(1)],[F(1)],eps,dense.LO,dense.HI) is None,'negative radical sum never selected')
        for method in ('same_positive','constant_dominates','radical_dominates'):
            rejected(lambda e=eps,m=method:sparse.radical_positive(sparse.P(-2),sparse.P(1),sparse.P(1),e,m,sparse.LO,sparse.HI),'unsigned-squaring sign guard')
    arithmetic.append('both radical signs reject invalid unsigned squaring')
    rejected(lambda:sparse.radical_positive({},sparse.P(1),{},1,'radical_dominates',sparse.LO,sparse.HI),'tangent zero is not a strict positive radical')
    arithmetic.append('tangent zero remains unresolved by strict radical guard')
    seen=[]
    complete=[{'path':'0'},{'path':'1'}]
    sparse.leaves_cover(complete,sparse.LO,sparse.HI,lambda leaf,a,b:seen.append((a,b)) or {})
    record('two closed half cells include their common boundary',seen==[(sparse.LO,(sparse.LO+sparse.HI)/2),((sparse.LO+sparse.HI)/2,sparse.HI)])
    rejected(lambda:sparse.leaves_cover([{'path':'0'}],sparse.LO,sparse.HI,lambda *args:{}),'missing half')
    rejected(lambda:sparse.leaves_cover([{'path':''},{'path':'0'}],sparse.LO,sparse.HI,lambda *args:{}),'nested overlapping cover')
    arithmetic.append('incomplete and non-prefix-free covers reject')

    # Complete geometric audit, rather than merely a record comparison.
    bad=deepcopy(data);branch=bad['other_four_fibers'][0]
    parent=json.loads(Path(__file__).with_name('PARENT.json').read_text())
    row=parent['overlap_rows'][branch['row']];shared=(20,21,22)[row[1:].index(branch['ear'])]
    branch['cover'][0]['pair']=[branch['ear'],shared]
    rejected(lambda:sparse.audit(bad),'shared point compared with itself')
    arithmetic.append('full fresh sparse audit rejects shared-self packing witness')

    damages=[]
    def damage(name,mutate):
        bad=deepcopy(data);mutate(bad)
        rejected(lambda:dense.compare_frozen(bad,baseline),name+' dense projection')
        rejected(lambda:sparse.compare_frozen(bad,audited),name+' sparse projection')
        damages.append(name)
    damage('widen closed cosine band',lambda x:x['closed_cosine_band'].__setitem__(0,'1/2'))
    damage('drop closed r endpoint',lambda x:x['closed_r_band'].__setitem__(0,'701/1000'))
    damage('corrupt entire parent digest',lambda x:x.__setitem__('parent_certificate_sha256','0'*64))
    damage('delete shared6 case',lambda x:x['shared6'].pop())
    damage('drop a literal overlap row',lambda x:x['shared6'][0]['rows'].pop())
    zero=next(i for i,a in enumerate(data['shared6']) if a['method']=='continuous_core_alias')
    damage('turn continuous zero resultant into strict sign',lambda x:x['shared6'][zero].update(method='nonzero_resultant',sign=1))
    damage('change distinct-label alias',lambda x:x['shared6'][zero].__setitem__('alias',[9,4]))
    forced=next(i for i,a in enumerate(data['shared6']) if 'basis_sign' in a)
    damage('reverse forced basis sign',lambda x:x['shared6'][forced].__setitem__('basis_sign',-x['shared6'][forced]['basis_sign']))
    quadratic=next(i for i,a in enumerate(data['shared6']) if a['method']=='quadratic_core_alias')
    damage('reverse exceptional cofactor sign',lambda x:x['shared6'][quadratic].__setitem__('cofactor_sign',-x['shared6'][quadratic]['cofactor_sign']))
    isolated=next(i for i,a in enumerate(data['shared6']) if a['method']=='isolated_packing')
    damage('crop unresolved root cell',lambda x:x['shared6'][isolated]['cell'].__setitem__(0,'3/4'))
    damage('omit outside root cover leaf',lambda x:x['shared6'][isolated]['outside_covers'][0].pop())
    damage('delete complete sphere orientation',lambda x:x['other_four_fibers'].pop())
    damage('duplicate sphere orientation',lambda x:x['other_four_fibers'].append(deepcopy(x['other_four_fibers'][0])))
    damage('reverse epsilon without its witnesses',lambda x:x['other_four_fibers'][0].__setitem__('eps',-x['other_four_fibers'][0]['eps']))
    damage('replace integer chi by boolean',lambda x:x['other_four_fibers'][0].__setitem__('chi',True))
    damage('replace integer row by float',lambda x:x['other_four_fibers'][0].__setitem__('row',float(x['other_four_fibers'][0]['row'])))
    damage('corrupt radicand coefficient',lambda x:x['other_four_fibers'][0]['radicand'].__setitem__(0,'1'))
    split=next(i for i,a in enumerate(data['other_four_fibers']) if len(a['cover'])>1)
    damage('delete half of packing cover',lambda x:x['other_four_fibers'][split]['cover'].pop())
    damage('corrupt polynomial gap fingerprint',lambda x:x['other_four_fibers'][0]['cover'][0].__setitem__('gap_digest','0'*64))
    damage('use unchecked radical guard',lambda x:x['other_four_fibers'][0]['cover'][0].__setitem__('method','unsigned_square'))
    damage('use actual shared-self pair',lambda x:x['other_four_fibers'][0]['cover'][0].__setitem__('pair',[branch['ear'],shared]))
    damage('drop necessary closed-J map',lambda x:x['full_band_disjoint_maps'].pop())
    damage('drop necessary strict-improvement map',lambda x:x['strict_improvement_disjoint_maps'].pop())
    damage('change physical-cohort application scope',lambda x:x.__setitem__('physical_scope','global optimizer'))
    damage('change literal distinctness scope',lambda x:x.__setitem__('literal_scope','coincident labels allowed'))
    damage('add unknown field',lambda x:x.__setitem__('unchecked',1))
    valid=[json.loads(json.dumps(data)),json.loads(json.dumps(data,indent=4,sort_keys=False)),dict(reversed(list(data.items())))]
    for x in valid:dense.compare_frozen(x,baseline);sparse.compare_frozen(x,audited)
    print(dense.canonical({'status':'PASS','actual_author':'six-tammes-1','role':'researcher',
          'whole_certificate_sha256':sha256(dense.canonical(data).encode()).hexdigest(),
          'complete_geometry_baselines':2,'full_sparse_shared_self_rejection':True,
          'arithmetic_controls':arithmetic,'arithmetic_control_count':len(arithmetic),
          'once_verified_projection_damages':damages,'projection_damage_count':len(damages),
          'valid_representation_count':len(valid),
          'limitation':'Geometry rebuilt once per baseline and for the shared-self damage; other damaged records compared to those freshly checked references, not separate full arithmetic reruns; all programs same author; independent review/formalization pending'}).strip())


if __name__=='__main__':main()
