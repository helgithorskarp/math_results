"""Full labelled marked-star census; generated packings remain in explicit scratch."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import resource
import time
from marked import model,instance,solve,packing,canonical,require

def run():
    data=model();inputs=sha256();results=sha256();counts=Counter();nodes=[];packings=[]
    for number,high in enumerate(combinations(range(14),4)):
        case=instance(data,high)
        inputs.update(canonical([high,case['R'],case['quota'],case['columns'],case['mandatory']]))
        if case['direct']:covers=();states=0;counts['direct']+=1
        else:
            covers,states=solve(data['eligible'],case['columns'],case['quota'],case['mandatory'])
            counts['quota_cases']+=1
        counts['raw_cases']+=1;counts['positive_high_placements']+=bool(covers)
        counts['packings']+=len(covers);nodes.append(states)
        results.update(canonical([high,covers,states]))
        for cover in covers:
            blocks=tuple(sorted(data['anchors']+tuple(case['columns'][i] for i in cover)))
            record=packing(blocks)
            require(record['high']==set(high)|{14},'restored wrong high set')
            packings.append(blocks)
    require(counts['raw_cases']==1001 and counts['direct']+counts['quota_cases']==1001,'incomplete raw carrier')
    require(len(set(packings))==len(packings),'raw packing counted twice')
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',
                counts=dict(counts),total_whole_star_states=sum(nodes),max_whole_star_states=max(nodes),
                input_sha256=inputs.hexdigest(),result_sha256=results.hexdigest(),
                packing_stream_sha256=sha256(canonical(sorted(packings))).hexdigest(),
                nodes=nodes,packings=sorted(packings))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();began=time.monotonic();result=run()
    args.output.write_bytes(canonical(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('nodes','packings')}|
                     {'seconds':time.monotonic()-began,'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
