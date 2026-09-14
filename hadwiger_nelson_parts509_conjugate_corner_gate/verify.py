#!/usr/bin/env python3
"""Verify a redundant exact transfer corner using 64 existing colouring words.

Python standard library; no SAT solver and no negative-status trust.
The only imported code is the pinned accepted exact geometry reader.
"""
import hashlib, importlib.util, itertools, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; REPO=HERE.parent
GEOMETRY='hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
GEOMETRY_SHA='a3f2de1702cbd55650e77ae97759294ff2915d183e8aec6944adb2813037d416'
INTERFACE='hadwiger_nelson_parts509_interface_lemma/interface_L.json'
INTERFACE_SHA='a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637'

def need(ok,msg):
    if not ok: raise ValueError(msg)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def transform(p):
    return tuple(tuple(c*(-1 if i&2 else 1)*(-1 if k==0 else 1)
                       for i,c in enumerate(z)) for k,z in enumerate(p))

def load():
    need(digest(REPO/GEOMETRY)==GEOMETRY_SHA,'geometry reader hash')
    need(digest(REPO/INTERFACE)==INTERFACE_SHA,'interface words hash')
    sp=importlib.util.spec_from_file_location('accepted_geometry',REPO/GEOMETRY)
    gm=importlib.util.module_from_spec(sp);sp.loader.exec_module(gm)
    den,P,V,U,E=gm.read_geometry()
    words=[r['witness_colouring_L'] for r in json.loads((REPO/INTERFACE).read_text())['classes']]
    return gm,den,P,list(V),list(U),list(E),words

def baseline(U):
    pins=json.loads((REPO/'hadwiger_nelson_parts509_shape8_transfer/seed_hashes.json').read_text())
    need(digest(REPO/'hadwiger_nelson_parts509_shape8_transfer/seed_hashes.json')==
         '7ed42704af6167e5bf0fd82ebaa8269926cc91ce0c033827bb6137afcf3673ce','seed manifest hash')
    for name,h in pins.items():need(digest(REPO/name)==h,'seed source hash '+name)
    paths=[REPO/'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json',
           REPO/'hadwiger_nelson_parts509_s_replacement_budget/certificate.json',
           REPO/'hadwiger_nelson_parts509_pool_shape6_verified/killing_clauses.cnf',
           REPO/'hadwiger_nelson_parts509_pool_shape7_verified/killing_clauses.cnf',
           REPO/'hadwiger_nelson_parts509_pool_cover_shrink01/colourings.json']
    Ds=[r['D'] for r in json.loads(paths[0].read_text())['sets']]
    Ds += [r['D'] for r in json.loads(paths[1].read_text())['killing_sets']]
    for p in paths[2:4]:
        for line in p.read_text().splitlines()[1:]:
            row=list(map(int,line.split()))
            need(row[-1]==0 and all(1<=x<=303 for x in row[:-1]),'positive DIMACS clause')
            Ds.append([U[x-1] for x in row[:-1]])
    Ds += [r['D'] for r in json.loads(paths[4].read_text())]
    Ds=set(tuple(sorted(d)) for d in Ds)
    need(len(Ds)==17266,'old cut count')
    p=REPO/'hadwiger_nelson_parts509_a8_residual_decision/baseline_cuts.json'
    need(digest(p)=='6e6ae80f6c3596c204d657ab7da38bf6f803dd273333006ea3eaed55ca33e55d','three baseline cuts hash')
    Ds.update(tuple(r['D']) for r in json.loads(p.read_text()))
    need(len(Ds)==17269,'R0 cut count');return Ds

def check_word(row,U,E,words):
    D=row['D'];ds=set(D);c=row['c'];p=row['p']
    need(D==sorted(ds) and ds<=set(U),'D labels')
    need(type(p)is int and 0<=p<len(words),'word index')
    need(len(c)==303 and set(c)<=set('.0123'),'word alphabet')
    need({v for v,t in zip(U,c) if t=='.'}==ds,'word domain')
    w=words[p];need(len(w)==374 and set(w)<=set('0123'),'L word')
    col=dict(enumerate(w));col.update({v:t for v,t in zip(U,c) if t!='.'})
    edges=0
    for a,b in E:
        if a in col and b in col:
            need(col[a]!=col[b],'monochromatic unit edge');edges+=1
    return edges

def explain(B,C,S,rows):
    B=set(B);C=set(C);S=set(S)
    projected=[]
    for row in rows:
        d=set(row['D']);bs=d&S;cs=d&C
        need(bs<=B and cs,'projected clause shape')
        projected.append((bs,cs))
    unary=[(bs,next(iter(cs))) for bs,cs in projected if len(cs)==1]
    forced_rejections=0;completions=0;residual_rows=0;hist={}
    for rr in itertools.combinations(sorted(B),9):
        R=set(rr);forced={q for bs,q in unary if bs<=R}
        hist[len(forced)]=hist.get(len(forced),0)+1
        if len(forced)>8:forced_rejections+=1;continue
        residual_rows+=1
        for extra in itertools.combinations(sorted(C-forced),8-len(forced)):
            A=forced|set(extra);X=(S-R)|A;completions+=1
            need(any(not X&set(row['D']) for row in rows),'uncovered corner support')
    return {'unary_cuts':len(unary),'forced_nine_or_more_R_rows':forced_rejections,
            'remaining_R_rows':residual_rows,'literal_completions_checked':completions,
            'forced_Q_histogram':dict(sorted(hist.items()))}

def main():
    data=json.loads((HERE/'certificate.json').read_text());gm,den,P,V,U,E,words=load()
    L=set(range(374));S=set(U[:135]);Q=set(U[135:]);vs=set(V)
    key={P[v]:v for v in V};images={v:transform(P[v]) for v in V}
    need(len(set(images.values()))==677,'all images distinct')
    need(all(transform(images[v])==P[v] for v in V),'coordinate involution')
    M={v:key.get(images[v]) for v in V}
    need({M[v] for v in L}==L,'L maps to L')
    B=sorted(v for v in S if M[v] in Q);C=sorted(v for v in Q if M[v] in S)
    F=sorted(v for v in Q if M[v] is None)
    need(B==data['B'] and C==data['C'] and len(B)==len(C)==16,'exchanged sets')
    need(len(F)==15 and all(M[v] in S for v in S-set(B)),'remaining overlap')
    need({M[v] for v in B}==set(C) and {M[v] for v in C}==set(B),'exchange bijection')
    # Reconstruct every strict unit edge on the complete transformed ambient.
    target=(den*den,0,0,0,0,0,0,0);image_edges=[]
    for a,b in itertools.combinations(sorted(V),2):
        if gm.squared_distance(images[a],images[b])==target:image_edges.append((a,b))
    need(image_edges==sorted(map(tuple,E)),'full transformed strict edge list')
    old=baseline(U);rows=data['rows'];need(len(rows)==64,'certificate size')
    need(len({tuple(r['D']) for r in rows})==64,'distinct cuts')
    need(all(tuple(r['D']) in old for r in rows),'all cuts already belong to R0')
    checked_edges=sum(check_word(r,U,E,words) for r in rows)
    summary=explain(B,C,S,rows)
    answer={'status':'EXACT_CONJUGATE_CORNER_REDUNDANCY_VERIFIED',
            'ambient_points':677,'ambient_edges':3400,'denominator':den,
            'original_and_image_pair_checks_each':228826,'mapped_back_to_pool':662,
            'selected_points':508,'image_selected_S':127,'image_selected_Q':7,
            'B':B,'C':C,'unmapped_Q':F,'R_choices':11440,'A_choices':12870,
            'corner_supports':147232800,'already_existing_cuts':64,
            'checked_positive_edge_incidences':checked_edges,**summary,
            'R0_survivors_in_corner':0,'new_cut_count':0,'strict_residual_shrink':False,
            'full_a8_closed':False,'record_candidate':False,'solver_used':False}
    print(json.dumps(answer,indent=2,sort_keys=True))

if __name__=='__main__':main()
