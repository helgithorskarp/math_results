#!/usr/bin/env python3
"""Reject malformed height-one certificates and exercise sublevel stop states."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import verify_escape as escape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    lower = escape.load_lower()
    parent = lower.load_parent()
    checker = parent.load_audit()
    component = json.loads((escape.HERE/'COMPONENT.json').read_text())
    initial = checker.decode({'format':'r55-triple-degree-exact-mixed-graph-v1',
                              'red_adjacency_hex':component['graphs'][2]})
    endpoint = checker.decode(json.loads((escape.HERE/'ESCAPE_GRAPH.json').read_text()))
    path = json.loads((escape.HERE/'ESCAPE_PATH.json').read_text())
    states,scores = escape.check_excursion(lower,parent,initial,endpoint,path)
    rejected = []
    for name in ('omit_uphill','wrong_ceiling','wrong_score','wrong_endpoint','wrong_start','exceptional_vertex','repeated_vertex'):
        mutant = copy.deepcopy(path)
        end = list(endpoint)
        if name=='omit_uphill':
            mutant['moves'].pop(0)
        elif name=='wrong_ceiling':
            mutant['ceiling'] = 73
        elif name=='wrong_score':
            mutant['scores'][-1] += 1
        elif name=='wrong_endpoint':
            end[3] ^= 1 << 4
            end[4] ^= 1 << 3
        elif name=='wrong_start':
            mutant['component_start_index'] = 0
        elif name=='exceptional_vertex':
            mutant['moves'][0][0] = 0
        else:
            mutant['moves'][0][0] = mutant['moves'][0][1]
        try:
            escape.check_excursion(lower,parent,initial,end,mutant)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad excursion accepted: '+name)
    stops = []
    with tempfile.TemporaryDirectory(prefix='r55-height-controls-') as scratch:
        for ceiling,cap,expected in ((73,512,'SUBLEVEL_CLOSED'),(74,1,'STATE_LIMIT')):
            work = Path(scratch)/expected
            subprocess.run([sys.executable,'-B',str(escape.HERE/'height_one_search.py'),
                            '--work',str(work),'--max-processed',str(cap),'--ceiling',str(ceiling),
                            '--start-index','2'],check=True,capture_output=True,text=True)
            result = json.loads((work/'result.json').read_text())
            checkpoint = json.loads((work/'checkpoint.json').read_text())
            escape.require(result['status']==expected and result['escape'] is None,'wrong bounded status')
            escape.require(not (work/'GRAPH.json').exists(),'non-escape emitted a witness')
            if ceiling==73:
                actual = {tuple(rows) for rows in checkpoint['nodes']}
                expected_graphs = {tuple(rows) for rows in component['graphs']}
                escape.require(actual==expected_graphs and result['processed']==5,'zero-height component mismatch')
            else:
                escape.require(result['processed']==1 and result['discovered']>1,'state-limit coverage')
            stops.append({'ceiling':ceiling,'status':expected,'processed':result['processed'],
                          'discovered':result['discovered'],'no_escape_graph':True})
    report = {'negative_controls_rejected':rejected,'positive_path_scores':scores,
              'sublevel_controls':stops}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
