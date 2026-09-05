from pathlib import Path
import json,importlib.util,sys
sys.dont_write_bytecode=True
import argparse
from review_geometry import R,host,colors as load_colors
p=argparse.ArgumentParser(description='Independent minus-host modular input.')
p.add_argument('--work',type=Path,required=True);a=p.parse_args();w=a.work
H=host()
groups=json.loads((w/'groups.json').read_text());colors=load_colors()
p,z,r=5051,2194,528;assert z*z%p==33 and r*r%p==(-408+72*z)%p
mp=lambda h:((h[0]+h[1]*z+h[4]*r+h[5]*z*r)%p,(h[2]+h[3]*z+h[6]*r+h[7]*z*r)%p)
seen=set();fibre_seen=set()
with (w/'audit_screen_input.txt').open('w') as f:
 f.write(f'{p} {(2*R.D)**2%p} {len(groups)}\n')
 for pal,rows in groups:
  f.write(str(len(rows))+'\n')
  for _,pairs in rows:
   a,b=pairs[0];m=R.add(H[a],H[b]);key=(tuple(pal),m);assert key not in fibre_seen;fibre_seen.add(key)
   x,y=mp(m);f.write(f'{x} {y} {len(pairs)}\n')
   for a,b in pairs:
    assert a<b and (a,b) not in seen and sorted([colors[a],colors[b]])==pal;seen.add((a,b));assert R.add(H[a],H[b])==m
    x,y=mp(R.scale(R.sub(H[b],H[a]),2));f.write(f'{a} {b} {x} {y}\n')
assert seen=={(i,j) for i in range(506) for j in range(i+1,506) if colors[i]!=colors[j]}
print(json.dumps({'host_pairs':len(seen),'midpoint_fibres':len(fibre_seen),'root':-1,'prime':p,'z':z,'r':r,'all_pair_entries_match':True},indent=2))
