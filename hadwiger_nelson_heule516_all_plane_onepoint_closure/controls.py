#!/usr/bin/env python3
"""Small exact controls for the exhaustive modular filter."""
from pathlib import Path
from itertools import combinations
import argparse,importlib.util,json,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--filter',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True)
    exact=load('independent_exact_triples',REPO/'hadwiger_nelson_heule510_completion_frontier/audit.py')
    source=json.loads((REPO/'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json').read_text())['coordinates']
    def point(x=0,y=0,ys=0):
        p=[[0]*8,[0]*8];p[0][0]=x;p[1][0]=y;p[1][1]=ys;return p
    fixtures=[[point(96),point(-48,ys=48),point(-48,ys=-48),point(),point(0,96),point(0,-96),point(96,96),point(144)],source[:20],source[::25]]
    rows=[]
    for i,points in enumerate(fixtures):
        inp=a.work/f'fixture{i}.txt';out=a.work/f'fixture{i}.tsv';inp.write_text(f'{len(points)} 96\n'+''.join(' '.join(str(c) for axis in p for c in axis)+'\n' for p in points))
        run=subprocess.run([str(a.filter.resolve()),str(inp),str(out)],text=True,capture_output=True,check=True)
        found={tuple(map(int,line.split())) for line in out.read_text().splitlines()}
        expected={t for t in combinations(range(len(points)),3) if exact.exact_unit_triple(*(points[j] for j in t),96)}
        if found!=expected:raise ValueError('Native/exact fixture mismatch')
        counts=json.loads(run.stdout);rows.append({'vertices':len(points),'triples':counts['triples'],'exact_unit_triples':len(expected)})
    malformed={'too_many_vertices':'517 96\n','wrong_scale':'3 95\n','coefficient_out_of_range':'3 96\n145 '+'0 '*15+'\n'}
    rejected=[]
    for name,text in malformed.items():
        inp=a.work/(name+'.txt');inp.write_text(text)
        run=subprocess.run([str(a.filter.resolve()),str(inp),str(a.work/(name+'.tsv'))],capture_output=True,text=True)
        if run.returncode==0:raise ValueError('Malformed input accepted: '+name)
        rejected.append(name)
    result={'status':'EXACT_FILTER_CONTROLS_PASSED','fixtures':rows,'total_triples':sum(r['triples'] for r in rows),'malformed_inputs_rejected':rejected}
    (a.work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
