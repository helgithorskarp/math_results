"""All six sequential parts; fixed entire records and damaged assemblies checked."""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from verify import semantic,expected_record,need
from geometry import F,Q


def aggregate(records):
    need(len(records)==6 and sorted(r['part'] for r in records)==list(range(6)),
         'all six complete root partitions required exactly once')
    rows=sorted(records,key=lambda r:r['part']);expected=json.loads((HERE/'expected.json').read_text());counts=Counter()
    for i,r in enumerate(rows):
        need(r['root_interval']==[18*i,18*(i+1)] and r.get('whole_expected_record_match'),
             'complete root coverage or expected record comparison missing')
        need(semantic(r)==expected_record(expected,i),'WHOLE mathematical part record differs')
        counts.update(r['counts'])
    need(dict(counts)==expected['aggregate_counts'] and counts['support']+counts['gauge']==1704
         and counts['tensor_coefficients']==137380,'whole source leaf/sign counts differ')
    minima=[F(Q(r['minimum'][0]),Q(r['minimum'][1])) for r in rows];i=min(range(6),key=lambda i:minima[i]);m=minima[i]
    need(m>F(Q(1,5000)),'whole exact margin1/5000 fails')
    stream=hashlib.sha256(json.dumps([semantic(r) for r in rows],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    need(stream==expected['whole_six_part_records_sha256'],'entire ordered source records differ')
    return {'agent':'six-rupert-3','role':'researcher','status':'EXACT entire closed phase box; all108 source roots and137380 signs',
            'counts':dict(counts),'minimum':m.encode(),'minimum_location':rows[i]['minimum_location'],
            'whole_six_part_records_sha256':stream,'forest_sha256':rows[0]['forest_sha256'],
            'optimized':rows[0]['optimized'],'summed_child_seconds':round(sum(r['seconds'] for r in rows),3),
            'peak_child_kib_upper':max(r['peak_kib'] for r in rows),'author_checked':True,
            'independently_reviewed':False,'global_RID_open':True}


def assembly_controls(rows):
    damages=[('omit a complete source partition',rows[:-1]),
             ('duplicate a source partition',[rows[0],rows[0],*rows[2:]])]
    bad=copy.deepcopy(rows);bad[1]['counts']['tensor_coefficients']-=1
    damages.append(('alter a complete coefficient record',bad))
    bad=copy.deepcopy(rows);bad[2]['domain']['closed_partition']='seam omitted'
    damages.append(('alter the closed receiving phase seam',bad))
    rejected=[]
    for title,bad in damages:
        try:aggregate(bad)
        except ValueError as e:rejected.append({'control':title,'rejection':str(e)});continue
        raise ValueError('damaged source/receiver assembly accepted')
    return rejected


def main():
    p=argparse.ArgumentParser();p.add_argument('--optimized',action='store_true');p.add_argument('--compare',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--assemble',type=Path,nargs=6);a=p.parse_args()
    target=HERE/'.generated'/('optimized' if a.optimized else 'normal');target.mkdir(parents=True,exist_ok=True)
    if a.assemble:paths=a.assemble
    else:
        paths=[]
        for part in range(6):
            path=target/('part'+str(part)+'.json')
            cmd=[sys.executable,*(['-O'] if a.optimized else []),str(HERE/'verify.py'),'--part',str(part),'--output',str(path)]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
            if r.returncode:raise RuntimeError('exact source partition failed:'+r.stderr[:1800])
            print(r.stdout.strip(),flush=True);paths.append(path)
    rows=[json.loads(path.read_text()) for path in paths];result=aggregate(rows)
    result['four_damaged_assemblies_reject']=assembly_controls(rows)
    if a.compare:
        old=json.loads(a.compare.read_text())
        need(old['whole_six_part_records_sha256']==result['whole_six_part_records_sha256'] and
             old['counts']==result['counts'] and old['minimum']==result['minimum'],
             'ordinary/optimized entire mathematical records differ')
        result['normal_optimized_whole_match']=True
    path=a.output or target/'complete.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
