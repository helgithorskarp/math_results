#!/usr/bin/env python3
"""Second geometry route: original Mathematica coordinates, all point pairs."""
from hashlib import sha256
import json
from pathlib import Path
import encode

REPO=Path(__file__).resolve().parent.parent


def main():
    source,U=encode.pool_input()
    original=encode.load('original_geometry',REPO/'hadwiger_nelson_parts509_pool_shape_closure/exactgeom.py')
    points,_=original.build(REPO)
    den,points=original.scale_points(points)
    vertices=list(range(374))+U
    encode.require(len({tuple(points[v][0])+tuple(points[v][1]) for v in vertices})==677,'distinct points')
    edges=original.unit_pairs(points,den,vertices)
    digest=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest()
    encode.require(digest=='64a0f52154cb05b657a320c16569316cd1cba90748ed6dff71d4f45ca862b550','edge stream')
    table=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    ipos={v:i for i,v in enumerate(table['interface_L'])}
    pos={v:i for i,v in enumerate(U)}
    pool=sorted((pos[a],pos[b]) for a,b in edges if a in pos and b in pos)
    cross=sorted((ipos[a],pos[b]) for a,b in edges if a<374<=b)
    encode.require(source['edges']==pool and source['cross']==cross,'encoding geometry differs')
    print(json.dumps(dict(status='QBF INPUT VERIFIED BY ORIGINAL GEOMETRY',points=677,
        unit_edges=len(edges),denominator=den,pool_edges=len(pool),cross_edges=len(cross),
        edge_sha256=digest),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
