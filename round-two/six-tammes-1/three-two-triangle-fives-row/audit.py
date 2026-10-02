"""Separate same-author bit/dart audit; imports no primary checker code."""
from collections import Counter,defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

F, D, U, V, A, B, C, I, R, S, P = range(11)
ORD = set(range(7, 15))
ONET = {A, B, C}
DEG = [5, 5, 3, 3] + [4] * 11
TQ = [3, 2, 0, 0] + [1] * 3 + [2] * 8
QQ = [1, 2, 3, 3] + [2] * 3 + [1] * 8


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
                    if o not in ({A,B,C}|({D}if v==F else{F})):
                        raise Reject()
                    if v == F and (nbr[F] & ((1 << U) | (1 << V))).bit_count() == 1 and not (nbr[F] & ((1 << U) | (1 << V)) & ((1 << a) | (1 << b))):
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
                    if a in (F,D) and b not in (U,V) or b in (F,D) and a not in (U,V):
                        raise Reject()
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


FAMILIES=[((A,B,C),(A,B,D)),((A,B,F),(A,B,D)),((A,B,D),(A,C,D)),((A,B,D),(A,F,D))]
def need(test,message):
    if not test:raise RuntimeError(message)
def edge(a,b):return (min(a,b),max(a,b))
def face(f):return boundary(f)
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def supplier_cover():
    triples=sorted(tuple(vertices(m))for m in range(32)if m.bit_count()==3)
    maps=[];orbits=Counter();rows=[]
    for u,v in product(triples,repeat=2):
        a,b=sum(1<<x for x in u),sum(1<<x for x in v)
        if (a&b).bit_count()!=2 or (a&b)&8 or not(a|b)&16:continue
        rows.append((u,v));images=[]
        for p in permutations(range(3)):
            ren=(*p,3,4);x,y=tuple(sorted(ren[i]for i in u)),tuple(sorted(ren[i]for i in v))
            images.extend(((x,y),(y,x)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    need(dict(orbits)=={((0,1,2),(0,1,4)):6,((0,1,3),(0,1,4)):6,
                       ((0,1,4),(0,2,4)):6,((0,1,4),(0,3,4)):12},'supplier mask role images')
    return {'input_rows':100,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}
def slots(length,start):
    words=[]
    for count in range(min(3,length)+1):
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

def closed_obstruction(st):
    n=st['contacts'];cells=sorted(st['faces']);types=[0]*15;qtypes=[0]*15;pairs={}
    need(len(cells)==17 and [sum(len(f)==k for f in cells)for k in (3,4)]==[8,9],'audit closed cell profile')
    for f in cells:
        for v in f:
            if len(f)==3:types[v]+=1
            else:qtypes[v]+=1
        for a,b in zip(f,f[1:]+f[:1]):pairs.setdefault(bit(a,b),[]).append(f)
    need(all(len(n[v])==DEG[v]and types[v]==TQ[v]and qtypes[v]==DEG[v]-TQ[v]for v in range(15)),'audit closed role profile')
    reached=1<<F;frontier=reached
    while frontier:
        nextmask=0
        for v in vertices(frontier):nextmask|=sum(1<<x for x in n[v])
        frontier=nextmask&~reached;reached|=frontier
    need(reached==(1<<15)-1,'audit closed connectedness')
    need(len(pairs)==30 and all(len(fs)==2 for fs in pairs.values()),'audit closed edge incidences')
    witnesses=[]
    for a in sorted(ORD):
        for b in sorted(ORD):
            if a>=b:continue
            fs=pairs.get(bit(a,b),[])
            if len(fs)==2 and all(len(f)==4 for f in fs):witnesses.append([a,b])
    need(bool(witnesses),'audit unexpected unexcluded closed terminal')
    return min(witnesses),digest(cells)

def all_covers():
    tested=Counter();admitted=Counter();events=Counter();whole=hashlib.sha256();kept=hashlib.sha256();terminals=[]
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n';whole.update(line)
        if value is True or tag.endswith('-selected'):kept.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=evaluate(q);admitted[tag]+=st is not None;record(tag,key,st is not None);return st
    def finish(tag,key,q,st):
        events[tag+' close nodes']+=1;n=st['contacts'];edges=defaultdict(list)
        for f in sorted(st['faces']):
            for i,v in enumerate(f):edges[edge(v,f[(i+1)%len(f)])].append(f)
        def other(v,w,f):
            i=f.index(v);old=f[i-1]if f[(i+1)%len(f)]==w else f[(i+1)%len(f)]
            if v in st['rotations']:
                mask=0
                for rot in st['rotations'][v]:
                    need(bool(rot&bit(w,old)),'known audit corner')
                    for x in n[v]-{w,old}:
                        if rot&bit(w,x):mask|=1<<x
                return set(vertices(mask))
            return {x for x in range(15)if x not in {v,w,old}and
                    (x in n[v]or(len(n[v])<DEG[v]and len(n[x])<DEG[x]))}
        options=[]
        for (u,v),fs in sorted(edges.items()):
            if len(fs)!=1:continue
            left,right=other(u,v,fs[0]),other(v,u,fs[0])
            candidates={face((u,v,w))for w in left&right}
            candidates|={face((u,v,x,w))for w,x in product(left,right)if w!=x}
            candidates-=st['faces'];options.append((len(candidates),u,v,sorted(candidates)))
        if not options:
            witness,sha=closed_obstruction(st);events[tag+' metric-excluded terminals']+=1
            record(tag+'-closed-selected',key,[witness,sha])
            terminals.append({'tag':tag,'family':key[0],'ordinary_QQ_edge':witness,'full_faces_sha256':sha})
            return
        count,u,v,candidates=min(options);record(tag+'-close-selected',(*key,u,v),count);passed=0
        for f in candidates:
            ky=(*key,u,v,*f);child=q.plus(f);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def threes(tag,key,q,st):
        events[tag+' three nodes']+=1;options=[]
        for v in (U,V):
            need(len(st['contacts'][v])==3,'three full supplier set')
            known={edge(f[f.index(v)-1],f[(f.index(v)+1)%len(f)])for f in st['faces']if v in f}
            for a,b in combinations(sorted(st['contacts'][v]),2):
                if edge(a,b)in known:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                options.append((len(choices),v,a,b,choices))
        if not options:
            events[tag+' full three stars']+=1;record(tag+'-full-selected',key,0);finish(tag,key,q,st);return
        count,v,a,b,choices=min(options,key=lambda x:x[:4]);record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    for fi,(un,vn)in enumerate(FAMILIES):
        extra=[(v,x)for v,nbr in ((U,un),(V,vn))for x in nbr]
        common=sorted(set(un)&set(vn));forced=[(common[0],U,common[1],V)]
        if F not in set(un)|set(vn):
            for a,b,c,d in slots(4,8):
                for h,k in product(sorted(ONET|{D}),repeat=2):
                    ky=(fi,a,b,c,d,h,k);fs=fan(F,(a,I,b,c,d),{0,1,3},(h,k))
                    q=DartAudit(fs+forced,extra);ss=accept('non-separated-initial',ky,q)
                    if ss is not None:threes('non-separated',ky,q,ss)
        else:
            t=U if F in un else V
            for e,p in slots(2,9):
                for h,k in product(sorted(ONET|{D}),repeat=2):
                    ky=(fi,e,p,t,h,k);fs=fan(F,(e,I,R,p,t),{0,1,2},(h,k))
                    q=DartAudit(fs+forced,extra);ss=accept('non-adjacent-initial',ky,q)
                    if ss is not None:threes('non-adjacent',ky,q,ss)
    un,vn=FAMILIES[2];extra=[(v,x)for v,nbr in ((U,un),(V,vn))for x in nbr]
    for a,b,c,d in slots(4,7):
        for t,w in ((U,V),(V,U)):
            for h,k,l,m in product(sorted(ONET),repeat=4):
                ky=(2,a,b,c,d,t,w,h,k,l,m)
                fs=fan(F,(a,D,b,c,d),{0,1,3},(h,k))+fan(D,(a,F,b,t,w),{0,1},(l,A,m))
                q=DartAudit(fs,extra,fd_contact=True);ss=accept('contact-initial',ky,q)
                if ss is not None:threes('contact',ky,q,ss)
    need(tested['non-separated-initial']==2336 and tested['non-adjacent-initial']==416
         and tested['contact-initial']==11826,'complete initial counts')
    return {'tested':dict(sorted(tested.items())),'admitted':dict(sorted(admitted.items())),
            'events':dict(sorted(events.items())),'all_tested_and_selected_sha256':whole.hexdigest(),
            'admitted_and_selected_sha256':kept.hexdigest(),'metric_excluded_closed_terminals':terminals,
            'geometrically_unexcluded_terminals':0}

def build_report():
    return {'claim':'r2_a3_b0_f0_0_f1_1_f2_1_O8_excluded','supplier_cover':supplier_cover(),
            'endpoint_words':{'four_slots':len(slots(4,8)),'two_slots':len(slots(2,9))},
            'local_covers':all_covers()}
def main():
    report=build_report();expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected,'complete output mismatch');print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
