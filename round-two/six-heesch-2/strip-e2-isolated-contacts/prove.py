"""Produce exact complete inventories for the three finite rejection trees."""
from datetime import datetime,timezone
import hashlib,json,resource,signal,time
from pathlib import Path
import model as M
from strip_point_suppliers import finite_suppliers
import strip_parametric_geometry as G

HERE=Path(__file__).resolve().parent
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def produce(data,guard):
    M.bind(data);trees=[]
    for tree in data['trees']:
        nodes=[]
        for node in tree['nodes']:
            guard();fixed=M.freeze(node['fixed']);point=M.freeze(node['point'])
            sup=finite_suppliers(point,fixed)
            M.require(sup['finite'],'Growing supplier family; inconclusive')
            wanted=set(M.freeze(node['expected']))|{M.freeze(b['pose']) for b in node['blocks']}
            M.require(set(sup['atlas'])==wanted,'Incomplete supplier or blocker inventory')
            rows=M.predicates(data,node);partition=G.partition(rows)
            for k in partition['representatives']:
                guard();M.require(all(G.evaluate(r,k) for r in rows),
                                  'False original demand, packing, supplier or E1 transport')
            nodes.append({'name':node['name'],'suppliers':sup,'partition':partition})
        trees.append({'contact_name':tree['contact_name'],'nodes':nodes})
    return {'trees':trees,'all_k_minimum':6,'E2_exclusions':list(M.CONTACTS),
            'Heesch_number_conclusion':False,'inputs_sha256':sha(data)}

def main():
    start=time.monotonic();calls=[0]
    def guard():
        calls[0]+=1
        if M.deps.paused() or time.monotonic()-start>=43 or calls[0]>100000:
            raise RuntimeError('Operational/time/work guard; incomplete is inconclusive')
    def alarm(a,b):raise RuntimeError('45s guard; incomplete is inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    data=json.loads((HERE/'inputs.json').read_text());evidence=produce(data,guard)
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':evidence,
            'mathematics_sha256':sha(evidence),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (HERE/'generated').mkdir(exist_ok=True);mode='normal' if __debug__ else 'optimized'
    (HERE/'generated'/f'produced-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({k:v for k,v in result.items() if k!='evidence'},sort_keys=True),flush=True)

if __name__=='__main__':main()
