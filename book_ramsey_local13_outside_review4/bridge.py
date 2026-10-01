#!/usr/bin/env python3
"""six-reviewer-4: independent literal incidence and row-removal controls.

These graphs can fail the book caps, so capacity defects are signed.
They are not admissible Ramsey hosts. No author or audit module imported.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def round_robin():
    factors=[]
    for offset in range(21):
        factor=[(21,offset)]
        factor += [((offset+i)%21,(offset-i)%21) for i in range(1,11)]
        need(len({x for edge in factor for x in edge}) == 22,'perfect factor')
        factors.append(factor)
    graphs=[]
    for step in (1,2,4,5,8,10):
        selected={(step*i)%21 for i in range(10)}
        need(len(selected)==10,'ten distinct factors')
        red=[set() for i in range(22)]
        for f in selected:
            for u,v in factors[f]:
                red[u].add(v);red[v].add(u)
        graphs.append(red)
    graphs.append([{j for j in range(22) if j!=i and i//11==j//11} for i in range(22)])
    graphs.append([{j for j in range(22) if i//11!=j//11 and i%11!=j%11} for i in range(22)])
    return graphs

def gram(rows,n=10):
    return [[sum(i in row and j in row for row in rows) for j in range(n)] for i in range(n)]

def quadratic(matrix,q):
    return sum(q[i]*matrix[i][j]*q[j] for i in range(len(q)) for j in range(len(q)))

def run():
    counts={'signed_regular_graphs':8,'root_controls':0,'literal_Gram_entries':0,
            'incident_slack_identities':0,'size_six_row_removals':0,'removed_Gram_entries':0,
            'synthetic_binary_Grams':0,'zero_sum_projection_identities':0}
    digest=hashlib.sha256()
    for number,red in enumerate(round_robin()):
        need(all(len(row)==10 and i not in row for i,row in enumerate(red)),'simple ten-regular fixture')
        need(all((j in red[i])==(i in red[j]) for i in range(22) for j in range(22)),'symmetric fixture')
        blue=[set(range(22))-{i}-red[i] for i in range(22)]
        for v in range(22):
            a,b=sorted(red[v]),sorted(blue[v])
            local=[red[i]&set(a) for i in a]
            h=list(map(len,local))
            misses=[{i for i,x in enumerate(a) if x not in red[y]} for y in b]
            actual=gram(misses)
            need([actual[i][i] for i in range(10)]==[x+2 for x in h],'column counts')
            s0=[[h[i]+2 if i==j else h[i]+h[j]-(5 if a[j] in red[a[i]] else 2)-
                 len(local[i]&local[j]) for j in range(10)] for i in range(10)]
            eps=[[0]*10 for i in range(10)]
            for i,j in combinations(range(10),2):
                value=(3-len(red[a[i]]&red[a[j]]) if a[j] in red[a[i]] else
                       6-len(blue[a[i]]&blue[a[j]]))
                eps[i][j]=eps[j][i]=value
            need(actual==[[s0[i][j]-eps[i][j] for j in range(10)] for i in range(10)],'literal local Gram')
            counts['literal_Gram_entries']+=100
            for i in range(10):
                u=sum(len(row)-4 for row in misses if i in row)
                neighbor_h=sum(h[j] for j in range(10) if a[j] in local[i])
                need(sum(eps[i])==3*h[i]+sum(h)-24-neighbor_h-u,'incident defect')
                counts['incident_slack_identities']+=1
            for selected,row in enumerate(misses):
                if len(row)!=6:
                    continue
                residual=gram([other for k,other in enumerate(misses) if k!=selected])
                forced=[[s0[i][j]-eps[i][j]-int(i in row and j in row) for j in range(10)] for i in range(10)]
                need(residual==forced,'literal six-row removal on all100 entries')
                counts['size_six_row_removals']+=1
                counts['removed_Gram_entries']+=100
                digest.update((json.dumps([number,v,selected,residual],separators=(',',':'))+'\n').encode())
            counts['root_controls']+=1
    for step in (1,3,7,9):
        rows=[{(i+step*j)%10 for j in range(4)} for i in range(10)]
        residual=gram(rows)
        full=gram(rows+[set(range(4,10))])
        need(all(residual[i][i]==4 and sum(residual[i])==16 for i in range(10)), 'synthetic four-row Gram')
        need([full[i][i] for i in range(10)]==[4]*4+[5]*6,'synthetic selected all-cubic row')
        vectors=[[int(i==j) for i in range(10)] for j in range(10)]
        vectors += [[i-4 for i in range(10)],[(-1)**i*(i+1) for i in range(10)]]
        for q in vectors:
            total=sum(q);projected=[10*x-total for x in q]
            need(sum(projected)==0 and quadratic(residual,projected)==
                 100*quadratic(residual,q)-160*total*total,'zero-sum projection polynomial')
            need(quadratic(residual,q)>=0 and quadratic(residual,projected)>=0,'synthetic Gram PSD control')
            counts['zero_sum_projection_identities']+=1
        counts['synthetic_binary_Grams']+=1
    counts.update({'agent':'six-reviewer-4','role':'independent mathematical reviewer',
                   'Ramsey_witnesses_claimed':False,'control_stream_sha256':digest.hexdigest()})
    return counts

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    data=(json.dumps(run(),sort_keys=True,separators=(',',':'))+'\n').encode()
    if args.check:
        need(args.check.read_bytes()==data,'complete expected bridge output')
    print(data.decode(),end='')

if __name__=='__main__':
    main()
