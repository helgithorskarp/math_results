"""Exact independent graph reconstruction, exhaustive forcing proof and compiler checks."""
import copy
import json
from hashlib import sha256
from pathlib import Path
from itertools import combinations
from radicals import point,row,cmul,neg,distance,scalar,ROT120
from colour_check import solve
from controls import run as small_controls
from assembly import summary as assembly_summary

ROOT=Path(__file__).resolve().parent

def require(condition,message):
    if not condition:raise ValueError(message)

def read(name):return json.loads((ROOT/name).read_text())
def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def reconstruct():
    representatives=read('appendix.json')
    require(len(representatives)==109 and all(len(p)==4 and all(type(x) is int for x in p)
                                            for p in representatives),'Malformed appendix')
    out=set()
    for p in map(point,representatives):
        for _ in range(3):
            out.add(row(p));out.add(row((neg(p[0]),p[1])))
            p=cmul(ROT120,p)
    first=[(0,0,12,0),(-6,0,-6,0),(6,0,-6,0)]
    require(set(first)<=out and len(out)==627,'Wrong reference vertex set')
    return first+sorted(out-set(first))

def edges(points,length=1296):
    return [[i,j] for i,j in combinations(range(len(points)),2)
            if distance(points[i],points[j])==scalar(length)]

def validate_certificate(cert,reference):
    keep=cert['retained_reference_indices']
    require(type(keep) is list and len(keep)==375 and
            all(type(v) is int and 0<=v<627 for v in keep) and
            keep==sorted(set(keep)) and keep[:3]==[0,1,2],'Malformed retained set')
    require(cert['vertices']==375 and cert['edges']==1661,'Wrong graph size')
    require(cert['terminals']==[0,1,2] and cert['terminal_distance_squared']==[1,3],
            'Wrong terminal convention')
    require(cert['forcing_gate_reached'] is True and cert['target_found'] is False,
            'Wrong claim scope')
    rows=[reference[i] for i in keep];points=list(map(point,rows));es=edges(points)
    require(len(es)==1661,'Wrong exact edge count')
    require(cert['point_sha256']==digest(rows) and cert['edge_sha256']==digest(es),
            'Wrong graph hash')
    word=cert['unpinned_colouring']
    require(type(word) is str and len(word)==375 and set(word)<=set('0123'),
            'Malformed colouring')
    require(all(word[i]!=word[j] for i,j in es),'Invalid unpinned colouring')
    require(all(distance(points[i],points[j])==scalar(432)
                for i,j in combinations(range(3),2)),'Wrong terminal geometry')
    return rows,es

def malformed_controls(cert,reference):
    def rejected(action):
        try:action()
        except ValueError:return
        raise RuntimeError('Malformed control accepted')
    for field,value in [
        ('retained_reference_indices',cert['retained_reference_indices'][:-1]),
        ('retained_reference_indices',[0]+cert['retained_reference_indices'][:-1]),
        ('retained_reference_indices',cert['retained_reference_indices'][:-1]+[627]),
        ('terminals',[0,1,3]),('terminal_distance_squared',[3,1]),
        ('forcing_gate_reached',False),('target_found',True),
        ('unpinned_colouring','4'*375),('unpinned_colouring','0'*375),
        ('point_sha256','0'*64),('edge_sha256','0'*64)]:
        bad=copy.deepcopy(cert);bad[field]=value
        rejected(lambda:validate_certificate(bad,reference))
    return 11

def main():
    reference=reconstruct();refpoints=list(map(point,reference));refedges=edges(refpoints)
    require(len(refedges)==2982,'Reference edge mismatch')
    answer,baseline=solve(627,refedges,[(0,0),(1,0),(2,0)])
    require(answer is None,'Reference is not a forcing graph')
    cert=read('certificate.json');rows,es=validate_certificate(cert,reference)
    answer,forcing=solve(375,es,[(0,0),(1,0),(2,0)])
    require(answer is None,'Marked triangle can be monochromatic')
    g40=list(map(point,read('g40.json')));g49=list(map(point,read('g49.json')))
    e40=edges(g40);pairs=edges(g40,4752);e49=edges(g49)
    require(len(g40)==40 and len(e40)==82 and len(pairs)==59,'Wrong G40')
    require(len(g49)==49 and len(e49)==180 and distance(g49[0],g49[1])==scalar(4752),
            'Wrong G49')
    require(distance(g40[0],g40[1])==scalar(9216),'Wrong spindle arm')
    answer,s40=solve(40,e40+pairs,[(0,0),(1,1)])
    require(answer is None,'G40 composition implication failed')
    triples=[t for t in combinations(range(49),3)
             if all(distance(g49[i],g49[j])==scalar(432) for i,j in combinations(t,2))]
    require(len(triples)==18,'Wrong small triangle count')
    answer,s49=solve(49,e49,[(0,0),(1,0)],triples)
    require(answer is None,'G49 composition implication failed')
    assembly=assembly_summary()
    controls=small_controls();bad=malformed_controls(cert,reference)
    result={'verified':True,'vertices':375,'edges':1661,
            'reference_vertices':627,'reference_edges':2982,
            'reference_search':baseline,'forcing_search':forcing,
            'g40_search':s40,'g49_search':s49,
            'proper_unpinned_four_colouring':True,'monochromatic_triangle_impossible':True,
            'point_sha256':digest(rows),'edge_sha256':digest(es),
            'small_exhaustive_controls':controls,'malformed_controls_rejected':bad,
            'assembly':assembly,'forcing_gate_reached':True,'target_found':False}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
