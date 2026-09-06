#!/usr/bin/env python3
"""Physical verifier controls, independent of the search objective."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import tempfile
import verify


def main():
    p=argparse.ArgumentParser();p.add_argument('--edges',type=Path,required=True)
    p.add_argument('--word',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();raw=a.edges.read_text();lines=raw.splitlines();red=verify.read(a.edges)
    counts=tuple(map(len,verify.literal(set())))
    verify.need(counts==(962598,0),'empty graph literal control')
    counts=tuple(map(len,verify.recursive(set(combinations(range(43),2)))))
    verify.need(counts==(0,962598),'complete graph recursive control')
    bad={'wrong_order':'42\n'+'\n'.join(lines[1:])+'\n',
         'duplicate':raw+lines[-1]+'\n','unsorted':'43\n'+'\n'.join(reversed(lines[1:]))+'\n',
         'out_of_range':raw+'0 43\n','loop':raw+'42 42\n'}
    # A single cross-cycle edge flip breaks the required C3 action.
    changed=red ^ {(0,12)}
    bad['broken_action']='43\n'+''.join(f'{u} {v}\n' for u,v in sorted(changed))
    rejected=[]
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'bad.edges'
        for name,data in bad.items():
            path.write_text(data)
            try:verify.audit(path,a.word)
            except ValueError:rejected.append(name)
            else:raise ValueError('accepted '+name)
        try:verify.audit(a.edges,('1' if a.word[0]=='0' else '0')+a.word[1:])
        except ValueError:rejected.append('wrong_core')
        else:raise ValueError('accepted wrong core')
    answer={'empty_literal':[962598,0],'complete_recursive':[0,962598],'rejected':rejected}
    a.output.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    print('PASS physical controls')


if __name__=='__main__':main()
