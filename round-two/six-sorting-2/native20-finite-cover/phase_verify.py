"""Independent numeric marker and truth-table-composition checks.
No producer, sibling checker, profiler or solver imports.
"""
import hashlib,json,resource,time
from collections import deque
from itertools import combinations
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
PREV=ROOT
PORTS=(1,2,3,5,7,8,9,10,11)
INDEX={p:i for i,p in enumerate(PORTS)}
def need(test,msg):
    if not test:raise ValueError(msg)
def statekey(low,high):return tuple(map(tuple,low)),tuple(map(tuple,high))
def mass(envelope):return sum(2**d for lo,hi,d in envelope)
def support(envelope):return {p for lo,hi,d in envelope for p in range(13) if (lo|hi)>>p&1}
def next_rows(rows,gate):
    classes={}
    a,b=gate
    for lo,hi,d in rows:
        values=[0]*13
        for j,p in enumerate(p for p in range(13) if lo>>p&1):values[p]=j-2
        for j,p in enumerate(p for p in range(13) if hi>>p&1):values[p]=j+2
        touched=values[a]<0 or values[b]<0 or values[a]>1 or values[b]>1
        values[a],values[b]=min(values[a],values[b]),max(values[a],values[b])
        tag=(sum(1<<p for p,x in enumerate(values) if x<0),sum(1<<p for p,x in enumerate(values) if x>1))
        classes[tag]=max(classes.get(tag,-1),d+int(touched))
    return tuple(sorted((lo,hi,d) for (lo,hi),d in classes.items()))
def scalar_function(word):
    cols=[0]*9
    for x in range(512):
        values=[x>>p&1 for p in range(9)]
        for a,b in word:
            i,j=INDEX[a],INDEX[b]
            values[i],values[j]=min(values[i],values[j]),max(values[i],values[j])
        for i,y in enumerate(values):
            if y:cols[i]|=1<<x
    return tuple(cols)
def scalar_preparations():
    packet=json.loads((PREV/'preparation-functions.json').read_text())
    words={0:[[]]};tables={0:[[0]]};controls=0
    for group in packet:
        n=group['n'];rows=group['functions'];out=[];paths=[]
        for i,row in enumerate(rows):
            if row['parent'] is None:
                need(i==0 and row['length']==0,'bad preparation root')
                actual=list(range(1<<n));word=[]
            else:
                parent=row['parent'];a,b=row['gate']
                need(0<=parent<i and 0<=a<b<n,'bad preparation parent/gate')
                actual=[]
                for x in out[parent]:
                    v=[x>>p&1 for p in range(n)]
                    v[a],v[b]=min(v[a],v[b]),max(v[a],v[b])
                    actual.append(sum(y<<p for p,y in enumerate(v)))
                word=paths[parent]+[[a,b]]
                need(row['length']==rows[parent]['length']+1,'preparation distance differs')
            encoded=sum(x<<(n*j) for j,x in enumerate(actual))
            need(encoded==row['function'] and len(word)==row['length'],'preparation full truth table differs')
            out.append(actual);paths.append(word)
        ids={tuple(x):i for i,x in enumerate(out)}
        need(len(ids)==len(rows),'duplicate preparation function')
        for i,actual in enumerate(out):
            for a,b in combinations(range(n),2):
                nxt=[]
                for x in actual:
                    values=[x>>p&1 for p in range(n)]
                    values[a],values[b]=min(values[a],values[b]),max(values[a],values[b])
                    nxt.append(sum(y<<p for p,y in enumerate(values)))
                need(tuple(nxt) in ids,'preparation function set not closed')
                need(rows[ids[tuple(nxt)]]['length']<=rows[i]['length']+1,'preparation distance not shortest')
                controls+=1
        words[n]=paths;tables[n]=out
    return words,tables,controls
def main():
    start=time.monotonic();metrics={}
    pins=json.loads((PREV/'initial-artifacts.json').read_text())
    for name in ['p20-intake.json','pre6-cover.json','preparation-functions.json']:
        need(hashlib.sha256((PREV/name).read_bytes()).hexdigest()==pins[name],'imported generated premise changed: '+name)
    phase=json.loads((PREV/'pre6-cover.json').read_text())
    states=phase['states'];ids={statekey(r['low'],r['high']):r['id'] for r in states}
    need(len(ids)==len(states) and [r['id'] for r in states]==list(range(len(states))),'state ids not bijective')
    intake=json.loads((PREV/'p20-intake.json').read_text())['cases'][1]
    need(statekey(states[0]['low'],states[0]['high'])==statekey(intake['families']['two_minima']['ordinary']['envelope'],intake['families']['two_maxima']['ordinary']['envelope']),'wrong phase root')
    reached={0};todo=deque([0]);phase_controls=first6_controls=0
    while todo:
        sid=todo.popleft();s=states[sid];low,high=statekey(s['low'],s['high'])
        need(mass(low)==mass(high)==480,'phase mass differs')
        dead=sorted(set(range(13))-support(low)-support(high))
        need(s['preparation_ports']==dead and len(dead)<=4,'preparation ports differ')
        edges=[]
        for gate in combinations(range(13),2):
            if 6 in gate:continue
            phase_controls+=1
            nl=next_rows(low,gate);nh=next_rows(high,gate)
            if mass(nl)>512 or mass(nh)>512:continue
            key=statekey(nl,nh);need(key in ids,'accepted successor missing')
            nxt=ids[key];selfloop=nxt==sid
            if selfloop:need(not set(gate)&(support(low)|support(high)),'nonpreparation selfloop')
            else:
                need(4 not in gate and len(nl)+len(nh)<len(low)+len(high),'nonmerge phase edge')
                if nxt not in reached:reached.add(nxt);todo.append(nxt)
            edges.append([list(gate),nxt,selfloop])
        need(edges==s['transitions'],'phase edge list differs')
        cases=[]
        for r in range(13):
            if r==6:continue
            first6_controls+=1;gate=tuple(sorted((6,r)))
            nl=next_rows(low,gate);nh=next_rows(high,gate)
            if mass(nl)<=512 and mass(nh)<=512:
                need(mass(nl)==mass(nh)==512,'joint did not saturate')
                need(not (support(nl)-{0})&(support(nh)-{12}),'joint supports overlap')
                cases.append({'partner':r,'low':list(map(list,nl)),'high':list(map(list,nh)),'native4_branch_excluded':r==4})
        need(cases==phase['first6_cases'][sid]['cases'],'all first6 cases differ')
    need(len(reached)==len(states),'unreachable phase states')
    generated=[]
    def descend(sid,word):
        generated.append({'state_id':sid,'event_word':word})
        for gate,nxt,selfloop in states[sid]['transitions']:
            if not selfloop:descend(nxt,word+[gate])
    descend(0,[])
    need(generated==phase['all_event_words'],'full event history cover differs')
    words,tables,prep_controls=scalar_preparations()
    data=json.loads((ROOT/'tf-cover.json').read_text())
    trows=data['T'];tfrows=data['TF']
    tkeys={}
    for i,row in enumerate(trows):
        origin=phase['all_event_words'][row['original_event_index']]
        need(row['state_id']==origin['state_id'] and row['word']==origin['event_word'],'T representative provenance differs')
        columns=scalar_function(row['word'])
        need(columns==tuple(row['columns']),'T full scalar function differs')
        key=(row['state_id'],columns)
        need(key not in tkeys,'duplicate T key')
        tkeys[key]=i
    for origin in phase['all_event_words']:
        columns=scalar_function(origin['event_word'])
        key=(origin['state_id'],columns)
        need(key in tkeys,'original event function omitted')
        need(len(trows[tkeys[key]]['word'])<=len(origin['event_word']),'folded T length increased')
    tfkeys={}
    for i,row in enumerate(tfrows):
        key=(row['state_id'],tuple(row['columns']))
        need(key not in tfkeys,'duplicate TF function/profile')
        tfkeys[key]=i
    allbits=(1<<512)-1;seen=set();chosen=set();compositions=0
    # Compose independent scalar F truth tables with T by disjoint truth cells.
    for ti,t in enumerate(trows):
        dead=states[t['state_id']]['preparation_ports'];k=len(dead)
        cells=[]
        for x in range(1<<k):
            cell=allbits
            for j,p in enumerate(dead):
                col=t['columns'][INDEX[p]]
                cell&=col if x>>j&1 else allbits^col
            cells.append(cell)
        need(sum(cells)==allbits,'T truth cells not a full partition')
        for fi,table in enumerate(tables[k]):
            cols=list(t['columns'])
            for j,p in enumerate(dead):
                out=0
                for x,values in enumerate(table):
                    if values>>j&1:out|=cells[x]
                cols[INDEX[p]]=out
            key=(t['state_id'],tuple(cols));need(key in tfkeys,'preparation function composition omitted')
            i=tfkeys[key];seen.add(i);record=tfrows[i]
            candidate_len=len(t['word'])+len(words[k][fi])
            need(len(record['word'])<=candidate_len,'TF length increased')
            if record['t_index']==ti and record['preparation_index']==fi:
                mapped=[[dead[a],dead[b]] for a,b in words[k][fi]]
                chosen.add(i)
                need(record['preparation_word']==mapped and record['word']==t['word']+mapped,'TF representative metadata differs')
            compositions+=1
    need(len(seen)==len(tfrows),'unreachable TF function/profile')
    need(len(chosen)==len(tfrows),'TF function does not match its chosen provenance')
    # Independently check each chosen TF word's own parent F and truth table.
    for row in tfrows:
        t=trows[row['t_index']];dead=states[t['state_id']]['preparation_ports']
        mapped=[[dead[a],dead[b]] for a,b in words[len(dead)][row['preparation_index']]]
        need(row['state_id']==t['state_id'] and row['preparation_word']==mapped and row['word']==t['word']+mapped,'chosen TF provenance differs')
    result={'agent':'six-sorting-2','role':'researcher','status':'NUMERIC_PHASE_AND_DNF_FUNCTION_COVER_VERIFIED','phase_states':len(states),'phase_gate_controls':phase_controls,'first6_gate_controls':first6_controls,'all_event_words':len(generated),'T_full_functions':len(trows),'TF_full_functions':len(tfrows),'all_preparation_compositions':compositions,'preparation_complete_closure_controls':prep_controls,'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Numeric marker vectors differ from producer masks; scalar T/full-F truth tables are composed by complete disjoint truth cells, rather than producer comparator-column composition. Imported P20 intake and zero-one/commutation proofs remain explicit. No suffix exclusion.'}
    (ROOT/'verify-phase-tf.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
