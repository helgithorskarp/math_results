#!/usr/bin/env python3
"""Cross-check the metric against generic Cartesian multiquadratic arithmetic."""
from pathlib import Path
import argparse,json,random,subprocess
import verify as V

def multiply(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   m=1
   for k,p in enumerate([2,3,11]):
    if (i&j)&(1<<k):m*=p
   out[i^j]+=x*y*m
 return out

def cartesian_unit(p,s):
 a,b,c,d,e,f,g,h=p;x=[a,0,0,e,0,3*f,b,0];y=[0,3*g,c,0,d,0,0,h]
 xx,yy=multiply(x,x),multiply(y,y);return [q+r for q,r in zip(xx,yy)]==[s*s,0,0,0,0,0,0,0]

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();W=args.work.resolve();W.mkdir(parents=True,exist_ok=True)
 subprocess.run(['g++','-O1','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',str(V.P/'interfaces.cpp'),'-o',str(W/'interfaces')],check=True)
 A,old,be,bridges,R,images=V.build();rng=random.Random(159646);ps=[(0,)*8,(5184,0,0,0,0,0,0,0),(0,0,1728,0,1728,0,0,0)]+rng.sample(old,60)+rng.sample(images[0],20)
 ps=list(dict.fromkeys(ps));ps += [tuple(rng.randrange(-10000,10001) for _ in range(8)) for j in range(10)];expect=[];zero=[]
 for i,a in enumerate(ps):
  for j,b in enumerate(ps):
   d=V.sub(a,b);u=cartesian_unit(d,5184);V.need(u==V.unit(d,5184),'metric formula mismatch')
   if u:expect.append((i,j))
   if not any(d):zero.append((i,j))
 rows,counts=V.run_interfaces(W,'controls',ps,[ps]);V.need(rows[0]['edges']==expect and rows[0]['collisions']==zero,'complete entry mismatch');V.need(len(expect)>2,'nonvacuous unit controls')
 rejected=0
 for word in ['', '0'*317, '4'*317, '0'*316+'?']:
  try:V.check_word(word,317,be)
  except ValueError:rejected+=1
 V.need(rejected==4,'bad word accepted');out={'status':'VERIFIED','cartesian_pairs':len(ps)**2,'unit_pairs':len(expect),'collisions':len(zero),'malformed_words_rejected':rejected,'sanitized':True};(W/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
