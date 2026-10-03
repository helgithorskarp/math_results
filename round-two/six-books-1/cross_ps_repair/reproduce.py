"""Portable serial correction of10020's unbounded T2 forcing bridge."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def require(t,m):
    if not t:raise ValueError(m)
def seal(root):
    for item in json.loads((root/'SOURCE.json').read_text())['files']:
        raw=(root/item['name']).read_bytes()
        require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],
                'sealed source mismatch: '+item['name'])
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check',type=Path);p.add_argument('--verify-source',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent;out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if a.verify_source:seal(root)
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    phases=[];records={}
    for name,script,inputs in [('reduction','reduce.py',[]),('columns109','columns109.py',['reduction']),
                              ('products109','products109.py',['columns109']),('primary21','baseline.py',[])]:
        output=out/(name+'.json');cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        cmd+=[str(root/script),*(str(out/(z+'.json')) for z in inputs),str(output)]
        r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
        require(r.returncode==0,'incomplete/failed '+name+': '+r.stderr.decode())
        raw=output.read_bytes();record=json.loads(raw)
        require(record.get('complete') is True and raw==canonical(record),'complete canonical '+name)
        records[name]=record;phases.append({'name':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        print(json.dumps(phases[-1]|{'complete':True}),flush=True)
    reduction=records['reduction'];columns=records['columns109'];products=records['products109']
    require(reduction['SY1_T2_is_red'] is False and reduction['literal_SY1_T2_Q_overlap_allowance']==3,
            'correct original SY1/T2 BLUE spine interface')
    require(len(reduction['all7500_first_exact_cuts'])==7500 and len(reduction['whole_pair_survivors'])==26,
            'entire unrestricted corrected P domain')
    keys=[z['key'] for z in reduction['whole_joint_survivors']]
    require(keys==[z['key'] for z in columns['results']]==[z['key'] for z in products['results']],
            'WHOLE original-label row/point/product interfaces')
    require(all(len(z['whole32_point_role_table'])==32 for z in columns['results']),'complete32 point role catalogue EACH core')
    require([len(z['whole_end_Q_packets']) for z in columns['results']]==[180,0,60],
            'complete labelled endpoint Q packet counts')
    require(sum(z['raw_products'] for z in products['results'])==115968 and
            sum(z['rank_matching_products'] for z in products['results'])==48 and
            all(not z['whole_known_spine_survivors'] for z in products['results']),
            'all actual-rank colored known-spine completions excluded')
    math=canonical({'agent':'six-books-1','role':'researcher','complete':True,'components':records})
    (out/'MATHEMATICAL.json').write_bytes(math)
    summary={'agent':'six-books-1','role':'researcher','complete':True,
      'proof_status':'Exact computer-assisted correction of10020 T2 row forcing; ordinary/source bridges unformalized; independent review pending',
      'phases':phases,'whole_mathematical_bytes':len(math),'whole_mathematical_sha256':hashlib.sha256(math).hexdigest(),
      'full_P_row_rank_domain':7500,'separate_pair_survivors':26,'joint_union_survivors':3,
      'omitted_SY1_P_core_retained':True,'terminal_edges':109,'full_endpoint_Q_packets':240,
      'raw_Q_column_products':115968,'actual_X_SX_rank_matches':48,'all_known_spine_survivor_sets_empty':True,
      'all120_physical_pages_compared_per_rank_match':True,'whole_P_S_r_transports':40,
      'whole_own_leaf_cells_all_T_rank_regimes':384,'Q_Q_graph_search_used':False,
      'ordinary_108_theorem_dependency':'9795','outside_global_degree_floor_assumed':False,
      'runtime_solver_float_ledger_census_review_input':False,'baseline_red_blue':[93,117],'baseline_max_pages':[3,6],
      'threads':1,'inner_mathematical_guard_seconds':30,'child_guard_seconds':90}
    compact=canonical(summary)
    if a.check:require(compact==a.check.read_bytes(),'ENTIRE compact expected record differs')
    (out/'SUMMARY.json').write_bytes(compact)
    if a.verify_source:seal(root)
    print(json.dumps({'complete':True,'whole_bytes':len(math),'whole_sha256':summary['whole_mathematical_sha256']}),flush=True)
if __name__=='__main__':main()
