"""Literal known21-vertex fixture; optional primary-source complement comparison."""
from pathlib import Path
import argparse,ast,json
from hashlib import sha256
from itertools import combinations
from incidence import need


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--primary');args=ap.parse_args()
    source=Path(__file__).resolve().parent
    raw=(source/'baseline21.rows').read_bytes();rows=raw.decode().splitlines()
    need(len(rows)==21 and all(len(s)==21 and set(s)<=set('01') for s in rows),'wrong21 fixture shape')
    a=[[int(s) for s in row] for row in rows]
    need(all(a[i][i]==0 and all(a[i][j]==a[j][i] for j in range(21)) for i in range(21)),'wrong21 fixture graph')
    maxima=[0,0]
    for i,j in combinations(range(21),2):
        red=a[i][j]
        common=sum(a[i][k]*a[j][k] if red else int(k!=i and k!=j and not a[i][k] and not a[j][k]) for k in range(21))
        maxima[0 if red else 1]=max(maxima[0 if red else 1],common)
    need(maxima==[3,6] and sum(map(sum,a))//2==93,'wrong21 fixture page bounds')
    result=dict(vertices=21,red_edges=93,red_page_max=3,blue_page_max=6,fixture_sha256=sha256(raw).hexdigest(),known_primary_construction=True)
    if args.primary:
        body=Path(args.primary).read_bytes();pin=json.loads((source/'INPUT.json').read_text())['primary_fixture']
        need(sha256(body).hexdigest()==pin['sha256'],'primary input bytes differ')
        b=ast.literal_eval(body.decode().split('\n\n',1)[0])
        need(len(b)==21 and all(len(row)==21 and all(type(x) is int and x in (0,1) for x in row) for row in b),'invalid primary matrix')
        need(all(a[i][j]==int(i!=j and not b[i][j]) for i in range(21) for j in range(21)),'primary complement differs')
        result['primary_complement_entries']=441
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
