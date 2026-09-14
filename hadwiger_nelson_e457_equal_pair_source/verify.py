#!/usr/bin/env python3
"""Definition-level E457 geometry, colouring, CNF and proof verifier."""
import argparse,hashlib,json,lzma,subprocess,tempfile
from itertools import combinations
from pathlib import Path
from build import clauses,edges,encode

HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def filehash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def native(checker,n,es):
 data=f'{n} {len(es)} 2\n'+''.join(f'{u} {v}\n' for u,v in es)+'0 0\n1 1\n'
 p=subprocess.run([str(checker)],input=data,text=True,capture_output=True,check=True);z=json.loads(p.stdout)
 need(z=={'satisfiable':False,'nodes':1348142,'conflicts':674115,'colouring':[]},'native decision mismatch');return z
def proof(tool):
 with tempfile.TemporaryDirectory() as td:
  raw=Path(td)/'state.drat'
  with lzma.open(HERE/'state.drat.xz','rb') as src:raw.write_bytes(src.read())
  p=subprocess.run([str(tool),str(HERE/'state.cnf'),str(raw)],capture_output=True,text=True)
  need(p.returncode==0 and 'VERIFIED' in p.stdout+p.stderr,'DRAT replay failed')
  return {'verified':True,'uncompressed_sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}
def verify(checker,drat_trim=None):
 c=json.loads((HERE/'core.json').read_text());need(c['schema']=='hn-e457-equal-pair-v1','schema')
 rows=c['points'];need(len(rows)==457 and len({tuple(r) for r in rows})==457,'points')
 need(all(len(r)==4 and all(type(q) is int for q in r) for r in rows),'coordinate row')
 es=edges(rows);need(len(es)==2329,'edge count')
 need(rows[0]==[0,0,0,0] and rows[1]==[0,0,96,0],'terminals')
 a,b,c0,d=(rows[1][q]-rows[0][q] for q in range(4));need(a*b+c0*d==0 and 9*(3*a*a+11*b*b+c0*c0+33*d*d)==64*1296,'terminal distance')
 word=c['equal_four_colouring'];need(len(word)==457 and all(type(q) is int and 0<=q<4 for q in word),'colour word')
 need(word[0]==word[1] and all(word[u]!=word[v] for u,v in es),'equal colouring')
 f=clauses(len(rows),es);raw=encode(len(rows),f);need(raw==(HERE/'state.cnf').read_bytes(),'CNF mismatch')
 ex=json.loads((HERE/'expected.json').read_text());out={'verified':True,'vertices':457,'edges':2329,'physical_pairs_checked':104196,'terminal_squared_distance':'64/9','proper_equal_four_colouring':True,'cnf_variables':1828,'cnf_clauses':12517,'point_sha256':digest(rows),'edge_sha256':digest(es),'cnf_sha256':hashlib.sha256(raw).hexdigest(),'compressed_drat_sha256':filehash(HERE/'state.drat.xz'),'native':native(checker,len(rows),es),'drat':proof(drat_trim) if drat_trim else {'verified':False,'reason':'optional checker not supplied'},'record_candidate':False}
 need({k:v for k,v in out.items() if k!='drat'}=={k:v for k,v in ex.items() if k!='drat'},'expected values')
 if drat_trim:need(out['drat']==ex['drat'],'expected proof')
 (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n');return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--checker',type=Path,required=True);p.add_argument('--drat-trim',type=Path);a=p.parse_args();print(json.dumps(verify(a.checker,a.drat_trim),sort_keys=True))
if __name__=='__main__':main()

