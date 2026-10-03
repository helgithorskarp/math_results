"""Exact Q65 plane-tiling and five-disc-corona reader, standard library only."""
from copy import deepcopy
import hashlib,json
from pathlib import Path
import lower,tiling
BASE=Path(__file__).resolve().parent
require=lower.require

def symmetry(certificate):
    """The known quarter turn permutes the eight copies modulo the lattice."""
    (a,b),(c,d)=certificate['periods'];det=a*d-b*c
    q=certificate['quarter_turn'];m=q['matrix'];shift=q['translation']
    require(m==[0,-1,1,0] and all(type(z) is int for z in shift),'not the declared grid quarter turn')
    reps=certificate['representatives'];permutation=[]
    for rep in reps:
        g,h,i,j=rep['matrix'];x,y=rep['translation']
        target=[-i,-j,g,h];tx,ty=shift[0]-y,shift[1]+x
        matches=[]
        for k,new in enumerate(reps):
            if target!=new['matrix']:continue
            dx,dy=tx-new['translation'][0],ty-new['translation'][1]
            if (d*dx-c*dy)%det==0 and (a*dy-b*dx)%det==0:matches.append(k)
        require(len(matches)==1,'quarter turn does not map this representative to one lattice class')
        permutation.append(matches[0])
    require(sorted(permutation)==list(range(8)),'quarter turn does not permute eight representatives')
    remaining=set(range(8));cycles=[]
    while remaining:
        first=min(remaining);cycle=[];current=first
        while current in remaining:
            remaining.remove(current);cycle.append(current);current=permutation[current]
        require(current==first,'invalid representative cycle');cycles.append(cycle)
    require(sorted(map(len,cycles))==[4,4],'not the two declared four-copy orbits')
    return {'quarter_turn_center':[0,5],'representative_permutation':permutation,'orbit_cycles':cycles}

def verify():
    data=json.loads((BASE/'input.json').read_text())
    construction=json.loads((BASE/'five-coronas.json').read_text())
    certificate=json.loads((BASE/'tiling.json').read_text())
    require(data['cells']==construction['cells'] and len(data['cells'])==65,'literal prototype binding differs')
    positive=lower.check(construction);plane=tiling.check(data['cells'],certificate);rotation=symmetry(certificate)
    require(positive['complete_disc_coronas']==5 and plane['copies_per_period']==8,'wrong declared counts')
    tests=[]
    def rejects(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):tests.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    bad=deepcopy(construction);bad['levels'][0][0][1]+=1
    rejects('translated literal root',lambda:lower.check(bad))
    bad=deepcopy(construction);bad['levels'][1]=[]
    rejects('missing first corona',lambda:lower.check(bad))
    bad=deepcopy(construction);bad['levels'][5]=[]
    rejects('missing fifth corona',lambda:lower.check(bad))
    bad=deepcopy(construction);bad['levels'][5].append(bad['levels'][5][0])
    rejects('duplicated fifth whole copy',lambda:lower.check(bad))
    bad=deepcopy(certificate);bad['representatives'].pop()
    rejects('dropped periodic representative',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(certificate);bad['representatives'][0]['translation'][0]+=1
    rejects('moved periodic whole copy',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(certificate);bad['representatives'][1]=deepcopy(bad['representatives'][0])
    rejects('duplicated periodic whole copy',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(certificate);bad['representatives'][0]['matrix']=[1,1,0,1]
    rejects('nonisometric shear',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(certificate);bad['periods'][1]=bad['periods'][0]
    rejects('singular period lattice',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(certificate);bad['periods'][0][0]+=1
    rejects('changed lattice area',lambda:tiling.check(data['cells'],bad))
    bad=deepcopy(data['cells']);bad[-1]=bad[0]
    rejects('duplicate prototype cell',lambda:tiling.check(bad,certificate))
    bad=deepcopy(certificate);bad['quarter_turn']['translation'][0]+=1
    rejects('changed quarter-turn center',lambda:symmetry(bad))
    return {'agent':'six-heesch-1','role':'researcher','plane_tiling':plane,'periods':certificate['periods'],
        'known_symmetry':rotation,'five_disc_coronas':positive,'damaged_cases_rejected':tests,
        'heesch_by_plane_tiler_convention':'infinity',
        'status':'Q65 tiles the plane and is excluded from the finite-Heesch search. The finite-five polyomino target remains open.'}

def main():
    result=verify();expected=json.loads((BASE/'expected.json').read_text())
    require(result==expected,'expected reader evidence differs')
    manifest=json.loads((BASE/'manifest.json').read_text())
    require(sorted(manifest)==sorted(p.name for p in BASE.iterdir() if p.is_file() and p.name!='manifest.json'),'manifest file coverage differs')
    for name,digest in manifest.items():require(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,'manifest mismatch: '+name)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
