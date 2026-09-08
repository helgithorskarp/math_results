#!/usr/bin/env python3
"""Physical arithmetic controls and malformed-certificate controls."""
import copy,itertools,json
from interface import extract,read_graph
from verify_physical import verify

def audit_graph(a):
    n=len(a);degrees=list(map(len,a))
    if len(set(degrees))!=1:raise ValueError('control not regular')
    k=degrees[0];physical=[(i,j) for i,j in itertools.combinations(range(n),2) if j in a[i]]
    bound=max((len(a[i]&a[j]) for i,j in physical),default=0);edges=shared_edges=outside_cases=0
    for u,v in physical:
        C=a[u]&a[v]
        if any(y in a[x] and z in a[x] and z in a[y] for x,y,z in itertools.combinations(C,3)):continue
        edges+=1;T=set(range(n))-a[u]-a[v];c=len(C);dc={w:len(a[w]&C) for w in C}
        local=[]
        for root in (u,v):
            H=a[root];d={w:len(a[w]&H) for w in C};P=sum(d.values());Q=0
            for x,y in itertools.combinations(C,2):
                if y in a[x]:Q+=d[x]+d[y]-len(a[x]&a[y]&H)
            local.append((P,Q,d))
        if len(T)!=n-2*k+c:raise ValueError('outside size identity')
        for w in C:
            if len(a[w]&T)!=k-local[0][2][w]-local[1][2][w]+dc[w]:raise ValueError('physical degree identity')
        for x,y in itertools.combinations(C,2):
            if y not in a[x]:continue
            shared_edges+=1
            if T:outside_cases+=1
            if len(a[x]&a[y])!=len(a[x]&a[y]&a[u])+len(a[x]&a[y]&a[v])+len(a[x]&a[y]&T):raise ValueError('physical common-edge identity')
        e=sum(dc.values())//2
        if local[0][0]+local[1][0] < c*(k-len(T))+2*e:raise ValueError('degree inequality')
        if local[0][1]+local[1][1] < sum(d*d for d in dc.values())+(2*k-len(T)-bound)*e:raise ValueError('edge inequality')
    return edges,shared_edges,outside_cases

def check_inequalities():
    pairs=list(itertools.combinations(range(6),2));regular=0;totals=[0,0,0]
    for word in range(1<<15):
        a=[set() for _ in range(6)]
        for bit,(i,j) in enumerate(pairs):
            if word>>bit&1:a[i].add(j);a[j].add(i)
        if len(set(map(len,a)))!=1:continue
        regular+=1
        for i,x in enumerate(audit_graph(a)):totals[i]+=x
    additional=[]
    for part in (1,2,3):
        n=4*part;additional.append([{j for j in range(n) if j//part!=i//part} for i in range(n)])
    for n in (10,12,16):
        additional.append([{j for j in range(n) if 1<=min((i-j)%n,(j-i)%n)<=3} for i in range(n)])
    for a in additional:
        for i,x in enumerate(audit_graph(a)):totals[i]+=x
    if totals[1]==0 or totals[2]==0:raise ValueError('vacuous common-edge controls')
    return {'all_six_vertex_graphs':32768,'regular_six_vertex_graphs':regular,'additional_regular_graphs':len(additional),'eligible_root_edges':totals[0],'checked_shared_edges':totals[1],'shared_edges_with_nonempty_outside':totals[2]}

def graph(degree,mult=1,shift=0):
    word=0
    for bit,(i,j) in enumerate(itertools.combinations(range(43),2)):
        x=(mult*i+shift)%43;y=(mult*j+shift)%43
        if min((x-y)%43,(y-x)%43)<=degree//2:word|=1<<bit
    return {'n':43,'red_hex':f'{word:0226x}'}

def main():
    result=check_inequalities();fixtures=0;bad=0
    for degree in (18,24):
        for mult,shift in ((1,0),(2,3),(7,19),(13,40)):
            g=graph(degree,mult,shift);c=extract(g);verify(g,c);fixtures+=1
            if c['regular_degree']!=degree:raise ValueError('regular recognition')
    for degree in (0,16,20,22,26,42):
        if extract(graph(degree))['status']!='OUTSIDE_PROVED_REGULAR_BRANCH':raise ValueError('scope')
    # Irregular graph with an 18-degree vertex must not be rejected by branch membership.
    irregular=graph(18);irregular['red_hex']=f'{int(irregular["red_hex"],16)^(1<<9):0226x}'
    if extract(irregular)['status']!='OUTSIDE_PROVED_REGULAR_BRANCH':raise ValueError('irregular scope')
    g=graph(18);cert=extract(g)
    mutations=[]
    x=copy.deepcopy(cert);x['color']=1-x['color'];mutations.append(x)
    x=copy.deepcopy(cert);x['vertices'][1]=x['vertices'][0];mutations.append(x)
    x=copy.deepcopy(cert);x['vertices'][0]=43;mutations.append(x)
    x=copy.deepcopy(cert);x['graph_word_sha256']='0'*64;mutations.append(x)
    for x in mutations:
        try:verify(g,x)
        except (ValueError,TypeError):bad+=1
        else:raise ValueError('accepted corrupt physical certificate')
    malformed=[{'n':42,'red_hex':g['red_hex']},{'n':43,'red_hex':'f'*226},{'n':43,'red_hex':'0'*225},{'n':True,'red_hex':g['red_hex']},dict(g,unexpected=1)]
    for x in malformed:
        try:read_graph(x)
        except (ValueError,TypeError):bad+=1
        else:raise ValueError('accepted malformed graph')
    result.update({'status':'VERIFIED_PHYSICAL_OVERLAP_IDENTITIES_AND_CONTROLS','regular43_fixtures':fixtures,'outside_branch_controls':7,'bad_physical_certificates_and_inputs_rejected':bad})
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
