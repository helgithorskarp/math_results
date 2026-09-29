"""Exact finite controls for fully unit-subdivided necklace cores."""
import argparse
from collections import Counter
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('single',ROOT/'planar_two_geodesic_anchor_mixed_annuli/verify.py')
single=importlib.util.module_from_spec(spec);spec.loader.exec_module(single)
metric,fan,require=single.metric,single.fan,single.require


class Lift:
    def __init__(self,g):
        self.adj=[set() for _ in g.adj];self.chain={};self.atoms=[]
        for u in range(len(g.adj)):
            for v,w in g.adj[u].items():
                if u>=v:continue
                assert int(w)==w and w>=1
                interior=tuple(range(len(self.adj),len(self.adj)+int(w)-1))
                self.adj.extend(set() for _ in interior)
                chain=(u,)+interior+(v,);self.chain[u,v]=chain;self.chain[v,u]=tuple(reversed(chain))
                if interior:self.atoms.append(set(interior))
                for a,b in zip(chain,chain[1:]):self.adj[a].add(b);self.adj[b].add(a)
        self.dist=[]
        for s in range(len(self.adj)):
            d=[None]*len(self.adj);d[s]=0;q=[s]
            for a in q:
                for b in self.adj[a]:
                    if d[b] is None:d[b]=d[a]+1;q.append(b)
            self.dist.append(d)
    def lift(self,path):
        ans=[path[0]]
        for u,v in zip(path,path[1:]):
            if v in self.adj[u]:ans.append(v)
            else:ans.extend(self.chain[u,v][1:])
        return tuple(ans)
    def check_path(self,path):
        assert len(path)==len(set(path)) and all(v in self.adj[u] for u,v in zip(path,path[1:]))
        assert len(path)-1==self.dist[path[0]][path[-1]],('nongeodesic',path,len(path)-1,self.dist[path[0]][path[-1]])
    def components(self,removed):
        left=set(range(len(self.adj)))-set(removed);out=[]
        while left:
            s=min(left);left.remove(s);part={s};q=[s]
            for a in q:
                for b in self.adj[a]:
                    if b in left:left.remove(b);part.add(b);q.append(b)
            out.append(part)
        return out


def core_graph(m,scale,lengths):
    g,A,C,arcs=single.mixed.core_graph('AD'*m,list(map(len,lengths)),scale)
    for arc,prices in zip(arcs,lengths):
        require(prices and all(x>0 for x in prices) ,'positive arc')
        for u,v,price in zip(arc,arc[1:],prices):g.adj[u][v]=g.adj[v][u]=price
    g.sphere()
    return g,A,C,arcs


def system(g,A0,C0,arcs0,core,dist,scale,result,shift=0,reverse=False):
    U=Lift(g);atoms=U.atoms
    k,m=len(A0),len(C0);require(k==2*m and m>=3,'necklace size')
    if reverse:
        A=[A0[(2*shift+1-i)%k] for i in range(k)]
        C=[C0[(shift-j)%m] for j in range(m)]
        arcs=[tuple(reversed(arcs0[(shift-j-1)%m])) for j in range(m)]
    else:
        A=A0[2*shift:]+A0[:2*shift];C=C0[shift:]+C0[:shift]
        arcs=arcs0[shift:]+arcs0[:shift]
    lengths=[sum(g.adj[u][v] for u,v in zip(arc,arc[1:])) for arc in arcs]
    require(all(x>0 for x in lengths) and lengths[-1]<=scale,'positive arcs and short preceding arc')
    positions=[F(0)]
    for ell in lengths:positions.append(positions[-1]+ell)
    total=positions[-1];delta=[min(x,total-x) for x in positions[:-1]]
    for j in range(m):
        require(dist[C[0]][A[2*j]]==scale+min(delta[j],scale+delta[(j-1)%m],2*scale),'left parent profile')
        require(dist[C[0]][A[2*j+1]]==scale+min(delta[j],scale+delta[(j+1)%m],2*scale),'right parent profile')
        require(dist[A[0]][C[j]]==scale+min(delta[j],2*scale),'anchor parent profile')
    result['distance_profiles']+=1
    def inner(j):
        if positions[j]<=total/2:
            return (C[0],)+tuple(v for arc in arcs[:j] for v in arc[1:])
        return (C[0],)+tuple(v for arc in reversed(arcs[j:]) for v in tuple(reversed(arc))[1:])
    r=0;P=(r,A[0],C[0]);alpha=[set()]+[{a}|set(U.chain[0,a][1:-1]) for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    beta=[set()]+[set(U.chain[a,C[i//2]][1:-1]) for i,a in enumerate(A) if i]
    tau=[set(T[1:-1]) for T in arcs];kappa=[set(U.chain[a,A[(i+1)%k]][1:-1]) for i,a in enumerate(A)];discarded=set(U.chain[0,A[0]][1:-1])|set(U.chain[A[0],C[0]][1:-1]);outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{r} and len(Y)<=2,'root-clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'consecutive boundary');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y)))]|=K
        else:discarded|=K
    represented=set(range(len(U.adj)))-set(P)-discarded
    outside=atoms
    require(set().union(*(alpha+gamma+tau+kappa+beta))==represented,'mass partition union')
    require(sum(map(len,alpha+gamma+tau+kappa+beta))==len(represented),'mass partition disjoint')
    def bounds(i,j):
        L=set().union(*(alpha[h]|kappa[h]|beta[h] for h in range(i)),*(gamma[h]|tau[h] for h in range(j)))
        return L,represented-L-alpha[i%k]-gamma[j%m]-beta[i%k]
    cuts=[]
    def pair(paths,sides,flavor):
        paths=[U.lift(path) for path in paths]
        for path in paths:U.check_path(path)
        removed=set().union(*map(set,paths));require(set(P)<=removed,('anchor',flavor,paths))
        parts=U.components(removed)
        for K in parts:
            require(any(K<=side for side in sides) or any(K<=atom for atom in atoms),('component',flavor,K,sides,paths))
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut)
        result[flavor+'_pairs']+=1;return cut
    def carrier(j,side):
        a=A[2*j+side];neighbor=(j+(-1 if side==0 else 1))%m
        options=[inner(j)+(a,), (C[0],A[0],r,a)]
        parent=A[(2*j-1)%k] if side==0 else A[(2*j+2)%k]
        options.append(inner(neighbor)+(parent,a))
        for path in options:
            if len(set(path))==len(path) and all(v in g.adj[u] for u,v in zip(path,path[1:])):
                if sum(g.adj[u][v] for u,v in zip(path,path[1:]))==dist[path[0]][path[-1]]:return path
        raise AssertionError(('no carrier',j,side))
    for j,c in enumerate(C):
        require(dist[r][c]==2*scale,'root distance')
        s=min(lengths[j],total-lengths[j],scale)
        require(dist[A[2*j+1]][C[(j+1)%m]]==scale+s,'opposite parent distance')
    sequence=[pair([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in 'AD'*m:
        ni=i+1;nj=j+int(letter=='D');L,Rold=bounds(i,j);Lnew,R=bounds(ni,nj)
        a,b=A[i%k],A[ni%k];heavy=None
        if letter=='A':
            if j==0:
                paths=[(r,A[0]),(C[0],A[1])];flavor='A_anchor'
            elif delta[j]>=2*scale:
                paths=[(A[0],r,a,C[j]),carrier(j,1)];flavor='A_root'
            elif dist[C[0]][b]==scale+delta[j]:
                paths=[inner(j)+(b,),(A[0],r,a)];flavor='A_right'
            elif dist[C[0]][a]==scale+delta[j]:
                paths=[inner(j)+(a,),(A[0],r,b)];flavor='A_left'
            else:
                walk=inner(j)
                if positions[j]<=total/2:
                    previous=(j-1)%m;T=arcs[previous]
                    require(walk[-len(T):]==T,'previous inner arrival')
                    cross=U.chain[a,C[j]];theta=scale+delta[j]-dist[C[0]][a]
                    p=max(h for h in range(len(cross)) if 2*h<=theta);q=min(h for h in range(len(cross)) if 2*h>=theta)
                    H1=R|gamma[j]|tau[previous]|beta[ni%k]|set(cross[p+1:-1]);H2=(L-tau[previous])|alpha[i%k]|kappa[i%k]|set(cross[1:q])
                    first=pair([inner(previous)+(A[(i-1)%k],a)+cross[1:p+1],(A[0],r,b)],[L,H1],'A_previous_carrier')
                    second=pair([walk+tuple(reversed(cross[q:]))[1:],(A[0],r,b)],[H2,R],'A_previous_inner')
                else:
                    after=(j+1)%m;T=tuple(reversed(arcs[j]))
                    require(walk[-len(T):]==T,'next inner arrival')
                    cross=U.chain[b,C[j]];theta=scale+delta[j]-dist[C[0]][b]
                    p=max(h for h in range(len(cross)) if 2*h<=theta);q=min(h for h in range(len(cross)) if 2*h>=theta)
                    H1=L|gamma[j]|tau[j]|beta[i%k]|set(cross[p+1:-1]);H2=(R-tau[j])|alpha[ni%k]|kappa[i%k]|set(cross[1:q])
                    first=pair([inner(after)+(A[(ni+1)%k],b)+cross[1:p+1],(A[0],r,a)],[H1,R],'A_next_carrier')
                    second=pair([walk+tuple(reversed(cross[q:]))[1:],(A[0],r,a)],[L,H2],'A_next_inner')
                choices=[first,second];heavy=H1,H2
        else:
            arc=arcs[j];ell=lengths[j];x,y=delta[j],delta[nj%m]
            coordinates=[F(0)]
            for u,v in zip(arc,arc[1:]):coordinates.append(coordinates[-1]+g.adj[u][v])
            if min(x,y)>=2*scale:
                radius=min(scale,ell,total-ell)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=ell-radius)
                p=max(h for h,z in enumerate(coordinates) if 2*z<=ell+radius)
                H1=L|gamma[j]|beta[i%k]|set(arc[1:q]);H2=R|gamma[nj%m]|beta[ni%k]|set(arc[p+1:-1])
                first=pair([(C[0],A[0],r,a),(b,)+tuple(reversed(arc[q:]))],[H1,R],'D_far_suffix')
                second=pair([(C[0],A[0],r,b),(a,)+arc[:p+1]],[L,H2],'D_far_prefix')
            elif x<=y:
                theta=ell+min(y,2*scale)-x
                p=max(h for h,z in enumerate(coordinates) if 2*z<=theta)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=ell)
                H1=R|gamma[nj%m]|tau[j]|beta[ni%k];H2=L|alpha[i%k]|kappa[i%k]|beta[i%k]
                first=pair([inner(j)+(a,),(A[0],r,b)],[L,H1],'D_near_left_carrier')
                second=pair([(A[0],)+inner(j)+arc[1:p+1],(r,b)+tuple(reversed(arc[q:]))],[H2,R],'D_near_left_split')
            else:
                theta=ell+y-min(x,2*scale)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=theta)
                p=max(h for h,z in enumerate(coordinates) if 2*z<=ell)
                H1=L|gamma[j]|tau[j]|beta[i%k];H2=R|alpha[ni%k]|kappa[i%k]|beta[ni%k]
                complement=(r,a) if j==m-1 else (A[0],r,a)
                first=pair([inner(nj%m)+(b,),complement],[H1,R],'D_near_right_carrier')
                second=pair([(A[0],)+inner(nj%m)+tuple(reversed(arc[q:]))[1:],(r,a)+arc[:p+1]],[L,H2],'D_near_right_split')
            require(q<=p+1,'ordered D cuts');choices=[first,second];heavy=H1,H2
        if heavy is None:choices=[pair(paths,[L,R],flavor)]
        else:
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint critical supports')
            result[letter+'_disjoint_checks']+=1
        transitions.append(choices);i,j=ni,nj
        sequence.append(pair([P,(r,A[i%k],C[j%m])],[Lnew,R],'spoke'))
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,sequence=sequence,
                transitions=transitions,cuts=cuts,sectors=kappa,arcs=arcs,outer=A,branches=C,lifted=U,beta=beta)

def system_long(g,A0,C0,arcs0,core,dist,scale,result,shift=0,reverse=False):
    U=Lift(g);atoms=U.atoms
    k,m=len(A0),len(C0)
    require(k==2*m and m>=4,'necklace size')
    if reverse:
        A=[A0[(2*shift+1-i)%k] for i in range(k)]
        C=[C0[(shift-j)%m] for j in range(m)]
        arcs=[tuple(reversed(arcs0[(shift-j-1)%m])) for j in range(m)]
    else:
        A=A0[2*shift:]+A0[:2*shift];C=C0[shift:]+C0[:shift]
        arcs=arcs0[shift:]+arcs0[:shift]
    coords=[]
    for arc in arcs:
        x=[F(0)]
        for u,v in zip(arc,arc[1:]):x.append(x[-1]+g.adj[u][v])
        require(x[-1]>=scale,'arc lower bound');coords.append(x)
    ell0,elllast=coords[0][-1],coords[-1][-1]
    r=0;P=(r,A[0],C[0])
    alpha=[set()]+[{a}|set(U.chain[0,a][1:-1]) for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    beta=[set()]+[set(U.chain[a,C[i//2]][1:-1]) for i,a in enumerate(A) if i]
    tau=[set(T[1:-1]) for T in arcs];kappa=[set(U.chain[a,A[(i+1)%k]][1:-1]) for i,a in enumerate(A)]
    discarded=set(U.chain[0,A[0]][1:-1])|set(U.chain[A[0],C[0]][1:-1]);outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{r} and len(Y)<=2,'root-clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'consecutive attachment');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y)))]|=K
        else:discarded|=K
    represented=set(range(len(U.adj)))-set(P)-discarded
    outside=atoms
    require(set().union(*(alpha+gamma+tau+kappa+beta))==represented,'mass partition union')
    require(sum(map(len,alpha+gamma+tau+kappa+beta))==len(represented),'mass partition disjoint')
    def bounds(i,j):
        L=set().union(*(alpha[s]|kappa[s]|beta[s] for s in range(i)),*(gamma[t]|tau[t] for t in range(j)))
        return L,represented-L-alpha[i%k]-gamma[j%m]-beta[i%k]
    cuts=[]
    def pair(paths,sides,flavor):
        paths=[U.lift(path) for path in paths]
        for path in paths:U.check_path(path)
        removed=set().union(*map(set,paths));require(set(P)<=removed,('prescribed triple',flavor,paths))
        parts=U.components(removed)
        for K in parts:
            require(any(K<=side for side in sides) or any(K<=atom for atom in atoms),('component',flavor,K,sides,paths))
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut)
        result[flavor+'_pairs']+=1;return cut
    carriers=[]
    for i,a in enumerate(A):
        if i==0:E=(C[0],A[0]);want=scale
        elif i==1:E=(C[0],A[1]);want=scale
        elif i==2:E=(C[0],A[1],a);want=2*scale
        elif i==k-1:E=(C[0],A[0],a);want=2*scale
        elif i==3 and ell0<2*scale:E=arcs[0]+(a,);want=scale+ell0
        elif i==k-2 and elllast<2*scale:E=tuple(reversed(arcs[-1]))+(a,);want=scale+elllast
        else:E=(C[0],A[0],r,a);want=3*scale
        require(dist[C[0]][a]==want,'anchor distance profile');g.check_path(E,dist);carriers.append(E)
        result['carrier_checks']+=1
    require(dist[A[0]][C[1]]==min(3*scale,scale+ell0),'first branch distance')
    require(dist[A[0]][C[-1]]==2*scale,'last branch distance')
    require(dist[A[1]][C[-1]]==min(3*scale,scale+elllast),'reflected branch distance')
    for c in C[2:-1]:require(dist[A[0]][c]==3*scale,'far branch distance')
    sequence=[pair([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in 'AD'*m:
        ni=i+1;nj=j+int(letter=='D');L,Rold=bounds(i,j);Lnew,R=bounds(ni,nj)
        a,b=A[i%k],A[ni%k]
        if letter=='A':
            heavy=None
            if j==0:
                paths=[(r,A[0]),(C[0],A[1])];flavor='A_anchor'
            elif j==1 and ell0<2*scale:
                paths=[carriers[3],(A[0],r,A[2])];flavor='A_first_short'
            elif j==m-1:
                paths=[carriers[-1],(r,A[-2],C[-1])];flavor='A_last'
            else:
                require(r in carriers[2*j+1],'reflected A carrier contains root')
                paths=[carriers[2*j+1],(A[2*j],C[j])]
                flavor='A_first_long' if j==1 else 'A_ordinary'
            choices=[pair(paths,[L,R],flavor)]
        else:
            arc=arcs[j];x=coords[j];ell=x[-1]
            if j==0:
                p=max(z for z,t in enumerate(x) if 2*t<=ell+min(2*scale,ell))
                q=min(z for z,t in enumerate(x) if 2*t>=ell+scale)
                H1=Rold-set(arc[1:p+1]);H2=set(arc[1:q])
                first=pair([(A[0],)+arc[:p+1],(r,A[1])],[L,H1],'D_anchor_prefix')
                second=pair([P,(A[1],A[2])+tuple(reversed(arc[q:]))],[L,H2,R],'D_anchor_suffix')
                choices=[first,second];heavy=H1,H2
            else:
                Ea,Eb=carriers[i%k],carriers[ni%k]
                if j==1 and ell0<2*scale:
                    threshold=ell+2*scale-ell0;start=(A[0],r,b);forward='D_first_short'
                else:
                    threshold=ell-(scale if r in Ea else 0)
                    start=(b,) if r in Ea else (r,b);forward='D_forward'
                q=min(z for z,t in enumerate(x) if 2*t>=threshold)
                suffix=start+tuple(reversed(arc[q:]))
                if j==m-2 and elllast<2*scale:
                    threshold2=ell-scale;start2=(A[0],r,a);backward='D_last_short'
                else:
                    threshold2=ell+(scale if r in Eb else 0)
                    start2=(a,) if r in Eb else (r,a);backward='D_backward'
                p=max(z for z,t in enumerate(x) if 2*t<=threshold2)
                prefix=start2+arc[:p+1]
                H1=L|gamma[j]|beta[i%k]|set(arc[1:q]);H2=R|gamma[nj%m]|beta[ni%k]|set(arc[p+1:-1])
                first=pair([Ea,suffix],[H1,R],forward);second=pair([Eb,prefix],[L,H2],backward)
                choices=[first,second];heavy=H1,H2
                require(threshold<=threshold2,'ordered D thresholds')
            require(q<=p+1,'D coordinate overlap')
        if heavy is not None:
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint potentially heavy supports')
            result['disjoint_checks']+=1
        transitions.append(choices);i,j=ni,nj
        sequence.append(pair([P,(r,A[i%k],C[j%m])],[Lnew,R],'spoke'))
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,sequence=sequence,transitions=transitions,cuts=cuts,
                outer=A,branches=C,arcs=arcs,coords=coords,sectors=kappa,lifted=U,beta=beta)


def main():
    rng=random.Random(2026092929);result=Counter()
    fixtures=[(3,[1,4,4,1]),(4,[2,5,5,1]),(4,[1,5,5,2]),
              (3,[3,4,8,3]),(2,[2,3,6,3,5]),(1,[1,2,3,4]),
              (4,[1,6,6,1]),(4,[2,6,6,1])]
    for trial in range(40):
        m=4+trial%4;scale=2+trial%3
        if trial%2:totals=[rng.randrange(scale,4*scale+1) for _ in range(m)]
        else:
            totals=[rng.randrange(1,3*scale+1) for _ in range(m)];totals[-1]=rng.randrange(1,scale+1)
        fixtures.append((scale,totals))
    for scale,totals in fixtures:
        m=len(totals);g,A,C,arcs=core_graph(m,scale,[[1]*ell for ell in totals]);core=set(range(len(g.adj)));dist=g.distances()
        for shift in range(m):
            for reverse in [False,True]:
                if all(ell>=scale for ell in totals):
                    sys1=system_long(g,A,C,arcs,core,dist,scale,result,shift,reverse);result['long_systems']+=1
                elif totals[shift if reverse else (shift-1)%m]<=scale:
                    sys1=system(g,A,C,arcs,core,dist,scale,result,shift,reverse);result['short_anchor_systems']+=1
                else:continue
                U=sys1['lifted'];n=len(U.adj)
                weights=[[1]*n]+[[rng.randrange(6) for _ in range(n)] for _ in range(4)]
                # Every edge atom also gets a concentrated heavy control.
                if U.atoms:
                    atom=U.atoms[(shift+int(reverse))%len(U.atoms)];mass=[0]*n
                    for v in atom:mass[v]=7
                    weights.append(mass)
                for masses in weights:
                    cut,twice_h=metric.choose(sys1,masses,result);W=sum(masses)
                    heavy=next((atom for atom in U.atoms if 2*sum(masses[v] for v in atom)>W),None)
                    if heavy:
                        chain=next(T for T in U.chain.values() if set(T[1:-1])==heavy);U.check_path(chain)
                        require(all(2*sum(masses[v] for v in part)<=W for part in U.components(chain)),'heavy edge repair')
                        result['heavy_edge_checks']+=1
                    else:
                        require(twice_h<=W,'half threshold')
                        require(all(2*sum(masses[v] for v in part)<=W for part in cut['parts']),'actual half components')
                        result['half_checks']+=1
                result['unit_vertices_checked']+=n
        result['unit_models']+=1
    for flavor in ['A_previous_carrier','A_previous_inner','A_next_carrier','A_next_inner']:
        require(result[flavor+'_pairs']>0,'cross-switch orientation '+flavor)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2))
