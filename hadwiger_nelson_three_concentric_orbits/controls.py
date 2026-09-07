import argparse, itertools, json, math, random, subprocess, sys
from fractions import Fraction
from pathlib import Path
from verify import parse,check_word,require

def run(harness,table,commands):
 r=subprocess.run([str(harness),str(table)],input='\n'.join(commands)+'\n',text=True,capture_output=True,check=True)
 rows=r.stdout.splitlines();require(len(rows)==len(commands),'harness line count');return rows

def controls(harness,bad_harness,table):
 S=1<<48;rng=random.Random(509508);commands=[];expected=[]
 for _ in range(1500):
  a=sorted(rng.randint(-20*S,20*S) for _ in range(2));b=sorted(rng.randint(-20*S,20*S) for _ in range(2))
  for op in ('A','S','M'):
   aa=[Fraction(x,S) for x in a];bb=[Fraction(x,S) for x in b]
   vals=[x+y if op=='A' else x-y if op=='S' else x*y for x in aa for y in bb]
   expected.append([math.floor(min(vals)*S),math.ceil(max(vals)*S)])
   commands.append(' '.join(map(str,[op,*a,*b])))
  b=sorted(rng.randint(S//8,20*S) for _ in range(2))
  vals=[Fraction(x,y)*S for x in a for y in b]
  expected.append([math.floor(min(vals)),math.ceil(max(vals))]);commands.append(' '.join(map(str,['D',*a,*b])))
  a=sorted(rng.randint(0,20*S) for _ in range(2));lo=math.isqrt(a[0]*S);hi=math.isqrt(a[1]*S)
  expected.append([lo,hi+(hi*hi<a[1]*S)]);commands.append(' '.join(map(str,['R',*a])))
 for a in ([0,0],[0,1],[1,1],[S-1,S+1],[S,S],[4*S,4*S]):
  lo=math.isqrt(a[0]*S);hi=math.isqrt(a[1]*S);expected.append([lo,hi+(hi*hi<a[1]*S)]);commands.append(' '.join(map(str,['R',*a])))
 actual=run(harness,table,commands)
 require(all(list(map(int,a.split()))==e for a,e in zip(actual,expected)),'arithmetic differs from Fraction/isqrt')
 bad=['D 1 1 0 0','D 1 1 -1 1','D 1 1 -2 -1','R -2 -1']
 require(run(harness,table,bad)==['REJECT']*len(bad),'invalid arithmetic not rejected')
 rows=Path(table).read_text().splitlines();grid_commands=[];grid_expected=[]
 lookup={}
 for row in rows[1:]:
  n,m,sl,sh,cl,ch=map(int,row.split())
  lookup[n,m]=(sl,sh,cl,ch)
  grid_commands.append(f'G {n} 2 {cl} {ch} {sl} {sh}');grid_expected.append([m])
  if m%2==0:grid_commands.append(f'G {n} 1 {cl} {ch} {sl} {sh}');grid_expected.append([m//2])
 for n in range(3,255):
  for factor in (1,2):
   grid_commands.append(f'G {n} {factor} {-S} {S} {-S} {S}');grid_expected.append(list(range(n*factor)))
 for binary in (harness,bad_harness):
  actual=run(binary,table,grid_commands)
  for line,e in zip(actual,grid_expected):
   a=list(map(int,line.split()));require(a==[len(e),*e],'root grid gate omitted or invented a test root')
 # Independent rational Taylor evaluation at one interior angle for every n.
 # Its pi bracket is reconstructed here, not imported from the table producer.
 def at(d):
  v=sum((Fraction((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(50)),Fraction())
  return v,v+Fraction(1,101*d**101)
 a,b=at(5);c,d=at(239);lo=16*a-4*d;hi=16*b-4*c
 den=10**30;plo=Fraction(math.floor(lo*den),den);phi=Fraction(math.ceil(hi*den),den)
 require(math.factorial(40)>2**150,'Taylor remainder bound')
 trig_checks=0
 for n in range(3,255):
  m=rng.randint(1,(n-1)//2);x=plo*m/n;gap=(phi-plo)*m/n;xx=x*x
  st=x;ct=Fraction(1);ss=st;cc=ct
  for j in range(1,20):
   st=-st*xx/((2*j)*(2*j+1));ct=-ct*xx/((2*j-1)*(2*j));ss+=st;cc+=ct
  err=Fraction(1,2**110)+gap;sl,sh,cl,ch=lookup[n,m]
  require(Fraction(sl,S)<=ss-err<=ss+err<=Fraction(sh,S),'sine table misses rational enclosure')
  require(Fraction(cl,S)<=cc-err<=cc+err<=Fraction(ch,S),'cosine table misses rational enclosure')
  trig_checks+=1
 # These failures address format, adjacency, and word validation separately.
 fixture='7 3 1 2 3 0 0 0 1 0 1 0 1 0'
 invalid=['','1 3 0 0 0 0 0 0 0 0 0','7 4 0 0 0 0 0 0 0 0',fixture+' 9',fixture.replace('1 2 3','1 2 9'),fixture.replace('0 0 0','0 2 0',1),fixture[:-1]+'7']
 rejected=0
 for x in invalid:
  try:parse(x)
  except (ValueError,IndexError):rejected+=1
 require(rejected==len(invalid),'malformed graph accepted')
 for word in ('0'*22,'0'*21,'4'*22):
  try:check_word(fixture,word)
  except ValueError:rejected+=1
 require(rejected==len(invalid)+3,'malformed/invalid word accepted')
 # Exact exhaustive 3-colouring control for Haugland's 21-vertex ring graph.
 N=21;nb=[set() for _ in range(N)]
 for u,v in itertools.combinations(range(N),2):
  i,x=divmod(u,7);j,y=divmod(v,7)
  if (i==j and (y-x)%7 in (i+1,7-(i+1))) or (i!=j and x==y):nb[u].add(v);nb[v].add(u)
 colour=[-1]*N;colour[0]=0;nodes=0
 def search():
  nonlocal nodes
  nodes+=1;vs=[v for v in range(N) if colour[v]<0]
  if not vs:return True
  v=max(vs,key=lambda v:(len({colour[u] for u in nb[v] if colour[u]>=0}),len(nb[v]),-v))
  for c in sorted(set(range(3))-{colour[u] for u in nb[v]}):
   colour[v]=c
   if search():return True
  colour[v]=-1;return False
 three=search()
 return {'exact_arithmetic_cases':len(commands),'arithmetic_rejections':len(bad),
  'independent_rational_trig_checks':trig_checks,
  'grid_cases_per_mode':len(grid_commands),'grid_modes':['ordinary_proposal','deliberately_zero_proposal'],
  'malformed_graph_or_word_rejections':rejected,'heptagonal_fixture_three_colourable':three,'heptagonal_fixture_search_nodes':nodes}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('harness',type=Path);p.add_argument('bad_harness',type=Path);p.add_argument('table',type=Path);a=p.parse_args()
 print(json.dumps(controls(a.harness.resolve(),a.bad_harness.resolve(),a.table.resolve()),indent=2))
