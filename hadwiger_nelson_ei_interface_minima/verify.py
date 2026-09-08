"""Exact conditional-interface certificate checker; standard library only."""
import copy
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE_HASHES={'g40': 'df1316f4351859dfe5751a56092ae73dbc5be73bea30813ce5133ebab140449f', 'g49': '1dfb84f8fca02ada017c5d7fc22aa66ac81ba90fd031f4ff94beb002e9b6fdca'}

def require(x,message):
    if not x: raise ValueError(message)

def multiply(x,y):
    out=[0]*4
    for a,b in itertools.product(range(4),repeat=2):
        common=a&b
        out[a^b]+=x[a]*y[b]*(3 if common&1 else 1)*(11 if common&2 else 1)
    return out

def geometric_graph(name):
    raw=(ROOT/(name+'.json')).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SOURCE_HASHES[name],'source identity')
    points=json.loads(raw)
    require(all(len(p)==4 and all(type(v) is int for v in p) for p in points),'source coordinate format')
    require(len({tuple(p) for p in points})==len(points),'point collision')
    def distance(i,j):
        a,b,c,d=[x-y for x,y in zip(points[i],points[j])]
        xx=multiply([0,a,b,0],[0,a,b,0])
        yy=multiply([c,0,0,d],[c,0,0,d])
        return [x+y for x,y in zip(xx,yy)]
    pairs={}
    for pair in itertools.combinations(range(len(points)),2):
        pairs[pair]=distance(*pair)
    require(pairs[(0,1)]==([4752,0,0,0] if name=='g49' else [9216,0,0,0]),'terminal distance')
    edges=[pair for pair,norm in pairs.items() if norm==[1296,0,0,0]]
    long=[pair for pair,norm in pairs.items() if norm==[4752,0,0,0]]
    small={pair for pair,norm in pairs.items() if norm==[432,0,0,0]}
    triangles=[t for t in itertools.combinations(range(len(points)),3)
               if all(p in small for p in itertools.combinations(t,2))]
    return len(points),edges,long,triangles

def word_check(word,n,edges,constraints,equal):
    require(type(word) is str and len(word)==n and set(word)<=set('0123'),'word format')
    require((word[0]==word[1])==equal,'wrong terminal relation')
    require(all(len({word[v] for v in t})>1 for t in edges+constraints),'monochromatic constraint')

def decide(n,constraints,equal):
    nodes=0
    leaves=0
    initial=[15]*n
    initial[0]=1
    initial[1]=1 if equal else 2
    incident=[0]*n
    for t in constraints:
        for v in t: incident[v]+=1
    def search(domains):
        nonlocal nodes,leaves
        nodes+=1
        changed=True
        while changed:
            changed=False
            for t in constraints:
                for v in t:
                    other=[domains[u] for u in t if u!=v]
                    if other and all(x==other[0] for x in other) and other[0].bit_count()==1:
                        new=domains[v]&~other[0]
                        if new==0:
                            leaves+=1
                            return False
                        if new!=domains[v]:
                            changed=True
                            domains[v]=new
        undecided=[v for v,d in enumerate(domains) if d.bit_count()>1]
        if not undecided:return True
        v=min(undecided,key=lambda v:(domains[v].bit_count(),-incident[v],v))
        for c in range(4):
            if domains[v]>>c&1:
                nxt=domains.copy();nxt[v]=1<<c
                if search(nxt):return True
        return False
    sat=search(initial)
    return sat,{'nodes':nodes,'conflicts':leaves}

def unsat(n,constraints,equal):
    sat,stats=decide(n,constraints,equal)
    require(not sat,'formula has a four-colouring')
    return stats

def check(certificate):
    result={}
    for name in ('g40','g49'):
        n,edges,long,triangles=geometric_graph(name)
        cons=triangles if name=='g49' else long
        require((n,len(edges),len(cons))==((49,180,18) if name=='g49' else (40,82,59)), 'wrong source inventory')
        row=certificate[name]
        essential=row['essential']
        require(all(type(i) is int and 0<=i<len(cons) for i in essential) and essential==sorted(set(essential)),'essential indices')
        require(len(row['essential_words'])==len(essential),'essential witness count')
        for i,word in zip(essential,row['essential_words']):
            word_check(word,n,edges,[t for j,t in enumerate(cons) if i!=j],name=='g49')
            require(len({word[v] for v in cons[i]})==1,'essential witness does not violate omitted premise')
        if name=='g49':
            proof=unsat(n,edges+[cons[i] for i in essential],True)
            result[name]={'essential':essential,'minimum':len(essential),'valid_supports':1<<(len(cons)-len(essential)),
                          'exhaustive_proof':proof,'triangles':[list(t) for t in triangles],
                          'required_triangles':[list(cons[i]) for i in essential]}
        else:
            optional=[i for i in range(len(cons)) if i not in essential]
            require(optional==row['optional'],'G40 optional indices')
            patterns=[]
            for item in row['patterns']:
                mask,word=item['mask'],item['word']
                require(type(mask) is int and 0<mask<(1<<len(optional)),'pattern mask')
                word_check(word,n,edges,[cons[i] for i in essential],False)
                actual=sum(1<<j for j,i in enumerate(optional) if word[cons[i][0]]==word[cons[i][1]])
                require(actual==mask,'pattern mismatch')
                patterns.append(mask)
            require(patterns==sorted(set(patterns)),'pattern order or repetition')
            require(all(not(a&b==a) for a,b in itertools.permutations(patterns,2)),'patterns not an antichain')
            covers=[m for m in range(1<<len(optional)) if all(m&p for p in patterns)]
            require(covers,'no valid support')
            covers_set=set(covers)
            minimal=[m for m in covers if all(not(m>>j&1) or (m^(1<<j)) not in covers_set for j in range(len(optional)))]
            require(minimal==row['minimal_covers'],'minimal covers differ')
            require(all(any(not(m>>j&1) for m in minimal) for j in range(len(optional))),'a claimed optional premise is compulsory')
            proofs={str(mask):unsat(n,edges+[cons[i] for i in essential]+[cons[i] for j,i in enumerate(optional) if mask>>j&1],False)
                    for mask in minimal}
            packing=row['disjoint_obstructions']
            require(len(set(packing))==len(packing) and all(p in patterns for p in packing),'packing membership')
            require(all(not(a&b) for a,b in itertools.combinations(packing,2)),'packing overlap')
            minimum=len(essential)+min(m.bit_count() for m in covers)
            require(minimum==len(essential)+len(packing),'packing does not prove minimum')
            result[name]={'essential':essential,'optional':optional,'minimal_patterns':patterns,
                          'minimal_covers':minimal,'valid_supports':len(covers),'minimum':minimum,
                          'minimum_covers':[m for m in covers if m.bit_count()==minimum-len(essential)],
                          'exhaustive_proofs':proofs,'optional_pairs':[list(cons[i]) for i in optional],
                          'disjoint_obstructions':packing}
    result['assembly_budget']={'G40_copies':2,'G49_copies':2*result['g40']['minimum'],
                               'T375_copies':2*result['g40']['minimum']*result['g49']['minimum'],
                               'vertex_upper_bound':79+2*result['g40']['minimum']*(47+result['g49']['minimum']*372)}
    result['source_sha256']=SOURCE_HASHES
    result['source_pair_checks']=40*39//2+49*48//2
    result['essential_witnesses']=sum(len(certificate[name]['essential']) for name in ('g40','g49'))
    result['pattern_witnesses']=len(certificate['g40']['patterns'])
    result['exhaustive_refutations']=1+len(certificate['g40']['minimal_covers'])
    result['record_improvement']=False
    return result

def main():
    actual=check(json.loads((ROOT/'certificate.json').read_text()))
    expected_path=ROOT/'expected.json'
    if expected_path.exists():require(actual==json.loads(expected_path.read_text()),'expected output mismatch')
    print(json.dumps(actual,sort_keys=True))

if __name__=='__main__':main()
