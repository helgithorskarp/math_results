"""Bounded serial semantic controls and cold whole-source normal/O replay."""
import argparse,copy,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
P=pathlib.Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
def child(where,mode=False,program='verify.py'):
    env=os.environ.copy();env.update({x:'1' for x in THREADS});cmd=[sys.executable,'-I','-B']+(['-O'] if mode else [])+[str(where/program)]
    start=time.monotonic();r=subprocess.run(cmd,cwd=where,capture_output=True,text=True,env=env,timeout=45)
    return r,time.monotonic()-start

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=pathlib.Path(args.out).resolve()
    if P in out.parents:raise ValueError('generated validation must remain outside source')
    sys.path.insert(0,str(P));import face,bridges
    cases=[];start=time.monotonic();base=json.loads((P/'COVER.json').read_text());record=None
    for mode in (False,True):
        r,seconds=child(P,mode)
        if r.returncode:raise ValueError('positive failed '+r.stderr)
        row=json.loads(r.stdout)
        if record is None:record=row
        if row!=record:raise ValueError('WHOLE positive records differ')
        cases.append(dict(case='local-O' if mode else 'local',status='PASS',seconds=seconds))
    def reject(name,fn):
        try:fn()
        except ValueError as e:cases.append(dict(case=name,status='REJECT',reason=str(e)));return
        raise ValueError('semantic fault accepted '+name)
    def datafault(name,edit):
        d=copy.deepcopy(base);edit(d);reject(name,lambda:face.make(d))
    datafault('missing-leaf',lambda d:d['leaves'].pop(next(iter(d['leaves']))))
    datafault('orphan-leaf',lambda d:d['leaves'].update({'1'*30:'standard-polar'}))
    datafault('boolean-axis',lambda d:d['splits'][''].update(axis=True))
    datafault('noncanonical-cut',lambda d:d['splits'][''].update(cut='1.0'))
    datafault('floating-root',lambda d:d['root'].__setitem__(0,0.675))
    datafault('changed-closed-endpoint',lambda d:d['root'].__setitem__(1,'2/3'))
    datafault('missing-coordinate',lambda d:d['root'].pop())
    datafault('unknown-role',lambda d:d['leaves'].__setitem__(next(iter(d['leaves'])),'unpaid'))
    datafault('parent-endpoint-cut',lambda d:d['splits'][''].update(cut=d['root'][2*d['splits']['']['axis']]))
    datafault('split-leaf-duplicate',lambda d:d['leaves'].update({'':'standard-polar'}))
    reject('negative-root-domain',lambda:face.root(face.Q(-1),4096,True))
    reject('undeclared-polynomial-degree',lambda:face.bernstein([face.Q(0)]*14,face.Q(0),face.Q(1),12))
    reject('unpaid-polar-phase',lambda:face.standard_polar(dict(A=face.Q(27,40),B=face.Q(11,16),tl=face.Q(0),th=face.Q(1),F1=face.Q(8)),face.Q(-1)))
    reject('larger-unpaid-gap',lambda:bridges.payment(face.Q(1,8500),face.Q(8,7)))
    reject('underpaid-origin-gradient',lambda:bridges.payment(face.Q(1,8800),face.Q(1)))
    reject('wrong-mass-entry',lambda:face.enclosure([face.Q(27,40),face.Q(11,16),face.Q(0),face.Q(0),face.Q(0),face.Q(0),face.Q(0),face.Q(0)]))
    with tempfile.TemporaryDirectory(prefix='r5-annulus-validation-',dir='/tmp') as tmp:
        C=pathlib.Path(tmp)/'source';C.mkdir()
        names=sorted(x.name for x in P.iterdir() if x.is_file())
        for name in names:shutil.copyfile(P/name,C/name)
        for mode in (False,True):
            r,seconds=child(C,mode)
            if r.returncode or json.loads(r.stdout)!=record:raise ValueError('WHOLE source-only cold record differs '+r.stderr)
            cases.append(dict(case='cold-O' if mode else 'cold',status='PASS',seconds=seconds))
        original=(C/'EXPECTED.json').read_bytes()
        for name,edit in (
            ('fixture-last-leaf',lambda d:d['face']['payments'][-1].update(payment_lower='0')),
            ('fixture-record-digest',lambda d:d['face'].update(full_polynomial_record_sha256='0'*64)),
            ('fixture-whole-bridge',lambda d:d['bridges']['strengthened_payment'].update(epsilon='1/8500'))):
            d=json.loads(original);edit(d);(C/'EXPECTED.json').write_text(json.dumps(d))
            r,seconds=child(C)
            if r.returncode==0 or 'COMPLETE INDEPENDENT FIXTURE' not in r.stderr or r.stdout:raise ValueError('whole fixture fault was not rejected')
            cases.append(dict(case=name,status='REJECT',reason='COMPLETE INDEPENDENT FIXTURE',seconds=seconds))
        (C/'EXPECTED.json').write_bytes(original)
        for name in ('face.py','bridges.py'):
            saved=(C/name).read_bytes();(C/name).write_bytes(saved+b'\nraise RuntimeError("SOURCE IMPORTED BEFORE SEAL")\n');r,seconds=child(C)
            if r.returncode==0 or 'PREIMPORT SOURCE' not in r.stderr or 'RuntimeError:' in r.stderr or r.stdout:raise ValueError('source fault not stopped before import')
            cases.append(dict(case='preimport-'+name,status='REJECT',reason='PREIMPORT SOURCE',seconds=seconds));(C/name).write_bytes(saved)
    result=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',complete=True,positive_replays=4,semantic_rejects=16,whole_fixture_rejects=3,preimport_source_rejects=2,total_rejects=21,canonical_bytes=record['canonical_bytes'],canonical_sha256=record['canonical_sha256'],fixed_child_seconds=45,all_native_threads=1,serial_children=True,total_seconds=time.monotonic()-start,cases=cases)
    if len(cases)!=25:raise ValueError('complete validation case census')
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
