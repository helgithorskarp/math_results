from pathlib import Path
from hashlib import sha256
import argparse,json,resource,time
from incidence import need
import parent,zero


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work-dir',required=True);ap.add_argument('--expected');a=ap.parse_args()
    work=Path(a.work_dir);work.mkdir(parents=True,exist_ok=True);st=time.monotonic()
    p=parent.audit();print(json.dumps(dict(stage='parent complete',result=p)),flush=True)
    z,fixtures=zero.audit();print(json.dumps(dict(stage='zero attachment complete',graphs=z['cubic10_graphs'],negative=z['negative_exact_congruences'],types=len(z['positive_classes']))),flush=True)
    result=json.loads(json.dumps(dict(agent='six-reviewer-2',role='independent mathematical reviewer',scope='Complete independent marked one-attachment and zero-attachment exclusions for the whole Book98 histogram(3,18,1)',parent=p,zero=z)))
    if a.expected:need(result==json.loads(Path(a.expected).read_text()),'completed cold audit differs from expected')
    (work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (work/'positive_grams.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    metrics=dict(seconds=time.monotonic()-st,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics),flush=True)


if __name__=='__main__':main()
