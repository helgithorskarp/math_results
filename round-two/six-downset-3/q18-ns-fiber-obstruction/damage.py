"""Same-author semantic rejection controls; no independent-review claim.

Scalar controls exercise the small claim checker against the sealed exact
record. Candidate/action controls freshly execute the corresponding exact
engine gates. Two factor controls are explicit small hand-checkable units.
Preimport controls separately prove source verification precedes data use.
Children run serially, with45s child and60s driver guards.
"""
from pathlib import Path
from time import monotonic
import argparse
import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
CASES={
    'candidate-short':'whole143 integer coefficients',
    'candidate-denominator':'named exact denominators',
    'comparison-alter':'entire attributed143 comparison list',
    'original-floor':'EVERY actual positive floor including loop',
    'physical-action':'new original physical action at EVERY coordinate',
    'factor-negative':'EVERY exact weighted lower-cone pivot',
    'factor-asymmetric':'EVERY exact complete factor identity',
    'tau-outside-premise':'stated real interval lies inside paid sharp-attainment premise',
    'tau-entry-floor':'uniform actual floor including the empty loop',
    'unpaid-proper-floor':'new full proper floor is paid by the weighted factors',
    'wrong-weights':'all81 literal weights match the claimed NS aggregate',
    'wrong-alpha':'literal maximum E2 product in the Schur budget',
    'unpaid-fiber-gap':'all-real fiber gap uses the original dual half factor',
    'wrong-norm-separator':'exact rational separators for both NS vector norms',
    'unpaid-vector-distance':'strict vector distance follows from the two norm separators',
    'unpaid-original-distance':'original NS movement pays all58 coordinates and the220 normalization',
}


def load_reader(root=ROOT):
    spec=importlib.util.spec_from_file_location('q18_reader',root/'verify.py')
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    return reader


def one_case(name):
    reader=load_reader();engine,manifest=reader.source_gate(ROOT)
    data=reader.read_inputs(ROOT,manifest)
    candidate=copy.deepcopy(data['CANDIDATE.json']);comparison=copy.deepcopy(data['COMPARISON.json'])
    claim=copy.deepcopy(data['CLAIM.json']);result=data['EXACT-RESULT.json']
    if name=='candidate-short':candidate['free_numerators'].pop()
    elif name=='candidate-denominator':candidate['denominator']=1<<31
    elif name=='comparison-alter':comparison['comparison_free_numerators'][-1]+=1
    elif name=='original-floor':candidate['free_numerators'][0]=-candidate['denominator']-1
    elif name=='physical-action':
        action=engine.image
        def damaged(C,v):
            col=action(C,v);col[-1]+=1;return col
        engine.image=damaged
    elif name=='factor-negative':engine.factor([[0]])
    elif name=='factor-asymmetric':engine.factor([[2,1],[0,2]])
    else:
        key,value={
            'tau-outside-premise':('tau_max','1/64'),
            'tau-entry-floor':('tau_max','1/128'),
            'unpaid-proper-floor':('proper_C_floor','1/1024'),
            'wrong-weights':('weights',['1/4','1/4','1/2']),
            'wrong-alpha':('alpha','1/8'),
            'unpaid-fiber-gap':('fiber_Delta_lower','1250'),
            'wrong-norm-separator':('optimizer_norm_upper','1'),
            'unpaid-vector-distance':('NS_vector_distance_lower','76'),
            'unpaid-original-distance':('original_NS_entry_distance_lower','1/600'),
        }[name]
        claim[key]=value;reader.validate_claim(claim,result)
        raise ValueError('CONTROL DID NOT REJECT: '+name)
    engine.check(candidate,comparison)
    raise ValueError('CONTROL DID NOT REJECT: '+name)


def controls():
    start=monotonic();env=os.environ.copy();env.update({k:'1' for k in THREADS})
    env['PYTHONDONTWRITEBYTECODE']='1';runs=[]
    def reject(name,cmd,gate,marker=None):
        timeout=min(45,60-(monotonic()-start))
        if timeout<=0:raise ValueError('60s serial rejection driver guard')
        began=monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=timeout)
        stderr=r.stderr.decode()
        if r.returncode==0 or r.stdout or 'ValueError:' not in stderr or gate not in stderr:
            raise ValueError('meaningful rejection failed: '+name+' '+stderr[-800:])
        if marker is not None and marker.exists():raise ValueError('untrusted engine was imported before source gate')
        runs.append({'defect':name,'optimized':'-O' in cmd,'seconds':monotonic()-began,
                     'meaningful_ValueError':True,'gate':gate,'no_success_output':True})
    for name,gate in CASES.items():
        for optimized in (False,True):
            reject(name,[sys.executable,'-I','-B']+(['-O'] if optimized else [])+
                   [str(ROOT/'damage.py'),'--case',name],gate)
    with tempfile.TemporaryDirectory(prefix='q18-fiber-source-') as td:
        cold=Path(td);marker=cold/'ENGINE-EXECUTED'
        for p in ROOT.iterdir():
            if p.is_file():shutil.copyfile(p,cold/p.name)
        # A deliberately malformed candidate would fail at JSON parsing if read.
        (cold/'CANDIDATE.json').write_text('{')
        (cold/'check.py').write_text((cold/'check.py').read_text()+
            "\nPath(__file__).with_name('ENGINE-EXECUTED').write_text('bad')\n")
        for optimized in (False,True):
            reject('source before malformed data and engine import',
                   [sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(cold/'verify.py')],
                   'whole sealed file changed: check.py',marker)
        shutil.copyfile(ROOT/'check.py',cold/'check.py')
        (cold/'PROOF.md').write_text((cold/'PROOF.md').read_text()+'\nUnpaid changed mathematical assertion.\n')
        for optimized in (False,True):
            reject('proof before malformed mathematical data',
                   [sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(cold/'verify.py')],
                   'whole sealed file changed: PROOF.md',marker)
    return {'actual_agent':'six-downset-3','role':'researcher','semantic_defects':len(CASES),
            'semantic_rejections':2*len(CASES),'preimport_source_rejections':4,
            'runs':runs,'elapsed_seconds':monotonic()-start,'native_threads':1,
            'serial_CPU_children':1,'child_guard_seconds':45,'driver_guard_seconds':60,
            'same_author_controls_not_independent_review':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=CASES);ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    if args.case:one_case(args.case)
    else:
        if args.out is None:raise ValueError('--out is required for the bounded driver')
        result=controls();args.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'semantic_rejections':result['semantic_rejections'],
                          'preimport_source_rejections':result['preimport_source_rejections'],
                          'seconds':result['elapsed_seconds']},sort_keys=True))
