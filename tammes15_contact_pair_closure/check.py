#!/usr/bin/env python3
"""Stdlib exact checker for the complete 5..8 external-contact pair classification."""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys

from geometry import DH,lens,witness
from patches import models,dot,one,t,sign_open
from polynomial import bernstein,need
from rational import Rat

ROOT=Path(__file__).resolve().parent
Q4=49*t**4+44*t**3+14*t*t+4*t+one
Q5=49*t**5-3*t**4-22*t**3+2*t*t+5*t+one
COMMON_ALPHA=16*t**4*(one-t)*(2*t+one)/Q5
COMMON_SQUARE=16*t*t*(one-t)**2*(one+t)**2*(2*t+one)**2*(3*t+one)*(5*t*t-one)/(Q4*Q5)

def certify(certificate):
    need(set(certificate)=={'version','blocked','exception'} and certificate['version']==1,'certificate schema')
    rows=certificate['blocked']
    need(all(type(r) is list and len(r)==5 and all(type(x) is int for x in r) for r in rows),'blocked schema')
    blocked={tuple(r[:4]):r[4] for r in rows}
    need(len(blocked)==len(rows),'duplicate blocked pair')
    exception=certificate['exception']
    need(type(exception) is dict and set(exception)=={'n','type','pair','orientation','rejected_witness'},'exception schema')
    need(type(exception['pair']) is list and len(exception['pair'])==2,'exception pair schema')
    need(all(type(x) is int for x in [exception['n'],exception['type'],*exception['pair'],exception['orientation'],exception['rejected_witness']]),'exception integers')
    need(exception['orientation'] in (-1,1),'exception orientation')
    exceptional_key=(exception['n'],exception['type'],*exception['pair'])
    mm,counts=models();seen=set();seen_exception=False
    classes={n:{'lens_excluded':0,'both_positions_blocked':0,'one_position':0} for n in (5,6,7,8)}
    grams=set()
    need(sign_open(one-t)==sign_open(one+2*t)==sign_open(DH)==1,'positive anchor Gram matrix')
    need(sign_open(Q4)==sign_open(Q5)==1,'common witness denominators')
    for model in mm:
        n,ai,a=model['n'],model['type'],model['a']
        for i,j in model['pairs']:
            key=(n,ai,i,j);w=dot(a[i],a[j]);grams.add((w.n,w.d))
            if sign_open(2*t*t-one-w)==1:
                need(key not in blocked and key!=exceptional_key,'unused certificate row on empty lens')
                classes[n]['lens_excluded']+=1
                continue
            need(sign_open(one+w)==sign_open(one-w)==1,'independent contact pair')
            c,normal,delta=lens(a,i,j)
            if key in blocked:
                k=blocked[key];need(k in a and k not in (i,j),'blocked witness label')
                alpha,beta,square=witness(a,c,normal,delta,k)
                need(alpha==COMMON_ALPHA and square==COMMON_SQUARE,'shared obstruction identities')
                need(sign_open(alpha)==sign_open(square)==1,'uniform two-position packing obstruction')
                seen.add(key);classes[n]['both_positions_blocked']+=1
                continue
            need(key==exceptional_key and not seen_exception,'unclassified contact pair')
            need(sign_open(delta)==1,'two real, distinct exceptional positions')
            # Strict inequalities construct the exceptional patch plus one point.
            for u,v in combinations(range(n),2):
                if (u,v) not in model['edges']:
                    need(sign_open(t-dot(a[u],a[v]))==1,'exceptional A packing')
            orientation=exception['orientation']
            for k in range(n):
                if k in (i,j):continue
                alpha,beta,square=witness(a,c,normal,delta,k)
                need(sign_open(alpha)==-1,'exceptional center gap')
                if beta==0 or sign_open(orientation*beta)==-1:
                    continue
                need(sign_open(orientation*beta)==sign_open(square)==1,'exceptional position packing')
            k=exception['rejected_witness'];need(k in a and k not in (i,j),'rejected witness label')
            alpha,beta,square=witness(a,c,normal,delta,k)
            need(sign_open(alpha)==-1 and sign_open(-orientation*beta)==1 and sign_open(square)==-1,'opposite position packing violation')
            seen_exception=True;classes[n]['one_position']+=1
    need(seen==set(blocked),'unvisited blocked pair')
    need(seen_exception,'unvisited exceptional pair')
    need([list(classes[n].values()) for n in (5,6,7,8)]==[[0,0,0],[1,0,0],[5,1,0],[24,7,1]],'classification counts')
    need(len(grams)==7,'pair Gram kernel count')
    return {'status':'VERIFIED_EXACT','cover':counts,
            'pair_classes':[{'n':n,**classes[n]} for n in (5,6,7,8)],
            'eligible_pair_entries':39,'distinct_pair_Gram_functions':7,
            'exception':exception,
            'claim_scope':'External double-contact closure for 5..7; one unique compatible exception at 8.'}

def selftest(c):
    # Sign and rational normalization controls, including endpoint vanishing.
    need(Rat((-2,),(4,))==Rat((-1,),(2,)),'constant normalization control')
    need(sign_open(t-Rat((1,),(2,)))==1 and sign_open(Rat((3,),(5,))-t)==1,'open interval sign control')
    need(bernstein((1,))==[Fraction(1)],'constant Bernstein control')
    mutations=[]
    d=deepcopy(c);d['blocked'].pop();mutations.append(d)
    d=deepcopy(c);d['blocked'][0][4]=2;mutations.append(d)
    d=deepcopy(c);d['blocked'][0][4]=0;mutations.append(d)
    d=deepcopy(c);d['exception']['orientation']=-1;mutations.append(d)
    d=deepcopy(c);d['exception']['rejected_witness']=6;mutations.append(d)
    d=deepcopy(c);d['exception']={};mutations.append(d)
    d=deepcopy(c);d['blocked'].append(d['blocked'][0][:]);mutations.append(d)
    d=deepcopy(c);d['blocked'].append([5,0,0,1,2]);mutations.append(d)
    for k,d in enumerate(mutations):
        rejected=False
        try:certify(d)
        except ValueError:rejected=True
        need(rejected,'false certificate accepted: '+str(k))

if __name__=='__main__':
    need(sys.argv[1:] in ([],['--selftest']),'usage: check.py [--selftest]')
    raw=(ROOT/'certificate.json').read_bytes();certificate=json.loads(raw)
    result=certify(certificate)
    if sys.argv[1:]:selftest(certificate)
    result['certificate_sha256']=sha256(raw).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))
