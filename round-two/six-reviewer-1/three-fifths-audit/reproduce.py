"""Cold, isolated, serial exact reproduction; bulk outputs remain temporary."""
import hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time
from pathlib import Path


def run():
    here=Path(__file__).resolve().parent
    seal=json.loads((here/'PRIMARY_SEAL.json').read_text())
    for n,row in seal['primary_files'].items():
        data=(here/n).read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('changed primary seal '+n)
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:
        env[n]='1'
    rows,records=[],{}
    with tempfile.TemporaryDirectory(prefix='three-fifths-review-') as tmp:
        cold=Path(tmp)/'cold';cold.mkdir()
        for n in seal['primary_files']:shutil.copyfile(here/n,cold/n)
        env['TMPDIR']=tmp
        def child(root,script,opt,damage=None):
            dest=Path(tmp)/('out-'+str(len(rows))+'.json')
            extra=['--output',str(dest)] if script=='check.py' else []
            if damage:extra+=['--damage',damage]
            bootstrap=('import runpy,sys;from pathlib import Path;'
                       'p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p.parent));'
                       'sys.argv=[str(p)]+sys.argv[2:];runpy.run_path(str(p),run_name="__main__")')
            cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])
            start=time.monotonic()
            p=subprocess.run(cmd+['-c',bootstrap,str(root/script),*extra],
                             capture_output=True,env=env,timeout=45)
            seconds=time.monotonic()-start
            if damage:
                if p.returncode==0 or b'ValueError:' not in p.stderr:
                    raise ValueError('semantic damage was not rejected '+damage)
                data=b''
            else:
                if p.returncode or p.stderr:raise ValueError('positive child failed '+p.stderr.decode())
                data=dest.read_bytes() if script=='check.py' else p.stdout
                json.loads(data)
            rows.append(dict(source='local' if root==here else 'cold',script=script,
                             optimized=opt,damage=damage,returncode=p.returncode,
                             seconds=round(seconds,6),result_bytes=len(data),
                             cumulative_peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
            return data
        for script in ['check.py','literal.py']:
            outputs=[child(root,script,opt) for root in [here,cold] for opt in [False,True]]
            if any(json.loads(x)!=json.loads(outputs[0]) or x!=outputs[0] for x in outputs):
                raise ValueError('whole parsed and byte result disagreement '+script)
            records[script]=dict(bytes=len(outputs[0]),sha256=hashlib.sha256(outputs[0]).hexdigest(),
                                 all_four_entire_parsed_and_byte_comparisons=True)
        for opt in [False,True]:
            for damage in ['radial-lower','phase-reciprocal','polar-terminal',
                           'missing-leaf','illegal-axis','lost-eighth-integral','lost-origin-margin']:
                child(here,'check.py',opt,damage)
    return dict(agent='six-reviewer-1',role='independent mathematical reviewer',
                all_five_primary_seals_unchanged=True,records=records,rows=rows,
                positive_children=8,mathematical_rejection_children=14,serial=True,native_threads=1,
                fixed_child_guard_seconds=45,total_child_seconds=round(sum(r['seconds'] for r in rows),6),
                maximum_child_seconds=max(r['seconds'] for r in rows),
                no_timeout_unknown_kill_or_incomplete_inference=True)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
