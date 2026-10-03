"""Bounded serial normal/-O checks and mathematical source damage controls."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ENV = dict(os.environ)
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    ENV[key] = '1'
WRAPPER = "import runpy,resource,sys,json\ntry:\n runpy.run_path(sys.argv[1],run_name='__main__')\nfinally:\n print('RESOURCE '+json.dumps({'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),file=sys.stderr)"


def child(path, optimized):
    start = time.monotonic()
    cmd = [sys.executable]+(['-O'] if optimized else [])+['-B','-c',WRAPPER,str(path)]
    p = subprocess.run(cmd,env=ENV,text=True,capture_output=True,timeout=45)
    resource_lines = [s for s in p.stderr.splitlines() if s.startswith('RESOURCE ')]
    if len(resource_lines) != 1:
        raise ValueError('missing resource receipt')
    return p, {'seconds':time.monotonic()-start,
               **json.loads(resource_lines[0][9:])}


def main():
    expected = json.loads((HERE/'SUMMARY.json').read_text())
    runs = []
    source = (HERE/'audit.py').read_text()
    damages = [
        ('omit_cross_contact','{edge(7, 12), edge(9, 10)}','{edge(9, 10)}','literal12/20'),
        ('wrong_P_order','P = (5, 7, 12, 10, 9)','P = (5, 7, 10, 12, 9)','unique oriented map'),
        ('erase_V','V = G20 | {edge(5,12)}','V = G20','unique oriented map'),
        ('reuse_core_corner','fresh = 3','fresh = 7','unique oriented map'),
        ('omit_strict_diagonal','if edge(7, 9) in chosen:','if False and edge(7, 9) in chosen:',
         'two complete necessary subdivisions'),
        ('incomplete_partition_cohort','if len(p) <= 8','if len(p) <= 7','partition scope'),
        ('wrong_residual_boundary','R = (7, 0, 6, 11, 9, 10, 2, 8, 4, 1, 12)',
         'R = (7, 0, 4, 11, 9, 10, 2, 8, 6, 1, 12)','full11-boundary'),
        ('wrong_upper_angle','F(8, 13)','F(3, 4)','whole strict angle/rhombus budget'),
        ('wrong_G24_edge_count',"('G24',13,24,11,1,0)","('G24',13,23,11,1,0)",
         'complete residual side incidence'),
        ('false_triangle_adjacency','len(triangles[i]&triangles[j]) == 2',
         'len(triangles[i]&triangles[j]) == 1','full triangle dual'),
    ]
    for opt in (False,True):
        p,stats = child(HERE/'audit.py',opt)
        if p.returncode or json.loads(p.stdout) != expected:
            raise ValueError('whole normal/O summary mismatch '+p.stderr)
        runs.append({'case':'baseline','optimized':opt,'status':'PASS',**stats})
    with tempfile.TemporaryDirectory(prefix='g20-independent-damages-') as temp:
        dst = Path(temp)/'audit.py'
        for name,before,after,diagnostic in damages:
            if source.count(before) != 1:
                raise ValueError('ambiguous mathematical damage '+name)
            dst.write_text(source.replace(before,after))
            for opt in (False,True):
                p,stats = child(dst,opt)
                if p.returncode == 0 or diagnostic not in p.stderr:
                    raise ValueError('damage not rejected at intended guard '+name+': '+p.stderr)
                runs.append({'case':name,'optimized':opt,'status':'REJECTED',
                             'diagnostic':diagnostic,**stats})
    # Complete-record damage and valid representation controls are evaluated
    # against the independent generator, not target fixtures.
    import copy
    import audit
    record = audit.whole_record()
    bad = []
    q = copy.deepcopy(record);q['pentagon_cases'].pop();bad.append(q)
    q = copy.deepcopy(record);q['fresh_core_candidates'].pop();bad.append(q)
    q = copy.deepcopy(record);q['residual_budgets'][2]['TQP'][0]=1;bad.append(q)
    q = copy.deepcopy(record);q['profiles']['assignments'][0]['V_possible']=True;bad.append(q)
    q = copy.deepcopy(record);q['G24_triangle_dual_edges'].pop();bad.append(q)
    q = copy.deepcopy(record);q['strict_margins']['9lo-square-2lo-1']='0';bad.append(q)
    for q in bad:
        try:audit.verify(q)
        except ValueError as e:
            if 'complete typed record mismatch' not in str(e):raise
        else:raise ValueError('whole record damage accepted')
    faces = [tuple(f) for f in record['G24']['faces']]
    graph = {tuple(e) for e in record['G24']['edges']}
    normal = audit.sphere_map(graph,faces)
    rotated = audit.sphere_map(graph,[f[i%len(f):]+f[:i%len(f)] for i,f in enumerate(faces)])
    if normal != rotated:raise ValueError('cyclic face normalization')
    reverse = audit.sphere_map(graph,[tuple(reversed(f)) for f in faces])
    if [audit.unoriented(tuple(f)) for f in sorted(reverse['faces'],key=lambda f:audit.unoriented(tuple(f)))] != \
       [audit.unoriented(tuple(f)) for f in sorted(normal['faces'],key=lambda f:audit.unoriented(tuple(f)))]:
        raise ValueError('whole reversal control')
    audit.verify(json.loads(json.dumps(record,sort_keys=True)))
    print(json.dumps({'status':'PASS','serial':True,'guard_seconds':45,'native_threads':1,
                      'python':sys.version,'runs':runs,'source_damages_each_mode':len(damages),
                      'whole_record_damages':len(bad),'valid_representation_controls':3,
                      'whole_record_sha256':expected['whole_record_sha256']},sort_keys=True))


if __name__ == '__main__':main()
