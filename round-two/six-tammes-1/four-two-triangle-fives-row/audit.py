"""Separate same-author bit/dart audit; imports no primary checker code."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

F, D, U, V, A, B, C, E, I, R, S, P = range(12)
ORD = set(range(8, 15))
ONET = {A, B, C, E}
DEG = [5, 5, 3, 3] + [4] * 11
TQ = [4, 2, 0, 0] + [1] * 4 + [2] * 7
QQ = [0, 2, 3, 3] + [2] * 4 + [1] * 7


def bit(a, b):
    if a == b:
        raise ValueError('a pair mask has two distinct originals')
    a, b = min(a, b), max(a, b)
    return 1 << (b * (b - 1) // 2 + a)


def vertices(mask):
    while mask:
        v = (mask & -mask).bit_length() - 1
        yield v
        mask &= mask - 1


def boundary(f):
    candidates = []
    for word in (tuple(f), tuple(reversed(f))):
        candidates.extend(word[k:] + word[:k] for k in range(len(word)))
    return min(candidates)


class Reject(Exception):
    pass


class DartAudit:
    def __init__(self, faces=(), extra=(), *, fd_contact=False, missing_capacity=True):
        self.cells = frozenset(boundary(f) for f in faces)
        self.bars = tuple(extra)
        self.fd_contact = fd_contact
        self.missing_capacity = missing_capacity

    def plus(self, *fs):
        return DartAudit(self.cells | {boundary(f) for f in fs}, self.bars, fd_contact=self.fd_contact, missing_capacity=self.missing_capacity)

    def inspect(self, pair_faces=True):
        cells = set(self.cells)
        e = 0
        no = 0 if self.fd_contact else bit(F, D)
        for a, b in self.bars:
            if a == b:
                raise Reject()
            e |= bit(a, b)
        for f in cells:
            if len(f) not in (3, 4) or len(set(f)) != len(f):
                raise Reject()
            for a, b in zip(f, f[1:] + f[:1]):
                e |= bit(a, b)
            if len(f) == 4:
                no |= bit(f[0], f[2]) | bit(f[1], f[3])
        if e & no:
            raise Reject()
        nbr = [0] * 15
        for b in range(15):
            for a in range(b):
                if e & bit(a, b):
                    nbr[a] |= 1 << b
                    nbr[b] |= 1 << a
        if any(nbr[v].bit_count() > DEG[v] for v in range(15)):
            raise Reject()
        if nbr[U] & (1 << V) or any(nbr[v] & sum(1 << x for x in ORD) for v in (U, V)):
            raise Reject()
        # Find triangles by common-neighbor masks, rather than scanning triples.
        for a in range(15):
            for b in vertices(nbr[a] & ~((1 << (a + 1)) - 1)):
                for c in vertices(nbr[a] & nbr[b] & ~((1 << (b + 1)) - 1)):
                    cells.add((a, b, c))
        t = [0] * 15
        qcounts = [0] * 15
        for f in cells:
            if len(f) == 4:
                for v in f: qcounts[v] += 1
        if any(qcounts[v] > DEG[v]-TQ[v] for v in range(15)): raise Reject()
        for v in range(15):
            if nbr[v].bit_count() == DEG[v]:
                for w in range(15):
                    if w != v and not nbr[v] & (1 << w): no |= bit(v,w)
        darts = {}
        corners = [dict() for _ in range(15)]
        for f in sorted(cells):
            if len(f) == 3:
                for v in f:
                    t[v] += 1
            for ix, v in enumerate(f):
                a, b = f[ix - 1], f[(ix + 1) % len(f)]
                corner = bit(a, b)
                if corner in corners[v] and corners[v][corner] != f:
                    raise Reject()
                corners[v][corner] = f
                ed = tuple(sorted((v, b)))
                darts.setdefault(ed, []).append(f)
                if len(f) == 4 and v in (F, D):
                    o = f[(ix + 2) % 4]
                    if o not in (A, B, C, E):
                        raise Reject()
                    if v == D and (nbr[D] & ((1 << U) | (1 << V))).bit_count() == 2 and not (nbr[D] & ((1 << U) | (1 << V)) & ((1 << a) | (1 << b))):
                        raise Reject()
        if any(t[v] > TQ[v] for v in range(15)) or any(len(fs) > 2 for fs in darts.values()):
            raise Reject()
        if any((nbr[a] & nbr[b]).bit_count() > 2 for a in range(15) for b in range(a)):
            raise Reject()
        qends = [0] * 15
        for a in range(15):
            for b in vertices(nbr[a] & ~((1 << (a + 1)) - 1)):
                fs = darts.get((a, b), [])
                if TQ[a] == 0 or TQ[b] == 0 or len(fs) == 2 and all(len(f) == 4 for f in fs):
                    qends[a] += 1
                    qends[b] += 1
        if any(qends[v] > QQ[v] for v in range(15)):
            raise Reject()
        rotations = {}
        for v in range(15):
            link = [0] * 15
            cmask = 0
            for corner, f in corners[v].items():
                ix = f.index(v)
                a, b = f[ix - 1], f[(ix + 1) % len(f)]
                link[a] |= 1 << b
                link[b] |= 1 << a
                cmask |= corner
            lm = sum(1 << a for a in range(15) if link[a])
            if any(x.bit_count() > 2 for x in link):
                raise Reject()
            left = lm
            while left:
                root = (left & -left).bit_length() - 1
                component, frontier = 1 << root, 1 << root
                while frontier:
                    reached = 0
                    for x in vertices(frontier):
                        reached |= link[x]
                    frontier = reached & ~component
                    component |= frontier
                left &= ~component
                if all(link[x].bit_count() == 2 for x in vertices(component)) and component.bit_count() != DEG[v]:
                    raise Reject()
            if self.missing_capacity and nbr[v].bit_count() == DEG[v] - 1 and lm == nbr[v] and cmask.bit_count() == nbr[v].bit_count() - 1:
                ends = [a for a in vertices(lm) if link[a].bit_count() == 1]
                if len(ends) == 2 and TQ[v] - t[v] > sum(t[a] < TQ[a] for a in ends):
                    raise Reject()
            if nbr[v].bit_count() != DEG[v]:
                continue
            options = []
            root = min(vertices(nbr[v]))

            def walk(path, todo):
                if todo:
                    for a in vertices(todo):
                        walk(path + [a], todo ^ (1 << a))
                    return
                if path[1] > path[-1]:
                    return
                mask = 0
                for a, b in zip(path, path[1:] + path[:1]):
                    mask |= bit(a, b)
                if cmask & ~mask:
                    return
                ntrue, possible = (mask & e).bit_count(), (mask & ~(e | no)).bit_count()
                if ntrue <= TQ[v] <= ntrue + possible:
                    options.append(mask)

            walk([root], nbr[v] ^ (1 << root))
            if not options:
                raise Reject()
            rotations[v] = options
        if pair_faces:
            for (u, v), fs in sorted(darts.items()):
                if len(fs) != 1 or u not in rotations or v not in rotations:
                    continue
                f = fs[0]

                def other_ends(a, b):
                    ix = f.index(a)
                    old = f[ix - 1] if f[(ix + 1) % len(f)] == b else f[(ix + 1) % len(f)]
                    choices = 0
                    for rot in rotations[a]:
                        for c in vertices(nbr[a] & ~((1 << old) | (1 << b))):
                            if rot & bit(b, c):
                                choices |= 1 << c
                    return list(vertices(choices))

                possible = False
                for a in other_ends(u, v):
                    for b in other_ends(v, u):
                        newface = (u, v, a) if a == b else (u, v, b, a)
                        try:
                            self.plus(newface).inspect(False)
                        except Reject:
                            continue
                        possible = True
                if not possible:
                    raise Reject()
        return {'contacts': {v: set(vertices(nbr[v])) for v in range(15)}, 'faces': cells, 'rotations': rotations}


FAMILIES=[((A,B,C),(A,B,D)),((A,B,D),(A,C,D))]
def need(test,message):
    if not test:raise RuntimeError(message)
def edge(a,b):return (min(a,b),max(a,b))
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def supplier_cover():
    triples=sorted(tuple(vertices(m))for m in range(32)if m.bit_count()==3)
    maps=[];orbits=Counter();rows=[]
    for u,v in product(triples,repeat=2):
        a,b=sum(1<<x for x in u),sum(1<<x for x in v)
        if (a&b).bit_count()!=2 or not(a|b)&16:continue
        rows.append((u,v));images=[]
        for p in permutations(range(4)):
            ren=(*p,4);x,y=tuple(sorted(ren[i]for i in u)),tuple(sorted(ren[i]for i in v))
            images.extend(((x,y),(y,x)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    need(dict(orbits)=={((0,1,2),(0,1,4)):24,((0,1,4),(0,2,4)):24},'supplier mask role images')
    return {'input_rows':100,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}
def contact_fan_cover():
    rows=[]
    for position in (1,2,3):
        cycle=[4,8,9,10,7];cycle[position]=D
        thirds=[cycle[position-1],cycle[position+1]]
        masks={sum(1<<v for v in (F,cycle[i],cycle[i+1]))for i in range(4)}
        need(sum(bool(m&(1<<D))for m in masks)==2,'contact D T mask quota')
        for t,w in ((U,V),(V,U)):
            rows.append([position,cycle,[thirds[0],F,thirds[1],t,w],
                         sorted(tuple(vertices(m))for m in masks)])
    return {'F_D_positions':3,'three_orders':2,'rows':6,'entry_sha256':digest(rows)}
def slots(length,start):
    words=[]
    for count in range(min(4,length)+1):
        for positions in combinations(range(length),count):
            for labels in permutations(sorted(ONET),count):
                names=dict(zip(positions,labels));ordinary=start;word=[]
                for i in range(length):
                    if i in names:word.append(names[i])
                    else:word.append(ordinary);ordinary+=1
                words.append(tuple(word))
    return sorted(words)
def fan(v,cycle,triangles,opposites):
    cells=[];op=iter(opposites)
    for i in range(5):
        a,b=cycle[i],cycle[(i+1)%5]
        cells.append((v,a,b)if i in triangles else(v,a,next(op),b))
    return cells
def evaluate(q):
    try:return q.inspect()
    except Reject:return None
def all_covers():
    tested=Counter();admitted=Counter();events=Counter();whole=hashlib.sha256();kept=hashlib.sha256()
    full_by_family=[0,0]
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n';whole.update(line)
        if value is True or tag.endswith('-selected'):kept.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=evaluate(q);admitted[tag]+=st is not None;record(tag,key,st is not None);return st
    def finish(tag,key,q,st):
        events[tag+' nodes']+=1;n=st['contacts'];darts={}
        for f in sorted(st['faces']):
            for a,b in zip(f,f[1:]+f[:1]):darts.setdefault(edge(a,b),[]).append(f)
        def other(v,w,f):
            ix=f.index(v);old=f[ix-1]if f[(ix+1)%len(f)]==w else f[(ix+1)%len(f)]
            if v in st['rotations']:
                choices=0
                for rotation in st['rotations'][v]:
                    need(bool(rotation&bit(w,old)),'known audit corner')
                    for x in n[v]-{old,w}:
                        if rotation&bit(w,x):choices|=1<<x
                return list(vertices(choices))
            return [x for x in range(15)if x not in {v,w,old}and
                    (x in n[v]or(len(n[v])<DEG[v]and len(n[x])<DEG[x]))]
        options=[]
        for (u,v),fs in sorted(darts.items()):
            if len(fs)!=1:continue
            left,right=other(u,v,fs[0]),other(v,u,fs[0]);cells=set()
            for w in left:
                for x in right:
                    f=boundary((u,v,w)if w==x else(u,v,x,w))
                    if f not in st['faces']:cells.add(f)
            options.append((len(cells),u,v,sorted(cells)))
        need(bool(options),'unexpected audit full map or closed component')
        count,u,v,cells=min(options);record(tag+'-selected',(*key,u,v),count);passed=0
        for f in cells:
            ky=(*key,u,v,*f);child=q.plus(f);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def complete_D(key,q,st):
        need(key[0]==1 and {U,V}<=st['contacts'][D],'both D suppliers at surviving full stars')
        cells=[f for f in st['faces']if len(f)==4 and D in f]
        ends=sorted(st['contacts'][D]-{U,V})
        need(len(cells)==3 and len(ends)==2,'audit D Q cover and endpoints')
        a,b=ends;events['D adjacent-T parents']+=1
        for i in sorted(ORD):
            ky=(*key,D,a,i,b);child=q.plus((D,a,i),(D,i,b));ss=accept('D-adjacent',ky,child)
            if ss is not None:finish('non-close',ky,child,ss)
    def threes(tag,key,q,st):
        events[tag+' nodes']+=1;options=[]
        for v in (U,V):
            nbr=sorted(st['contacts'][v]);need(len(nbr)==3,'audit complete supplier set')
            corners=set()
            for f in st['faces']:
                if v in f:
                    ix=f.index(v);corners.add(bit(f[ix-1],f[(ix+1)%len(f)]))
            for a,b in combinations(nbr,2):
                if bit(a,b)in corners:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                options.append((len(choices),v,a,b,choices))
        if not options:
            events[tag+' full three stars']+=1;record(tag+'-full-selected',key,0)
            if tag=='non':full_by_family[key[0]]+=1;complete_D(key,q,st)
            else:finish('contact-close',key,q,st)
            return
        count,v,a,b,choices=min(options,key=lambda x:x[:4]);record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    for fi,(un,vn)in enumerate(FAMILIES):
        bars=[(v,w)for v,nbr in ((U,un),(V,vn))for w in nbr]
        common=sorted(set(un)&set(vn));forced=[(common[0],U,common[1],V)]
        for e,p in slots(2,11):
            for h in sorted(ONET):
                ky=(fi,e,p,h);q=DartAudit(fan(F,(e,I,R,S,p),{0,1,2,3},(h,))+forced,bars)
                ss=accept('non-initial',ky,q)
                if ss is not None:threes('non',ky,q,ss)
    un,vn=FAMILIES[1];bars=[(v,w)for v,nbr in ((U,un),(V,vn))for w in nbr]
    for position in (1,2,3):
        for e,p in slots(2,10):
            cycle=(e,D,I,R,p)if position==1 else(e,I,D,R,p)if position==2 else(e,I,R,D,p)
            a,b=cycle[position-1],cycle[position+1]
            for t,w in ((U,V),(V,U)):
                for h,k,l in product(sorted(ONET),repeat=3):
                    ky=(position,e,p,t,w,h,k,l)
                    cells=fan(F,cycle,{0,1,2,3},(h,))
                    cells+=fan(D,(a,F,b,t,w),{0,1},(k,A,l))
                    q=DartAudit(cells,bars,fd_contact=True);ss=accept('contact-initial',ky,q)
                    if ss is not None:threes('contact',ky,q,ss)
    return {'tested':dict(sorted(tested.items())),'admitted':dict(sorted(admitted.items())),
            'events':dict(sorted(events.items())),'noncontact_full_three_stars_by_family':full_by_family,
            'all_tested_and_selected_sha256':whole.hexdigest(),'admitted_and_selected_sha256':kept.hexdigest(),
            'completed_maps':0}
def build_report():
    return {'claim':'r2_a4_b0_f0_1_f1_0_f2_1_O7_excluded','supplier_cover':supplier_cover(),
            'contact_fan_cover':contact_fan_cover(),'endpoint_words':len(slots(2,11)),
            'local_covers':all_covers()}
def main():
    report=build_report();expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected,'complete independent output mismatch');print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
