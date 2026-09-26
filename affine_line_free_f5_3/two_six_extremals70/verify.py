"""Complete constructive census, affine certificates, and 262 checked exclusions."""
import argparse
from collections import Counter, defaultdict
import ctypes
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import time

from pysat.solvers import Cadical195
from point_model import generate, geometry, POINTS, fiber_clauses

HERE=Path(__file__).resolve().parent
PLANAR=list(product(range(5),repeat=2))
NORMALS=[(1,a) for a in range(5)]+[(0,1)]
VALUES=[[(a*x+b*y)%5 for x,y in PLANAR] for a,b in NORMALS]


def require(condition,message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def determinant(A):
    a,b,c=A
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))%5


def validate_word(w):
    require(len(w)==25 and set(w)<=set('01234'),'word format')
    weights=list(map(int,w))
    require(sum(weights)==70,'quotient cardinality')
    profiles=[[sum(weights[i] for i in range(25) if values[i]==t)
               for t in range(5)] for values in VALUES]
    require(profiles[0]==profiles[-1]==[6,16,16,16,16],'axis profiles')
    require(all(6<=v<=16 for row in profiles for v in row),'plane cap')
    require(weights[0]<=1 and max(weights[:5]+weights[::5])<=3,'axis bounds')
    return profiles


def orbit(w):
    profiles=validate_word(w)
    low=[(d,t) for d in range(6) for t in range(5) if profiles[d][t]==6]
    images=set()
    for (d,t),(e,u) in permutations(low,2):
        if d==e:
            continue
        for a,b in product(range(1,5),repeat=2):
            image=['']*25
            for i in range(25):
                j=5*(a*(VALUES[d][i]-t)%5)+b*(VALUES[e][i]-u)%5
                require(not image[j],'singular quotient map')
                image[j]=w[i]
            image=''.join(image)
            validate_word(image)
            images.add(image)
    return images


def partition(words):
    remaining=set(words);out=[]
    require(len(remaining)==len(words),'duplicate quotient')
    for w in sorted(words):
        if w not in remaining:
            continue
        images=orbit(w)
        require(images<=remaining and min(images)==w,'invalid orbit cover')
        out.append({'word':w,'orbit_size':len(images)})
        remaining-=images
    require(not remaining,'incomplete orbit partition')
    return out


def independent_lines():
    """Construct lines from all pairs of points, without normalizing directions."""
    index={p:i for i,p in enumerate(POINTS)}
    result=set()
    for a,b in combinations(POINTS,2):
        result.add(tuple(sorted(index[tuple((x+t*(y-x))%5 for x,y in zip(a,b))]
                                for t in range(5))))
    require(len(result)==775,'independent affine geometry')
    return sorted(result)


def inspect_points(points,lines):
    S=set(points)
    require(len(points)==len(S)==70 and S<=set(range(125)),'point list')
    require(not any(set(line)<=S for line in lines),'full affine line')
    mu=[sum(POINTS[p][j] for p in points)%5 for j in range(3)]
    free=[q for q in range(125) if q not in S
          and not any(set(line)<=S|{q} for line in lines if q in line)]
    require(mu==[0,0,0],'nonzero coordinate sum')
    require(not free,'extendable 70-point set')
    return S


def validate_models(representatives):
    lines=independent_lines()
    encoded,_=geometry()
    require(lines==sorted(tuple(p-1 for p in line) for line in encoded),'geometry mismatch')
    seeds={s['name']:s for s in json.loads((HERE/'seeds.json').read_text())}
    for seed in seeds.values():
        inspect_points(seed['points'],lines)
    _,all_planes=geometry()
    six_counts={name:sum(sum(p-1 in set(seed['points']) for p in plane)==6
                         for plane in all_planes) for name,seed in seeds.items()}
    require(sorted(six_counts.values())==[4,5,7],'three distinct seed types')
    models=json.loads((HERE/'models.json').read_text());groups=defaultdict(list);seen=set()
    words={r['word'] for r in representatives}
    for model in models:
        w=model['word'];points=model['points'];S=inspect_points(points,lines)
        require(w in words,'unknown model quotient')
        require(tuple(points) not in seen,'duplicate model')
        seen.add(tuple(points))
        require(all(sum(p//5==i for p in points)==int(w[i]) for i in range(25)),
                'model fiber mismatch')
        formula,gauge=generate(w)
        require(all(5*i not in S for i in gauge),'height gauge')
        truth={p+1 for p in S}
        require(all(any((v>0)==(abs(v) in truth) for v in c) for c in formula.clauses),'model CNF')
        cert=model['affine_map'];A=cert['matrix'];t=cert['translation']
        require(len(A)==3 and all(len(row)==3 for row in A) and len(t)==3,'affine map shape')
        require(all(type(x) is int and 0<=x<5 for row in A for x in row)
                and all(type(x) is int and 0<=x<5 for x in t) and determinant(A),'invertible affine map')
        require(cert['seed'] in seeds,'seed name')
        image=set()
        for p in seeds[cert['seed']]['points']:
            y=[(sum(A[j][k]*POINTS[p][k] for k in range(3))+t[j])%5 for j in range(3)]
            image.add(25*y[0]+5*y[1]+y[2])
        require(image==S,'incorrect affine equivalence certificate')
        groups[w].append(points)
    # Negative fixture control: the checked matrix must reject an incorrect map.
    damaged=json.loads(json.dumps(models[0]));damaged['affine_map']['matrix'][0]=[0,0,0]
    require(determinant(damaged['affine_map']['matrix'])==0,'singular-map control')
    return groups,len(models),six_counts


def cnf_bytes(formula):
    return (f'p cnf {formula.nv} {len(formula.clauses)}\n'
            +''.join(' '.join(map(str,c))+' 0\n' for c in formula.clauses)).encode()


def checker_accepts(checker,cnf,proof,log):
    with log.open('w') as output:
        result=subprocess.run([str(checker),str(cnf),str(proof)],stdout=output,stderr=subprocess.STDOUT)
    return result.returncode==0 and 's VERIFIED' in log.read_text()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--drat-trim',type=Path,required=True)
    ap.add_argument('--sanitize',action='store_true')
    ap.add_argument('--write-expected',action='store_true')
    ap.add_argument('--conflicts',type=int,default=1000000)
    args=ap.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    checker=args.drat_trim.resolve();started=time.monotonic()
    flags=['-std=c++20','-Wall','-Wextra','-Wconversion','-Werror']
    flags+=['-O1','-g','-fsanitize=address,undefined','-fno-pie','-no-pie'] if args.sanitize else ['-O3']
    for name in ['deficit_quotients','row_quotients','full_affine','planar_cap']:
        subprocess.run(['g++',*flags,str(HERE/(name+'.cpp')),'-o',str(out/name)],check=True)
    cap=subprocess.check_output([str(out/'planar_cap')],text=True).strip()
    require(cap=='PLANAR_CAP16 1081575 0','planar cap census')
    catalogues=[]
    for name in ['deficit_quotients','row_quotients']:
        p=subprocess.run([str(out/name)],capture_output=True,text=True,check=True)
        words=p.stdout.splitlines()
        require(len(words)==len(set(words)),'duplicate generated quotient')
        words.sort()
        for w in words:validate_word(w)
        catalogues.append(words)
    require(catalogues[0]==catalogues[1],'independent quotient disagreement')
    words=catalogues[0];raw=('\n'.join(words)+'\n').encode();(out/'quotients.txt').write_bytes(raw)
    reps=partition(words);repbytes=('\n'.join(r['word'] for r in reps)+'\n').encode()
    (out/'representatives.txt').write_bytes(repbytes)
    affine=json.loads(subprocess.check_output([str(out/'full_affine'),str(out/'quotients.txt'),
                                              str(out/'representatives.txt')],text=True))
    require(affine['sizes']==[r['orbit_size'] for r in reps],'full affine orbit disagreement')
    require(affine['covered']==len(words) and affine['maps']==12000*len(reps),'affine audit counters')
    groups,model_count,six_counts=validate_models(reps)
    # Audit all 160 truth assignments of the direct five-variable cardinality code.
    for n in range(5):
        clauses=fiber_clauses([1,2,3,4,5],n)
        for assignment in product([False,True],repeat=5):
            sat=all(any((v>0)==assignment[abs(v)-1] for v in c) for c in clauses)
            require(sat==(sum(assignment)==n),'fiber encoding')
    # Missing-model control must expose the deliberately omitted feasible object.
    control_word=next(iter(groups));formula,_=generate(control_word)
    for model in groups[control_word][1:]:formula.append([-p-1 for p in model])
    with Cadical195(bootstrap_with=formula.clauses) as s:
        require(s.solve() is True,'missing-model control must be SAT')
        actual=sorted(v-1 for v in s.get_model() if 0<v<=125)
        require(actual==groups[control_word][0],'missing-model control returned another object')
    # An invalid proof of a satisfiable formula must not pass the independent checker.
    badcnf=out/'invalid.cnf';badproof=out/'invalid.drat';badlog=out/'invalid.log'
    badcnf.write_text('p cnf 2 1\n1 2 0\n');badproof.write_text('0\n')
    require(not checker_accepts(checker,badcnf,badproof,badlog),'invalid proof accepted')
    libc=ctypes.CDLL(None);libc.fflush.argtypes=[ctypes.c_void_p];libc.fflush.restype=ctypes.c_int
    records=[];proof_bytes=0
    for i,r in enumerate(reps):
        formula,gauge=generate(r['word'])
        for model in groups[r['word']]:formula.append([-p-1 for p in model])
        require(formula.nv==125,'unexpected primary variable domain')
        cnf=out/f'case_{i:03}.cnf';proof=out/f'case_{i:03}.drat';log=out/f'case_{i:03}.log'
        data=cnf_bytes(formula);cnf.write_bytes(data)
        with Cadical195(bootstrap_with=formula.clauses,with_proof=True) as solver:
            solver.conf_budget(args.conflicts);answer=solver.solve_limited()
            require(answer is False,f'incomplete census at case {i}: {answer}')
            require(libc.fflush(None)==0,'proof stream flush')
            solver.prfile.seek(0);proof.write_bytes(solver.prfile.read())
        require(checker_accepts(checker,cnf,proof,log),f'proof check failed at {i}')
        proof_bytes+=proof.stat().st_size
        records.append({'index':i,'word':r['word'],'models':len(groups[r['word']]),
                        'cnf_sha256':sha(data),'proof_sha256':sha(proof.read_bytes()),
                        'proof_bytes':proof.stat().st_size})
        if (i+1)%50==0:print(json.dumps({'checked':i+1,'total':len(reps)}),flush=True)
    stable={'status':'TWO_SIX_EXTREMALS_CLASSIFICATION_VERIFIED','planar_17_subsets':1081575,
            'quotients':len(words),'quotient_sha256':sha(raw),'classes':len(reps),
            'representative_sha256':sha(repbytes),'full_affine_maps':affine['maps'],
            'models':model_count,'positive_classes':sum(bool(v) for v in groups.values()),
            'positive_counts':{w:len(v) for w,v in sorted(groups.items()) if v},
            'checked_unsat_formulas':len(records),'models_sha256':sha((HERE/'models.json').read_bytes()),
            'all_models_zero_sum':True,'all_models_maximal':True,'affine_seed_types':len(six_counts),
            'seed_six_plane_counts':six_counts}
    expected=HERE/'EXPECTED.json'
    if args.write_expected:expected.write_text(json.dumps(stable,indent=2)+'\n')
    else:require(stable==json.loads(expected.read_text()),'expected summary mismatch')
    run={'result':stable,'proof_bytes':proof_bytes,'checker_sha256':sha(checker.read_bytes()),
         'seconds':time.monotonic()-started,'compiler_flags':flags,'records':records}
    (out/'verification.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps({**stable,'proof_bytes':proof_bytes,'seconds':run['seconds']},indent=2))


if __name__=='__main__':
    main()
