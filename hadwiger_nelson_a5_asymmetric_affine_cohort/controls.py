#!/usr/bin/env python3
"""Small exact projection, coverage, geometry and semantic corruption controls."""
import copy
import importlib.util
import json
import model as M
spec=importlib.util.spec_from_file_location('affine_cohort_verifier_control',M.HERE/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)


def run():
    x,y=M.sp.symbols('x y')
    cases=[(x,y,1),(x,y*y-1,2),(x,y*y+1,0),(x*x-2,y-x,2),
           (x*y-1,x*y+x-1,0),(x*x+y*y-1,x*x-y*y,4)]
    for f,g,n in cases:
        sparse=lambda f:tuple(sorted((i,j,int(c)) for (i,j),c in M.sp.Poly(f,x,y).terms()))
        polys={0:sparse(f),1:sparse(g)}
        a=M.charts([0,1],polys,'groebner');b=M.charts([0,1],polys,'resultant')
        M.need(a==b and sum(c['real_embeddings'] for c in a)==n,'hand-checkable real-root cover')
        for c in a:M.root_intervals(c)
    fixtures=[({'q':['0','1'],'x':['0'],'y':['0']},3,3),
              ({'q':['0','1'],'x':['1'],'y':['0']},21,45),
              ({'q':['0','1'],'x':['1/2'],'y':['1/2']},27,63)]
    for c,n,e in fixtures:
        points,labels,edges,triangle=M.physical.graph(c)
        M.need((len(points),len(edges))==(n,e),'exact elementary physical fixture')
    c=dict(fixtures[0][0],real_embeddings=1,colour_count=3,colour_word=[0,1,2])
    points,labels,edges,_=M.physical.graph(c)
    c.update(root_intervals=M.root_intervals(c),point_count=len(points),edge_count=len(edges),
             point_sha256=M.digest(M.point_stream(points)),label_map_sha256=M.digest(labels),edge_sha256=M.digest(edges))
    V.check_physical(c)
    changes=[('colour_word',[0,0,2]),('colour_count',5),('point_count',4),
             ('edge_sha256','0'*64),('label_map_sha256','0'*64),('point_sha256','0'*64),
             ('root_intervals',[['1','1']]),('q',['0','-1','1'])]
    for key,val in changes:
        bad=copy.deepcopy(c);bad[key]=val
        try:V.check_physical(bad)
        except ValueError:pass
        else:raise ValueError('corruption was accepted: '+key)
    return {'status':'PASS','exact_root_cover_cases':len(cases),'elementary_complete_graphs':len(fixtures),'semantic_corruptions_rejected':len(changes)}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
