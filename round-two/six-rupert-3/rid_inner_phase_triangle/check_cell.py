"""Exact closed receiving-cell/source-product replay; no floating signs enter."""
from pins import verify_pins
verify_pins()
from pathlib import Path
from time import monotonic
from collections import Counter
import argparse,json,os,platform,resource
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from kernel import ROOT,F,Q,Z,need,encode,midpoint,digest,source_geometry,make_domain,coefficients,independent_check,structural,semantic_controls
from forest import load_forest
OUT=ROOT
CELLS={
    'first-source-cell':('1/8','3/16','0','1/2'),
    'cell01':('1/8','3/16','1/2','1'),
    'cell10':('3/16','1/4','0','1/2'),
    'cell11':('3/16','1/4','1/2','1'),
    'cell20':('1/4','3/8','0','1/2'),
    'cell21':('1/4','3/8','1/2','1'),
    'cell30':('3/8','1/2','0','1/2'),
    'cell31':('3/8','1/2','1/2','1'),
}

def evaluate(cell,part):
    need(cell in CELLS and part in range(6),'named closed cell and six disjoint18-root products required')
    start=monotonic()
    bounds=tuple(map(Q,CELLS[cell]))
    data,roots,volume=source_geometry();domain=make_domain(data,bounds)
    proposal=load_forest(cell,domain)
    need(tuple(map(Q,proposal['receiving_closed_rectangle_in_s_units']))==bounds,'proposal receiving cell differs from exact target')
    entries=structural(proposal)
    need(proposal['source_roots']==108 and proposal['actual_source_root_alpha']=='1/22','proposed source domain differs')
    need(len(proposal['cut_labels'])==600,'proposed cut label inventory differs')
    for label,cut in zip(proposal['cut_labels'],domain['cuts']):
        expected={'kind':cut['kind']}
        if cut['kind']=='support':expected.update(support=cut['support'],source=cut['source'])
        else:expected['k']=encode(cut['k'])
        need(expected==label,'proposed actual cut label differs')
    lo,hi=18*part,18*(part+1)
    expected={key for key in entries if lo<=key[0]<hi};visited=set();counts=Counter();independent=Counter()
    queue=[(ri,'',roots[ri]) for ri in reversed(range(lo,hi))];records=[];minimum=None;location=None
    root_counts={ri:Counter() for ri in range(lo,hi)}
    while queue:
        ri,path,T=queue.pop();key=(ri,path)
        need(key in expected and key not in visited,'source replay missing/duplicate node')
        visited.add(key);row=entries[key]
        if 'edge' in row:
            i,j=row['edge'];mid=midpoint(T[i],T[j]);left=list(T);right=list(T);left[j]=mid;right[i]=mid
            queue.extend([(ri,path+'1',tuple(right)),(ri,path+'0',tuple(left))])
            records.append([ri,path,'branch',i,j]);counts['internal']+=1;root_counts[ri]['internal']+=1;continue
        ci=row['cut'];cut=domain['cuts'][ci];kind=cut['kind'];need(row['kind']==kind,'source cut interpretation differs')
        values=coefficients(cut,T,domain);need(len(values)==(40 if kind=='support' else 90),'joint control degree/count differs')
        counts[kind]+=1;counts['tensor_coefficients']+=len(values);root_counts[ri][kind]+=1
        if not independent[kind]:independent[kind]+=independent_check(cut,T,values,domain)
        m=min(values)
        if minimum is None or m<minimum:minimum=m;location={'root':ri,'path':path,'cut':ci,'kind':kind,'coefficient':values.index(m)}
        if m<=Z:
            failure={'status':'FAILED exact sign; no mathematical nonexistence conclusion','cell':cell,'part':part,'location':location,
                     'value':m.encode(),'all_controls':encode(values),'T':[encode(c) for c in T]}
            print(json.dumps(failure))
            raise ValueError('selected proposed leaf has a nonpositive exact joint control')
        records.append([ri,path,kind,ci,encode(values)])
    need(visited==expected and all(root_counts[ri] for ri in range(lo,hi)),'source replay incomplete')
    need(minimum>F(Q(1,100000)),'exact selected forest margin1/100000 failed')
    if not independent['gauge']:
        cut=domain['cuts'][540];independent['gauge']+=independent_check(cut,roots[lo],coefficients(cut,roots[lo],domain),domain)
    controls=semantic_controls(proposal,domain)
    skeleton={k:proposal[k] for k in ['internal_nodes','leaves','cut_labels']}
    geometry={'actual_body_geometry_sha256':digest(data['record']),
              'new_source_closed_roots_sha256':digest([[encode(v) for v in T] for T in roots]),
              'all108_abs_determinants_sum':volume.encode(),
              '36_actual_facet_triangles':data['record']['face_triangles']}
    return {'agent':'six-rupert-3','role':'researcher','status':'complete exact18-root product; whole six-product assembly required',
            'cell':cell,'part':part,'root_interval':[lo,hi],'domain':domain['record'],'geometry':geometry,
            'forest_sha256':digest(skeleton),'literal_complete_forest_counts':dict(Counter(x.get('kind','internal') for x in entries.values())),
            'counts':dict(counts),'root_counts':{str(ri):dict(v) for ri,v in root_counts.items()},
            'minimum':minimum.encode(),'minimum_location':location,'margin':'1/100000',
            'independent_literal_comparisons':dict(independent),'semantic_controls':controls,
            'complete_root_visitation':True,'all_leaf_control_records_sha256':digest(records),
            'all_leaf_control_records':records,
            'all_source_theorem_from_this_product':False,'seconds':round(monotonic()-start,3),
            'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,
            'threads':1,'external_guard_seconds':20,'python':platform.python_version()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cell',choices=list(CELLS),required=True)
    parser.add_argument('--part',type=int,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(not args.output.exists(),'fresh unique output required; stale records cannot count as replay')
    record=evaluate(args.cell,args.part)
    expected=json.loads((OUT/'expected.json').read_text())['cells'][args.cell]['parts'][args.part]
    need(all(record[k]==v for k,v in expected.items()),'entire expected control stream or literal product differs')
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['cell','part','counts','minimum','minimum_location','seconds','peak_kib','optimized']}),flush=True)

if __name__=='__main__':main()
