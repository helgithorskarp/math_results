"""Exact selected EI composition; default checks frames without a large graph dump.

The T375 nonmonochromatic-terminal theorem is an explicitly cited dependency.
Only its hash-pinned geometry helpers are imported here.
"""
import importlib.util
import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEPENDENCY=ROOT.parent/'hadwiger_nelson_small_triangle_forcer375'
DEPENDENCY_HASHES={'radicals.py': '6561705844e5c5c3d34bc692f3ffad569227d77e7a9c022c841abef9c1b7b7be', 'geometry.py': '921fa358c620ed86bd11c6fc9f97ae03ddb491da94612f086cd165a94ffc77bd', 'appendix.json': 'dd74c3ef0bb3e9cc1c9c32f7ecc703c1d85cacaca6fca97834d162e8c05997fa', 'certificate.json': '282fd209157b0c327e02451c32a3d2f2dbb40c4ec31e6531bdd3b8316854b28e', 'verify.py': '31bcc9d2192850a89c82087e15e7a2eeb889ace67fee96b71358a1ebb2b8c02f'}

def load_dependency(name):
    for file,expected in DEPENDENCY_HASHES.items():
        if sha256((DEPENDENCY/file).read_bytes()).hexdigest()!=expected:
            raise ValueError('Changed T375 dependency: '+file)
    spec=importlib.util.spec_from_file_location('ei_minimum_'+name,DEPENDENCY/(name+'.py'))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

radicals=load_dependency('radicals')
ZERO,ONE,ROT_SPINDLE=radicals.ZERO,radicals.ONE,radicals.ROT_SPINDLE
point,scalar,norm,distance=radicals.point,radicals.scalar,radicals.norm,radicals.distance
cmul,frame,apply=radicals.cmul,radicals.frame,radicals.apply

def placements():
    g40=list(map(point,json.loads((ROOT/'g40.json').read_text())))
    g49=list(map(point,json.loads((ROOT/'g49.json').read_text())))
    rotated=[cmul(ROT_SPINDLE,p) for p in g40]
    if norm(ROT_SPINDLE)!=ONE or distance(g40[1],rotated[1])!=scalar(1296):
        raise ValueError('Incorrect spindle rotation')
    base=sorted(set(g40+rotated))
    if len(base)!=79:raise ValueError('Wrong base order')
    pairs=[(i,j) for i,j in combinations(range(40),2)
           if distance(g40[i],g40[j])==scalar(4752)]
    triangles=[t for t in combinations(range(49),3)
               if all(distance(g49[i],g49[j])==scalar(432)
                      for i,j in combinations(t,2))]
    terminals=list(map(point,[(0,0,12,0),(-6,0,-6,0),(6,0,-6,0)]))
    if len(pairs)!=59 or len(triangles)!=18:raise ValueError('Wrong local counts')
    certificate=json.loads((ROOT/'certificate.json').read_text())
    selected=set(certificate['g40']['essential'])|{i for j,i in enumerate(certificate['g40']['optional']) if 151>>j&1}
    pairs=[p for i,p in enumerate(pairs) if i in selected]
    triangles=[t for i,t in enumerate(triangles) if i in certificate['g49']['essential']]
    if len(pairs)!=53 or len(triangles)!=8:raise ValueError('Incorrect selected interfaces')
    g49_frames=[];forcing_frames=[]
    for host in (g40,rotated):
        for i,j in pairs:
            outer=frame(g49[0],g49[1],host[i],host[j],4752)
            if apply(outer,g49[0])!=host[i] or apply(outer,g49[1])!=host[j]:
                raise ValueError('Pair attachment mismatch')
            g49_frames.append(outer)
            for t in triangles:
                targets=[apply(outer,g49[v]) for v in t]
                f=frame(terminals[0],terminals[1],targets[0],targets[1],432)
                if apply(f,terminals[2])!=targets[2]:
                    f=frame(terminals[0],terminals[1],targets[0],targets[1],432,True)
                if any(apply(f,s)!=t for s,t in zip(terminals,targets)):
                    raise ValueError('Triangle attachment mismatch')
                forcing_frames.append(f)
    return base,g49,g49_frames,forcing_frames

def summary():
    from verify import check
    check(json.loads((ROOT/'certificate.json').read_text()))
    base,g49,pair_frames,triangle_frames=placements()
    def canonical(frame):
        z,t,r=frame
        return [[[str(v) for v in xy] for xy in p] for p in (z,t)]+[r]
    data=json.dumps([canonical(f) for f in pair_frames+triangle_frames],separators=(',',':')).encode()
    return {'base_vertices':len(base),'pair_attachments':len(pair_frames),
            'triangle_attachments':len(triangle_frames),
            'vertex_upper_bound':79+len(pair_frames)*47+len(triangle_frames)*372,
            'all_frames_are_exact_isometries':True,
            'frame_sha256':sha256(data).hexdigest()}

def vertices(forcer_points=None):
    """Stream a finite point multiset; the graph uses its set of distinct points.

    The input must be the 375 paper-convention rows, with terminals first.
    The omitted attachment vertices already occur in the earlier components.
    """
    if forcer_points is None:
        reference=load_dependency('geometry').reference()
        certificate=json.loads((DEPENDENCY/'certificate.json').read_text())
        forcer_points=[reference[i] for i in certificate['retained_reference_indices']]
    if len(forcer_points)!=375:raise ValueError('Wrong forcing gadget order')
    base,g49,pair_frames,triangle_frames=placements()
    yield from base
    for f in pair_frames:
        for p in g49[2:]:yield apply(f,p)
    for f in triangle_frames:
        for p in forcer_points[3:]:yield apply(f,point(p))

if __name__=='__main__':
    print(json.dumps(summary(),sort_keys=True))
