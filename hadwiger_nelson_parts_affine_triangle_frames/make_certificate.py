"""Optional positive SAT witness discovery; no solver verdict is a proof premise."""
import argparse,json
from pathlib import Path
from pysat.solvers import Solver
import model as m
from check import check_word

def main():
    ap=argparse.ArgumentParser();ap.add_argument('work',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args();w=args.work
    lines=(w/'input.txt').read_text().splitlines();groups=[]
    for line in lines[510:]:
        v=list(map(int,line.split()));groups.append(list(zip(v[4::2],v[5::2])))
    metrics=[list(map(int,l.split())) for l in (w/'scan_metrics.txt').read_text().splitlines()];P,den=m.points();cert={}
    for line in (w/'scan_residual.txt').read_text().splitlines():
        v=list(map(int,line.split()));mid,ng=v[:2];m.require(ng==len(v)-2,'residual malformed');edges=[e for g in v[2:] for e in groups[g]]
        row=metrics[mid];nf=row[6];frames=list(zip(row[7:7+2*nf:2],row[8:7+2*nf:2]))
        if all(m.is_original(m.metric(P[a],P[b]),den) for a,b in frames):continue
        clauses=[]
        for i in range(509):
            clauses.append([4*i+c+1 for c in range(4)])
            for c in range(4):
                for d in range(c+1,4):clauses.append([-4*i-c-1,-4*i-d-1])
        for i,j in edges:
            for c in range(4):clauses.append([-4*i-c-1,-4*j-c-1])
        with Solver(name='cadical195',bootstrap_with=clauses) as solver:
            solver.conf_budget(1000000);m.require(solver.solve_limited() is True,'not positively certified; investigate exact geometry')
            positive={v for v in solver.get_model() if v>0}
            word=''.join(str(next(c for c in range(4) if 4*i+c+1 in positive)) for i in range(509))
        check_word(word,edges);cert[str(mid)]=word
    args.output.write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n');print('positive words',len(cert))
if __name__=='__main__':main()
