"""Own multiple-leading Gaussian and finite-difference certificate checker.

Only exact data inputs, stdlib only; no producer/checker modules or CAS.
"""
import argparse,json,pathlib,hashlib
from fractions import Fraction as F
from math import comb,lcm

def need(ok,why):
    if not ok:raise ValueError(why)

def columns(poly,h):
    a={}
    for (i,j),c in poly:a[j]=a.get(j,F(0))+F(c)*h**i
    return a

def val(poly,q):
    if not poly:return F(0)
    out=F(0)
    for e in range(max(poly),-1,-1):out=out*q+poly.get(e,0)
    return out

def native_poly(p):
    need(type(p['denominator']) is int and p['denominator']>0,'exact point denominator')
    a={}
    for (i,j),c in p['terms']:
        need(i==0 and type(j) is int and j>=0 and j not in a,'complete canonical q polynomial')
        a[j]=F(c)/p['denominator']
    return a

def determinant(a):
    a=[list(row) for row in a];d=F(1);n=len(a)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];d=-d
        t=a[i][i];d*=t
        for j in range(i+1,n):
            r=a[j][i]/t
            for k in range(i+1,n):a[j][k]-=r*a[i][k]
    return d

def leading(a):
    original=[list(row) for row in a];a=[list(row) for row in a];d=F(1);out=[];n=len(a)
    for i in range(n):
        t=a[i][i]
        if not t:return [determinant([row[:k] for row in original[:k]]) for k in range(1,n+1)]
        d*=t;out.append(d)
        for j in range(i+1,n):
            r=a[j][i]/t
            for k in range(i+1,n):a[j][k]-=r*a[i][k]
    return out

def point(binding,point,damage=None):
    h=point['h'];need(type(h) is int and 3<=h<=133,'complete exact h point')
    expected=[(r['group'],r['order']) for r in binding['bounds']]
    need([(r['group'],r['order']) for r in point['rows']]==expected,'entire point catalogue')
    rows={(r['group'],r['order']):r for r in point['rows']}
    if damage=='shift-coefficient':rows[expected[0]]['q4_shifted']['terms'][0][1]='-99'
    if damage=='missing-minor':rows.pop(expected[-1])
    bound={(r['group'],r['order']):r for r in binding['bounds']};identities=0;shift=0
    for name,form in binding['forms'].items():
        matrix=[[columns(z,h) for z in row] for row in form['cleared']];n=len(matrix)
        original=[];shifted=[]
        for k in range(1,n+1):
            r=rows[(name,k)];d=bound[(name,k)]['q_degree_bound']
            original.append(native_poly(r['original']));shifted.append(native_poly(r['q4_shifted']))
            need(max(original[-1],default=0)<=d and max(shifted[-1],default=0)<=d,'entire q degree')
        maxq=max(bound[(name,k)]['q_degree_bound'] for k in range(1,n+1))
        for u in range(maxq+1):
            q=4+u;minor=leading([[val(z,q) for z in row] for row in matrix])
            for k in range(1,n+1):
                if u<=bound[(name,k)]['q_degree_bound']:
                    need(minor[k-1]==val(original[k-1],q),'every degree-complete determinant identity')
                    need(val(original[k-1],q)==val(shifted[k-1],u),'every degree-complete q4 shift identity')
                    identities+=1;shift+=1
    return dict(h=h,complete=True,determinant_nodes=identities,shift_nodes=shift,point_sha256=hashlib.sha256(json.dumps(point,sort_keys=True,separators=(',',':')).encode()).hexdigest())

def differences(a):
    out=[]
    while a:
        out.append(a[0]);a=[a[i+1]-a[i] for i in range(len(a)-1)]
    return out

def newton(binding,directory,certificate,damage=None):
    expected=[(r['group'],r['order']) for r in binding['bounds']]
    need([(r['group'],r['order']) for r in certificate['rows']]==expected,'complete Newton catalogue')
    need(certificate['domain']=='integer h>=3, real q>=4' and certificate['basis']=='binom(h-3,m)*(q-4)^e','exact integer-only basis domain')
    bound={(r['group'],r['order']):r for r in binding['bounds']};points={};receipts=[]
    for h in range(3,134):
        p=json.loads((directory/f'h{h}.json').read_text());need(p['h']==h,'original point labels')
        checked=json.loads((directory/f'independent-h{h}.json').read_text());need(checked['complete'] and checked['h']==h,'every independent point completed')
        need(checked['point_sha256']==hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'whole point bound to independent determinant receipt')
        receipts.append(checked);points[h]={(r['group'],r['order']):native_poly(r['q4_shifted']) for r in p['rows']}
    if damage=='Newton-coefficient':certificate['rows'][0]['Newton_coefficients_by_q_power'][0][0]='999'
    if damage=='real-domain':certificate['domain']='real h>=3, real q>=4'
    need(certificate['domain']=='integer h>=3, real q>=4','never real-h transport')
    count=0;fullcoeff=0;reconstruct=0;canon=[]
    for r in certificate['rows']:
        key=r['group'],r['order'];b=bound[key];dh,dq=b['h_degree_bound'],b['q_degree_bound']
        cc=r['Newton_coefficients_by_q_power'];need(len(cc)==dq+1,'all q columns')
        owncols=[]
        for e,col in enumerate(cc):
            need(len(col)==dh+1,'all h columns')
            actual=[points[3+i][key].get(e,F(0)) for i in range(dh+1)];fresh=differences(actual)
            claimed=[F(c) for c in col];need(claimed==fresh,'EVERY independently regenerated finite difference')
            need(all(c>=0 for c in fresh),'all integer Newton coefficients nonnegative')
            for u in range(dh+1):
                need(sum(fresh[m]*comb(u,m) for m in range(u+1))==actual[u],'entire Newton reconstruction')
                reconstruct+=1
            count+=sum(bool(c) for c in fresh);fullcoeff+=len(fresh);owncols.append([str(c) for c in fresh])
        need(F(owncols[0][0])>0,'positive h3/q4 constant');canon.append(dict(group=key[0],order=key[1],columns=owncols))
    return dict(actual_agent='six-reviewer-5',role='independent reviewer',complete=True,integer_h_domain_only=True,points=len(points),nonzero_positive_coefficients=count,all_coefficients=fullcoeff,Newton_identity_nodes=reconstruct,determinant_nodes=sum(r['determinant_nodes'] for r in receipts),shift_nodes=sum(r['shift_nodes'] for r in receipts),whole_fresh_coefficient_sha256=hashlib.sha256(json.dumps(canon,sort_keys=True,separators=(',',':')).encode()).hexdigest())

def main():
    a=argparse.ArgumentParser();a.add_argument('binding',type=pathlib.Path);a.add_argument('path',type=pathlib.Path);a.add_argument('output',type=pathlib.Path);a.add_argument('--newton',type=pathlib.Path);a.add_argument('--damage');opts=a.parse_args()
    b=json.loads(opts.binding.read_text())
    out=newton(b,opts.path,json.loads(opts.newton.read_text()),opts.damage) if opts.newton else point(b,json.loads(opts.path.read_text()),opts.damage)
    opts.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
