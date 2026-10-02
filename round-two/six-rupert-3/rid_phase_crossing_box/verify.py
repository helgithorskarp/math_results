"""Exact18-root replay; all six parts and complete fixed records are mandatory."""
from pathlib import Path
from time import monotonic
from collections import Counter
import argparse,hashlib,json,os,platform,resource
HERE=Path(__file__).resolve().parent
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
for name,row in deps['before_import_source_pins'].items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('pinned source changed before import:'+name)
from geometry import build,F,Q,Z,dot,midpoint,need,encode
from forest import read_certificate
from kernel import structural,negative_controls
from domain import make_box
from kernel import coefficients,independent_check


COMMON_KEYS=['geometry_sha256','domain','forest_sha256','literal_complete_forest_counts']
PART_KEYS=['status','part','root_interval','counts','minimum','minimum_location','margin','failure',
           'independent_literal_comparisons','controls','complete_root_visitation','root_leaf_records_sha256','all_source_theorem_from_this_part']
SEMANTIC_KEYS=COMMON_KEYS+PART_KEYS

def semantic(row):return {k:row[k] for k in SEMANTIC_KEYS}

def expected_record(expected,part):return dict(expected['common'],**expected['parts'][part])

def evaluate(part):
    need(part in range(6),'six complete18-root parts required')
    start=monotonic();data=build();domain=make_box(data,1000)
    forest=read_certificate(HERE/'certificate.txt',domain['record']);structural(forest)
    entries={(x['root'],x['path']):x for x in forest['internal_nodes']+forest['leaves']}
    lo,hi=part*18,(part+1)*18;expected={key for key in entries if lo<=key[0]<hi}
    queue=[(ri,'',domain['roots'][ri]) for ri in reversed(range(lo,hi))];visited=set();counts=Counter();independent=Counter()
    minimum=None;location=None;records=[];failure=None;example=None
    while queue:
        ri,bits,T=queue.pop();key=(ri,bits);need(key in expected and key not in visited,'missing/duplicate source node')
        visited.add(key);row=entries[key]
        if 'edge' in row:
            i,j=row['edge'];mid=midpoint(T[i],T[j]);left=list(T);right=list(T);left[j]=mid;right[i]=mid
            queue.extend([(ri,bits+'1',tuple(right)),(ri,bits+'0',tuple(left))]);counts['internal']+=1
            records.append([ri,bits,'branch',i,j]);continue
        kind=row['kind'];counts[kind]+=1
        if kind=='local':
            need(all(dot(c,c)<=F(Q(1,625)) for c in T),'source leaf outside local collar');records.append([ri,bits,'local']);continue
        ci=row['cut'];need(type(ci) is int and 0<=ci<540,'invalid cut index');cut=data['cuts'][ci];need(kind==cut['kind'],'cut interpretation differs')
        if kind=='support' and example is None:example=(cut,T)
        values=coefficients(cut,T,domain);need(len(values)==(80 if kind=='support' else 90),'tensor count differs')
        counts['tensor_coefficients']+=len(values)
        if not independent[kind]:independent[kind]+=independent_check(cut,T,values,domain,data)
        m=min(values)
        if minimum is None or m<minimum:minimum=m;location={'root':ri,'path':bits,'cut':ci,'kind':kind,'coefficient':values.index(m)}
        records.append([ri,bits,kind,ci,[v.encode() for v in values]])
        if m<=Z:
            failure={'location':location,'coefficient':m.encode(),'source_tetrahedron':[encode(c) for c in T]};break
    need(visited==expected and failure is None,'nonpositive source tensor or incomplete closed coverage')
    need(minimum>F(Q(1,5000)),'uniform raw margin1/5000 failed')
    if not independent['gauge']:
        independent['gauge']+=independent_check(data['cuts'][480],domain['roots'][lo],coefficients(data['cuts'][480],domain['roots'][lo],domain),domain,data)
    controls=negative_controls(forest,example,domain,data)
    complete=True
    record={'agent':'six-rupert-3','role':'researcher','status':'complete exact part' if complete else 'candidate source cut FAILED; no nonexistence conclusion',
            'part':part,'root_interval':[lo,hi],'domain':domain['record'],
            'literal_complete_forest_counts':dict(Counter(x.get('kind','internal') for x in entries.values())),
            'geometry_sha256':hashlib.sha256(json.dumps(data['record'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'forest_sha256':hashlib.sha256((HERE/'certificate.txt').read_bytes()).hexdigest(),
            'counts':dict(counts),'minimum':minimum.encode(),'minimum_location':location,'failure':failure,
            'margin':'1/5000','controls':controls,'independent_literal_comparisons':dict(independent),'complete_root_visitation':complete,
            'root_leaf_records_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
            'all_source_theorem_from_this_part':False,'seconds':round(monotonic()-start,3),
            'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,
            'threads':1,'guard_seconds':20,'python':platform.python_version()}
    return record


def main():
    p=argparse.ArgumentParser();p.add_argument('--part',type=int,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    record=evaluate(args.part);expected=json.loads((HERE/'expected.json').read_text())
    need(semantic(record)==expected_record(expected,args.part),'WHOLE exact mathematical part record differs')
    record['whole_expected_record_match']=True
    need(args.output.resolve().parent!=HERE.resolve(),'generated replay output belongs in a separate directory')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['status','part','counts','minimum','minimum_location','seconds','peak_kib','optimized']}),flush=True)

if __name__=='__main__':main()
