"""Meaningful postbinding mathematical controls; same author, not review.

Each mutation is rejected by its designated original/count/shift identity.
Only arithmetic modules pinned by SOURCE are imported. Deliberate in-memory
formula changes simulate defects after source binding; restore every one.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
import importlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

HERE = Path(__file__).resolve().parent
EARLY = ('geometry.py','upper_reader.py','shift_reader.py','symbolic.py',
         'reader.py','adverse.py','reproduce.py','PROOF.md','README.md',
         'DEPENDENCIES.json','PROVENANCE.json')
sys.dont_write_bytecode = True


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pins_before_import():
    pins = json.loads((HERE/'SOURCE.json').read_bytes())
    require(set(pins['early']) == set(EARLY), 'whole early source census')
    for name in EARLY:
        raw = (HERE/name).read_bytes()
        require(dict(bytes=len(raw),sha256=sha256(raw).hexdigest())==pins['early'][name],
                'source pin mismatch ' + name)
    sys.path.insert(0,str(HERE))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    require(not args.out.exists(),'unique adverse output')
    def expire(_signal,_frame):
        raise TimeoutError('unchanged60s; incomplete is not mathematical absence')
    signal.signal(signal.SIGALRM,expire);signal.alarm(60)
    started=time.monotonic();pins_before_import()
    geometry,upper,shift,symbolic=[importlib.import_module(name) for name in
                                  ('geometry','upper_reader','shift_reader','symbolic')]
    data=geometry.build(4,[4,3,2]);eps=F(1,4096);records=[]
    def reject(name,call,needle,classification='mathematical'):
        try:
            call()
        except ValueError as error:
            message=str(error)
            require(needle in message,'designated semantic rejection '+name+': '+message)
            records.append(dict(name=name,classification=classification,rejected=True,
                                designated_error=message))
        else:
            raise ValueError('mutation accepted: '+name)
    def damaged(name,modify,needle):
        item=deepcopy(data);modify(item)
        reject(name,lambda:upper.read(item),needle)
    def at(item,key,i,j,amount):
        if j is None:
            item[key][i]=str(F(item[key][i])+amount)
        else:
            item[key][i][j]=str(F(item[key][i][j])+amount)
    proper_private=2**4-1+3*sum(data['counts'])
    damaged('heavy weights retain sum, wrong standard projection',
            lambda x:(at(x,'a',proper_private,None,eps),at(x,'a',proper_private+1,None,-eps)),
            'three new count scalars')
    first_light=proper_private+3*data['counts'][0]+2
    damaged('light full weights retain sum, wrong facet projection',
            lambda x:(at(x,'b',first_light,None,eps),at(x,'b',first_light+3,None,-eps)),
            'three new count scalars')
    damaged('actual empty original row',lambda x:at(x,'rows',0,0,eps),
            'complete original constant action')
    coordinate=data['retained_dimension']
    damaged('heavy mean metric diagonal',lambda x:at(x,'metric',coordinate,coordinate,eps),
            'three new count scalars')
    cross=coordinate+data['counts'][0]
    damaged('whole cross-group mean metric',
            lambda x:(at(x,'metric',coordinate,cross,eps),at(x,'metric',cross,coordinate,eps)),
            'three new count scalars')
    wf=coordinate+data['F']-1+1+2*data['counts'][0]
    damaged('private WF trace metric',lambda x:at(x,'metric',wf,wf,eps),
            'three new count scalars')
    tcoordinate=(2**4-1)+(data['counts'][0]-1)+sum(data['counts'][1:])
    light_t=tcoordinate+2*data['counts'][0]
    damaged('entire light T trace off-diagonal',
            lambda x:(at(x,'metric',light_t,light_t+1,eps),at(x,'metric',light_t+1,light_t,eps)),
            'three new count scalars')
    damaged('credited lower boundary scalar',
            lambda x:x.__setitem__('kappa',str(F(x['kappa'])+eps)),
            'credited lower-bound scalar identification')
    original_count=upper.count_formula
    for key in ('Abar','Bbar','Cbar'):
        def formula(n,counts,key=key):
            result=original_count(n,counts);result[key]+=eps;return result
        upper.count_formula=formula
        try:
            reject('wrong count numerator '+key,lambda:upper.read(deepcopy(data)),
                   'three new count scalars' if key!='Cbar' else 'three new count scalars')
        finally:
            upper.count_formula=original_count
    original_solve=upper.full_positive_solve
    def wrong_image(form,rhs,original_centered=True):
        images,record=original_solve(form,rhs,original_centered)
        images[0][1]+=eps;images[0][2]-=eps
        return images,record
    upper.full_positive_solve=wrong_image
    try:
        reject('inverse image defect outside A/B support',lambda:upper.read(deepcopy(data)),
               'whole original algebraic endpoint kernel')
    finally:
        upper.full_positive_solve=original_solve
    original_shift=shift.count_shift
    for index,label in ((0,'w'),(1,'z'),(2,'g'),(3,'sigma')):
        def wrong_shift(q,h,counts,theta,index=index):
            result=list(original_shift(q,h,counts,theta));result[index]+=eps;return tuple(result)
        shift.count_shift=wrong_shift
        try:
            reject('wrong shifted '+label,lambda:shift.read(deepcopy(data)),
                   'whole original FIRST Schur-square identity' if index==3 else
                   'three count shifts equal FULL original FIRST inverse products')
        finally:
            shift.count_shift=original_shift
    bad=deepcopy(data);bad['N']=81
    reject('N80 before original construction',lambda:upper.read(bad),
           'original N80 preflight','preflight')
    bad=deepcopy(data);bad['counts'][0]=11
    reject('h10 before original construction',lambda:upper.read(bad),
           'literal unique-heavy h/count preflight','preflight')
    bad=deepcopy(data);bad['counts'][1]=bad['counts'][0]
    reject('unique-heavy domain before construction',lambda:upper.read(bad),
           'literal unique-heavy h/count preflight','preflight')
    result=dict(agent='six-downset-1',role='researcher',status='DESIGNATED SEMANTIC CONTROLS COMPLETE',
                records=records,rejection_count=len(records),
                mathematical_rejections=sum(r['classification']=='mathematical' for r in records),
                preflight_rejections=sum(r['classification']=='preflight' for r in records),
                independently_reviewed=False,large_original_constructed=False)
    raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n'
    args.out.write_bytes(raw);signal.alarm(0)
    print(json.dumps(dict(status=result['status'],rejections=len(records),
                         mathematical_bytes=len(raw),mathematical_sha256=sha256(raw).hexdigest(),
                         seconds=time.monotonic()-started,
                         peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__=='__main__':
    main()
