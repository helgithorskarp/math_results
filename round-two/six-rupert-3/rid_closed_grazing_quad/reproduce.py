"""Sequential full reproduction; incomplete partitions establish no theorem."""
from pathlib import Path
from collections import Counter
from time import monotonic
import argparse,copy,hashlib,json,os,subprocess,sys

HERE=Path(__file__).resolve().parent
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
             'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from verify import SEMANTIC_KEYS,need
from geometry import F,Q

def semantic(record):return {k:record[k] for k in SEMANTIC_KEYS}

def aggregate(records):
    need(len(records)==3 and sorted(r['part'] for r in records)==[0,1,2],
         'all three exact source partitions are required exactly once')
    rows=sorted(records,key=lambda r:r['part'])
    expected=json.loads((HERE/'expected.json').read_text());counts=Counter()
    for i,r in enumerate(rows):
        need(r['root_interval']==[36*i,36*(i+1)] and r.get('whole_expected_record_match'),
             'complete root coverage or full expected comparison missing')
        need(semantic(r)==expected['parts'][i],'complete mathematical partition differs')
        need(r['forest_sha256']==expected['forest_sha256'],'literal source forest differs')
        need(r['geometry_sha256']==rows[0]['geometry_sha256'] and r['domain']==rows[0]['domain'],
             'source partitions use different continuum hypotheses')
        counts.update(r['counts'])
    need(dict(counts)==expected['aggregate_counts'] and counts['support']+counts['gauge']==1687,
         'complete source leaf/sign count differs')
    minima=[F(Q(r['minimum_positive_coefficient'][0]),Q(r['minimum_positive_coefficient'][1])) for r in rows]
    m=min(minima);need(m>F(Q(1,20000)),'full exact tensor margin does not close')
    return {'status':'EXACT complete new receiving triangle; all108 source roots/101220 signs',
            'counts':dict(counts),'minimum_positive_coefficient':m.encode(),
            'minimum_location':rows[min(range(3),key=lambda i:minima[i])]['minimum_location'],
            'whole_three_part_records_sha256':hashlib.sha256(json.dumps([semantic(r) for r in rows],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'forest_sha256':rows[0]['forest_sha256'],'normal_or_optimized':rows[0]['optimized'],
            'summed_child_seconds':round(sum(r['seconds'] for r in rows),3),
            'peak_child_kib_upper':max(r['peak_kib'] for r in rows),
            'author_checked':True,'independently_reviewed':False,'global_RID_open':True}

def assembly_controls(rows):
    rejected=[]
    for title,bad in [('omit a full source partition',rows[:-1]),
                      ('duplicate a full source partition',[rows[0],rows[0],rows[2]])]:
        try:aggregate(bad)
        except ValueError:rejected.append(title);continue
        raise ValueError('damaged source assembly accepted')
    bad=copy.deepcopy(rows);bad[1]['counts']['tensor_coefficients']-=1
    try:aggregate(bad)
    except ValueError:rejected.append('alter a complete exact coefficient record')
    else:raise ValueError('altered coefficient assembly accepted')
    return rejected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--optimized',action='store_true')
    parser.add_argument('--compare',type=Path);parser.add_argument('--assemble',type=Path,nargs=3)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    target=HERE/'.generated'/('optimized' if args.optimized else 'normal');target.mkdir(parents=True,exist_ok=True)
    if args.assemble:paths=args.assemble
    else:
        paths=[]
        for part in range(3):
            path=target/('part'+str(part)+'.json')
            cmd=[sys.executable,*(['-O'] if args.optimized else []),str(HERE/'verify.py'),
                 '--part',str(part),'--output',str(path)]
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
            if result.returncode:raise RuntimeError('exact partition failed: '+result.stderr[:1000])
            print(result.stdout.strip(),flush=True);paths.append(path)
    rows=[json.loads(p.read_text()) for p in paths]
    result=aggregate(rows);result['three_assembly_controls_reject']=assembly_controls(rows)
    if args.compare:
        previous=json.loads(args.compare.read_text())
        need(previous['whole_three_part_records_sha256']==result['whole_three_part_records_sha256'] and
             previous['counts']==result['counts'] and previous['minimum_positive_coefficient']==result['minimum_positive_coefficient'],
             'ordinary/optimized WHOLE mathematical records differ')
        result['normal_optimized_whole_match']=True
    output=args.output or target/'complete.json';output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
