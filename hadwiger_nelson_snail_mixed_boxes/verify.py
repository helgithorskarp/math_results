#!/usr/bin/env python3
"""Standard-library checker for all 4,400 Snail mixed boxes."""
from __future__ import annotations
import argparse,base64,hashlib,json,time
from pathlib import Path
import geometry as G

HERE=Path(__file__).parent


def require(test,message):
    if not test:raise ValueError(message)


def unpack(word,n):
    require(type(word) is str,'colour word type')
    try:data=base64.b64decode(word,validate=True)
    except Exception as e:raise ValueError('colour word encoding') from e
    require(len(data)==(n+3)//4,'colour word length')
    if n%4:require(data[-1]>>(2*(n%4))==0,'nonzero colour padding')
    return tuple((data[i//4]>>(2*(i%4)))&3 for i in range(n))


def load(path):
    x=json.loads(Path(path).read_text())
    require(type(x) is dict and set(x)=={'version','family','source_seed_sha256',
            'prime','parameters','high_source_indices','high_overlaps','rows'},'certificate keys')
    require(x['version']==1 and x['family']=='Snail mixed congruence boxes','version/family')
    require(x['source_seed_sha256']==hashlib.sha256((HERE/'seed.json').read_bytes()).hexdigest(),'seed hash')
    require(x['prime']==G.PRIME,'prime')
    require(x['parameters']=={'high_generators':20,'augmentation_generators':22,
            'orders':2,'short_min':2,'short_max':6,'long_min':2,
            'long_max':30,'physical_vertex_cap':508},'parameters')
    require(type(x['rows']) is list and len(x['rows'])==4400,'row count')
    return x


def check_row(row,hpowers,upowers,expected_key,check_maximal=True):
    require(type(row) is list and len(row)==9,'row format')
    require(all(type(v) is int for v in row[:8]),'row integer fields')
    hr,ai,order,long,short,copies,n,edge_count,word=row
    require((hr,ai,order,short)==expected_key,'row key/order')
    require(2<=long<=30 and 2<=short<=6,'box dimensions')
    transforms=G.box(hpowers,upowers,order,long,short)
    require(len(transforms)==copies,'copy count')
    points,edges=G.residue_graph(transforms)
    require(len(points)==n and n<=508,'physical point count')
    require(len(edges)==edge_count,'residue edge count')
    colours=unpack(word,n)
    require(all(colours[i]!=colours[j] for i,j in edges),'monochromatic residue edge')
    if check_maximal and long<30:
        nxt=G.box(hpowers,upowers,order,long+1,short)
        if len(nxt)>len(transforms):
            next_points={x for f in nxt for x in G.cloud(f)}
            require(len(next_points)>508,'nonmaximal long side')
    return {'vertices':n,'copies':copies,'edges':edge_count}


def verify(path,progress=False):
    x=load(path)
    require(len(G.POINTS)==29 and len(set(G.POINTS))==29,'seed points')
    require(len(G.distance_classes())==34,'repeated distance classes')
    require(len(G.all_generators())==925,'all generator count')
    high=G.high_generators();aug=G.augmentation_generators()
    require(len(high)==20 and len(aug)==22,'selected generator counts')
    require([i for _,i,_ in high]==x['high_source_indices'],'high indices')
    require([o for o,_,_ in high]==x['high_overlaps'],'high overlaps')
    rows=iter(x['rows']);stats=[];started=time.monotonic();done=0
    hpowers=[G.powers(t,31) for _,_,t in high]
    upowers=[G.powers(t,7) for t in aug]
    for hr,hp in enumerate(hpowers):
        for ai,up in enumerate(upowers):
            for order in (0,1):
                for short in range(2,7):
                    stats.append(check_row(next(rows),hp,up,(hr,ai,order,short)))
                    done+=1
                    if progress and done%250==0:
                        print(json.dumps({'checked':done,'elapsed_seconds':time.monotonic()-started}),flush=True)
    try:next(rows);raise ValueError('extra row')
    except StopIteration:pass
    result={'verified':True,'cases':len(stats),'all_four_colourable':True,
            'record_improvement':False,
            'physical_vertices_range':[min(s['vertices'] for s in stats),max(s['vertices'] for s in stats)],
            'copy_count_range':[min(s['copies'] for s in stats),max(s['copies'] for s in stats)],
            'residue_edges_range':[min(s['edges'] for s in stats),max(s['edges'] for s in stats)],
            'high_source_indices':x['high_source_indices'],'high_overlaps':x['high_overlaps'],
            'certificate_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    p.add_argument('--progress',action='store_true');a=p.parse_args()
    result=verify(a.certificate,a.progress)
    expected=json.loads((HERE/'expected.json').read_text())
    require(result==expected,'expected result')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
