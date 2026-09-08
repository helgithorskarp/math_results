"""Write the fixed graph CNF without loading or calling a SAT solver."""
from pathlib import Path
import json,os,hashlib
P=Path(os.environ.get('VND_WORKDIR',str(Path(__file__).resolve().parent/'work'))).resolve()
def main():
 points=json.loads((P/'exact_points.json').read_text())['points'];edges=json.loads((P/'exact_edges.json').read_text());n=len(points);m=len(edges)
 if (n,m)!=(64513,542472):raise ValueError('source dimensions')
 with (P/'gate.cnf').open('w') as f:
  f.write(f'p cnf {4*n} {n+4*m+3}\n')
  for v in range(n):f.write(' '.join(str(4*v+c+1) for c in range(4))+' 0\n')
  for u,v in edges:
   for c in range(4):f.write(f'{-(4*u+c+1)} {-(4*v+c+1)} 0\n')
  f.write('1 0\n6 0\n23 0\n')
 h=hashlib.sha256((P/'gate.cnf').read_bytes()).hexdigest()
 if h!='aa4305ebd561a52e89fe77738deee93c53f0c062a7715b879a51d0ada69b3bef':raise ValueError('CNF identity')
 print('VERIFIED_CNF_IDENTITY',h)
if __name__=='__main__':main()
