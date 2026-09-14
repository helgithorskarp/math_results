"""Positive replay using actual inverted modular coordinates and all pair ratios."""
import argparse,json,hashlib,subprocess,time
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import model as m
from scan import run
import fixture
HERE=Path(__file__).resolve().parent

def alternate_projection():
    # Directly evaluate all eight Cartesian radical coefficients, independently
    # of the producer's four-dimensional parity reduction.
    p=m.P;r3=pow(3,(p+1)//4,p);m.require(r3*r3%p==3,'sqrt3 unavailable')
    r11=m.ROOT33*pow(r3,-1,p)%p
    basis=[1,r3,m.ROOT5,r3*m.ROOT5%p,r11,r3*r11%p,m.ROOT5*r11%p,r3*m.ROOT5%p*r11%p]
    rad=[1,3,5,15,11,33,55,165]
    m.require(all(a*a%p==b for a,b in zip(basis,rad)),'Cartesian radical images')
    raw=json.loads(m.SOURCE.read_text())['coordinates'];out=[]
    def rat(s):
        q=F(s);return q.numerator*pow(q.denominator,-1,p)%p
    for i in range(509):
        x,y=[sum(rat(t)*b for t,b in zip(row,basis))%p for row in raw[str(i)]]
        out.append((x,y*pow(r3,-1,p)%p))
    m.require(out==m.projected(),'two source evaluations disagree');return out

def controls(cert):
    rejected=0
    for args in ((1000000272,m.ROOT5,m.ROOT33),(m.P,0,m.ROOT33),(m.P,m.ROOT5,0)):
        try:m.projection(*args)
        except ValueError:rejected+=1
        else:raise ValueError('invalid projection accepted')
    for word in ('0'*508,'4'*508,'',None):
        try:m.word_check(word,[(0,1)])
        except ValueError:rejected+=1
        else:raise ValueError('bad word accepted')
    K4=list(combinations(range(4),2));K5=list(combinations(range(5),2))
    m.require(m.peel(K4) is not None and m.peel(K5) is None,'peeling boundary')
    # Bipartite K4,4 has a4-core but a positive two-colouring; a core is not UNSAT.
    bip=[(i,j) for i in range(4) for j in range(4,8)]
    m.require(m.peel(bip) is None,'4-core control');m.word_check('0'*4+'1'*4+'0'*500,bip)
    # A four-point source with nonunit leaf separations inverts to an exact
    # unit triangle after removing the pole. This tests the physical recipe.
    Z=m.ZERO;one=m.ONE;half=m.scale(one,F(1,2));seed=[(Z,Z),(one,Z),(half,Z),(half,m.scale(one,F(1,6)))]
    a=0;Q=[]
    for b in seed[1:]:
        d=m.norm(b,seed[a]);Q.append(tuple(m.mul(row,m.inverse(d)) for row in b))
    m.require(len(set(Q))==3 and all(m.norm(Q[i],Q[j])==one for i,j in combinations(range(3),2)),'unit triangle inversion control')
    return {'bad_inputs_rejected':rejected,'peeling_controls':3,'inversion_control_order':3}

def verify(work,sanitize):
    t=time.time();work=work.resolve();m.require(not work.is_relative_to(HERE.parent),'scratch must be outside repository');work.mkdir(parents=True,exist_ok=True)
    cert=json.loads((HERE/'certificate.json').read_text());xy=alternate_projection()
    (work/'input.txt').write_text(f'{m.P} 509\n'+''.join(f'{x} {y}\n' for x,y in xy))
    cmd=['g++','-std=c++17','-O3','-Wall','-Wextra']
    if sanitize:cmd+=['-fsanitize=undefined','-fno-sanitize-recover=all']
    subprocess.run(cmd+[str(HERE/'invert.cpp'),'-o',str(work/'invert')],check=True)
    native=subprocess.run([str(work/'invert'),str(work/'input.txt'),str(work/'inverted_distances.u32')],check=True,capture_output=True,text=True)
    census,residual=run(work,certificate=cert,native_file=work/'inverted_distances.u32')
    physical=fixture.run(work/'fixture');physical.pop('seconds')
    fe=json.loads((work/'fixture/fixture_edges.json').read_text());largest=next(r for r in residual if r['pole']==0 and r['residue']==250000070)
    m.require(fe==[list(e) for e in largest['edge_list']],'physical largest graph differs from residue graph')
    out={'census':{k:v for k,v in census.items() if k!='seconds'},'fixture':physical,'controls':controls(cert),'native':native.stdout.strip(),'certificate_sha256':hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),'PASS':True,'seconds':time.time()-t}
    expected=HERE/'expected.json'
    if expected.exists():
        m.require(json.loads(json.dumps({k:v for k,v in out.items() if k!='seconds'}))==json.loads(expected.read_text()),'unexpected verified result')
    (work/'verified.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['seconds'],flush=True);return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--sanitize',action='store_true');args=ap.parse_args();verify(args.work,args.sanitize)
