"""Untrusted bounded DFS proposes one gap-(2,3)-rooted word per cyclic class."""
import argparse
import json
from pathlib import Path
import resource
import time
from common import pins,require,sha

def profiles():
    def visit(word,remaining):
        slots=10-len(word)
        if remaining<0 or remaining>6*slots:return
        if not slots:
            if remaining==0:yield tuple(word)
            return
        for digit in range(2 if word[-1]==0 else 7):
            yield from visit(word+[digit],remaining-digit)
    yield from visit([0,1],23)

def canonical(word):
    return min(word[i:]+word[:i] for i in range(10)
               if word[i]==0 and word[(i+1)%10]==1)

def main(work):
    began=time.monotonic();pins()
    require(not work.exists(),'fresh generated-data directory required')
    work.mkdir(parents=True)
    representatives=set();rooted=0
    for word in profiles():
        rooted+=1;representatives.add(canonical(word))
    path=work/'representatives.txt'
    path.write_text(''.join(' '.join(str(x+2) for x in word)+'\n'
                           for word in sorted(representatives)))
    result=dict(agent='six-vdw-2',role='researcher',status='PROPOSED_NOT_CHECKED',
        selected_count=10,cycle_length=44,deficit_cap=6,deficit_total=24,
        rooted_23_profiles=rooted,phase_rotation_classes=len(representatives),
        period22_phase_classes=sum(word[:5]==word[5:] for word in representatives),
        corpus_sha256=sha(path),corpus_bytes=path.stat().st_size,
        seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        admissible_field_coloring_count=False,global_W_bound=False)
    (work/'generated.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
