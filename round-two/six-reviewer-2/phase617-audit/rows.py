"""Full one-phase AP reconstruction, independent of any supplied witness."""
import json,sys,hashlib
from field import inputs,tables,require

def run(N):
    data=inputs(N);witnesses=[[None]*256 for _ in range(6)];total=regular=0
    sets=[set()for _ in range(6)]
    for d in range(6,(N-1)//6+1,6):
        for a in range(N-6*d):
            total+=1;pts=tuple(a+j*d for j in range(7))
            if any(data[n]is None for n in pts):continue
            regular+=1;s=a%6;ks=tuple(4*data[n][0]+2*data[n][1]+data[n][2] for n in pts)
            mask=sum(1<<k for k in set(ks));sets[s].add(mask)
            candidates=tuple(t for t in range(256)if t&mask in (0,mask))
            for t in candidates:
                rec=[a+6*d,a,d]
                if witnesses[s][t]is None or rec<witnesses[s][t]:witnesses[s][t]=rec
    permitted=tables()
    for s in range(6):require([t for t in range(256)if witnesses[s][t]is None]==sorted(permitted),'whole exact projection row domain')
    cutoffs=[max(w[0]+1 for w in row if w is not None)for row in witnesses]
    unique=sorted({(w[1],w[2])for row in witnesses for w in row if w is not None})
    return dict(N=N,phase_ap_count=total,root_free_count=regular,phase_cutoffs=cutoffs,projection_bytes=sorted(permitted),whole_witnesses=witnesses,unique_witness_count=len(unique),largest_witness_step=max(d for a,d in unique),pattern_sets=[sorted(s)for s in sets])
if __name__=='__main__':
    x=run(int(sys.argv[1]));print(json.dumps(x,sort_keys=True,separators=(',',':')))
