"""Small positive-hint LRAT checker. Only referenced original clauses are stored.

The input is still scanned completely. RAT hints and malformed/dead references
are rejected. This checks actual unit propagation, not a solver status receipt.
"""
from pathlib import Path
import argparse,hashlib,json

def require(condition,message):
 if not condition:raise ValueError(message)

def steps(path):
 for line in Path(path).read_text().splitlines():
  words=line.split();require(len(words)>=3,'short proof line')
  label=int(words[0])
  if words[1]=='d':
   ids=list(map(int,words[2:]));require(ids[-1]==0 and all(i>0 for i in ids[:-1]),'deletion syntax')
   yield label,None,ids[:-1]
  else:
   nums=list(map(int,words[1:]));j=nums.index(0);clause=tuple(nums[:j]);hints=nums[j+1:]
   require(hints and hints[-1]==0 and all(i>0 for i in hints[:-1]),'only positive RUP hints accepted')
   require(all(x!=0 for x in clause),'clause syntax');yield label,clause,hints[:-1]

def check(cnf,proof):
 raw=Path(cnf).read_bytes();lines=raw.decode('ascii').splitlines();header=lines[0].split()
 require(len(header)==4 and header[:2]==['p','cnf'],'DIMACS header')
 variables,initial=map(int,header[2:]);require(len(lines)==initial+1,'DIMACS line count')
 instructions=list(steps(proof));wanted={i for _,c,h in instructions if c is not None for i in h if i<=initial}
 database={}
 for i,line in enumerate(lines[1:],1):
  nums=tuple(map(int,line.split()));require(nums and nums[-1]==0 and all(0<abs(x)<=variables for x in nums[:-1]),'DIMACS literal range')
  if i in wanted:database[i]=nums[:-1]
 last=initial;count=0;empty=False;deleted=set()
 for label,clause,hints in instructions:
  if clause is None:
   require(label>=last,'deletion label order')
   for i in hints:
    require(i<=initial or i in database or i in deleted,'deletion of unknown clause')
    database.pop(i,None);deleted.add(i)
   continue
  require(label>last,'addition IDs must increase');last=label
  require(all(0<abs(x)<=variables for x in clause),'proof variable range')
  values={};conflict=False
  for x in clause:
   v=abs(x);value=x<0
   if v in values and values[v]!=value:conflict=True
   values[v]=value
  if not conflict:
   for h in hints:
    require(h in database,'missing or deleted propagation hint')
    unknown=[];satisfied=False
    for x in database[h]:
     v=abs(x)
     if v not in values:unknown.append(x)
     elif values[v]==(x>0):satisfied=True;break
    require(not satisfied,'satisfied propagation hint')
    unknown=list(dict.fromkeys(unknown))
    require(len(unknown)<=1,'nonunit propagation hint')
    if not unknown:conflict=True;break
    x=unknown[0];values[abs(x)]=x>0
  require(conflict,'RUP conflict not derived')
  database[label]=clause;count+=1
  if not clause:empty=True
 require(empty,'no checked empty clause')
 return dict(status='VERIFIED_LRAT_UNSAT',variables=variables,input_clauses=initial,referenced_input_clauses=len(wanted),checked_additions=count,input_sha256=hashlib.sha256(raw).hexdigest(),proof_sha256=hashlib.sha256(Path(proof).read_bytes()).hexdigest())

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('proof');a=p.parse_args();print(json.dumps(check(a.cnf,a.proof),indent=2))
