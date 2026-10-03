"""Serial source-only replay. Ordinary proof and cited108/109 lemmas remain prerequisites."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path

def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def require(t,m):
    if not t:raise ValueError(m)
def seal(root):
    manifest=json.loads((root/'SOURCE.json').read_text())
    for item in manifest['files']:
        raw=(root/item['name']).read_bytes()
        require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],
                'sealed source mismatch: '+item['name'])
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check',type=Path)
    p.add_argument('--verify-source',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent
    if a.verify_source:seal(root)
    a.output.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    records={};phases=[]
    for name,script in [('C','c_main.py'),('P-S','ps.py'),('110','terminal110.py'),('primary21','baseline.py')]:
        output=(a.output/(name+'.json')).resolve()
        command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(root/script),str(output)]
        r=subprocess.run(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
        require(r.returncode==0,'incomplete/failed '+name+' phase: '+r.stderr.decode())
        raw=output.read_bytes();record=json.loads(raw)
        require(record.get('complete') is True and raw==canonical(record),'complete canonical '+name)
        records[name]=record;phases.append({'name':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        print(json.dumps({'phase':name,'complete':True,'bytes':len(raw),'sha256':phases[-1]['sha256']}),flush=True)
    require(records['C']['possible_terminal_T_Q_ranks']==[[3,2,3],[3,2,4]],'ordinary rank interface')
    require(len(records['P-S']['T2_rank_row_candidates'])==12,'complete T2 rank/row interface')
    require(records['110']['all_X_rank_solution_sets_empty'] is True,'new110 terminal')
    math=canonical({'agent':'six-books-1','role':'researcher','complete':True,'components':records})
    (a.output/'MATHEMATICAL.json').write_bytes(math)
    summary={'agent':'six-books-1','role':'researcher','complete':True,
             'proof_status':'Exact computer-assisted conditional lemma, with ordinary unformalized reduction and cited108/109 theorem dependencies',
             'phases':phases,'whole_mathematical_bytes':len(math),'whole_mathematical_sha256':hashlib.sha256(math).hexdigest(),
             'ordinary_T_Q_ranks':[[3,2,3],[3,2,4]],'terminal110_labelled_cases':12,'terminal110_actual_cores':48,
             'terminal110_all_X_solution_sets_empty':True,'terminal110_semantic_damage_rejections':12,
             'baseline_edges_red_blue':[93,117],'baseline_max_pages':[3,6],
             'runtime_external_census_solver_ledger_review_input':False,'threads':1,'inner_mathematical_guard_seconds':30,
             'child_guard_seconds':90}
    compact=canonical(summary)
    if a.check:require(compact==a.check.read_bytes(),'ENTIRE compact expected record differs')
    (a.output/'SUMMARY.json').write_bytes(compact)
    if a.verify_source:seal(root)
    print(json.dumps({'complete':True,'whole_bytes':len(math),'whole_sha256':summary['whole_mathematical_sha256']}),flush=True)
if __name__=='__main__':main()
