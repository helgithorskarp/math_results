"""Square-character/bit-mask proposals for actual-AP implications.

Every trace is a proposal. An incomplete closure or absence of contradiction
is not a mathematical exclusion. Independent Euler/set checking is required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

N,P,C=3704,617,1852


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',type=Path,required=True)
    parser.add_argument('--root',type=int,default=-1);parser.add_argument('--caps',type=int,nargs=2,default=[197,-1])
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--summary',type=Path,required=True)
    parser.add_argument('--rounds',type=int,default=16);a=parser.parse_args();start=time.monotonic()
    base=a.base.read_bytes();data=json.loads(base);s=data['s'];D=data['denominator']
    squares={r*r%P for r in range(1,P)}
    colors=[]
    for x in range(N):
        r=(x-C+(s if x<C else (1-s)%P))%P
        colors.append(-1 if not r else int(r not in squares)^int(x>=C))
    loads=[0]*N;S=sum(w for _,_,w in data['color0_APs'])
    for aa,d,w in data['color0_APs']:
        for a0 in [aa,N-1-aa-6*d]:
            for j in range(7):loads[a0+j*d]+=w
    caps=[None if v==-1 else v for v in a.caps]
    if any(v is not None and v<0 for v in caps):raise ValueError('Nonnegative caps or -1 uncapped')
    budget=[None if k is None else k*D-S for k in caps]
    known=[-1]*N;masks=[0,0];edits=[0,0];cost=[0,0]
    for x,c in enumerate(colors):
        if c>=0 and caps[c] is not None and D-loads[x]>budget[c]:
            known[x]=c;masks[c]|=1<<x
    initial_fixed=[sum(v==c for v in known) for c in [0,1]]
    units=[];terminal=None
    def assign(x,b):
        nonlocal terminal
        if known[x]!=-1:raise RuntimeError('Only fresh implications recorded')
        known[x]=b;masks[b]|=1<<x
        c=colors[x]
        if c>=0 and b!=c:
            edits[c]+=1;cost[c]+=D-loads[x]
            if caps[c] is not None and edits[c]>caps[c]:terminal={'kind':'class_cap','class':c}
            elif caps[c] is not None and cost[c]>budget[c]:terminal={'kind':'base_defect','class':c}
    if a.root!=-1:
        if colors[a.root]!=0 or known[a.root]!=-1:raise ValueError('A permitted original0 root is required')
        assign(a.root,1)
    rounds=0
    for round_id in range(a.rounds):
        rounds+=1;before=len(units)
        for d in range(1,(N-1)//6+1):
            starts=(1<<(N-6*d))-1
            for c in [0,1]:
                shifted=[masks[c]>>(j*d) for j in range(7)]
                full=starts
                for v in shifted:full&=v
                if full:
                    aa=(full&-full).bit_length()-1
                    terminal={'kind':'mono_AP','AP':[aa,d]};break
                for j in range(7):
                    candidates=starts
                    for k in range(7):
                        if k!=j:candidates&=shifted[k]
                    candidates&=~shifted[j]
                    while candidates:
                        bit=candidates&-candidates;candidates-=bit;aa=bit.bit_length()-1;x=aa+j*d
                        if known[x]==1-c:continue
                        if known[x]==c:
                            terminal={'kind':'mono_AP','AP':[aa,d]};break
                        units.append([aa,d,x,1-c]);assign(x,1-c)
                        if terminal:break
                    if terminal:break
                if terminal:break
            if terminal:break
        if terminal or len(units)==before:break
    out={'format':'QR617_ACTUAL_UNIT_TRACE_1','phase':s,'caps':caps,'root':a.root,
         'base_certificate_sha256':hashlib.sha256(base).hexdigest(),'units':units,'terminal':terminal}
    encoded=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
    a.output.write_bytes(encoded)
    summary={'agent':'six-vdw-3','role':'researcher','phase':s,'caps':caps,'root':a.root,
             'initial_fixed_candidate_colors':initial_fixed,'base_defect_budgets':budget,
             'units':len(units),'rounds':rounds,'terminal':terminal,'forced_original_class_edits':edits,
             'consumed_base_defects':cost,'fixed_candidate_colors':[sum(v==c for v in known) for c in [0,1]],
             'forced_poles':sum(c<0 and b>=0 for c,b in zip(colors,known)),
             'proposal_only':True,'no_contradiction_proves_no_exclusion':True,
             'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'certificate_sha256':hashlib.sha256(encoded).hexdigest()}
    a.summary.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
