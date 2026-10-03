"""Whole affine basis and a fresh four-AP kernel; independent direct squares."""
import argparse, hashlib, json
from field import candidates, gauss, label as normalized_label
Q=103
SQUARES={x*x%Q for x in range(1,Q)}
def require(test,reason):
    if not test: raise ValueError(reason)
def char(x):
    x%=Q;require(x!=0,'original root');return int(x not in SQUARES)
def label(x,p,u):
    return sum(b*char(x-p-u*r) for b,r in ((4,1),(2,2),(1,4)))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lo',type=int,required=True);ap.add_argument('--hi',type=int,required=True);args=ap.parse_args()
    require(0<=args.lo<args.hi<=Q,'pole partition')
    require(all(gauss(x)==char(x) for x in range(1,Q)),'whole independent field equality')
    counts=[sum(normalized_label(x)==k for x in range(Q) if x not in {0,1,2,4}) for k in range(8)]
    require(counts==[11,14,14,11,14,11,11,13],'label multiplicities')
    records=candidates();kernel=[]
    for pattern in ({1,2},{1,4},{1,5},{2,4,5}):
        choices=[(a,d) for a,d,points,labels in records if labels==pattern]
        require(bool(choices),'missing kernel pattern');kernel.append(min(choices,key=lambda x:(x[1],x[0])))
    require(all(any(len({(w>>normalized_label((a+j*d)%Q))&1 for j in range(7)})==1 for a,d in kernel) for w in range(256)),'whole256 kernel obstruction')
    digest=hashlib.sha256();entries=0;aps=0;points=0
    for p in range(args.lo,args.hi):
        for u in range(1,Q):
            mapping=[(p+u*x)%Q for x in range(Q)]
            require(set(mapping)==set(range(Q)),'whole affine bijection')
            free={p,(p+u)%Q,(p+2*u)%Q,(p+4*u)%Q}
            require({mapping[x] for x in (0,1,2,4)}==free and len(free)==4,'original free columns')
            for x in range(Q):
                if x in {0,1,2,4}:continue
                expected=normalized_label(x)^(7*char(u))
                actual=label(mapping[x],p,u);require(actual==expected,'original character tuple transport')
                digest.update(bytes((p,u,x,actual)));entries+=3
            for a,d in kernel:
                A,D=mapping[a],u*d%Q;delta=next(k for k in range(1,Q) if 6*k%Q==D)
                if delta>51:A=(A+6*D)%Q;delta=Q-delta;D=Q-D
                n=next(n for n in range(1,1+6*Q,6) if n%Q==A)
                seq=[n+6*delta*j for j in range(7)]
                require(seq[-1]<=2449 and min(seq)>0,'native2449 endpoint')
                require(len({v%618 for v in seq})==7,'actual cyclic distinctness')
                require(all(seq[j]%Q==(A+j*D)%Q and seq[j]%Q not in free for j in range(7)),'original CRT lift/free columns')
                original={label(v%Q,p,u) for v in seq}
                normalized={normalized_label((a+j*d)%Q)^(7*char(u)) for j in range(7)}
                require(original==normalized,'actual kernel labels');aps+=1;points+=7
    print(json.dumps({'lo':args.lo,'hi':args.hi,'configurations':(args.hi-args.lo)*102,'character_entries':entries,'kernel_aps':aps,'kernel_points':points,'basis_sha256':digest.hexdigest(),'kernel':kernel,'label_counts':counts,'complete256tables':True},sort_keys=True))
if __name__=='__main__':main()
