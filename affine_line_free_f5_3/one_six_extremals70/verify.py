"""Replay the complete six-plane extremal census using only Python and C++20."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
from itertools import combinations,product
import json
from pathlib import Path
import subprocess
import time

HERE=Path(__file__).resolve().parent
P=list(product(range(5),repeat=3))


def require(condition,message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def det(A):
    a,b,c=A
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))%5


def audit_caps(menu):
    caps=json.loads((HERE/'CAPS.json').read_text())
    require(caps['sets']==len(menu)==148000,'six-set menu cardinality')
    maps=[[5*((a*y+b*z+e)%5)+(c*y+d*z+f)%5 for y,z in product(range(5),repeat=2)]
          for a,b,c,d in product(range(5),repeat=4) if (a*d-b*c)%5
          for e,f in product(range(5),repeat=2)]
    require(len(maps)==12000,'affine map count')
    remaining=set(menu)
    for cap in caps['classes']:
        mask=cap['mask'];selected=[i for i in range(25) if mask>>i&1]
        require(len(selected)==6,'six-set representative weight')
        orbit={sum(1<<g[i] for i in selected) for g in maps}
        require(len(orbit)==cap['orbit'] and min(orbit)==mask,'six-set orbit')
        require(orbit<=remaining,'disjoint orbit cover')
        remaining-=orbit
    require(not remaining and len(caps['classes'])==21,'complete six-set cover')
    return [c['mask'] for c in caps['classes']]


def spatial_geometry():
    index={p:i for i,p in enumerate(P)}
    lines={sum(1<<index[tuple((x+t*(y-x))%5 for x,y in zip(a,b))] for t in range(5))
           for a,b in combinations(P,2)}
    normals=[v for v in P if any(v) and next(x for x in v if x)==1]
    planes=[sum(1<<i for i,p in enumerate(P) if sum(a*b for a,b in zip(v,p))%5==t)
            for v in normals for t in range(5)]
    require(len(lines)==775 and len(planes)==155,'independent spatial geometry')
    return lines,planes


def inspect(S,lines,planes):
    require(0<=S<1<<125 and S.bit_count()==70,'spatial cardinality')
    require(not any(S&line==line for line in lines),'full affine line')
    sizes=Counter((S&H).bit_count() for H in planes)
    require(min(sizes)==6 and max(sizes)<=16,'plane sizes')
    mu=tuple(sum(P[i][j] for i in range(125) if S>>i&1)%5 for j in range(3))
    require(mu==(0,0,0),'nonzero coordinate sum')
    blocked=0
    for line in lines:
        if (line&S).bit_count()==4:
            blocked|=line&~S
    require(not (((1<<125)-1)&~S&~blocked),'extendable extremal set')
    return sizes[6]


def audit_models():
    lines,planes=spatial_geometry()
    planar_lines=[line for line in lines if line<1<<25]
    require(len(planar_lines)==30 and all((3238&line).bit_count()<=2 for line in planar_lines),
            'six-point section is not an arc')
    seeds={s['name']:s['points'] for s in json.loads((HERE/'seeds.json').read_text())}
    seed_sixes={name:inspect(sum(1<<i for i in points),lines,planes)
                for name,points in seeds.items()}
    require(sorted(seed_sixes.values())==[4,5,7],'distinct seed affine types')
    models=json.loads((HERE/'models.json').read_text());sections=[];counts=Counter()
    for model in models:
        masks=model['sections']
        require(len(masks)==5 and all(type(m) is int and 0<=m<1<<25 for m in masks),'section format')
        require([m.bit_count() for m in masks]==[6,16,16,16,16],'section sizes')
        require(masks[0]==3238,'six-set type')
        S=sum(m<<(25*x) for x,m in enumerate(masks));six=inspect(S,lines,planes)
        cert=model['affine_map'];A=cert['matrix'];b=cert['translation']
        require(len(A)==3 and all(len(row)==3 for row in A) and len(b)==3,'map dimensions')
        require(all(type(x) is int and 0<=x<5 for row in A for x in row)
                and all(type(x) is int and 0<=x<5 for x in b) and det(A),'invertible affine map')
        require(cert['seed'] in seeds,'unknown seed')
        image=0
        for i in seeds[cert['seed']]:
            q=[(sum(A[j][k]*P[i][k] for k in range(3))+b[j])%5 for j in range(3)]
            image|=1<<(25*q[0]+5*q[1]+q[2])
        require(image==S and six==seed_sixes[cert['seed']],'affine map image')
        sections.append(tuple(masks));counts[cert['seed']]+=1
    require(len(sections)==len(set(sections))==104,'model catalogue')
    # Definition-level negative controls, with no reliance on assert.
    S=sum(m<<(25*x) for x,m in enumerate(sections[0]))
    for damaged in [S&(S-1),S|next(line for line in lines if line&S!=line)]:
        try:
            inspect(damaged,lines,planes)
        except ValueError:
            pass
        else:
            raise ValueError('invalid point-set control accepted')
    require(det([[0,0,0],[0,1,0],[0,0,1]])==0,'singular map control')
    return sorted(sections),dict(sorted(counts.items())),seed_sixes


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--jobs',type=int,choices=[1,2],default=2)
    ap.add_argument('--sanitize',action='store_true')
    ap.add_argument('--write-expected',action='store_true')
    args=ap.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic();flags=['-std=c++20','-Wall','-Wextra','-Wconversion','-Werror']
    flags+=['-O1','-g','-fsanitize=address,undefined','-fno-pie','-no-pie'] if args.sanitize else ['-O3']
    for name in ['planar_menus','section_matching']:
        subprocess.run(['g++',*flags,str(HERE/(name+'.cpp')),'-o',str(out/name)],check=True)
    raw=subprocess.check_output([str(out/'planar_menus'),str(out)],text=True)
    planar=[json.loads(line) for line in raw.splitlines()]
    require(planar==[{'size':6,'line_cap':3,'visited':177100,'accepted':148000},
                     {'size':16,'line_cap':4,'visited':2042975,'accepted':28375},
                     {'size':17,'line_cap':4,'visited':1081575,'accepted':0}], 'planar enumeration')
    menu6=list(map(int,(out/'planar6.txt').read_text().splitlines()))
    require(len(menu6)==len(set(menu6)),'duplicate planar six-set')
    caps=audit_caps(menu6);capfile=out/'caps6.txt'
    capfile.write_text(''.join(str(c)+'\n' for c in caps))
    expected_models,type_counts,seed_sixes=audit_models()
    binary=out/'section_matching';menu=out/'planar16.txt'
    def run(case):
        stem=out/f'case{case:02}';scan=stem.with_suffix('.scan.jsonl')
        triples=stem.with_suffix('.triples.txt');models=stem.with_suffix('.models.jsonl')
        finish=stem.with_suffix('.finish.json')
        census=json.loads(subprocess.check_output([str(binary),'balanced-scan',str(menu),str(capfile),
                                                  str(case),'0','1135',str(scan)],text=True))
        rows=[json.loads(line) for line in scan.read_text().splitlines()]
        require(len(rows)==len({(r['small'],r['a'],r['b']) for r in rows}),'duplicate pair')
        triples.write_text(''.join(f"{r['small']} {r['a']} {r['b']}\n" for r in rows))
        subprocess.run([str(binary),'finish',str(menu),str(triples),str(models),str(finish)],check=True)
        done=json.loads(finish.read_text());actual=[tuple(json.loads(line)) for line in models.read_text().splitlines()]
        require(census['pairs']==32205625 and sum(census['histogram'].values())==census['pairs'],'pair coverage')
        require(done['pairs']==done['balanced_pass']==len(rows) and done['models']==len(actual),'completion coverage')
        census.pop('seconds');done.pop('seconds')
        print(json.dumps({'case':case,'models':len(actual),'retained_pairs':len(rows)}),flush=True)
        return {'case':case,'scan':census,'finish':done},actual
    records=[];actual=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for future in as_completed([pool.submit(run,i) for i in range(21)]):
            record,models=future.result();records.append(record);actual+=models
    records.sort(key=lambda r:r['case'])
    require(len(records)==21 and [r['case'] for r in records]==list(range(21)),'complete case family')
    require(len(actual)==len(set(actual)) and sorted(actual)==expected_models,'complete model census')
    model_data=('\n'.join(','.join(map(str,m)) for m in sorted(actual))+'\n').encode()
    result={'status':'ONE_SIX_EXTREMALS70_VERIFIED','planar':planar,'six_orbits':21,
            'affine_maps_checked':252000,'pairs':sum(r['scan']['pairs'] for r in records),
            'retained_pairs':sum(r['finish']['pairs'] for r in records),'models':len(actual),
            'models_sha256':digest(model_data),'types':type_counts,'seed_six_planes':seed_sixes,
            'menu6_sha256':digest((out/'planar6.txt').read_bytes()),
            'menu16_sha256':digest(menu.read_bytes()),'records':records}
    expected=HERE/'EXPECTED.json'
    if args.write_expected:
        expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(result==json.loads(expected.read_text()),'expected summary mismatch')
    (out/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'models':len(actual),'pairs':result['pairs'],
                      'seconds':time.monotonic()-started}),flush=True)


if __name__=='__main__':
    main()
