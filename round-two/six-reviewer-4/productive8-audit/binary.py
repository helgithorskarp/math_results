"""Every inactive/half/quarter pattern, plus complete allocations T<=7."""
import argparse,itertools,json
from base import need,digest

def generate():
    rows=[];inventories={}
    for parent,counts in ((2,(1,2,3)),(6,(2,3,4)),(1,(2,))):
        placed=5 if parent==2 else 1 if parent==6 else 0
        for extra in counts:
            for h in range(extra+1):
                q=extra-h;covered=0
                for H in itertools.product((-1,0,1),repeat=h):
                    for Q in itertools.product((-1,0,1,2,3),repeat=q):
                        word=placed;without=0
                        for x in H:
                            v=0 if x<0 else 5 if x==0 else 10;word|=v;without|=v
                        for x in Q:
                            v=0 if x<0 else 1<<x;word|=v;without|=v
                        full=word==15;activeH=sum(x>=0 for x in H);activeQ=sum(x>=0 for x in Q)
                        if full:
                            if parent==2:need(activeH>0 or activeQ>=2,'necessary half-or-two-quarter footprint')
                            elif parent==6:
                                need(activeH>0 or activeQ>=3,'necessary half-or-three-quarter footprint')
                                if q==0:need(without==15,'all-H extras imply placed32 redundancy')
                                if extra==2:need((h,q)==(1,1) or without==15,'minimum parent6 inventory')
                            else:need(h==2 and set(H)=={0,1},'third parent two-class repair')
                        rows.append([parent,extra,h,list(H),list(Q),word,without,full]);covered+=full
                inventories[f'{parent},{extra},{h}']=covered
    allocations=[]
    for T in (5,6,7):
        for a in range(2,T-2):
            b=T-a
            for h2 in range(a):
                q2=a-1-h2
                for h6 in range(b):
                    q6=b-1-h6
                    if not inventories.get(f'2,{a-1},{h2}',0)or not inventories.get(f'6,{b-1},{h6}',0)or q6==0:continue
                    H=h2+h6;need(H<=4,'globally at most four extra half labels')
                    S=[0,90,120,150,175][H];oddQ2=30 if q2==2 else 54 if q2==3 else 0;oddQ6=18 if q6==3 else 72 if q6==4 else 0
                    allocations.append([T,a,b,h2,q2,h6,q6,S+oddQ2+oddQ6,(170 if H==4 else S)+oddQ2+oddQ6])
    return dict(whole_local_controls=rows,local_control_count=len(rows),main_control_count=sum(r[0]!=1 for r in rows),third_control_count=sum(r[0]==1 for r in rows),inventory_covering_patterns=inventories,two_parent_allocations=allocations,complete_T5_max=max(r[-1]for r in allocations if r[0]==5),complete_T6_max=max(r[-1]for r in allocations if r[0]==6),complete_T7_max=max(r[-1]for r in allocations if r[0]==7),three_parent_T7_maxima=[[r,120+(25 if r==4 else 28)]for r in (1,3,4,5,7)])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();data=generate();open(a.output,'w').write(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in data.items()if k not in ('whole_local_controls','inventory_covering_patterns','two_parent_allocations')}|dict(record_sha256=digest(data),allocation_rows=len(data['two_parent_allocations'])),sort_keys=True))
if __name__=='__main__':main()
