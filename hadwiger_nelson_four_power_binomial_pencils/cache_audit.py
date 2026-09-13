#!/usr/bin/env python3
"""Compare complete literal and cached physical edge lists at pencil412 anchors."""
import argparse,json
from pathlib import Path
from interface import A,physical
import direct

def run(path):
    cert=json.loads(Path(path).read_text());records={c['key']:c for c in cert['components']}
    row=next(p for p in cert['pairs'] if p['pair']==[231,395]);out=[]
    for key in row['components']:
        c=records[key]
        if not c['real_embeddings']:continue
        plain=physical.graph(c);cached=direct.graph(c)
        A.need(plain==cached[:4],'entrywise literal/cached coordinates, collisions, edges and triangle')
        out.append({'degree':len(c['q'])-1,'real_parameters':c['real_embeddings'],'points':len(plain[0]),'edges':len(plain[2]),'physical_pairs':len(plain[0])*(len(plain[0])-1)//2,'cached_norm_tests':cached[4],'edge_sha256':A.digest(plain[2])})
    A.need(sorted(c['degree'] for c in out)==[1,23],'rational collision and high-degree injective fixtures')
    return {'status':'PASS','anchor_pair':[231,395],'complete_graph_comparisons':sorted(out,key=lambda c:c['degree'])}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.certificate),sort_keys=True,indent=2))
