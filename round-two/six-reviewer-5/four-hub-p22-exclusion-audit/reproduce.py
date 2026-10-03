"""One serial mathematical child; fixed60s external/fixed internal phase guards.
Full records kept in user-selected workspace scratch, never projection hashes.
"""
import hashlib,json,os,pathlib,resource,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent

def main():
    mode='optimized' if sys.flags.optimize else 'normal';started=time.monotonic()
    flags=['-O'] if sys.flags.optimize else [];env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    phases=[]
    def run(name,args):
        s=time.monotonic()
        child=subprocess.run([sys.executable,*flags,*args],cwd=P,env=env,capture_output=True,timeout=60)
        (P/(name+'-'+mode+'.log')).write_bytes(child.stdout+child.stderr)
        if child.returncode:raise RuntimeError('INCOMPLETE child '+name+': '+child.stderr.decode())
        phases.append(dict(name=name,seconds=time.monotonic()-s,returncode=child.returncode))
        print(json.dumps(dict(phase=name,seconds=phases[-1]['seconds'])),flush=True)
    run('physical',['physical22.py']);run('census',['census22.py'])
    populations=json.loads((P/'census22.json').read_text())['survivors']
    for start in range(0,len(populations),64):run('column-%05d'%start,['columns22.py',str(start),str(start+64)])
    files=[P/'physical22.json',P/'census22.json']+sorted((P/'column-phases').glob('*.json'))
    stream=hashlib.sha256();records=[];total=0
    for f in files:
        b=f.read_bytes();stream.update(b);total+=len(b)
        records.append(dict(name=str(f.relative_to(P)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
    result=dict(method='complete ordered mathematical file bytes; no provenance normalization',
                record_files=records,mathematical_stream_bytes=total,mathematical_stream_sha256=stream.hexdigest())
    (P/('whole-'+mode+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    receipt=dict(mode=mode,python=sys.version,phases=phases,seconds=time.monotonic()-started,
                 peak_self_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 peak_children_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                 one_serial_mathematical_child=True,threads=1,unchanged_scope='1CPU2GiB',child_timeout=60,
                 unchanged_internal_guards=True)
    (P/('receipt-'+mode+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(mode=mode,complete_phases=len(phases),bytes=total,sha256=stream.hexdigest(),seconds=receipt['seconds'])),flush=True)

if __name__=='__main__':main()
