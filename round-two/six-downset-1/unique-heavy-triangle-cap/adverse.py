"""Semantic damaged-input and BEFORE-construction guard controls.

Actual six-downset-1 / researcher, same-author testing, not review.
No original geometry beyond n4/counts4,3,2/N70 is constructed here.
The larger headers below are rejected before any family/metric allocation.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
from pathlib import Path
from fractions import Fraction as Q
import argparse
import copy
import importlib.util
import json
import signal
import tempfile

HERE=Path(__file__).resolve().parent

def module(filename,name):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

def main():
    def expire(a,b):
        raise TimeoutError('unchanged60s adverse guard; incomplete is not nonexistence')
    signal.signal(signal.SIGALRM,expire);signal.alarm(60)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    reader=module('reader.py','unique_heavy_reader_subject')
    producer=module('geometry.py','unique_heavy_preflight_subject')
    producer.barrier();reader.require(not args.out.exists(),'unique actual adverse output')
    good=reader.load(args.input)
    reader.require(good['n']==4 and good['counts']==[4,3,2] and good['N']==70,
                   'declared original asymmetric adverse control')
    rejected=[]
    def trial(name,fragment,fn):
        try:
            fn()
        except ValueError as e:
            reader.require(fragment in str(e),'intended semantic rejection: '+name)
            rejected.append(dict(name=name,reason=str(e),result='REJECTED'))
        else:
            raise ValueError('damaged input accepted: '+name)
    def changed(name,fragment,fn):
        bad=copy.deepcopy(good);fn(bad)
        trial(name,fragment,lambda:reader.check(bad))
    def set_item(key,index,value):
        return lambda v:v[key].__setitem__(index,value)
    def set_cell(key,i,j,value):
        return lambda v:v[key][i].__setitem__(j,value)
    changed('whole-schema extra omitted-bridge field','whole geometry schema',
            lambda v:v.__setitem__('unpaid_quotient',True))
    changed('boolean version','whole geometry schema',lambda v:v.__setitem__('version',True))
    changed('float literal family index','ENTIRE literal original family',set_item('family',1,1.0))
    changed('overlapped/relabelled private pair','ENTIRE literal original family',
            set_item('family',-1,good['family'][-2]))
    changed('omitted original row','whole matrix dimensions',lambda v:v['rows'].pop())
    changed('omitted physical direction','whole original dimensions/counts',
            lambda v:v.__setitem__('dimension',v['dimension']-1))
    changed('actual empty replaced by zeros','ACTUAL empty negative proper-row sum',
            set_item('rows',0,['0']*good['dimension']))
    changed('actual empty replaced by old empty','ACTUAL empty negative proper-row sum',
            set_item('rows',0,[str(-Q(x)) for x in good['rows'][1]]))
    changed('late light mean physical norm damaged','mandatory norm/intersection',
            set_cell('metric',21,21,str(Q(good['metric'][21][21])+1)))
    changed('late residual full physical norm damaged','mandatory norm/intersection',
            set_cell('metric',66,66,str(Q(good['metric'][66][66])+1)))
    changed('whole actual-loop centroid norm damaged','ACTUAL empty norm',
            lambda v:v.__setitem__('common_norm',str(Q(v['common_norm'])+1)))
    changed('late variable-count scalar field damaged','ALL variable-count original scalar fields',
            lambda v:v['group_scalars'][-1].__setitem__('nu',str(Q(v['group_scalars'][-1]['nu'])+1)))
    def unweighted(v):
        L=sum(v['counts'][1:])
        v['b']=[str(Q(1,L)) if Q(x) else '0' for x in v['b']]
    changed('unweighted light-full repair rejected','COUNT-WEIGHTED repair coefficients',unweighted)
    changed('late count-weighted dual score damaged','EVERY original dual score',
            set_item('dual_vector',66,'0'))
    changed('original inverse energy changed','weighted dual inverse energy',
            lambda v:v.__setitem__('kappa',str(Q(v['kappa'])+1)))
    changed('late noncanonical rational','exact canonical rational string',
            set_cell('rows',-1,-1,'0/1'))
    changed('late floating rational','exact canonical rational string',
            set_cell('metric',-1,-1,0.5))
    # Headers alone suffice: the reader's guard must precede row decoding.
    for name,n,counts,fragment in (
        ('first unequal four-mark N82',4,[4,3,2,2],'N80 parent guard BEFORE construction'),
        ('minimal original five-mark N98',5,[3,2,2,2,2],'N80 parent guard BEFORE construction'),
        ('balanced-four N88',4,[3,3,3,3],'unique heavy literal'),
        ('qualified original n5 N86',5,[4,3,2],'N80 parent guard BEFORE construction'),
        ('unqualified F7',4,[3,2,2],'qualified total F>=9'),
        ('literal h11',4,[11,2,2],'literal h<=10'),
        ('literal n7',7,[4,3,2],'literal n<=6'),
        ('boolean literal n',True,[4,3,2],'literal n<=6'),
        ('boolean literal count',4,[4,True,2],'count/mark types')):
        trial('reader BEFORE construction: '+name,fragment,lambda n=n,counts=counts:
              reader.literal(n,counts))
        trial('producer BEFORE construction: '+name,fragment,lambda n=n,counts=counts:
              producer.preflight(n,counts))
    trial('full leading-minor last pivot fails','exact positive leading minor',
          lambda:reader.positive([[Q(1),Q(2)],[Q(2),Q(1)]]))
    trial('full positive-form asymmetry','whole positive form symmetry',
          lambda:reader.positive([[Q(1),Q(0)],[Q(1),Q(1)]]))
    with tempfile.TemporaryDirectory(prefix='reader-float-',dir=args.out.parent) as path:
        target=Path(path)/'bad.json';target.write_text('{"bad":0.5}')
        trial('JSON floating parse rejected','floating input',lambda:reader.load(target))
        target.write_text('{"bad":NaN}')
        trial('JSON nonfinite parse rejected','floating input',lambda:reader.load(target))
    result=dict(agent='six-downset-1',role='researcher',status='COMPLETE SEMANTIC ADVERSE CONTROLS',
                control=dict(n=4,counts=[4,3,2],N=70),rejections=rejected,
                rejection_count=len(rejected),large_original_constructed=False,
                new_source_commit=None,new_graph_ref=None,independent_review=False)
    raw=json.dumps(result,indent=2).encode()+b'\n'
    reader.require(len(raw)<=reader.LIMIT_BYTES,'unchanged32MiB adverse output guard')
    args.out.write_bytes(raw);signal.alarm(0)
    print(json.dumps(dict(status=result['status'],rejection_count=len(rejected),
                         optimized=not __debug__)))

if __name__=='__main__':
    main()
