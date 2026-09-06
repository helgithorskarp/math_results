"""Reconstruct the overlap supports using the compact retained indices, no SAT."""
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'hadwiger_nelson_small_triangle_forcer375'))
import geometry as g
from colour_check import solve

def main():
    w=ROOT/'out';w.mkdir(exist_ok=True)
    cert=json.loads((ROOT/'certificate.json').read_text())
    subprocess.run([sys.executable,str(ROOT/'compose.py')],cwd=ROOT,check=True)
    def check(key,name):
        raw=json.loads((w/(name+'.json')).read_text());x=cert[key]
        points=[raw['points'][i] for i in x['retained_union_indices']]
        if points!=x['points'] or raw['denominator']!=x['denominator']:
            raise ValueError('Retained coordinate mismatch: '+key)
        return len(raw['points']),len(raw['edges'])
    first=check('unequal','inequality_union')
    (w/'inequality_union_reduced.json').write_text(json.dumps(cert['unequal'])+'\n')
    pts=g.read('g40.json');es=g.edges(pts);pairs=g.edges(pts,4752)
    ks=[pairs[i] for i in cert['g40_pair_indices']]
    answer,stats=solve(len(pts),es+ks,pins=[(0,0),(1,1)])
    if answer is not None:raise ValueError('G40 implication fails')
    (w/'g40_kernel.json').write_text(json.dumps({'points':pts,'pairs':ks})+'\n')
    subprocess.run([sys.executable,str(ROOT/'outer.py')],cwd=ROOT,check=True)
    second=check('equal','equality_union')
    print(json.dumps({'inequality_union':first,'equality_union':second,'g40_unit_edges':len(es),'g40_long_constraints':len(ks),'g40_search':stats},sort_keys=True))
if __name__=='__main__':main()
