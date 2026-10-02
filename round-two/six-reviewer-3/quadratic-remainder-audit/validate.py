"""Serial fresh independent proof/decoder/damage runs; fixed 45s per math child."""
import os,sys,json,time,subprocess,tempfile,resource,hashlib,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
PYTHON=sys.executable
ENV=os.environ.copy()
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:ENV[k]='1'

def run(path,flags=(),fixture=None,reject=False,label=''):
    args=[PYTHON,'-I','-B',*flags,str(path)]+([] if fixture is None else [str(fixture)])
    st=time.monotonic();p=subprocess.run(args,env=ENV,text=True,capture_output=True,timeout=45)
    if (p.returncode==0)==reject:raise ValueError('unexpected child result '+label+' '+p.stderr[-1200:])
    row={'label':label,'flags':list(flags),'seconds':time.monotonic()-st,'exit_code':p.returncode}
    if not reject:row['summary']=json.loads(p.stdout)
    else:row['reason']=p.stderr.strip().splitlines()[-1]
    print(json.dumps(row),flush=True);return row

if __name__=='__main__':
    seal=json.loads((HERE/'INDEPENDENCE.json').read_text())
    for n,sha in seal['files'].items():
        if hashlib.sha256((HERE/n).read_bytes()).hexdigest()!=sha:raise ValueError('sealed independent source differs '+n)
    runs=[]
    for name in ['audit.py','gaussian.py']:
        for flags in [[],['-O']]:runs.append(run(HERE/name,flags,label=name))
    with tempfile.TemporaryDirectory(prefix='independent-quadratic-') as td:
        td=Path(td);d=json.loads((HERE/'EXPECTED.json').read_text());d['domain']['critical_multiplicity_count']=7
        (td/'semantic.json').write_text(json.dumps(d))
        (td/'duplicate.json').write_text('{"domain":1,"domain":2}')
        (td/'malformed.json').write_text('{')
        for name in ['semantic','duplicate','malformed']:
            for flags in [[],['-O']]:runs.append(run(HERE/'audit.py',flags,td/(name+'.json'),True,label='fresh_fixture_'+name))
        damages=[('wrong_centered_quartic', '7*V*V-8*S4','6*V*V-8*S4'),('wrong_signed_fourth_phase',"C(phases[4]['paired_cubic_coefficient'])","C(phases[3]['paired_cubic_coefficient'])"),('invalid_smaller_physical_budget','for b in [390,370]:','for b in [390,320]:')]
        for name,old,new in damages:
            dst=td/name;dst.mkdir()
            for f in ['audit.py','polys.py','cosine.py','EXPECTED.json']:shutil.copy2(HERE/f,dst/f)
            s=(dst/'audit.py').read_text()
            if s.count(old)!=1:raise ValueError('damage does not have one substantive site')
            (dst/'audit.py').write_text(s.replace(old,new))
            for flags in [[],['-O']]:runs.append(run(dst/'audit.py',flags,reject=True,label=name))
    normal=[r for r in runs if r['label']=='audit.py']
    if normal[0]['summary']!=normal[1]['summary']:raise ValueError('entire normal/O independent records differ')
    print(json.dumps({'whole_validation':True,'runs':runs,'guard_seconds':45,'serial_math_children':True,'native_threads':1,'scope':'unchanged1CPU2GiB','peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},sort_keys=True),flush=True)
