#!/usr/bin/env python3
"""Independent labeled-word cover, physical unit/relabeling and literal fixture checks."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import hashlib
import json


def need(ok,why):
    if not ok:raise ValueError(why)


def rotation(v):
    return v if v>=33 else 3*(v//3)+(v%3+1)%3


def primary():
    left=set(combinations(range(43),2));parts=[[],[],[]]
    while left:
        e=min(left);orb={e};f=tuple(sorted(map(rotation,e)))
        while f!=e:orb.add(f);f=tuple(sorted(map(rotation,f)))
        left-=orb;a,b=e
        if b<33 and a//3==b//3:continue
        kind=0 if b<33 else 1 if a>=33 else 2
        parts[kind].append((e,orb))
    parts[0].sort(key=lambda r:(r[0][0]//3,r[0][1]//3,(r[0][1]-r[0][0])%3))
    parts[1].sort();parts[2].sort(key=lambda r:(r[0][1],r[0][0]//3))
    need(list(map(len,parts))==[165,45,110],'physical primary partition')
    return {e:k for k,(_,orb) in enumerate(sum(parts,[]),1) for e in orb}


def normalized_units(counts,all_fixed=False):
    ids=primary();u,v=33,34;answer=[]
    for k,n in enumerate(counts[:3]):
        for i in range(4+sum(counts[:k]),4+sum(counts[:k+1])):
            answer += [ids[3*i,u]*(1 if k!=2 else -1),ids[3*i,v]*(1 if k!=1 else -1)]
    if all_fixed:
        fixed=counts[3:]
        for k,n in enumerate(fixed):
            for f in range(35+sum(fixed[:k]),35+sum(fixed[:k+1])):
                answer += [ids[u,f]*(1 if k!=2 else -1),ids[v,f]*(1 if k!=1 else -1)]
    return answer


def check_permutation(p,ids):
    need(sorted(p)==list(range(43)),'vertex bijection')
    need(list(p[:12])==list(range(12)) and {p[33],p[34]}=={33,34},'core and pair preserved')
    need(all(p[rotation(v)]==rotation(p[v]) for v in range(43)),'commutes with C3')
    mapped={}
    for e,x in ids.items():
        f=tuple(sorted((p[e[0]],p[e[1]])));need(f in ids,'noninternal orbit preserved')
        y=ids[f];need(x not in mapped or mapped[x]==y,'well-defined orbit map');mapped[x]=y
    need(sorted(mapped.values())==list(range(1,321)),'primary bijection')


def word_census(n,moving):
    hist=Counter();permutations=set();words=0
    for word in product(range(3),repeat=n):
        words+=1;counts=tuple(word.count(k) for k in range(3));hist[counts]+=1
        order=sorted(range(n),key=lambda i:word[i]);p=list(range(43))
        for new,old in enumerate(order):
            if moving:
                for s in range(3):p[12+3*old+s]=12+3*new+s
            else:p[35+old]=35+new
        sorted_word=[None]*n
        for old,k in enumerate(word):
            target=(p[12+3*old]-12)//3 if moving else p[35+old]-35
            sorted_word[target]=k
        need(sorted_word==sorted(word),'literal star normalization')
        permutations.add(tuple(p))
    return hist,permutations,words


def expected():
    moving,mp,mn=word_census(7,True);fixed,fp,fn=word_census(8,False)
    ids=primary()
    for p in mp|fp:check_permutation(p,ids)
    swap=list(range(43));swap[33],swap[34]=34,33;check_permutation(swap,ids)
    profiles=Counter();degrees=Counter();raw=0;allowed=0
    for (a,b,c),wm in moving.items():
        for (x,y,z),wf in fixed.items():
            weight=wm*wf;raw+=weight
            # Read degrees as weighted physical contacts, not blue-degree inequalities.
            red_u=3*a+3*b+x+y;red_v=3*a+3*c+x+z
            if red_u not in range(18,25) or red_v not in range(18,25):continue
            allowed+=weight;degrees[red_u,red_v]+=weight
            key=min((a,b,c,x,y,z),(a,c,b,x,z,y));profiles[key]+=weight
    need(raw==14348907 and allowed==4806900,'all factored labeled assignments')
    return profiles,dict(moving_words=mn,fixed_words=fn,normalizing_permutations=len(mp|fp),pair_swaps=1,
        all_no_BB_assignments=raw,allowed_labeled_assignments=allowed,
        red_degree_census=[dict(degrees=list(k),count=v) for k,v in sorted(degrees.items())])


def verify_certificate(cert,wanted=None):
    if wanted is None:wanted=expected()
    profiles,census=wanted
    need(cert['types']==['RR','RB','BR'] and cert['counts_order']==['a','b','c','x','y','z'],'type conventions')
    need(cert['pair']==[33,34] and cert['blue_cycles']==list(range(4,11)) and cert['other_fixed']==list(range(35,43)),'literal domain')
    need(cert['degree_window']==[18,24],'valid degree window')
    need(cert['all_no_BB_assignments']==census['all_no_BB_assignments'] and cert['allowed_labeled_assignments']==census['allowed_labeled_assignments'],'labeled census')
    rows=cert['profiles'];keys=[tuple(r['counts']) for r in rows]
    need(keys==sorted(profiles),'complete unique119profiles')
    for r in rows:
        a,b,c,x,y,z=r['counts']
        need(r['labeled_assignments']==profiles[a,b,c,x,y,z],'exact orbit weight')
        need(r['red_degrees']==[3*a+3*b+x+y,3*a+3*c+x+z],'literal root degrees')
        need(r['units']==normalized_units(r['counts'],True),'all30physical star units')
    abc=sorted({k[:3] for k in profiles})
    need([tuple(r['counts']) for r in cert['moving_cases']]==abc,'complete9moving cases')
    for r in cert['moving_cases']:
        key=tuple(r['counts']);part=[k for k in profiles if k[:3]==key]
        need(r['id']=='a%d_b%d_c%d'%key and r['units']==normalized_units(list(key)),'moving id and14physical units')
        need(r['joint_profiles']==len(part) and r['labeled_assignments']==sum(profiles[k] for k in part),'moving weights')
    return dict(census=census,joint_profiles=len(rows),moving_profiles=len(abc),full_star_units_checked=30*len(rows),moving_units_checked=14*len(abc))


def fixture(path):
    lines=Path(path).read_text().splitlines();need(lines and lines[0]=='19','local19vertexorder')
    edges=[tuple(map(int,s.split())) for s in lines[1:]]
    need(edges==sorted(set(edges)) and all(len(e)==2 and 0<=e[0]<e[1]<19 for e in edges),'literal edge list')
    red=set(edges);core=(1742,3477,2915,1777,3498,2908,941,1371,2294,3181,2715,1846)
    need(all(((a,b) in red)==bool(core[a]&(1<<b)) for a,b in combinations(range(12),2)),'exact Core194')
    need(all((a,18) not in red for a in range(18)) and all((a,12) not in red for a in range(12)),'empty blue pair12,18')
    need(all((12,f) in red and (f,18) not in red for f in range(13,18)),'five other fixed blue neighbors of18')
    signatures=[]
    for f in range(13,18):
        mask=0
        for i in range(4):
            colors={(a,f) in red for a in range(3*i,3*i+3)};need(len(colors)==1,'uniform fixed incidences')
            if next(iter(colors)):mask|=1<<i
        signatures.append(mask)
    need(signatures==[0,0,1,6,10],'fixture signatures')
    for q in combinations(range(19),5):need(len({e in red for e in combinations(q,2)})==2,'Ramsey19fixture')
    for q in combinations(range(18),4):need(any(e in red for e in combinations(q,2)),'blue-neighborhood has no blueK4')
    for a,b in combinations(range(19),2):
        def rotate(v):return 3*(v//3)+(v%3+1)%3 if v<12 else v
        need(((a,b) in red)==(tuple(sorted((rotate(a),rotate(b)))) in red),'localC3action')
    common=[f for f in range(19) if f not in (12,18) and tuple(sorted((12,f))) not in red and tuple(sorted((18,f))) not in red]
    need(common==list(range(12)),'exact common blue core')
    return dict(order=19,red_edges=len(red),five_sets=11628,neighborhood_four_sets=3060,signatures=signatures,blue_pair=[12,18],five_blue_fixed_neighbors=list(range(13,18)),common_blue=common,
        scope='counterexample to a local four-fixed-neighbor cap, not a full43extension')


def controls(cert,fixture_path,work,wanted):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    for name in ('missing_profile','wrong_weight','wrong_degree','wrong_full_unit','missing_moving','wrong_moving_unit','wrong_window','wrong_total'):
        bad=copy.deepcopy(cert)
        if name=='missing_profile':bad['profiles'].pop()
        if name=='wrong_weight':bad['profiles'][0]['labeled_assignments']+=1
        if name=='wrong_degree':bad['profiles'][0]['red_degrees'][0]+=1
        if name=='wrong_full_unit':bad['profiles'][0]['units'][-1]*=-1
        if name=='missing_moving':bad['moving_cases'].pop()
        if name=='wrong_moving_unit':bad['moving_cases'][0]['units'][0]*=-1
        if name=='wrong_window':bad['degree_window']=[17,25]
        if name=='wrong_total':bad['allowed_labeled_assignments']+=1
        reject(name,lambda:verify_certificate(bad,wanted))
    for name in ('wrong_order','duplicate_edge','red_empty_link','blue_vf','wrong_core'):
        lines=Path(fixture_path).read_text().splitlines()
        if name=='wrong_order':lines[0]='18'
        if name=='duplicate_edge':lines.append(lines[1])
        if name=='red_empty_link':lines.append('0 18')
        if name=='blue_vf':lines.remove('12 13')
        if name=='wrong_core':lines.remove('0 1')
        path=work/'bad.edges';path.write_text('\n'.join(lines)+'\n');reject(name,lambda:fixture(path))
    (work/'bad.edges').unlink();need(len(rejected)==13,'all negative controls');return rejected


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    c=json.loads(a.certificate.read_text());expected_profiles=expected()
    result=dict(profile_check=verify_certificate(c,expected_profiles),fixture=fixture(a.fixture),rejected=controls(c,a.fixture,a.work,expected_profiles))
    a.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS complete attachment cover, physical normalization and local counterfixture')
