"""Original integer AP realization of every local binary row; independent cases."""
import argparse,itertools,json
from base_check import need,digest

def check(data,odd):
    expected=[];inventories={}
    for parent,counts in ((2,(1,2,3)),(6,(2,3,4)),(1,(2,))):
        n=parent if parent!=1 else 17;placed=[(16,2)] if parent==2 else [(32,6)] if parent==6 else []
        for extra in counts:
            for h in range(extra+1):
                q=extra-h;covered=0
                for H in itertools.product((-1,0,1),repeat=h):
                    for Q in itertools.product((-1,0,1,2,3),repeat=q):
                        classes=[]
                        for scale,states in ((16,H),(32,Q)):
                            for d,state in zip((3,5,7,9),states):
                                m=scale*d;a=(n+8 if state<0 else n+2520*state)%m;need(a%8==parent,'actual original parent');classes.append((m,a))
                        need(len({m for m,a in classes+placed})==extra+len(placed),'globally original labels inside local realization')
                        word=0;without=0
                        for ell in range(4):
                            point=n+2520*ell
                            if any(point%m==a for m,a in classes+placed):word|=1<<ell
                            if any(point%m==a for m,a in classes):without|=1<<ell
                        expected.append([parent,extra,h,list(H),list(Q),word,without,word==15]);covered+=word==15
                inventories[f'{parent},{extra},{h}']=covered
    need(data['whole_local_controls']==expected,'EVERY physical original four-lift control')
    need(data['inventory_covering_patterns']==inventories,'whole inventory cover census')
    need((data['local_control_count'],data['main_control_count'],data['third_control_count'])==(2140,2091,49),'complete local Cartesian domains')
    C=dict(odd['capacities']);extra=odd['divisors'][1:];S={h:max(sum(C[d]for d in v)for v in itertools.combinations(extra,h))for h in range(5)}
    I2=max(r[-1]for r in odd['pairs']);I3=max(r[-2]for r in odd['triples']);Q3=max(r[-1]for r in odd['triples']);alloc=[]
    for T in range(5,8):
        splits=[(a,T-a)for a in range(2,T)if T-a>=3]
        for a,b in splits:
            for h2 in range(a):
                q2=a-1-h2
                for h6 in range(b):
                    q6=b-1-h6
                    if not inventories.get(f'2,{a-1},{h2}',0)or not inventories.get(f'6,{b-1},{h6}',0)or q6==0:continue
                    H=h2+h6;tail2=I2 if q2==2 else Q3 if q2==3 else 0;tail6=I3 if q6==3 else 4*I3 if q6==4 else 0
                    alloc.append([T,a,b,h2,q2,h6,q6,S[H]+tail2+tail6,(odd['two_parent_four_H_bound']if H==4 else S[H])+tail2+tail6])
    need(data['two_parent_allocations']==alloc,'complete physical binary inventory/allocation rows')
    for T in (5,6,7):need(data[f'complete_T{T}_max']==max(r[-1]for r in alloc if r[0]==T),'whole tail-count maximum')
    need(data['three_parent_T7_maxima']==[[r,120+max(max(v[-1])for v in odd['third_parent_phase_counts']if v[0]==r)]for r in (1,3,4,5,7)],'literal third-parent allocation maxima')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--odd',required=True);a=ap.parse_args();data=json.load(open(a.input));check(data,json.load(open(a.odd)));print(json.dumps(dict(all_physical_rows_equal=True,record_sha256=digest(data),all_original_local_controls=2140,complete_T5_max=data['complete_T5_max'],complete_T6_max=data['complete_T6_max'],complete_T7_max=data['complete_T7_max']),sort_keys=True))
if __name__=='__main__':main()
