"""Generate one positive word or a retained solver trace for the frozen graph."""
import argparse,hashlib,json,subprocess,time
from pathlib import Path
from model import geometry,summary

def cnf(n,edges,k):
    v=lambda i,c:k*i+c+1
    clauses=[[v(i,c) for c in range(k)] for i in range(n)]
    clauses += [[-v(i,a),-v(i,b)] for i in range(n) for a in range(k) for b in range(a+1,k)]
    clauses += [[-v(i,c),-v(j,c)] for i,j in edges for c in range(k)]
    clauses.append([1])
    return 'p cnf %d %d\n'%(n*k,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
def check(word,n,edges,k):
    if len(word)!=n or any(c not in '0123456'[:k] for c in word) or any(word[i]==word[j] for i,j in edges): raise ValueError('bad word')
def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True,type=Path);p.add_argument('--kissat',required=True);a=p.parse_args()
    a.work.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();g=geometry();s=summary(g)
    (a.work/'geometry.json').write_text(json.dumps(g,indent=2)+'\n')
    (a.work/'summary.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    if s['vertices']>508 or s['overlaps']!=[[0,1,1],[0,2,1],[1,2,0]]:raise RuntimeError('geometry gate failed')
    ed=set(g['edges']);B=g['special']['B'];C=g['special']['C']
    if tuple(sorted((B,C))) not in ed:raise RuntimeError('no global cycle')
    text=cnf(s['vertices'],g['edges'],4);path=a.work/'four.cnf';path.write_text(text)
    cmd=[a.kissat,'--time=60','--conflicts=1000000','--no-binary',str(path),str(a.work/'four.drat')]
    t=time.monotonic();run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=75)
    (a.work/'solver.log').write_text(run.stdout)
    meta={'command':cmd,'returncode':run.returncode,'solver_seconds':time.monotonic()-t,'cnf_sha256':hashlib.sha256(text.encode()).hexdigest(),'geometry_seconds':t-start,'geometry':s}
    (a.work/'run.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    if run.returncode!=10:
        print(json.dumps(meta,indent=2));return
    values={int(t) for line in run.stdout.splitlines() if line.startswith('v ') for t in line.split()[1:] if int(t)>0}
    colours=[]
    for i in range(s['vertices']):
        c=[j for j in range(4) if 4*i+j+1 in values]
        if len(c)!=1:raise ValueError('bad model')
        colours.append(str(c[0]))
    word=''.join(colours);check(word,s['vertices'],g['edges'],4)
    five='4'+word[1:];check(five,s['vertices'],g['edges'],5)
    cert={'four_word':word,'five_word':five,'expected':s}
    (a.work/'certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'SAT_WORD_CHECKED','geometry':s,'solver_seconds':meta['solver_seconds'],'geometry_seconds':meta['geometry_seconds']},indent=2,sort_keys=True))
if __name__=='__main__':main()
