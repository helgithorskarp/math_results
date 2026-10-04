"""Serial bounded normal/optimized/cold replays and mathematical fault controls."""
from pathlib import Path
import hashlib, json, os, resource, shutil, subprocess, sys, tempfile, time

HERE = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
DEFECT_GATES = {
 'mean-axis':'old real mean channel',
 'imaginary-axis':'old imaginary mean channel',
 'real-transverse':'ENTIRE twelve-dimensional old cost to axis cost',
 'imaginary-transverse':'ENTIRE twelve-dimensional old cost to axis cost',
 'cubic-factor':'complete cubic first jet, all eight slots',
 'second-tangent':'all second imaginary means',
 'third-real-sign':'entire higher primitive derivative column 7',
 'third-imag-sign':'entire higher primitive derivative column 6',
 'slack-weight':'physical even dual first response',
 'fourth-constant':'credited fourth constant',
 'kappa-sign':'credited common imaginary weight',
 'normal-factor':'actual half-normal slack normalization'}


def main():
    if len(sys.argv)!=2:
        raise RuntimeError('usage: python validate.py OUTPUT_DIRECTORY')
    out = Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ);env.update({n:'1' for n in THREADS})
    manifest = json.loads((HERE/'SOURCE.json').read_text())
    for name,pin in manifest['mathematical_files'].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=pin:
            raise RuntimeError('validator pre-import source hash '+name)
    rows = []

    def run(label, directory, options, gate=None, optimized=False):
        command = [sys.executable]+(['-O'] if optimized else [])+[str(directory/'verify.py'),*options]
        start = time.monotonic()
        p = subprocess.run(command,cwd=directory,env=env,stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,timeout=45)
        elapsed = time.monotonic()-start
        if gate is None:
            if p.returncode!=0:
                raise RuntimeError(label+': '+p.stderr.decode())
        elif p.returncode==0 or gate not in p.stderr.decode():
            raise RuntimeError(label+': defect not rejected at intended mathematical/source gate')
        rows.append({'label':label,'seconds':round(elapsed,6),'exit_code':p.returncode,
                     'status':'PASS' if gate is None else 'EXPECTED_REJECTION','gate':gate})
        return p

    reference = None
    for optimized in (False,True):
        f = out/('local-O.json' if optimized else 'local.json')
        run('local optimized' if optimized else 'local',HERE,['--output',str(f)],optimized=optimized)
        data = f.read_bytes()
        if reference is None:
            reference = data
        elif reference!=data:
            raise RuntimeError('entire local record differs')
    with tempfile.TemporaryDirectory(prefix='full-cap-cold-',dir=out) as directory:
        cold = Path(directory)
        for name in ('arithmetic.py','verify.py','EXPECTED.json','SOURCE.json'):
            shutil.copyfile(HERE/name,cold/name)
        for optimized in (False,True):
            f = out/('cold-O.json' if optimized else 'cold.json')
            run('cold optimized' if optimized else 'cold',cold,['--output',str(f)],optimized=optimized)
            if f.read_bytes()!=reference:
                raise RuntimeError('entire cold record differs')
        for name,gate in DEFECT_GATES.items():
            # These switches alter whole mathematical inputs, not only digests;
            # the expected-output comparison is deliberately disabled.
            run('mathematical defect '+name,cold,['--without-expected','--defect',name],gate,True)
        for name in ('arithmetic.py','verify.py'):
            original = (cold/name).read_bytes()
            (cold/name).write_bytes(original+b'\n# deliberate unsealed mathematical source damage\n')
            run('unsealed source '+name,cold,[], 'pre-import source hash: '+name,True)
            (cold/name).write_bytes(original)
        f = out/'final-cold.json'
        run('final cold',cold,['--output',str(f)])
        if f.read_bytes()!=reference:
            raise RuntimeError('entire final cold record differs')
    result = {'agent':'six-sendov-3','role':'researcher','python':sys.version.split()[0],
              'scope':'Exact finite coordinate/higher-trace corroboration; ordinary actual uniform bridges remain credited premises.',
              'source_hashes':manifest['mathematical_files'],'whole_record_bytes':len(reference),
              'whole_record_sha256':hashlib.sha256(reference).hexdigest(),
              'complete_record_bytes_compared':True,'replays':rows,'threads':{n:1 for n in THREADS},
              'one_cpu_child_at_a_time':True,'per_child_timeout_seconds':45,
              'max_completed_seconds':max(r['seconds'] for r in rows),
              'cumulative_child_peak_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'resource_limited':False,'mathematical_rejections':len(DEFECT_GATES),'source_rejections':2}
    (out/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','whole_bytes':len(reference),'whole_sha256':result['whole_record_sha256'],
                      'replays':5,'mathematical_rejections':len(DEFECT_GATES),'source_rejections':2,
                      'max_seconds':result['max_completed_seconds'],'peak_kib':result['cumulative_child_peak_kib']}),flush=True)


if __name__ == '__main__':
    main()
