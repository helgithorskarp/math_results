from itertools import product,permutations
from pathlib import Path
import json,time

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'profiles.json').read_text())
PROFILES=tuple(map(tuple,data['profiles']));PAIRS=tuple(map(tuple,data['pairs']))
PROFILE_ID={p:i for i,p in enumerate(PROFILES)}
PAIR_ID={p:i for i,p in enumerate(PAIRS)}
POINTS=tuple(product(range(5),repeat=2))
NORMALS=tuple((1,a) for a in range(5))+((0,1),)
VALUES=tuple(tuple((a*x+b*y)%5 for x,y in POINTS) for a,b in NORMALS)
LINES=tuple(tuple(tuple(i for i in range(25) if values[i]==b) for b in range(5)) for values in VALUES)

def validate(key):
    kind,word=key
    if not 0<=kind<20 or len(word)!=25 or any(c not in '01234' for c in word):raise ValueError('invalid typed word')
    w=tuple(map(int,word))
    if sum(w)!=71:raise ValueError('incorrect total')
    profiles=tuple(tuple(sum(w[i] for i in line) for line in family) for family in LINES)
    if any(min(p)<7 or max(p)>16 for p in profiles):raise ValueError('invalid plane bound')
    a,b=PAIRS[kind]
    if (profiles[0],profiles[5])!=(PROFILES[a],PROFILES[b]):raise ValueError('incorrect pair profile')
    if w[0]>(PROFILES[a][0]+PROFILES[b][0]-7)//5:raise ValueError('intersection cap')
    if any(w[i]>3 or w[5*i]>3 for i in range(5)):raise ValueError('axis cap')
    return profiles

def orbit(key):
    profiles=validate(key);word=key[1];low=[]
    for direction,profile in enumerate(profiles):
        for b,m in enumerate(profile):
            if m>10:continue
            for scale in range(1,5):
                transformed=tuple(profile[(b+pow(scale,-1,5)*j)%5] for j in range(5))
                kind=PROFILE_ID.get(transformed)
                if kind is not None:low.append((direction,b,scale,kind))
    images=set()
    for (d,b,s,i),(e,c,t,j) in permutations(low,2):
        kind=PAIR_ID.get((i,j))
        if d==e or kind is None:continue
        image=['']*25
        for k in range(25):
            image[5*(s*(VALUES[d][k]-b)%5)+t*(VALUES[e][k]-c)%5]=word[k]
        if any(x=='' for x in image):raise RuntimeError('singular map')
        images.add((kind,''.join(image)))
    return images

def classify(keys, progress=None):
    keys=sorted(keys)
    remaining=set(keys)
    if len(remaining)!=len(keys):raise RuntimeError('duplicate input')
    representatives=[]
    for representative in keys:
        if representative not in remaining:continue
        images=orbit(representative)
        if not images<=remaining or min(images)!=representative:raise RuntimeError('bad orbit cover')
        for image in images:validate(image)
        remaining-=images
        representatives.append({'type':representative[0],'weights':representative[1],'orbit_size':len(images)})
        if progress is not None and len(representatives)%5000==0:
            progress(len(representatives),len(remaining))
    if remaining or sum(x['orbit_size'] for x in representatives)!=len(keys):raise RuntimeError('incomplete')
    return representatives

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--catalogue',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    keys=[(int(parts[0]),parts[1]) for parts in map(str.split,args.catalogue.read_text().splitlines())]
    r=classify(keys)
    args.out.write_text('[\n'+',\n'.join(json.dumps(x,separators=(',',':')) for x in r)+'\n]\n')
    print(json.dumps({'typed':len(keys),'orbits':len(r)}))
