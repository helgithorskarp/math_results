from prepare import *
from census import emb,p
import subprocess

def qnorm(a,b,s):return ea(en(a),em(s,en(b))),ea(em(a,ec(b)),em(b,ec(a)))
def reference(V,s):
 for j in range(490,len(V)):
  for i in range(j):
   a,ca,b,cb=[(x-y)%p for x,y in zip(V[i],V[j])]
   if (a*cb+ca*b)%p==0 and (a*ca+s*b*cb)%p==1:yield [i,j]

if __name__=='__main__':
 st=time.time();x=json.loads((W/'inventory.json').read_text());classes=list(map(parse,x['classes']));points=[(cl,parse(a),parse(b))for cl,a,b in x['points']];P,word=seed();edges=[];counts=Counter();neighbours=[[]for _ in points];info=[]
 for cl,s in enumerate(classes):
  ids=[i for i,z in enumerate(points)if z[0]==cl];Q=[(a,EZ)for a in P]+[(points[i][1],points[i][2])for i in ids];vals=[[emb(a),emb(a,True),emb(b),emb(b,True)]for a,b in Q];sv=emb(s);inp=W/f'class{cl}.txt';out=W/f'class{cl}.edges';stat=W/f'class{cl}.stats'
  with inp.open('w')as f:
   f.write(f'{len(Q)} {sv}\n')
   for v in vals:f.write(' '.join(map(str,v))+'\n')
  with out.open('w')as f,stat.open('w')as g:subprocess.run([str(W/'within'),str(inp)],stdout=f,stderr=g,check=True)
  cand=[list(map(int,line.split()))for line in out.open()];require(cand==list(reference(vals,sv)),'native/reference candidates');kept=0
  for i,j in cand:
   a=es(Q[i][0],Q[j][0]);b=es(Q[i][1],Q[j][1])
   if qnorm(a,b,s)!=(EO,EZ):counts['false_modular']+=1;continue
   kept+=1
   if i<490:neighbours[ids[j-490]].append(i);counts['old_new']+=1
   else:edges.append((ids[i-490],ids[j-490]));counts['same_class']+=1
  info.append({'class':cl,'points':len(ids),'pair_instances':len(ids)*490+len(ids)*(len(ids)-1)//2,'candidates':len(cand),'edges':kept});print('CLASS',cl,info[-1],'sec',time.time()-st,flush=True)
 centers=defaultdict(list);radii=[]
 for i,(cl,a,b)in enumerate(points):centers[a].append(i);radii.append(em(classes[cl],en(b)))
 for center,ids in centers.items():
  byrad=defaultdict(list)
  for i in ids:byrad[radii[i]].append(i)
  for i in ids:
   for j in byrad.get(es(EO,radii[i]),[]):
    if j<=i or points[i][0]==points[j][0]:continue
    counts['different_class_radial_candidates']+=1
    bi,bj=points[i][2],points[j][2]
    if ea(em(bi,ec(bj)),em(bj,ec(bi)))!=EZ:continue
    edges.append((i,j));counts['different_class']+=1
 edges=sorted(edges);require(len(set(edges))==len(edges),'duplicate edges')
 out={'edges':edges,'neighbours':neighbours,'counts':dict(counts),'classes':info,'points_sha256':digest(x['points']),'edges_sha256':digest(edges),'neighbours_sha256':digest(neighbours),'seconds':time.time()-st};(W/'geometry.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('DONE',dict(counts),'sec',time.time()-st,flush=True)
