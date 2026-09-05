#!/usr/bin/env python3
"""Reject incomplete component certificates and distinguish bounded nonclosure."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    parent = verify.load_parent()
    checker = parent.load_audit()
    certificate = json.loads((verify.HERE/'COMPONENT.json').read_text())
    graphs = [checker.decode({'format':'r55-triple-degree-exact-mixed-graph-v1',
                              'red_adjacency_hex':rows}) for rows in certificate['graphs']]
    report = json.loads((verify.HERE/'report.json').read_text())
    censuses = report['complete_censuses']
    adjacency,boundary = verify.check_closure(graphs,censuses,parent)
    verify.require(adjacency==report['neutral_adjacency'],'positive adjacency control')
    rejected = []
    for name in ('omitted_graph','duplicate_graph','omitted_neutral_edge','improving_exit','missing_census'):
        gg,cc = list(graphs),copy.deepcopy(censuses)
        if name=='omitted_graph':
            gg.pop()
            cc.pop()
        elif name=='duplicate_graph':
            gg[-1] = gg[0]
        elif name=='omitted_neutral_edge':
            cc[0]['neutral_switch_supports'].pop()
        elif name=='improving_exit':
            cc[0]['counts']['decreasing_admissible'] = 1
        else:
            cc.pop()
        try:
            verify.check_closure(gg,cc,parent)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad component control accepted: '+name)
    initial = checker.decode(json.loads(verify.INPUT.read_text()))
    path = json.loads((verify.HERE/'PATH.json').read_text())
    for name in ('omitted_path_move','wrong_path_score','wrong_endpoint'):
        changed = copy.deepcopy(path)
        endpoint = list(graphs[0])
        if name=='omitted_path_move':
            changed['moves'].pop(0)
        elif name=='wrong_path_score':
            changed['scores'][-1] += 1
        else:
            endpoint[3] ^= 1 << 4
            endpoint[4] ^= 1 << 3
        try:
            verify.check_path(parent,initial,endpoint,changed)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad path accepted: '+name)
    limits = []
    with tempfile.TemporaryDirectory(prefix='r55-plateau-controls-') as scratch:
        for total,plateau,expected in ((1,256,'TOTAL_STATE_LIMIT'),(512,1,'PLATEAU_STATE_LIMIT')):
            work = Path(scratch)/expected
            subprocess.run([sys.executable,'-B',str(verify.HERE/'search.py'),'--work',str(work),
                            '--max-processed',str(total),'--max-plateau',str(plateau)],
                           check=True,capture_output=True,text=True)
            result = json.loads((work/'result.json').read_text())
            verify.require(result['status']==expected and result['total_processed']==1,'state limit misreported')
            verify.require(result['initial_score']==result['final_score']==78 and result['path_length']==0,'limited path mutated')
            limited = checker.decode(json.loads((work/'GRAPH.json').read_text()))
            verify.require(limited==initial,'limited endpoint changed')
            limits.append({'status':expected,'processed':1,'endpoint_unchanged':True})
    result = {'negative_controls_rejected':rejected,'state_limit_controls':limits,
              'positive_component_adjacency':adjacency,'minimum_positive_exit_by_vertex':boundary}
    args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
