"""Freeze the entire finite cohort before ordinary SAT queries. No widening."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time
import model as m

def encode(vertices, edges):
    index = {v:i for i,v in enumerate(vertices)}
    var = lambda v,c: 4*index[v]+c+1
    clauses = []
    for v in vertices:
        clauses.append([var(v,c) for c in range(4)])
        for a in range(4):
            for b in range(a):
                clauses.append([-var(v,a),-var(v,b)])
    for u,v in edges:
        for c in range(4):
            clauses.append([-var(u,c),-var(v,c)])
    # Fix one existing vertex's colour; every colouring has such a renaming.
    clauses.append([var(0,0)])
    return f'p cnf {4*len(vertices)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--solver',type=Path,required=True)
    args = ap.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    m.require(not (args.work/'frozen.json').exists(), 'refuse to overwrite or rerun frozen cohort')
    edges,adj = m.load()
    frozen = []
    for seed in range(8):
        for orientation in (0,1):
            vertices = m.support(seed,orientation,adj)
            ie = m.induced(vertices,edges)
            frozen.append({'seed':seed,'orientation':orientation,'vertices':vertices,
                'vertex_sha256':m.digest_labels(vertices),'edge_sha256':m.digest_edges(ie),
                'order':len(vertices),'size':len(ie)})
    text = json.dumps(frozen,indent=2)+'\n'
    (args.work/'frozen.json').write_text(text)
    print('FROZEN',len(frozen),hashlib.sha256(text.encode()).hexdigest(),flush=True)
    cert = {'version':1,'graph_sha256':m.GRAPH_SHA,'source_strict_edge_sha256':m.EDGE_SHA,'records':[]}
    for row in frozen:
        tag = f"s{row['seed']}-o{row['orientation']}"
        vs = row['vertices']; ie = m.induced(vs,edges)
        cnf = args.work/(tag+'.cnf'); proof = args.work/(tag+'.drat')
        cnf.write_text(encode(vs,ie))
        start = time.monotonic()
        proc = subprocess.run([str(args.solver),'--time=10','--conflicts=100000','--no-binary',str(cnf),str(proof)],capture_output=True,text=True,timeout=20)
        (args.work/(tag+'.log')).write_text(proc.stdout+'\n'+proc.stderr)
        status = 'SAT' if proc.returncode==10 else 'UNSAT' if proc.returncode==20 else 'UNKNOWN'
        result = {k:v for k,v in row.items() if k!='vertices'}
        result.update(status=status,seconds=time.monotonic()-start,cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest())
        if status == 'SAT':
            true = {int(x) for line in proc.stdout.splitlines() if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
            word = ''
            for i in range(len(vs)):
                colours = [c for c in range(4) if 4*i+c+1 in true]
                m.require(len(colours)==1,'SAT decoder: missing/ambiguous colour')
                word += str(colours[0])
            m.check_word(vs,ie,word,4)
            result['four_word'] = word
        cert['records'].append(result)
        (args.work/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
        print(tag,status,row['size'],round(result['seconds'],3),flush=True)
        if status != 'SAT':
            print('STOP: proof-bearing candidate check needed' if status=='UNSAT' else 'STOP: unshrunk UNKNOWN',flush=True)
            return
    print('ALL_SAT; fixed cohort finished; no expansion',flush=True)

if __name__ == '__main__':
    main()
