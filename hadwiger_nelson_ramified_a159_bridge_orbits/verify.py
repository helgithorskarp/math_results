#!/usr/bin/env python3
"""Regenerate complete exact bridge-orbit graphs; verify positive colourings."""
from pathlib import Path
from hashlib import sha256
from itertools import permutations
import argparse,json,subprocess,sys,time
P=Path(__file__).resolve().parent;ROOT=P.parent
PIN={
'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv':'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',
'hadwiger_nelson_nonmono_field_obstruction/coloring.py':'a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
for file,h in PIN.items():need(sha256((ROOT/file).read_bytes()).hexdigest()==h,'dependency '+file)
sys.path.insert(0,str(ROOT/'hadwiger_nelson_nonmono_field_obstruction'));import coloring as K

def mul(x,y):
 a,b,c,d=x;A,B,C,D=y
 return (a*A+33*b*B-3*c*C-11*d*D,a*B+b*A-c*D-d*C,a*C+c*A+11*(b*D+d*B),a*D+d*A+3*(b*C+c*B))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def conj(x):return x[:2]+(-x[2],-x[3])
def unit(x,s):
 a,b,c,d,e,f,g,h=x
 return (a*a+33*b*b+3*c*c+11*d*d+6*(e*e+33*f*f+3*g*g+11*h*h)==s*s and
  a*b+c*d+6*(e*f+g*h)==0 and a*e+33*b*f+3*c*g+11*d*h==0 and a*f+b*e+c*h+d*g==0)
def source():
 A=[]
 for l in (ROOT/next(iter(PIN))).read_text().splitlines():
  if not l or l.startswith('#'):continue
  p=tuple(map(int,l.split()));need(len(p)==16 and all(p[i]==0 for i in range(16) if i not in (0,5,9,12)),'basis');A.append(tuple(p[i] for i in (0,5,9,12)))
 need(len(set(A))==len(A)==159 and A[0]==(0,0,0,0),'A');return A

def build():
 A=source();internal=[(j,i) for i in range(159) for j in range(i) if unit(sub(A[i],A[j])+(0,0,0,0),12)];need(len(internal)==646,'source edges')
 u=(0,0,1,0,1,0,0,0);old=[tuple(432*x for x in p)+(0,0,0,0) for p in A]+[tuple(144*x for x in mul(u[:4],p))+tuple(144*x for x in mul(u[4:],p)) for p in A[1:]]
 need(len(set(old))==317,'base collisions');base_edges=[(j,i) for i in range(317) for j in range(i) if unit(sub(old[i],old[j]),5184)];bridges=[(a,b-158) for a,b in base_edges if a>0 and a<159 and b>=159];bridges.sort();need(len(base_edges)==1312 and len(bridges)==20,'base edges')
 R=set()
 for c0,d0 in internal:
  for c,d in [(c0,d0),(d0,c0)]:
   e=conj(sub(A[d],A[c]))
   for z in A:
    r=mul(e,sub(z,A[c]));R.add(r);R.add(conj(r))
 R=sorted(R);need(len(R)==8428,'orbit size');need(max(abs(x) for r in R for x in r)<=432,'native arithmetic bound')
 images=[]
 for a,b in bridges:
  e=sub(old[158+b],old[a]);ps=[]
  for r in R:
   delta=mul(e[:4],r)+mul(e[4:],r);need(all(x%144==0 for x in delta),'integral scale');ps.append(tuple(old[a][i]+delta[i]//144 for i in range(8)))
  need(len(set(ps))==8428,'image collisions');need(max(abs(x) for p in ps for x in p)<=10368,'arithmetic bound');images.append(ps)
 return A,old,base_edges,bridges,R,images

def run_interfaces(work,name,left,rights):
 f=work/(name+'.in');out=work/(name+'.txt')
 with f.open('w') as h:
  h.write(f'{len(left)} {len(rights[0])} {len(rights)} 5184\n')
  for ps in [left]+rights:
   for p in ps:h.write(' '.join(map(str,p))+'\n')
 r=subprocess.run([str(work/'interfaces'),str(f),str(out)],check=True,capture_output=True,text=True)
 rows=[{'edges':[],'collisions':[]} for _ in rights]
 for l in out.read_text().splitlines():
  t,a,b,kind=l.split();t,a,b=int(t),int(a),int(b);need(0<=t<len(rows) and 0<=a<len(left) and 0<=b<len(rights[t]),'interface labels')
  delta=sub(left[a],rights[t][b]);need((kind=='E' and unit(delta,5184)) or (kind=='C' and not any(delta)),'independent positive interface')
  rows[t]['edges' if kind=='E' else 'collisions'].append((a,b))
 return rows,r.stdout.strip()
def check_word(word,n,edges):
 need(len(word)==n and set(word)<=set('0123'),'word format');need(all(word[a]!=word[b] for a,b in edges),'monochromatic unit edge')
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--coupled',action='store_true');p.add_argument('--sanitize',action='store_true');args=p.parse_args();W=args.work.resolve();W.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 flags=['-O2','-std=c++17']+(['-fsanitize=undefined','-fno-sanitize-recover=all'] if args.sanitize else [])
 for name in ['interfaces','native_edges']:subprocess.run(['g++',*flags,str(P/(name+'.cpp')),'-o',str(W/name)],check=True)
 A,old,be,bridges,R,images=build();cert=json.loads((P/'certificate.json').read_text());base=cert['base_word'];check_word(base,317,be)
 with (W/'R.txt').open('w') as f:
  f.write(f'{len(R)}\n');f.writelines(' '.join(map(str,r))+'\n' for r in R)
 r=subprocess.run([str(W/'native_edges'),str(W/'R.txt'),str(W/'R-edges.txt')],capture_output=True,text=True,check=True);need(r.stdout.strip()=='8428 75413','native edges')
 re=[tuple(map(int,l.split())) for l in (W/'R-edges.txt').read_text().splitlines()];native=''.join(str(K.color_numerators(r,144)) for r in R);check_word(native,len(R),re)
 need(all(unit(sub(R[a],R[b])+(0,0,0,0),144) for a,b in re),'independent positive native edges')
 rows,counts=run_interfaces(W,'orbits',old,images);need(counts=='53433520 2872 40','interface counts');results=[];maps=[];graphs=[]
 for j,(row,ps) in enumerate(zip(rows,images)):
  need(len(row['collisions'])==2,'overlap count');coords=list(old);ix={x:i for i,x in enumerate(coords)};mp=[]
  for x in ps:
   if x not in ix:ix[x]=len(coords);coords.append(x)
   mp.append(ix[x])
  need(len(coords)==8743,'physical count');ee=set(be);ee.update(tuple(sorted((mp[a],mp[b]))) for a,b in re);ee.update(tuple(sorted((a,mp[b]))) for a,b in row['edges']);palette=cert['palettes'][j];need(sorted(palette)==[0,1,2,3],'palette');word=list(base)+['?']*(len(coords)-317)
  for a,b in enumerate(mp):
   v=str(palette[int(native[a])]);need(b>=317 or word[b]==v,'glue collision');word[b]=v
  check_word(''.join(word),len(coords),ee);results.append({'bridge':bridges[j],'vertices':len(coords),'edges':len(ee),'interface_edges':len(row['edges'])});maps.append(mp);graphs.append(ee)
 out={'status':'VERIFIED','A_vertices':159,'A_edges':646,'base_vertices':317,'base_edges':1312,'normalized_vertices':8428,'normalized_edges':75413,'raw_474_attachments':51680,'orbits':results,'cross_checks':53433520,'sat_calls_in_verifier':0}
 if args.coupled:
  js=[0,10];coords=list(old);ix={p:i for i,p in enumerate(coords)};mm=[];ee=set(be)
  for j in js:
   mp=[]
   for x in images[j]:
    if x not in ix:ix[x]=len(coords);coords.append(x)
    mp.append(ix[x])
   mm.append(mp);ee.update(tuple(sorted((mp[a],mp[b]))) for a,b in re);ee.update(tuple(sorted((a,mp[b]))) for a,b in rows[j]['edges'])
  rr,cc=run_interfaces(W,'coupled',images[0],[images[10]]);need(cc=='71031184 88 1','coupled counts');ee.update(tuple(sorted((mm[0][a],mm[1][b]))) for a,b in rr[0]['edges']);word=(P/'coupled_word.txt').read_text().strip();check_word(word,len(coords),ee);need(len(coords)==17168 and len(ee)==152201,'coupled physical size');out['coupled']={'vertices':len(coords),'edges':len(ee),'decision':'FOUR'}
 out['seconds']=time.monotonic()-start;(W/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
