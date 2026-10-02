"""Independent scalar image proof of all762 original-domain minimum outcomes.
Whole original cubes produce full11-bit images, with no current-profile stand-in.
Five-variable functions are scalar32-row comparator tables. No producer imports.
"""
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent


def need(test,message):
    if not test:raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def simulate(row,gates):
    row=list(row)
    for a,b in gates:
        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
    return row


def gate(x,a,b):
    if x>>a&1 and not x>>b&1:x ^= (1<<a)|(1<<b)
    return x


def function(word,dead):
    index={p:j for j,p in enumerate(dead)}
    rows=[]
    for x in range(32):
        for a,b in word:x=gate(x,index[a],index[b])
        rows.append(x)
    return rows


def apply_table(x,dead,table,shift):
    pattern=sum((x>>(p-shift)&1)<<j for j,p in enumerate(dead))
    out=table[pattern]
    for j,p in enumerate(dead):
        old=x>>(p-shift)&1;new=out>>j&1
        if old!=new:x ^= 1<<(p-shift)
    return x


def main():
    start=time.monotonic();deadline=start+45
    f=json.loads((ROOT/'fixture.json').read_text())
    prefix=f['B23']+f['LOW_suffixes']['4']
    proposal=json.loads((ROOT/'work/low26-fiveport-preparation-partner4.json').read_text())
    claimed=json.loads((ROOT/'work/partner4-fiveport-minimum-lock-screen.json').read_text())
    domains={};metrics=Counter()
    for lo,hi in combinations(range(13),2):
        ref=[0]*13;ref[lo],ref[hi]=-2,-1;D=0
        for a,b in prefix:
            D+=ref[a]<0 or ref[b]<0
            if ref[a]>ref[b]:ref[a],ref[b]=ref[b],ref[a]
        if D!=9:continue
        need(ref[:2]==[-2,-1],'Original marker route differs')
        free=[p for p in range(13) if p not in (lo,hi)]
        states=set();active=touches=0
        for x in range(2048):
            row=[0]*13;row[lo],row[hi]=-2,-1
            for j,p in enumerate(free):row[p]=x>>j&1
            hit=0
            for t,(a,b) in enumerate(prefix):
                marked=row[a]<0 or row[b]<0
                if marked:hit |= 1<<t
                if row[a]>row[b]:
                    if not marked:active |= 1<<t
                    row[a],row[b]=row[b],row[a]
            need(row[:2]==[-2,-1] and hit.bit_count()==9,'Scalar original cube route failed')
            touches=hit
            states.add(sum(row[p]<<(p-2) for p in range(2,13)))
        need(touches|active==(1<<26)-1,'Selected original D9 base identity')
        domains[(1<<lo)|(1<<hi)]=states
        metrics['original_LOW_free_assignments']+=2048
        metrics['original_LOW_gate_evaluations']+=2048*26
    need(len(domains)==39,'Complete original D9 cube count differs')
    full={}
    for x in range(8192):
        row=simulate([x>>i&1 for i in range(13)],prefix)
        value=sum(v<<i for i,v in enumerate(row))
        full.setdefault(value,x)
    metrics['original_Boolean_inputs']=8192
    metrics['original_Boolean_gate_evaluations']=8192*26
    records=[];counts=Counter();branch_counts=[]
    for branch_id,b in enumerate(proposal['branches']):
        a,q=b['HIGH_zero_gate'];dead=b['dead_preparation_ports']
        conditional={lo:{gate(x,a-2,q-2) for x in states} for lo,states in domains.items()}
        global_image={gate(x,a,q):original for x,original in full.items()}
        census=Counter()
        for function_id,word in enumerate(b['functions']):
            need(time.monotonic()<deadline,'Operational45s check guard; no negative inference')
            table=function(word['shortest_word'],dead)
            need(table==[sum((col>>x&1)<<j for j,col in enumerate(word['full_five_variable_columns'])) for x in range(32)],
                 'Complete scalar function differs from proposed packed columns')
            masks=[]
            for lo,states in conditional.items():
                good=all((apply_table(x,dead,table,2)&1)==int(x==2047) for x in states)
                metrics['conditional_image_tests']+=len(states)
                if good:masks.append(lo)
            masks.sort()
            wrong=any((apply_table(x,dead,table,0)>>2&1)!=int(x.bit_count()>=11) for x in global_image)
            metrics['global_image_tests']+=len(global_image)
            status='MINIMUM_LOCK_EXCLUDES_STANDARD_SIZE44' if masks and wrong else (
                   'MINIMUM_LOCK_BUT_GLOBAL_ORDER_STATISTIC_CORRECT' if masks else 'NO_SINGLE_D9_MINIMUM_LOCK')
            c=claimed['records'][len(records)]
            need(c['branch_id']==branch_id and c['function_id']==function_id and c['original_D9_minimum_masks']==masks and
                 c['status']==status and c['shortest_word']==word['shortest_word'],'Original classification differs')
            witness=c['full_Boolean_wrong_statistic_witness']
            need((witness is not None)==wrong,'Global witness existence differs')
            if witness is not None:
                row=[witness>>i&1 for i in range(13)]
                actual=simulate(row,prefix+[b['HIGH_zero_gate']]+word['shortest_word'])
                need(actual[2]!=sorted(row)[2],'Whole original scalar counterexample failed')
                metrics['full_original_scalar_witnesses']+=1
            need(c['function_columns_sha256']==digest(word['full_five_variable_columns']), 'Complete function fingerprint differs')
            records.append(c);counts[status]+=1;census[status]+=1
        branch_counts.append({'branch_id':branch_id,'HIGH_zero_gate':b['HIGH_zero_gate'],
                              'function_count':len(b['functions']),'census':dict(census)})
    need(len(records)==762 and dict(counts)==claimed['census'] and branch_counts==claimed['branches'],
         'Complete screen or branch census differs')
    need(digest(records)==claimed['records_sha256'],'Full classified records differ')
    result={'agent':'six-sorting-1','role':'researcher','status':'PRIVATE_ALL762_MINIMUM_CLASSIFICATIONS_INDEPENDENTLY_VERIFIED',
            'census':dict(counts),'complete_functions':762,'complete_original_D9_cubes':39,
            'records_sha256':digest(records),'metrics':dict(metrics),
            'same_author_algorithmic_independence':True,'external_person_review_claimed':False,
            'scope':claimed['scope'],'seconds':time.monotonic()-start,
            'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
