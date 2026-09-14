"""Optional native discovery replay; bulky output remains under HN_PAIR_RUN_DIR."""
from prepare import *
from colour import greedy,checked
import subprocess
inv=json.loads((W/'inventory.json').read_text());geo=json.loads((W/'geometry.json').read_text());P,old=seed();domains=[]
for ns in geo['neighbours']:
 mask=0
 for r in ns:mask|=1<<int(old[r])
 domains.append(15^mask)
with(W/'pair_input.txt').open('w')as f:
 f.write(f"{len(domains)} {len(geo['edges'])} {len(inv['copies'])}\n");f.write(' '.join(map(str,domains))+'\n')
 for a,b in geo['edges']:f.write(f'{a} {b}\n')
 for v in inv['copies']:f.write(' '.join(map(str,v['points']))+'\n')
D=Path(__file__).resolve().parent
subprocess.run(['c++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(D/'discover_pairs.cpp'),'-o',str(W/'discover_pairs')],check=True)
subprocess.run([str(W/'discover_pairs'),str(W/'pair_input.txt'),str(W/'discovery')],check=True)
exception=[];h=hashlib.sha256()
for line in (W/'discovery_templates.txt').open():
 r=line.split();n=int(r[1]);require(int(r[2])==1,'non-positive discovery verdict');word=r[3];dom=list(map(int,r[4:4+n]));adj=list(map(int,r[4+n:]));checked(word,dom,adj)
 if greedy(dom,adj)is None:exception.append({'domains':dom,'adjacency':adj,'word':word})
exception.sort(key=lambda z:(z['domains'],z['adjacency']));data=json.dumps(exception,separators=(',',':'))+'\n';require(data==(D/'exceptions.json').read_text(),'exception reproduction');(W/'exceptions.json').write_text(data)
with (W/'verified_pair_choices.txt').open()as verification:
 for line in (W/'discovery_pairs.txt').open():
  a,b,_=line.split();row=f'{a} {b}\n';require(next(verification,None)==row,'native/Python entry mismatch');h.update(row.encode())
 require(verification.read()=='','missing native pairs')
expected=json.loads((D/'EXPECTED.json').read_text());require(h.hexdigest()==expected['selection_stream_sha256'],'native/Python pair enumeration mismatch');print('NATIVE DISCOVERY AND EXCEPTIONS REPRODUCED')
