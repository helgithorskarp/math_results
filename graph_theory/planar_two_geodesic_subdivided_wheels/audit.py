"""No-import named unit-graph check of the new cross-edge switch."""
import json


def model():
    t=4;scale=3;totals=[1,4,4,1];g={};chains={}
    A=[v for j in range(t) for v in (f'a{j}',f'b{j}')]
    C=[f'c{j}' for j in range(t)]
    def chain(u,v,n):
        p=(u,)+tuple(f'{u}|{v}|{h}' for h in range(1,n))+(v,)
        chains[u,v]=p;chains[v,u]=tuple(reversed(p))
        for a,b in zip(p,p[1:]):g.setdefault(a,set()).add(b);g.setdefault(b,set()).add(a)
    for i,a in enumerate(A):chain('r',a,scale);chain(a,A[(i+1)%len(A)],scale)
    for j,c in enumerate(C):
        for a in A[2*j:2*j+2]:chain(a,c,scale)
        chain(c,C[(j+1)%t],totals[j])
    def lift(path):
        answer=(path[0],)
        for u,v in zip(path,path[1:]):answer+=chains[u,v][1:]
        return answer
    d={}
    for s in g:
        ds={s:0};q=[s]
        for a in q:
            for b in g[a]:
                if b not in ds:ds[b]=ds[a]+1;q.append(b)
        d[s]=ds
    def components(removed):
        left=set(g)-set(removed);answer=[]
        while left:
            s=min(left);left.remove(s);part={s};q=[s]
            for a in q:
                for b in g[a]:
                    if b in left:left.remove(b);part.add(b);q.append(b)
            answer.append(part)
        return answer
    return g,chains,lift,d,components


def main():
    g,chains,lift,d,components=model();assert len(g)==67 and sum(map(len,g.values()))//2==82
    result={'vertices':len(g),'edges':82,'controls':[]}
    for side,I,J,target,complement,remote in [
        ('previous',('c0','c1','c2'),('c0','c1','b1','a2'),'a2','b2','c3'),
        ('next',('c0','c3','c2'),('c0','c3','a3','b2'),'b2','a2','c1'),
    ]:
        cross=chains[target,'c2'];theta=3+d['c0']['c2']-d['c0'][target];assert theta==1
        p=max(h for h in range(len(cross)) if 2*h<=theta);q=min(h for h in range(len(cross)) if 2*h>=theta)
        assert p==0 and q==1
        old_carrier=[lift(J),lift(('a0','r',complement))]
        old_inner=[lift(('a0',)+I),lift(('r',complement))]
        new_carrier=[lift(J)+cross[1:p+1],lift(('a0','r',complement))]
        new_inner=[lift(I)+tuple(reversed(cross[q:]))[1:],lift(('a0','r',complement))]
        mass={cross[1]:4,chains['a2','b2'][1]:4,remote:3}
        def residual(pair):
            removed=set().union(*map(set,pair));assert {'r','a0','c0'}<=removed
            for path in pair:
                assert len(set(path))==len(path) and all(v in g[u] for u,v in zip(path,path[1:]))
                assert len(path)-1==d[path[0]][path[-1]]
            return max(sum(mass.get(v,0) for v in part) for part in components(removed))
        values=[residual(pair) for pair in [old_carrier,old_inner,new_carrier,new_inner]]
        assert sum(mass.values())==11 and values==[7,8,7,4]
        atom_max=max(sum(mass.get(v,0) for v in T[1:-1]) for (u,v),T in chains.items() if not(u.startswith('c') and v.startswith('c')))
        assert atom_max==4
        result['controls'].append({'side':side,'W':11,'B':4,'theta':theta,'old_residuals':values[:2],'new_residuals':values[2:]})
    result['status']='PASS';return result


if __name__=='__main__':print(json.dumps(main(),indent=2))
