"""Serial exact reproduction, fixed90s per case, no researcher imports."""
from pathlib import Path
import json,os,subprocess,sys,time
import core as c

ROOT=Path(__file__).resolve().parent
NAMES=['conventions','neg4','neg5','neg6','neg7',
       'corner0a','corner0b','corner1a','corner1b',
       'continue4','continue5','continue6','continue9','continue10','continue11','q8_cut']

def strict_json(text):
    def pairs(items):
        out={}
        for k,v in items:
            c.need(k not in out,'duplicate JSON key');out[k]=v
        return out
    return json.loads(text,object_pairs_hook=pairs,
                      parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))

def main():
    c.need(len(sys.argv)==1,'no unproved case/guard overrides')
    env=dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[name]='1'
    result={}
    for name in NAMES:
        argv=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        argv += [str(ROOT/('q8_cut.py' if name=='q8_cut' else 'cases.py'))]
        if name!='q8_cut':argv.append(name)
        started=time.monotonic()
        try:r=subprocess.run(argv,text=True,capture_output=True,env=env,timeout=90)
        except subprocess.TimeoutExpired:raise RuntimeError('Operational90s limit: incomplete, no mathematical exclusion')
        c.need(r.returncode==0,'case failed: '+name+'\n'+r.stderr)
        result[name]=strict_json(r.stdout)
        print(json.dumps({'case':name,'seconds':round(time.monotonic()-started,3)}),file=sys.stderr,flush=True)
    expected=strict_json((ROOT/'EXPECTED.json').read_text())
    c.need(json.dumps(c.canonical(result),sort_keys=True,separators=(',',':'))==
           json.dumps(expected,sort_keys=True,separators=(',',':')),
           'entire typed independent mathematical record')
    print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer',
        'ok':True,'cases':len(NAMES),'complete_record_sha256':c.digest(result),
        'record':result},sort_keys=True,indent=2))

if __name__=='__main__':main()
