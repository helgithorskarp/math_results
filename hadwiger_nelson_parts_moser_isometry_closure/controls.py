"""Small exhaustive controls and certificate corruption checks."""
import argparse,base64,itertools,json,tempfile
from pathlib import Path
import geometry as G
import verify as V

def recursive(edges,masks):
 n=len(masks)
 def walk(i,col):
  if i==n:return True
  for c in range(4):
   if masks[i]>>c&1 and all(col[a]!=c for a,b in edges if b==i):
    if walk(i+1,col+[c]):return True
  return False
 return walk(0,[])
def controls(frontier):
 assignments=0;lists=0
 for n in range(1,5):
  pairs=list(itertools.combinations(range(n),2))
  for bits in range(1<<len(pairs)):
   edges=tuple(e for i,e in enumerate(pairs)if bits>>i&1);tab=V.tables(n,edges)
   for word in itertools.product(range(4),repeat=n):
    V.require(V.possible(tab,[1<<c for c in word])==all(word[a]!=word[b]for a,b in edges),'one-hot word');assignments+=1
   if n<=3:
    for masks in itertools.product(range(16),repeat=n):
     V.require(V.possible(tab,masks)==recursive(edges,masks),'all-list control');lists+=1
 K5=tuple(itertools.combinations(range(5),2));V.require(not V.possible(V.tables(5,K5),[15]*5),'K5 obstruction')
 M=G.spindle();edges=[(i,j)for i,j in itertools.combinations(range(7),2)if G.norm(G.sub(M[i],M[j]))==G.O]
 counts={k:sum(all(w[i]!=w[j]for i,j in edges)for w in itertools.product(range(k),repeat=7))for k in [3,4]}
 V.require(len(edges)==11 and counts[3]==0 and counts[4]>0,'Moser control')
 data=json.loads(frontier.read_text());cert=json.loads((V.HERE/'certificate.json').read_text());bad=[]
 x=json.loads(json.dumps(cert));x['rows'].pop();bad.append(x)
 x=json.loads(json.dumps(cert));x['rows'][0]['colours']=base64.b64encode(bytes(127)).decode();bad.append(x)
 x=json.loads(json.dumps(cert));x['rows'][0]['colours']=base64.b64encode(bytes(126)).decode();bad.append(x)
 x=json.loads(json.dumps(cert));x['rows'][0]['fresh'][0]=-1;bad.append(x)
 x=json.loads(json.dumps(cert));x['rows'].append(x['rows'][0]);bad.append(x)
 rejected=0
 with tempfile.TemporaryDirectory()as tmp:
  p=Path(tmp)/'bad.json'
  for x in bad:
   p.write_text(json.dumps(x))
   try:V.check_targets(data['geometry'],data['frontier'],p)
   except (ValueError,IndexError):rejected+=1
   else:raise ValueError('corrupt certificate accepted')
 return {'single_colour_assignments':assignments,'arbitrary_colour_lists':lists,'moser_unit_edges':len(edges),'moser_colour_counts':counts,'corrupt_certificates_rejected':rejected}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('frontier',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=controls(a.frontier);s=json.dumps(r,indent=2,sort_keys=True)+'\n';print(s)
 if a.output:a.output.write_text(s)
