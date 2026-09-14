#!/usr/bin/env python3
"""Check exact geometry and positive words; generate/replay the negative proof.

Uses the previously accepted geometry reader as an explicit pinned dependency.
No solver is used to accept a positive colouring. No solver status alone is
used to accept any negative interface claim.
"""
import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PINNED={
 'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py':'a3f2de1702cbd55650e77ae97759294ff2915d183e8aec6944adb2813037d416',
 'hadwiger_nelson_parts509_interface_lemma/interface_L.json':'a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637',
}

def need(ok,message):
 if not ok:raise ValueError(message)

def digest(path):return sha256(path.read_bytes()).hexdigest()

def inputs():
 for name,h in PINNED.items():need(digest(REPO/name)==h,'dependency hash: '+name)
 path=REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
 spec=importlib.util.spec_from_file_location('pinned_exact_geometry',path)
 m=importlib.util.module_from_spec(spec)
 before=sys.dont_write_bytecode;sys.dont_write_bytecode=True
 try:spec.loader.exec_module(m)
 finally:sys.dont_write_bytecode=before
 den,points,vertices,U,edges=m.read_geometry()
 f=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
 words=[r['witness_colouring_L'] for r in f['classes']];pins=f['interface_L']
 need(len(words)==20 and len(pins)==19,'source relation dimensions')
 crosspins={a if a<374 else b for a,b in edges if (a<374)!=(b<374)}
 need(crosspins==set(pins),'the entire pool uses exactly the known interface')
 for word in words:check_word(list(range(374)),[(a,b) for a,b in edges if b<374],word,4)
 need(len({''.join(word[v] for v in pins) for word in words})==20,'distinct input restrictions')
 return den,points,list(vertices),list(U),list(edges),words,pins

def check_word(vertices,edges,word,q):
 need(len(word)==len(vertices) and set(word)<=set(map(str,range(q))),'colour word length/alphabet')
 need(len(set(vertices))==len(vertices),'duplicate vertex labels')
 col=dict(zip(vertices,word))
 need(all(col[a]!=col[b] for a,b in edges),'improper physical colouring')
 return col

def validate(cert,data):
 den,points,vertices,U,edges,words,pins=data
 X=cert['X'];xs=set(X);S=set(U[:135]);Q=set(U[135:]);vs=list(range(374))+X
 need(X==sorted(xs) and xs<=set(U),'canonical pool labels')
 need(len(xs&S)==126 and len(xs&Q)==8 and len(vs)==508,'fixed a=8 budget')
 need(len({points[v] for v in vs})==508,'physical collision')
 present=set(vs);E=[(a,b) for a,b in edges if a in present and b in present]
 need((cert['source_order'],cert['driver_order'],cert['full_order'],cert['unit_edges'])==(374,134,508,len(E)),'reported geometry')
 allowed=cert['allowed_classes'];forbidden=cert['forbidden_classes']
 need(allowed==sorted(set(allowed)) and forbidden==sorted(set(forbidden)),'canonical relation sets')
 need(set(allowed).isdisjoint(forbidden) and sorted(allowed+forbidden)==list(range(20)),'complete input partition')
 need(0<len(allowed)<20,'positive strict reduction')
 need([r['class'] for r in cert['positive_words']]==allowed,'positive rows cover allowed classes')
 for row in cert['positive_words']:
  col=check_word(vs,E,row['word'],4);p=row['class']
  need(all(col[v]==words[p][v] for v in pins),'positive interface mismatch')
 check_word(vs,E,cert['five_colouring'],5)
 pool5=(HERE/'pool_five_colouring.txt').read_text().strip()
 check_word(vertices,edges,pool5,5)
 return vs,E

def negative_cnf(cert,E,words):
 X=cert['X'];xs=set(X);idx={v:i for i,v in enumerate(X)}
 def var(v,c):return 4*idx[v]+c+1
 clauses=[]
 for v in X:
  clauses.append([var(v,c) for c in range(4)])
  for a,b in combinations(range(4),2):clauses.append([-var(v,a),-var(v,b)])
 for a,b in E:
  if a in xs and b in xs:
   for c in range(4):clauses.append([-var(a,c),-var(b,c)])
 selectors=[4*len(X)+i+1 for i in range(len(cert['forbidden_classes']))]
 clauses.append(selectors)
 for z,p in zip(selectors,cert['forbidden_classes']):
  for a,b in E:
   if (a<374)!=(b<374):
    l,u=(a,b) if a<374 else (b,a)
    clauses.append([-z,-var(u,int(words[p][l]))])
 nv=4*len(X)+len(selectors)
 return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode(),nv,len(clauses)

def old_constraints(U):
 paths=[REPO/'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json',REPO/'hadwiger_nelson_parts509_s_replacement_budget/certificate.json',REPO/'hadwiger_nelson_parts509_pool_shape6_verified/killing_clauses.cnf',REPO/'hadwiger_nelson_parts509_pool_shape7_verified/killing_clauses.cnf',REPO/'hadwiger_nelson_parts509_pool_cover_shrink01/colourings.json']
 rows=[r['D'] for r in json.loads(paths[0].read_text())['sets']]+[r['D'] for r in json.loads(paths[1].read_text())['killing_sets']]
 for p in paths[2:4]:
  for line in p.read_text().splitlines()[1:]:
   q=list(map(int,line.split()));need(q[-1]==0 and all(1<=v<=303 for v in q[:-1]),'seed format');rows.append([U[v-1] for v in q[:-1]])
 rows += [r['D'] for r in json.loads(paths[4].read_text())]
 return {tuple(sorted(r)) for r in rows},{str(p.relative_to(REPO)):digest(p) for p in paths}

def validate_cuts(data):
 _,_,_,U,edges,words,_=data;us=set(U);seed,hashes=old_constraints(U);need(len(seed)==17266,'imported relaxation size')
 expected=json.loads((HERE/'seed_hashes.json').read_text());need(hashes==expected,'seed family hashes')
 sizes=[]
 for row in json.loads((HERE/'colouring_cuts.json').read_text()):
  D=row['D'];X=set(row['excluded_X']);p=row['p'];c=row['c']
  need(D==sorted(set(D)) and set(D)<=us and 0<=p<20,'cut definition')
  need(len(c)==303 and set(c)<=set('.0123') and {v for v,t in zip(U,c) if t=='.'}==set(D),'cut word domain')
  col=dict(enumerate(words[p]));col.update({v:t for v,t in zip(U,c) if t!='.'})
  check_word(sorted(col),[(a,b) for a,b in edges if a in col and b in col],''.join(col[v] for v in sorted(col)),4)
  need(len(X)==134 and len(X&set(U[:135]))==126 and len(X&set(U[135:]))==8,'cut excluded support budget')
  need(not X&set(D) and all(X&set(d) for d in seed),'strict refinement of previous Boolean relaxation')
  seed.add(tuple(D));sizes.append(len(D))
 return sizes

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--kissat',type=Path);ap.add_argument('--drat-trim',type=Path);args=ap.parse_args()
 need(bool(args.kissat)==bool(args.drat_trim),'provide both proof executables')
 args.work.mkdir(parents=True,exist_ok=True);data=inputs();cert=json.loads((HERE/'certificate.json').read_text());vs,E=validate(cert,data);sizes=validate_cuts(data)
 encoded,nv,nc=negative_cnf(cert,E,data[5]);cnf=args.work/'forbidden-interface.cnf';cnf.write_bytes(encoded)
 result={'status':'POSITIVE_WORDS_AND_CNF_VERIFIED_NEGATIVE_PROOF_NOT_RUN','points':len(vs),'unit_edges':len(E),'input_patterns':20,'allowed':len(cert['allowed_classes']),'forbidden':len(cert['forbidden_classes']),'new_cut_sizes':sizes,'cnf_variables':nv,'cnf_clauses':nc,'cnf_sha256':digest(cnf),'certificate_sha256':digest(HERE/'certificate.json'),'four_colourable':True,'record_candidate':False}
 if args.kissat:
  proof=args.work/'forbidden-interface.drat'
  with (args.work/'solver.log').open('w') as f:r=subprocess.run([str(args.kissat.resolve()),'--time=300','-f',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
  need(r.returncode==20,'negative proof producer did not report UNSAT')
  with (args.work/'checker.log').open('w') as f:r=subprocess.run([str(args.drat_trim.resolve()),str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
  need(r.returncode==0 and 's VERIFIED' in (args.work/'checker.log').read_text(),'negative proof not verified')
  result.update(status='EXACT_COMPLETE_INTERFACE_VERIFIED',proof_bytes=proof.stat().st_size,proof_sha256=digest(proof),solver_sha256=digest(args.kissat),checker_sha256=digest(args.drat_trim))
 print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
