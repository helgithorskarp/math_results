"""Independent literal family and witness verification; no producer imports."""
from itertools import combinations
import json


def verify(data,certificate):
    def need(ok,msg):
        if not ok:raise ValueError(msg)
    need(type(data.get('n')) is int and data['n']==43,'order')
    core=data.get('core_embedding');c=data.get('core_color')
    need(isinstance(core,list) and len(core)==20 and all(type(v) is int and 0<=v<43 for v in core) and len(set(core))==20,'embedding')
    need(type(c) is int and c in (0,1),'color orientation')
    need(isinstance(data.get('red_edges'),list),'edge list')
    red=set()
    for pair in data['red_edges']:
        need(isinstance(pair,list) and len(pair)==2 and all(type(v) is int for v in pair),'pair syntax')
        u,v=pair;need(0<=u<v<43 and (u,v) not in red,'pair identity');red.add((u,v))
    degrees=[0]*43
    for u,v in combinations(range(43),2):
        if ((u,v) in red)==bool(c):degrees[u]+=1;degrees[v]+=1
    need(sorted(degrees)==[19]*2+[20]*5+[21]*36,'full physical degree profile')
    pentagon={(0,1),(1,2),(2,3),(3,4),(0,4)}
    for i,j in combinations(range(20),2):
        b,d=i//5,j//5
        expected=(i%5,j%5) in pentagon if b==d else (b,d) in ((0,1),(1,2),(2,3))
        physical=tuple(sorted((core[i],core[j]))) in red
        need((physical==bool(c))==expected,'literal core pair')
    need(certificate.get('schema')==1,'witness schema')
    q=certificate.get('five');color=certificate.get('color')
    need(isinstance(q,list) and len(q)==5 and all(type(v) is int and 0<=v<43 for v in q) and len(set(q))==5,'five labels')
    need(type(color) is int and color in (0,1),'witness color')
    need(all((tuple(sorted((u,v))) in red)==bool(color) for u,v in combinations(q,2)),'ten physical pairs')
    mechanism=certificate.get('mechanism');number=sum(v in core for v in q)
    need((mechanism=='one_vertex_attachment' and number==4) or
         (mechanism=='edge_class_red_triangle' and number==2 and color==c) or
         (mechanism=='edge_class_blue_four' and number==1 and color!=c),'mechanism scope')
    return {'status':'VERIFIED_PHYSICAL_PROFILE_BRANCH_FIVE','color':color,'five':q,
            'mechanism':mechanism,'pairs_checked':10,'profile_vertices_checked':43,'core_pairs_checked':190}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('certificate');args=p.parse_args()
    print(json.dumps(verify(json.load(open(args.graph)),json.load(open(args.certificate))),indent=2))
