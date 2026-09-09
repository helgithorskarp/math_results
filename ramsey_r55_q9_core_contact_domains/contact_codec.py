"""Exact rank/unrank of all ordered labelled contacts and full q9 colorings."""
from bisect import bisect_right
from functools import lru_cache
from itertools import permutations
from math import prod
from pathlib import Path
import argparse,json,struct
from inputs import HERE,catalogue,need,parents,sha
from reference import Domain
PAIRS=[(a,b) for a in range(128) for b in range(a,128)]
PAIR_INDEX={p:i for i,p in enumerate(PAIRS)}
WIDTH=len(PAIRS)+1

class Contacts:
    def __init__(self,cache,tables,counts=None):
        self.words=catalogue(cache);self.raw=Path(tables).read_bytes()
        need(len(self.raw)==362*2*WIDTH*4,'prefix table length')
        counts_raw=(Path(counts) if counts else HERE/'COUNTS.tsv').read_bytes()
        self.rows=[list(map(int,s.split())) for s in counts_raw.decode().splitlines()]
        need(len(self.rows)==362 and all(x[0]==i and len(x)==5 for i,x in enumerate(self.rows)),'counts shape')
        identity=json.loads((HERE/'TABLE.json').read_text())
        need(sha(self.raw)==identity['sha256'],'prefix table digest')
        need(sha(counts_raw)==identity['counts_sha256'],'contact census digest')
        self._domain=lru_cache(8)(lambda c,j:Domain(7,self.words[c],j))
        self._prefix=lru_cache(8)(self.read_prefix)
    def read_prefix(self,c,joint):
        need(type(c) is int and 0<=c<362 and type(joint) is bool,'domain selector')
        p=struct.unpack_from('<'+str(WIDTH)+'I',self.raw,(2*c+int(joint))*WIDTH*4)
        need(p[0]==0 and list(p)==sorted(p) and p[-1]==self.rows[c][2 if joint else 1],'prefix invariant');return p
    def size(self,c,joint):return self._prefix(c,joint)[-1]
    def rank(self,c,joint,rows):
        need(type(rows) in (list,tuple) and len(rows)==4 and all(type(x) is int and 0<=x<128 for x in rows),'four row masks')
        x,y,z,w=sorted(rows);d=self._domain(c,joint);choices=d.choices(x,y,z)
        need((choices>>w)&1,'contact outside domain')
        answer=self._prefix(c,joint)[PAIR_INDEX[x,y]]
        for t in range(y,z):
            b=d.choices(x,y,t);high,tie=d.weights(x,y,t)
            answer+=(b>>(t+1)).bit_count()*high+((b>>t)&1)*tie
        high,tie=d.weights(x,y,z)
        if w>z:answer+=((choices>>z)&1)*tie+(choices&(((1<<w)-1)^((1<<(z+1))-1))).bit_count()*high
        answer+=sorted(set(permutations((x,y,z,w)))).index(tuple(rows))
        need(0<=answer<self.size(c,joint),'contact rank');return answer
    def unrank(self,c,joint,index):
        need(type(index) is int and 0<=index<self.size(c,joint),'contact index')
        p=self._prefix(c,joint);bucket=bisect_right(p,index)-1;x,y=PAIRS[bucket];index-=p[bucket];d=self._domain(c,joint)
        for z in range(y,128):
            b=d.choices(x,y,z);high,tie=d.weights(x,y,z);weight=(b>>(z+1)).bit_count()*high+((b>>z)&1)*tie
            if index>=weight:index-=weight;continue
            if (b>>z)&1:
                if index<tie:return list(sorted(set(permutations((x,y,z,z))))[index])
                index-=tie
            ordinal,residual=divmod(index,high);b>>=z+1
            for unused in range(ordinal):b&=b-1
            w=z+1+(b&-b).bit_length()-1
            return list(sorted(set(permutations((x,y,z,w))))[residual])
        raise ValueError('prefix partition gap')
    def physical(self,c,red,index):
        if red:return self.unrank(c,True,index)
        dest=self.rows[c][3];packed=self.rows[c][4];p=[(packed>>(3*k))&7 for k in range(7)]
        canonical=self.unrank(dest,False,index)
        return [127^sum(((s>>k)&1)<<p[k] for k in range(7)) for s in canonical]
    def physical_rank(self,c,red,rows):
        if red:return self.rank(c,True,rows)
        need(len(rows)==4 and all(type(s) is int and 0<=s<128 for s in rows),'physical blue rows')
        dest=self.rows[c][3];packed=self.rows[c][4];p=[(packed>>(3*k))&7 for k in range(7)]
        return self.rank(dest,False,[sum((1^((s>>p[k])&1))<<k for k in range(7)) for s in rows])
    def physical_size(self,c,red):return self.size(c,True) if red else self.size(self.rows[c][3],False)

class PhysicalCarrier:
    def __init__(self,name,cache,contacts):
        old=parents().Carrier(name,cache);need(old.q==9,'q9 interface only')
        self.old=old;self.contact=contacts;self.c=old.old.c;self.r=old.r;self.name=name
        self.matrix_radices=old.radices()[:-63]
        self.radices=self.matrix_radices+[contacts.physical_size(self.c,i<self.r) for i in range(9)]
        self.size=prod(self.radices)
    def unrank(self,index):
        need(type(index) is int and 0<=index<self.size,'q9 code')
        digits=[]
        for radix in reversed(self.radices):index,d=divmod(index,radix);digits.append(d)
        digits.reverse();prefix=0
        for digit,radix in zip(digits,self.matrix_radices):prefix=prefix*radix+digit
        old_code=prefix
        for i,code in enumerate(digits[len(self.matrix_radices):]):
            rows=self.contact.physical(self.c,i<self.r,code)
            for v in range(7):
                star=sum(((row>>v)&1)<<u for u,row in enumerate(rows));digit=star if i<self.r else star-1
                need(0<=digit<15,'star digit');old_code=15*old_code+digit
        return self.old.unrank(old_code)
    def rank(self,graph):
        old_code=self.old.rank(graph);stars=[]
        for unused in range(63):old_code,d=divmod(old_code,15);stars.append(d)
        stars.reverse();answer=old_code
        for i in range(9):
            actual=[s if i<self.r else s+1 for s in stars[7*i:7*i+7]]
            rows=[sum(((actual[v]>>u)&1)<<v for v in range(7)) for u in range(4)]
            digit=self.contact.physical_rank(self.c,i<self.r,rows)
            answer=answer*self.radices[len(self.matrix_radices)+i]+digit
        return answer

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('tables');p.add_argument('task');p.add_argument('code',type=int);a=p.parse_args()
    carrier=PhysicalCarrier(a.task,a.cache,Contacts(a.cache,a.tables));g=carrier.unrank(a.code)
    need(carrier.rank(g)==a.code,'physical round trip')
    print(json.dumps({'status':'BARE_CARRIER_ASSIGNMENT_NOT_A_TARGET','task':a.task,'code':a.code,'size':carrier.size,'graph':g},sort_keys=True))
