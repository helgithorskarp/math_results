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
TQ = [3, 3, 0, 0] + [1] * 4 + [2] * 7
QQ = [1, 1, 3, 3] + [2] * 4 + [1] * 7


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
                    if o not in (F, D, A, B, C, E):
                        raise Reject()
                    if nbr[v] & ((1 << U) | (1 << V)) and not (nbr[v] & ((1 << U) | (1 << V)) & ((1 << a) | (1 << b))):
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


PARTS = ('noncontact', 'contact-separated', 'contact-adjacent')
FAMILIES = [((A,B,C),(A,B,E)), ((A,B,C),(A,B,D)),
            ((A,B,F),(A,B,D)), ((A,B,C),(E,F,D)), ((A,B,F),(C,E,D))]

def need(test,message):
    if not test:raise RuntimeError(message)

def edge(a,b):return (min(a,b),max(a,b))

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def supplier_cover():
    # Generate triples by masks and all group images of the actual role labels.
    triples=sorted(tuple(vertices(m))for m in range(64)if m.bit_count()==3)
    rows=[];maps=[];orbits=Counter()
    for u,v in product(triples,repeat=2):
        intersection=sum(1<<x for x in u)&sum(1<<x for x in v)
        if intersection&48 or intersection.bit_count()not in (0,2):continue
        rows.append((u,v));images=[]
        for p in permutations(range(4)):
            for swap in (False,True):
                ren=(*p,5,4)if swap else(*p,4,5)
                a,b=tuple(sorted(ren[x]for x in u)),tuple(sorted(ren[x]for x in v))
                images.extend(((a,b),(b,a)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    expected={((0,1,2),(0,1,3)):12,((0,1,2),(0,1,4)):48,
              ((0,1,4),(0,1,5)):12,((0,1,2),(3,4,5)):8,((0,1,4),(2,3,5)):12}
    need(dict(orbits)==expected,'supplier masks and role images')
    return {'input_rows':400,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}

def paired_fans():
    rows=[];admitted=[]
    for j in (2,3,4):
        for k in (2,3,4):
            contact_cells=[(0,1,2),(0,1,3),
                (0,(2,1,3,4,5)[j],(2,1,3,4,5)[(j+1)%5]),
                (1,(2,0,3,6,7)[k],(2,0,3,6,7)[(k+1)%5])]
            masks={sum(1<<v for v in t)for t in contact_cells}
            good=all(sum(bool(m&(1<<v))for m in masks)<=2 for v in range(2,8))
            ts=sorted(tuple(vertices(m))for m in masks)
            rows.append([j,k,ts,good])
            if good:admitted.append([j,k])
    need(admitted==[[2,3],[2,4],[3,2],[3,3],[3,4],[4,2],[4,3]],'paired sector masks')
    return {'rows':9,'admitted':admitted,'entry_sha256':digest(rows)}

def slots(length,start):
    # Choose occupied one-T positions, inject distinct names there, then give
    # all remaining positions distinct ordinary labels in first-use order.
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
        if i in triangles:cells.append((v,a,b))
        else:cells.append((v,a,next(op),b))
    return cells

def inspect(q):
    try:return q.inspect()
    except Reject:return None

def cover(part):
    need(part in PARTS,'audit partition')
    tested=Counter();admitted=Counter();events=Counter();allhash=hashlib.sha256();keep=hashlib.sha256()
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n'
        allhash.update(line)
        if value is True or tag.endswith('-selected'):keep.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=inspect(q);admitted[tag]+=st is not None
        record(tag,key,st is not None);return st
    def finish_faces(tag,key,q,st):
        events[tag+' nodes']+=1;n=st['contacts'];edges={}
        for f in sorted(st['faces']):
            for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(edge(a,b),[]).append(f)
        def other(v,w,f):
            ix=f.index(v);old=f[ix-1]if f[(ix+1)%len(f)]==w else f[(ix+1)%len(f)]
            if v in st['rotations']:
                possible=0
                for rotation in st['rotations'][v]:
                    need(bool(rotation&bit(w,old)),'known audit corner')
                    for x in n[v]-{old,w}:
                        if rotation&bit(w,x):possible|=1<<x
                return list(vertices(possible))
            return [x for x in range(15)if x not in {v,w,old} and
                    (x in n[v]or(len(n[v])<DEG[v]and len(n[x])<DEG[x]))]
        options=[]
        for (u,v),fs in sorted(edges.items()):
            if len(fs)!=1:continue
            left,right=other(u,v,fs[0]),other(v,u,fs[0]);cells=set()
            for w in left:
                for x in right:
                    candidate=boundary((u,v,w)if w==x else(u,v,x,w))
                    if candidate not in st['faces']:cells.add(candidate)
            options.append((len(cells),u,v,sorted(cells)))
        need(bool(options),'unexpected audit full map or closed component')
        count,u,v,choices=min(options);record(tag+'-selected',(*key,u,v),count);passed=0
        for cell in choices:
            ky=(*key,u,v,*cell);child=q.plus(cell);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish_faces(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def complete_D(key,q,st):
        th=sorted(st['contacts'][D]&{U,V})
        if not th:
            events['D separated parents']+=1
            t=[0]*15
            for f in st['faces']:
                if len(f)==3:
                    for v in f:t[v]+=1
            eligible=[v for v in range(15)if v not in (F,D,U,V)and
                (D in st['contacts'][v]or(len(st['contacts'][v])<DEG[v]and t[v]<TQ[v]))]
            record('D-supply-selected',key,eligible)
            need(len(eligible)<5,'audit separated D uncovered')
            events['D neighbor-T-supply reject']+=1;return
        need(len(th)==1,'audit D unique three')
        quadrilaterals=[f for f in st['faces']if len(f)==4 and D in f]
        need(len(quadrilaterals)==2 and all(th[0]in f for f in quadrilaterals),'D Q cover')
        ends=sorted(st['contacts'][D]-set(th));need(len(ends)==2,'D endpoint cover')
        a,d=ends;events['D adjacent parents']+=1
        for i in sorted(ORD):
            for j in sorted(ORD-{i}):
                ky=(*key,D,a,i,j,d)
                child=q.plus((D,a,i),(D,i,j),(D,j,d))
                ss=accept('D-completion',ky,child)
                if ss is not None:finish_faces('non-close',ky,child,ss)
    def threes(tag,key,q,st):
        events[tag+' nodes']+=1;options=[]
        for v in (U,V):
            nbr=sorted(st['contacts'][v]);need(len(nbr)==3,'audit supplier degree')
            known=set()
            for f in st['faces']:
                if v in f:
                    ix=f.index(v);known.add(bit(f[ix-1],f[(ix+1)%len(f)]))
            for a,b in combinations(nbr,2):
                if bit(a,b)in known:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                options.append((len(choices),v,a,b,choices))
        if not options:
            events[tag+' full stars']+=1;record(tag+'-full-selected',key,0)
            if tag=='non':complete_D(key,q,st)
            else:finish_faces('contact-close',key,q,st)
            return
        count,v,a,b,choices=min(options,key=lambda x:x[:4]);record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    if part=='noncontact':
        for fi,(un,vn)in enumerate(FAMILIES):
            bars=[(v,w)for v,neighbours in ((U,un),(V,vn))for w in neighbours]
            overlap=sorted(set(un)&set(vn));shared=[(overlap[0],U,overlap[1],V)]if overlap else[]
            three=U if F in un else V if F in vn else None
            if three is None:
                for a,b,c,d in slots(4,9):
                    for h,k in product((*sorted(ONET),D),repeat=2):
                        ky=(fi,a,b,c,d,h,k)
                        q=DartAudit(fan(F,(a,I,b,c,d),{0,1,3},(h,k))+shared,bars)
                        ss=accept('non-separated',ky,q)
                        if ss is not None:threes('non',ky,q,ss)
            else:
                for a,d in slots(2,10):
                    for h,k in product((*sorted(ONET),D),repeat=2):
                        ky=(fi,a,d,h,k)
                        q=DartAudit(fan(F,(a,I,R,d,three),{0,1,2},(h,k))+shared,bars)
                        ss=accept('non-adjacent',ky,q)
                        if ss is not None:threes('non',ky,q,ss)
    else:
        for fi,(un,vn)in enumerate(FAMILIES):
            if fi==3 or (part=='contact-separated')!=(fi==0):continue
            bars=[(v,w)for v,neighbours in ((U,un),(V,vn))for w in neighbours]
            overlap=sorted(set(un)&set(vn));shared=[(overlap[0],U,overlap[1],V)]if overlap else[]
            ft=U if F in un else V if F in vn else None
            dt=U if D in un else V if D in vn else None
            cases=[(3,3)]if ft is None and dt is None else [(3,2),(3,4)]if ft is None else [(2,4),(4,2)]
            for j,k in cases:
                if (j,k)==(3,3):words=slots(6,8)
                elif (j,k)==(3,2):words=[(a,8,c,d,e,dt)for a,c,d,e in slots(4,9)]
                elif (j,k)==(3,4):words=[(8,b,c,d,dt,f)for b,c,d,f in slots(4,9)]
                elif (j,k)==(2,4):words=[(8,9,c,ft,dt,f)for c,f in slots(2,10)]
                elif (j,k)==(4,2):words=[(8,9,ft,d,e,dt)for d,e in slots(2,10)]
                else:raise RuntimeError('audit contact cases')
                for a,b,c,d,e,f in words:
                    for opposites in product(sorted(ONET),repeat=4):
                        ky=(fi,j,k,a,b,c,d,e,f,*opposites)
                        cells=fan(F,(a,D,b,c,d),{0,1,j},opposites[:2])
                        cells+=fan(D,(a,F,b,e,f),{0,1,k},opposites[2:])+shared
                        q=DartAudit(cells,bars,fd_contact=True);ss=accept('paired-fans',ky,q)
                        if ss is not None:threes('contact',ky,q,ss)
    return {'part':part,'tested':dict(sorted(tested.items())),
            'admitted':dict(sorted(admitted.items())),'events':dict(sorted(events.items())),
            'all_tested_and_selected_sha256':allhash.hexdigest(),
            'admitted_and_selected_sha256':keep.hexdigest(),'completed_maps':0}

def build_report(part):
    return {'claim':'r2_a4_b0_f0_0_f1_2_f2_0_O7_excluded',
            'supplier_cover':supplier_cover(),'paired_fans':paired_fans(),
            'canonical_slot_counts':{'two':len(slots(2,10)),'four':len(slots(4,9)),'six':len(slots(6,8))},
            'local_cover':cover(part)}

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--part',required=True,choices=PARTS)
    part=parser.parse_args().part;report=build_report(part)
    expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected[part],'complete independent partition mismatch')
    print(json.dumps(report,sort_keys=True,indent=2))

if __name__=='__main__':main()
