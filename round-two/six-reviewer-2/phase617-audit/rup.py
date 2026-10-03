"""Independent positive-hint RUP proof checker, with deletion and failure tests."""
import json,sys
from pathlib import Path

def need(ok,why):
    if not ok:raise ValueError(why)

def dimacs(text):
    head=None;tokens=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith('c'):continue
        if line.startswith('p '):
            need(head is None and not tokens,'sole initial header');parts=line.split();need(len(parts)==4 and parts[:2]==['p','cnf'],'DIMACS header');head=tuple(map(int,parts[2:]));continue
        need(head is not None,'header precedes literals');tokens.extend(map(int,line.split()))
    need(head is not None,'missing header');n,m=head;need(n>0 and m>=0,'header counts');clauses=[];clause=[]
    for v in tokens:
        if v==0:clauses.append(tuple(clause));clause=[]
        else:need(1<=abs(v)<=n,'literal variable bounds');clause.append(v)
    need(not clause and len(clauses)==m,'entire declared CNF');return n,clauses

def replay(n,initial,text):
    live={i+1:tuple(c)for i,c in enumerate(initial)};last=len(initial);added=deleted=hints_count=0;final=None
    for raw in text.splitlines():
        raw=raw.strip()
        if not raw or raw.startswith('c'):continue
        words=raw.split();cid=int(words[0]);need(cid>last,'strict action identifiers');last=cid
        if len(words)>1 and words[1]=='d':
            ids=list(map(int,words[2:]));need(ids and ids[-1]==0 and 0 not in ids[:-1],'deletion termination')
            for i in ids[:-1]:need(i in live,'only available deleted clause');del live[i];deleted+=1
            continue
        ints=list(map(int,words[1:]));need(ints.count(0)==2 and ints[-1]==0,'exact two clause/hint terminators');cut=ints.index(0);clause=tuple(ints[:cut]);hints=ints[cut+1:-1]
        need(all(1<=abs(v)<=n for v in clause),'added literal bounds');need(all(h>0 and h in live for h in hints),'only currently available positive hints')
        assumption={};conflict=False
        for v in clause:
            var=abs(v);value=int(v<0)
            if var in assumption and assumption[var]!=value:conflict=True
            assumption[var]=value
        if conflict:need(not hints,'explicit tautological assumption control')
        for index,h in enumerate(hints):
            premise=live[h]
            if any(assumption.get(abs(v))==int(v>0)for v in premise):continue
            unset={v for v in premise if abs(v)not in assumption}
            if not unset:conflict=True;need(index==len(hints)-1,'conflict is final propagation hint');break
            need(len(unset)==1,'hint must be unit or conflicting');v=next(iter(unset));assumption[abs(v)]=int(v>0)
        need(conflict,'RUP propagation contradiction required')
        live[cid]=clause;added+=1;hints_count+=len(hints);final=clause
    need(final==(),'last proved addition is empty')
    return dict(additions=added,deletions=deleted,positive_hints=hints_count)

def controls():
    valid=[(2,[(1,2),(-1,),(-2,)],'4 2 0 1 2 0\n5 d 1 0\n6 0 3 4 0\n'),(1,[(1,),(-1,)],'3 0 1 2 0\n')]
    positives=[replay(*v)for v in valid];bad=[(1,[(1,),(-1,)],'3 0 -1 2 0\n'),(1,[(1,),(-1,)],'3 0 1 4 0\n'),(2,[(1,2)],'2 0 1 0\n'),(1,[(1,),(-1,)],'3 d 1 0\n4 0 1 2 0\n'),(1,[(1,),(-1,)],'2 0 1 2 0\n'),(1,[(1,),(-1,)],'3 2 0 1 2 0\n'),(1,[(1,),(-1,)],'3 0 1 2\n')]
    rejected=0
    for v in bad:
        try:replay(*v)
        except(ValueError,IndexError):rejected+=1
        else:raise ValueError('damaged RUP accepted')
    n,C=dimacs('c valid\np cnf 2 3\n1 2 0\n-1 0\n-2 0\n');need((n,C)==(2,[(1,2),(-1,),(-2,)]),'literal DIMACS parse')
    for t in ['p cnf 1 2\n1 0\n','p cnf 1 1\n2 0\n','p cnf 1 1\n1\n']:
        try:dimacs(t)
        except ValueError:rejected+=1
        else:raise ValueError('damaged DIMACS accepted')
    return dict(status='STRICT_RUP_CONTROLS_COMPLETE',positive_proofs=positives,rejected=rejected)
if __name__=='__main__':
    if len(sys.argv)==1:x=controls()
    else:
        n,C=dimacs(Path(sys.argv[1]).read_text());x=replay(n,C,Path(sys.argv[2]).read_text())
    print(json.dumps(x,sort_keys=True,separators=(',',':')))
