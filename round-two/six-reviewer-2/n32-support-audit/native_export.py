"""AFTER-seal instrumentation of unchanged native public coefficient functions.

Explicit researcher imports HERE only; not used by primary verify.py.
"""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json,sys,signal

def canon(x):
 if isinstance(x,Fraction):return str(x)
 if isinstance(x,dict):return{str(k):canon(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return[canon(v)for v in x]
 return x

def main():
 p=argparse.ArgumentParser();p.add_argument('author',type=Path);p.add_argument('output',type=Path);args=p.parse_args();root=args.author.resolve();sys.path.insert(0,str(root));from verify import seed_fixture
 from fixed32 import ordinary_reference
 from model import blocks
 seed=json.loads((root/'seed.json').read_text());pairs,beta=seed_fixture(seed);result={'all255_supported_coordinates':[[a,b,str(beta[a][b])]for a,b in __import__('affine').supported_pairs(32)]}
 for name,b in [('seed',beta),('ordinary_reference',ordinary_reference()[2])]:
  fields=[]
  for j,aa,g,K,U in blocks(32,b):fields.append({'degree':j,'layers':aa,'metric':g,'K':K,'U':U,'G':[[g[i]*v for v in row]for i,row in enumerate(K)],'H':[[g[i]*v for v in row]for i,row in enumerate(U)]})
  result[name]=fields
 raw=json.dumps(canon(result),sort_keys=True,separators=(',',':')).encode();args.output.write_bytes(raw+b'\n');print(json.dumps({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'sectors':34,'role':'postseal original native field instrumentation, not independent derivation'}))
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s native export')));signal.alarm(45);main()
