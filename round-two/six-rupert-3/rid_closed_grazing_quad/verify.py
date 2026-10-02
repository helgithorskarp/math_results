"""Exact deterministic source-root partition replay, never a partial theorem.

All three36-root parts are required. Each part reconstructs the whole named
geometry/closed receiver supports and the entire literal forest structure,
then checks every coefficient in its disjoint roots. No source sign is
obtained from the floating producer.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
from time import monotonic
import argparse,hashlib,importlib.util,json,platform,resource
HERE=Path(__file__).resolve().parent
deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
for name,row in deps['before_import_source_pins'].items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=row['sha256']:
        raise ValueError('pinned proof source changed before import: '+name)
from domain import make_domain
from geometry import build,F,Q,Z,O,phi,dot,cross,sub,midpoint,need,encode,neg
from forest import read_certificate

import kernel as parent
OUT=Path(__file__).resolve().parent
SEMANTIC_KEYS=['status','part','root_interval','geometry_sha256','domain','forest_sha256',
 'literal_complete_forest_counts','counts','minimum_positive_coefficient','minimum_location',
 'margin','independent_literal_double_polarization','controls','root_leaf_records_sha256',
 'all_source_extension_inferred_from_this_part']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--part',type=int,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(args.part in range(3),'only three complete root partitions exist')
    start=monotonic();DATA=build();parent.DATA=DATA;domain=make_domain(DATA)
    forest=read_certificate(OUT/'certificate.txt',domain['record']);parent.structural(forest)
    entries={(x['root'],x['path']):x for x in forest['internal_nodes']+forest['leaves']}
    need(all(type(r) is int and 0<=r<108 and set(p)<=set('01') for r,p in entries),'invalid full rooted forest address')
    complete_counts=Counter(r.get('kind','internal') for r in entries.values())
    lower,upper=36*args.part,36*(args.part+1)
    expected={key for key in entries if lower<=key[0]<upper}
    queue=[(ri,'',domain['roots'][ri]) for ri in reversed(range(lower,upper))]
    visited=set();counts=Counter();minimum=None;location=None;independent=Counter();example=None
    records=[]
    while queue:
        ri,bits,T=queue.pop();key=(ri,bits);need(key in expected and key not in visited,'missing/duplicate source node')
        visited.add(key);row=entries[key]
        if 'edge' in row:
            need('kind' not in row and len(row['edge'])==2,'ambiguous source branch')
            i,j=row['edge'];need(type(i) is int and type(j) is int and 0<=i<j<4,'invalid exact bisection edge')
            mid=midpoint(T[i],T[j]);left=list(T);right=list(T);left[j]=mid;right[i]=mid
            queue.extend([(ri,bits+'1',tuple(right)),(ri,bits+'0',tuple(left))]);counts['internal']+=1
            records.append([ri,bits,'branch',i,j]);continue
        kind=row.get('kind');need(kind in ['local','support','gauge'],'unknown exact leaf');counts[kind]+=1
        if kind=='local':
            need(all(dot(c,c)<=F(Q(1,625)) for c in T),'closed leaf is outside whole receiver local collar')
            records.append([ri,bits,'local']);continue
        ci=row['cut'];need(type(ci) is int and 0<=ci<540,'invalid actual cut index')
        cut=DATA['cuts'][ci];need(kind==cut['kind'],'wrong actual cut interpretation')
        values=parent.coefficients(cut,T,domain)
        need(len(values)==60 and all(x>Z for x in values),'nonpositive actual joint Bernstein coefficient')
        counts['tensor_coefficients']+=60
        if independent[kind]<1:
            parent.independent_check(cut,T,values,domain);independent[kind]+=1
        if kind=='support' and example is None:example=(cut,T)
        m=min(values)
        if minimum is None or m<minimum:minimum=m;location={'root':ri,'path':bits,'cut':ci,'kind':kind}
        records.append([ri,bits,kind,ci,[v.encode() for v in values]])
    need(visited==expected,'unconsumed/orphan region in selected complete source roots')
    need(minimum is not None and minimum>F(Q(1,20000)),'uniform exact raw margin1/20000 not proved')
    controls=parent.negative_controls(forest,example,domain)
    record={'agent':'six-rupert-3','role':'researcher','status':'EXACT complete root partition; all three parts required',
            'part':args.part,'root_interval':[lower,upper],
            'geometry_sha256':hashlib.sha256(json.dumps(DATA['record'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'domain':domain['record'],'forest_sha256':hashlib.sha256((OUT/'certificate.txt').read_bytes()).hexdigest(),
            'literal_complete_forest_counts':dict(complete_counts),'counts':dict(counts),
            'minimum_positive_coefficient':minimum.encode(),'minimum_location':location,'margin':'1/20000',
            'independent_literal_double_polarization':dict(independent),'controls':controls,
            'root_leaf_records_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
            'all_source_extension_inferred_from_this_part':False,'python':platform.python_version(),
            'optimized':not __debug__,'seconds':round(monotonic()-start,3),
            'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    semantic={k:record[k] for k in SEMANTIC_KEYS}
    expected=json.loads((OUT/'expected.json').read_text())['parts'][args.part]
    need(semantic==expected,'WHOLE exact mathematical partition record differs')
    record['whole_expected_record_match']=True
    need(args.output.resolve().parent!=OUT.resolve(),'generated replay output belongs in a separate directory')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['status','part','root_interval','counts','minimum_positive_coefficient',
            'minimum_location','margin','seconds','peak_kib','optimized']}))

if __name__=='__main__':main()
