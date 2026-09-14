#!/usr/bin/env python3
"""Exact local-square gate for the 1490 archived origin-rotation pencils."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse,sys,json,math
P=Path(__file__).resolve().parent;ROOT=P.parent
CFILE=ROOT/'hadwiger_nelson_nonmono159_origin_pencil/census.py'
if sha256(CFILE.read_bytes()).hexdigest()!='31d1cf2e93b7b0cd6903425acbe6d30dcc0c089226bd7e588720327121bd1b43':raise ValueError('census dependency hash')
sys.path.insert(0,str(CFILE.parent));import census as C
K=C.K
add=K.add;mul=K.multiply

def sub(a,b):return K.add(a,K.negate(b))
def scale(a,b):return tuple(x*b for x in a)
def local_square(d,sign):
 a,b=d;den=math.lcm(a.denominator,b.denominator);aa=int(a*den);bb=int(b*den);vd=(den&-den).bit_length()-1
 for bits in [16,32,64,128,256]:
  r=sign*K.root33_mod_power2(bits);z=(aa+bb*r)%(1<<bits)
  if not z:continue
  v=(z&-z).bit_length()-1
  if v+3>=bits:continue
  odd=((z>>v)*pow(den>>vd,-1,8))%8
  return (v-vd)%2==0 and odd==1,{'valuation':v-vd,'unit_mod8':odd,'bits':bits}
 raise ValueError('unresolved local square')
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 A=C.points();_,groups=C.enumerate_pencils(A,False,sha256());N=[mul(a,K.conjugate(a)) for a in A];rows=[]
 for (T,V),es in groups.items():
  i,j=es[0];s=sub(add(N[i],N[j]),K.ONE);d=scale(sub(scale(mul(N[i],N[j]),4),mul(s,s)),F(1,3));aa,ab=local_square(d[:2],1);ba,bb=local_square(d[:2],-1);rows.append({'edges':len(es),'example_pair':es[0],'D':[str(x) for x in d[:2]],'embeds_plus':aa,'embeds_minus':ba,'plus':ab,'minus':bb,'trace':[str(x) for x in T],'norm':[str(x) for x in V]})
 rows.sort(key=lambda r:(-r['edges'],r['D'],r['trace']));fields=[]
 for r in rows:
  if r['embeds_plus'] or r['embeds_minus']:continue
  d=tuple(map(F,r['D']))+(F(0),F(0));j=next((j for j,(dd,rr) in enumerate(fields) if C.real_square(mul(d,K.inverse(dd))[:2])),None)
  if j is None:fields.append((d,[r]))
  else:fields[j][1].append(r)
 out={'classes':len(rows),'embeddable_classes':sum(r['embeds_plus'] or r['embeds_minus'] for r in rows),'remaining_classes':sum(not(r['embeds_plus'] or r['embeds_minus']) for r in rows),'remaining_fields':[{'D':[str(x) for x in d[:2]],'classes':len(rr),'max_edges':max(r['edges'] for r in rr),'example':rr[0]} for d,rr in fields]}
 if (out['classes'],out['embeddable_classes'],out['remaining_classes'],len(fields))!=(1490,1260,230,7):raise ValueError('census counts')
 # Gate controls include both embeddings and positive/negative square answers.
 for d,expected in [((F(6),F(0)),False),((F(17),F(0)),True),((F(13),F(4)),True),((F(3),F(0)),False)]:
  if any(local_square(d,sign)[0] != expected for sign in [-1,1]):raise ValueError('local-square control')
 (args.work/'field-rows.json').write_text(json.dumps(rows,separators=(',',':'))+'\n');(args.work/'field-summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
