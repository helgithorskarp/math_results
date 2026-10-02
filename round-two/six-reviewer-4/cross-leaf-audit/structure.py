#!/usr/bin/env python3
"""Exact signed controls for the written degree-sensitive deficit identities.

Controls need not satisfy the book caps. Positivity is proved in REVIEW.md,
not inferred from sampling these invalid hosts.
"""
from itertools import combinations
import json

def need(value, message):
    if not value:
        raise ValueError(message)

def mm(a,b):
    n=len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def quadratic(a,z):
    return sum(a[i][j]*z[i]*z[j] for i in range(len(z)) for j in range(len(z)))

def check(a):
    n=22;need(len(a)==n and all(len(r)==n for r in a),'matrix dimension')
    need(all(a[i][j] in (0,1) and a[i][j]==a[j][i] for i in range(n) for j in range(n)),'simple symmetry')
    need(all(a[i][i]==0 for i in range(n)),'diagonal')
    degree=list(map(sum,a));edges=sum(degree)//2
    red=[{j for j in range(n) if a[i][j]} for i in range(n)]
    blue=[set(range(n))-red[i]-{i} for i in range(n)]
    d=[[0 if i==j else 3-len(red[i]&red[j]) if a[i][j] else 6-len(blue[i]&blue[j])
        for j in range(n)] for i in range(n)]
    a2=mm(a,a)
    expression=[[(14-degree[i] if i==j else 0)+degree[i]+degree[j]-14
                 -(degree[i]+degree[j])*a[i][j]+17*a[i][j]-a2[i][j]
                 for j in range(n)] for i in range(n)]
    need(d==expression,'general deficit identity')
    s=[sum(degree[j] for j in red[i]) for i in range(n)]
    row=list(map(sum,d))
    need(row==[2*edges-294+38*degree[i]-degree[i]**2-2*s[i] for i in range(n)],'general row identity')
    carrier=sorted(degree)==[9]*4+[10]*18
    if carrier:
        f=[10-v for v in degree];ell=[sum(f[j] for j in red[i]) for i in range(n)]
        specialized=[[(4+f[i] if i==j else 0)-3*a[i][j]-a2[i][j]
                      +(f[i]+f[j])*a[i][j]+6-f[i]-f[j] for j in range(n)] for i in range(n)]
        need(d==specialized,'tag matrix identity')
        need(row==[2+f[i]+2*ell[i] for i in range(n)],'tagged rows')
        need(sum(row)==120,'total deficit weight')
        for i in range(n):
            e=sum(a[j][k] for j,k in combinations(sorted(red[i]),2))
            redsum=sum(d[i][j] for j in red[i])
            need(redsum==3*degree[i]-2*e,'red local deficit identity')
    energies=0
    for z in [[1]*n, [i-10 for i in range(n)], [(-1)**i*(i%5) for i in range(n)]]:
        minus=[[ (row[i] if i==j else 0)-d[i][j] for j in range(n)] for i in range(n)]
        plus=[[ (row[i] if i==j else 0)+d[i][j] for j in range(n)] for i in range(n)]
        need(quadratic(minus,z)==sum(d[i][j]*(z[i]-z[j])**2 for i in range(n) for j in range(i+1,n)),'weighted Laplacian energy')
        need(quadratic(plus,z)==sum(d[i][j]*(z[i]+z[j])**2 for i in range(n) for j in range(i+1,n)),'weighted signless energy')
        energies+=2
    commutes=mm(a,d)==mm(d,a)
    return {'carrier':carrier,'energies':energies,'commutes':commutes,
            'nonnegative':all(v>=0 for r in d for v in r),'row_sum_total':sum(row)}

def controls():
    n=22;a=[[int(i!=j and min((i-j)%n,(j-i)%n)<=5) for j in range(n)] for i in range(n)]
    for i,j in [(0,1),(10,11)]:a[i][j]=a[j][i]=0
    seen=set();results=[]
    for step in range(24):
        result=check(a);need(result['carrier'],'switched carrier');results.append(result)
        seen.add(tuple(tuple(r) for r in a));found=False
        for i,j,k,l in combinations(range(n),4):
            for x,y,z,w in [(i,j,k,l),(i,k,j,l),(i,l,j,k)]:
                if a[x][y] and a[z][w] and not a[x][z] and not a[y][w]:
                    b=[r[:] for r in a]
                    for u,v in [(x,y),(z,w)]:b[u][v]=b[v][u]=0
                    for u,v in [(x,z),(y,w)]:b[u][v]=b[v][u]=1
                    if tuple(tuple(r) for r in b) not in seen:
                        a=b;found=True;break
            if found:break
        need(found,'distinct degree-preserving control unavailable')
    varied=[]
    for kind in ['empty','full','path','star']:
        b=[[0]*n for _ in range(n)]
        for i,j in combinations(range(n),2):
            if kind=='full' or (kind=='path' and j==i+1) or (kind=='star' and i==0):b[i][j]=b[j][i]=1
        varied.append(check(b))
    need(any(not r['commutes'] for r in results),'irregular degrees alone do not supply commutation')
    return {'signed_four_low_controls':len(results),'distinct_carriers':len(seen),
            'general_noncarrier_controls':len(varied),'exact_integer_energy_checks':sum(r['energies'] for r in results+varied),
            'four_low_noncommuting_controls':sum(not r['commutes'] for r in results),
            'four_low_deficit_sum':120,'valid_host_construction_claimed':False,
            'positivity_basis':'ordinary nonnegative colored page deficits under valid-host hypotheses; signed controls test identities only'}

if __name__=='__main__':
    print(json.dumps(controls(),sort_keys=True))
