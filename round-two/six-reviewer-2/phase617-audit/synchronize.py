"""Exhaust all6**6 table choices by independently reconstructed actual AP boxes."""
import json,sys
from field import inputs,OPTIONS,progressions,phase_masks,decode_index,require

def run(N):
    data=inputs(N);members=phase_masks();live=(1<<(6**6))-1;initial=live
    history=[];checked=regular=0
    for a,d in progressions(N):
        checked+=1;pts=tuple(a+j*d for j in range(7))
        if any(data[n]is None for n in pts):continue
        regular+=1
        before=live
        for c in [0,1]:
            allowed=[63]*6
            for n in pts:
                good=sum(1<<i for i,(j,b)in enumerate(OPTIONS)if data[n][j]^b==c)
                allowed[n%6]&=good
            bad=initial
            for s in range(6):bad&=members[s][allowed[s]]
            live&=~bad
        if live!=before:history.append({'a':a,'d':d,'end':a+6*d,'before':before.bit_count(),'after':live.bit_count()})
    survivors=[]
    while live:
        low=live&-live;i=low.bit_length()-1;live-=low;survivors.append(list(decode_index(i)))
    return dict(N=N,all_phase_choices=6**6,all_actual_aps=checked,all_root_free_aps=regular,eliminating_progressions=history,survivors=survivors)
if __name__=='__main__':print(json.dumps(run(int(sys.argv[1])),sort_keys=True,separators=(',',':')))
