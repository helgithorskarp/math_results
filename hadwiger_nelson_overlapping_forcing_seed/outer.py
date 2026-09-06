from compose import *

def build():
 t=time.monotonic();z=json.loads((w/'inequality_union_reduced.json').read_text());den=z['denominator']
 child=[tuple(F(x,den) for x in p) for p in z['points']];ce=g.edges(child)
 ks=json.loads((w/'g40_kernel.json').read_text());host=list(map(tuple,ks['points']))
 pts=list(host);idx={p:i for i,p in enumerate(pts)};edges=set(map(tuple,g.edges(host)));maps=[];choices=[]
 for k,(a,b) in enumerate(ks['pairs']):
  options=[]
  for rev in (False,True):
   for ref in (False,True):
    f=pair_frame(child[:2],[host[b],host[a]] if rev else [host[a],host[b]],4752,ref)
    image=[transform(f,p) for p in child]
    score=sum(p in idx for p in image);options.append((score,rev,ref,image))
  best=max(range(4),key=lambda i:options[i][0]);score,rev,ref,image=options[best];ids=[]
  for p in image:
   if p not in idx:idx[p]=len(pts);pts.append(p)
   ids.append(idx[p])
  edges.update(tuple(sorted((ids[i],ids[j]))) for i,j in ce);maps.append(ids);choices.append({'pair':[a,b],'reverse':rev,'reflect':ref,'overlap':score})
  if k%5==0:print('ATTACH',k+1,len(pts),round(time.monotonic()-t,2),flush=True)
 save('equality_union',pts,sorted(edges),maps)
 (w/'outer_choices.json').write_text(json.dumps(choices,separators=(',',':'))+'\n')
 print('CHILD_EDGES',len(ce),'seconds',time.monotonic()-t,flush=True)
if __name__=='__main__':build()
