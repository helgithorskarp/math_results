#!/usr/bin/env python3
"""Optional SHA-pinned author replay and generic coefficient comparison.

Usage: python3 -I -B compare_author.py ANGULAR_DIR OPTIMIZER_DIR
The primary independent_check.py never imports either author implementation.
"""
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from io import StringIO
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
def load(name,path):
    spec=spec_from_file_location(name,path);module=module_from_spec(spec)
    spec.loader.exec_module(module);return module
native=load('review3_native',HERE/'independent_check.py')
P,M,MI=native.P,native.M,native.MI
def demand(ok,label):
    if not ok:raise ValueError(label)
def from_record(rows):
    return P({tuple(row[:native.NV]):F(row[native.NV],row[native.NV+1]) for row in rows})

PINNED={
 'angular':{
  'verify.py':'bdc9dac2f768ece3e8f5492219cf4356ca59526ebbe1b8ce9d3bb4200726cc91',
  'algebra.py':'d5c527d1fda16a409af3f299c1b80a24f07da74a91451de45e062e7a350750be',
  'expected.json':'fe0589381ab2d03f8945d248633069480a7dc33a18af81ad2da0d5a8ce1545c6'},
 'optimizer':{
  'verify.py':'6dd9ea921af48f1ab5ae35dc56880eb3c32d196b98dbe5ce85f38c50310b9419',
  'expected.json':'ac5a0af11df1926bd7447a8f88333cfe9a8282a24b21cd0aba146033c5c74a2c'}}

def replay(label,directory):
    for filename,digest in PINNED[label].items():
        demand(sha256((directory/filename).read_bytes()).hexdigest()==digest,
               label+' pinned source: '+filename)
    author=load('review3_'+label,directory/'verify.py');captured={}
    def profile(frame,event,arg):
        if event=='return' and frame.f_code is author.run.__code__:
            captured.update(frame.f_locals)
    sys.setprofile(profile)
    try:result=author.run()
    finally:sys.setprofile(None)
    stream=StringIO()
    with redirect_stdout(stream):author.main()
    manifest=json.loads(stream.getvalue())
    demand(manifest['checks']==result['checks'],'replay manifest checks')
    return author,captured,manifest

def angular_rf(rf):
    terms={}
    for (a,b),coefficient in rf.p.t.items():
        demand(b==0,'unused multiplicity indeterminate')
        e=list(native.ZE);e[0]=a;terms[tuple(e)]=coefficient
    denominator=M**rf.d[0]*(3*M+2)**rf.d[1]*(M+2)**rf.d[2]
    return P(terms),denominator

def optimizer_rf(rf):
    terms={}
    for (a,b,c,d),coefficient in rf.p.t.items():
        demand(c%2==0 and d==0,'even skewness and unused shift indeterminate')
        e=list(native.ZE);e[0]=a;e[7]=b;e[8]=c//2;terms[tuple(e)]=coefficient
    denominator=M**rf.d[0]*(M-1)**rf.d[1]*(M-2)**rf.d[2]*(M-3)**rf.d[3]
    return P(terms),denominator

def main():
    demand(len(sys.argv)==3,'provide angular and optimizer source directories')
    angular=Path(sys.argv[1]).resolve();optimizer=Path(sys.argv[2]).resolve()
    aa,ac,am=replay('angular',angular)
    oa,oc,om=replay('optimizer',optimizer)
    scalar=native.scalar_characteristic();gram=native.concentration();checks=[]
    def compare(label,left,right):
        native.cutoff_zero('author comparison '+label,left-right);checks.append(label)
    fourth=from_record(scalar['F4_before_cutoff'])
    for key,name,degree in [('mu4','mu4',1),('mu2square','mu2',2),('Psi','psi',1)]:
        numerator,denominator=angular_rf(ac['closed'][key])
        compare('F4 '+key,fourth.coef(name,degree)*denominator,numerator)
    for ell in (2,3,4):
        coefficients={key:angular_rf(value) for key,value in ac['computed'][ell].items()}
        common=native.product(d for _,d in coefficients.values())
        weights={
          'mu4':{'T4':1-4*MI,'U':MI,'R2':P()},
          'mu2square':{'T4':2*MI**2,'U':-MI**2,'R2':MI**2}}
        own=from_record(scalar['M'+str(ell)+'_fourth'])
        for key,name,degree in [('mu4','mu4',1),('mu2square','mu2',2)]:
            assembled=P()
            for basis,(numerator,denominator) in coefficients.items():
                other=native.product(d for b,(_,d) in coefficients.items() if b!=basis)
                assembled=assembled+numerator*weights[key][basis]*other
            compare('M'+str(ell)+' fourth '+key,own.coef(name,degree)*common,assembled)
    D=from_record(gram['D_numerator']);N=from_record(gram['N_numerator'])
    own={
      'gram_d':(D,M**2*(M-1)*(M-2)),
      'gram_n':(N,M*(M-1)*(M-2)),
      'base':((M-2)+M*(M-1)*native.Z,(M-1)*(M-2)),
      'ell':(M*(M-1)*native.X-(2*M-3),(M-2)*(M-3)),
      't4':(M*(M-4)*native.X+2,M**2)}
    for key,(numerator,denominator) in own.items():
        an,ad=optimizer_rf(oc[key])
        compare('Gram '+key,numerator*ad,an*denominator)
    output={
      'reviewer':'six-reviewer-3','role':'independent mathematical reviewer',
      'generic_entrywise_comparisons':len(checks),'labels':checks,
      'author_angular_checks':am['checks'],
      'author_angular_rejected_mutations':len(am['rejected_mutations']),
      'author_optimizer_checks':om['checks'],
      'author_optimizer_rejected_mutations':len(om['rejected_mutations']),
      'comparison_arithmetic':'independent Laurent polynomials; exact cutoff denominator clearing',
      'author_replay_is_independence_evidence':False}
    expected=HERE/'author_comparison_expected.json'
    if expected.exists():
        demand(json.loads(expected.read_text())==output,'generic comparison manifest differs')
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=='__main__':main()
