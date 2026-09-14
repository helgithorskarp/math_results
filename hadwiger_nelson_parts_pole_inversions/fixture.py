"""Direct Cartesian eight-radical inversion of the largest residue example."""
import json,hashlib,time,argparse
from fractions import Fraction as F
from math import lcm
from pathlib import Path
from itertools import combinations
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json'
SOURCE_SHA='41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729'
RAD=(1,3,5,15,11,33,55,165)
ZERO=(0,)*8
ONE=(1,)+(0,)*7
def need(c,message):
    if not c:raise ValueError(message)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i^j]+=x*y*RAD[i&j]
    return tuple(out)
def inverse(a):
    b=ONE
    for mask in range(1,8):b=mul(b,tuple(-x if (i&mask).bit_count()%2 else x for i,x in enumerate(a)))
    d=mul(a,b);need(d[0]!=0 and d[1:]==(0,)*7,'inverse norm')
    return tuple(F(x)/d[0] for x in b)
def run(work):
    t=time.time();work=Path(work);work.mkdir(parents=True,exist_ok=True)
    need(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA,'changed source')
    raw=json.loads(SOURCE.read_text())['coordinates'];P=[tuple(tuple(F(x) for x in row) for row in raw[str(i)]) for i in range(509)]
    out=[]
    for i in range(1,509):
        x,y=(sub(a,b) for a,b in zip(P[i],P[0]));n=add(mul(x,x),mul(y,y));iv=inverse(n)
        q=tuple(tuple(F(2,3)*z for z in mul(row,iv)) for row in (x,y))
        den=lcm(*(z.denominator for row in q for z in row));out.append((tuple(int(den*z) for z in q[0]),tuple(int(den*z) for z in q[1]),den))
    need(len(set(out))==508,'inverted collision')
    edges=[];stream=hashlib.sha256()
    for i,j in combinations(range(508),2):
        x1,y1,d1=out[i];x2,y2,d2=out[j]
        x=tuple(a*d2-b*d1 for a,b in zip(x1,x2));y=tuple(a*d2-b*d1 for a,b in zip(y1,y2))
        dist=add(mul(x,x),mul(y,y));need(dist!=(0,)*8,'exact point collision')
        if dist==((d1*d2)**2,)+(0,)*7:edges.append((i,j))
        # Complete physical squared-distance stream, with canonical fractions.
        stream.update(('|'.join(str(F(z,(d1*d2)**2)) for z in dist)+'\n').encode())
    cert=json.loads((HERE/'certificate.json').read_text());row=next(c for c in cert if c['pole']==0 and c['residue']==250000070)
    need(all(row['word'][i]!=row['word'][j] for i,j in edges),'exact word failure')
    edge_hash=hashlib.sha256(''.join(f'{i} {j}\n' for i,j in edges).encode()).hexdigest()
    result={'pole':0,'scale_numerator':2,'scale_denominator':3,'points':508,'edges':len(edges),'pair_checks':128778,'edges_sha256':edge_hash,'squared_distance_stream_sha256':stream.hexdigest(),'word_verified':True,'max_coordinate_numerator_bits':max(abs(z).bit_length() for a,b,d in out for z in a+b),'max_coordinate_denominator_bits':max(d.bit_length() for a,b,d in out),'seconds':time.time()-t}
    (work/'fixture_edges.json').write_text(json.dumps(edges)+'\n');(work/'fixture.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();run(args.work)
