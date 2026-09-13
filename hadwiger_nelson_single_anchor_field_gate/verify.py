"""Positive certificate audit and exact physical controls, no SAT solver."""
from common import *
import argparse,copy,time
from build_certificate import profiles,templates

def colour_map(word):
 seen=[];canon=[]
 for c in word:
  if c not in seen:seen.append(c)
  canon.append(seen.index(c))
 return tuple(canon),seen+[c for c in range(4)if c not in seen]

def check_template(t):
 n=t['new_vertices'];edges=t['new_edges'];masks=t['old_neighbour_masks'];pr=list(profiles(len(masks)));words=t['words'];require(len(words)==len(pr),'profile coverage');lookup=dict(zip(pr,words))
 require(n in(6,9)and all(0<m<(1<<n)for m in masks),'template shape')
 for e in edges:require(len(e)==2 and 0<=e[0]<e[1]<n,'edge shape')
 for word in words:require(len(word)==n and all(c in '0123'for c in word),'word shape')
 for old in product(range(4),repeat=len(masks)):
  canonical,perm=colour_map(old);new=[perm[int(c)]for c in lookup[canonical]]
  require(all(new[i]!=new[j]for i,j in edges),'new edge colour')
  require(all(new[j]!=c for mask,c in zip(masks,old)for j in range(n)if mask>>j&1),'old contact colour')
 return 4**len(masks)

def seed_edges(P):
 # Independent real-coordinate metric in Q(sqrt33,sqrt5).
 rows=[]
 for z in P:
  a,b,c,d=z[0];A,B,C,D=z[1];rows.append((a,b,A,B,c,d/3,C,D/3))
 den=lcm(*(x.denominator for row in rows for x in row));ii=[tuple(int(x*den)for x in row)for row in rows]
 def square(r):
  a,b,c,d=r;return(a*a+33*b*b+5*c*c+165*d*d,2*a*b+10*c*d,2*a*c+66*b*d,2*a*d+2*b*c)
 es0=[]
 for i,j in combinations(range(len(ii)),2):
  d=tuple(a-b for a,b in zip(ii[i],ii[j]));xx=square(d[:4]);yy=square(d[4:]);z=tuple(a+3*b for a,b in zip(xx,yy))
  if z==(den*den,0,0,0):es0.append((i,j))
 return es0

def fixture(name,g,P,word,base,cert):
 v=g['outside_groups'][0];C=patterns(name)[v['pattern']];pp=v['p'];rr,jj=v['events'][0];a=es(P[pp],P[rr]);b=C[jj];ci=ei(sc(ec(a),b));T,J=parse(v['T']),parse(v['J']);s2=sc(parse(v['disc']),scale(ONE,F(1,3)));require(sgn(s2)>0 and sq(s2)is None,'outside field')
 u0=sc(T,scale(ONE,F(1,2)));u1=sc(ci,scale(ALPHA,F(1,2)))
 def qmul(x,y):return ea(em(x[0],y[0]),em(s2,em(x[1],y[1]))),ea(em(x[0],y[1]),em(x[1],y[0]))
 def qnorm(x):return qmul(x,(ec(x[0]),ec(x[1])))
 require(qnorm((u0,u1))==(EO,EZ),'unit multiplier')
 u2=qmul((u0,u1),(u0,u1));require(ea(es(u2[0],em(T,u0)),J)==EZ and es(u2[1],em(T,u1))==EZ,'root equation')
 extra=[(ea(P[pp],sc(u0,z)),sc(u1,z))for z in C[1:]];require(len(set(extra))==len(extra)and all(z[1]!=EZ for z in extra),'exact distinctness')
 contacts=[];inside=[]
 for j,q in enumerate(extra):
  for r,z in enumerate(P):
   if qnorm((es(q[0],z),q[1]))==(EO,EZ):contacts.append((r,j+1))
  for i,t in enumerate(extra[:j]):
   if qnorm((es(q[0],t[0]),es(q[1],t[1])))==(EO,EZ):inside.append((i+1,j+1))
 contacts=sorted(contacts);inside=sorted(inside)
 require([list(e)for e in contacts]==v['cross'] and [list(e)for e in inside]==v['inside'],'complete physical contact audit')
 old=sorted({r for r,j in contacts});masks=[sum(1<<(j-1)for r0,j in contacts if r0==r)for r in old];order=sorted(range(len(old)),key=lambda i:masks[i]);ordered_masks=[masks[i]for i in order];ordered_word=[int(word[old[i]])for i in order];ie=[[i-1,j-1]for i,j in inside]
 t=next(t for t in cert if t['new_edges']==ie and t['old_neighbour_masks']==ordered_masks);canonical,perm=colour_map(ordered_word);w=t['words'][list(profiles(len(old))).index(canonical)];new=''.join(str(perm[int(c)])for c in w);physical=word+new;edges=base+[(r,489+j)for r,j in contacts]+[(489+i,489+j)for i,j in inside];require(all(physical[a]!=physical[b]for a,b in edges),'full physical word')
 return {'vertices':len(P)+len(extra),'edges':len(edges),'all_old_new_pairs_checked':len(P)*len(extra),'new_pairs_checked':len(extra)*(len(extra)-1)//2,'outside_K':True,'proper_four_colouring':True,'point_stream_sha256':digest([[ser(a),ser(b)]for a,b in [(z,EZ)for z in P]+extra]),'colouring':physical}

def main(work):
 st=time.time();cert=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text());P,word=seed();base=seed_edges(P);require(len(base)==2435 and all(word[a]!=word[b]for a,b in base),'seed metric/word');out={'status':'PASS','seed_vertices':490,'seed_edges':2435,'seed_pairs':len(P)*(len(P)-1)//2,'motifs':{}}
 for name in ['M','G']:
  g=json.loads((work/(name+'_census.json')).read_text());require(g['name']==name,'motif identity');require(digest(g['outside_groups'])==g['outside_sha256'],'census stream hash');require(digest([ser(z)for z in P])==g['seed_sha256'],'seed stream hash');tt=templates(g);cc=cert[name]
  require(len(tt)==len(cc),'template coverage')
  for (edges,masks),t in zip(tt,cc):require([list(e)for e in edges]==t['new_edges'] and list(masks)==t['old_neighbour_masks'],'template matching')
  n=sum(check_template(t)for t in cc);fx=fixture(name,g,P,word,base,cc);out['motifs'][name]={'counts':g['counts'],'outside_sha256':g['outside_sha256'],'templates':len(cc),'canonical_profiles':sum(len(t['words'])for t in cc),'labelled_profiles':n,'boundary_counts':dict(Counter(v['old_vertices']for v in g['outside_groups'])),'fixture':fx}
 controls=0
 for name in ['M','G']:
  t=cert[name][0]
  for mode in ['short','missing','constant']:
   q=copy.deepcopy(t)
   if mode=='short':q['words'][0]=q['words'][0][:-1]
   elif mode=='missing':q['words'].pop()
   else:q['words'][0]='0'*q['new_vertices']
   try:check_template(q)
   except ValueError:controls+=1
   else:raise ValueError('corrupt certificate accepted')
 # Exact square extraction, including extension components, is checked on controls.
 for j in range(1,21):
  z=((F(j),F(1-j),F(0),F(0)),(F(j-3),F(j%3),F(0),F(0)));root=sq(em(z,z));require(root is not None and em(root,root)==em(z,z),'square control')
 out['rejected_controls']=controls;out['square_controls']=20;out['record_improvement']=False;expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text());require(json.loads(json.dumps(out))==expected,'expected census/geometry result');out['seconds']=time.time()-st;(work/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='motifs'},sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--work',required=True,type=Path);args=ap.parse_args();main(args.work)
