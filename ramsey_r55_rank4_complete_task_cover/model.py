"""Canonical row tasks, physical factor models, and exact full-graph CNFs."""
from collections import Counter
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import re


def rank(xs):
    basis={}
    for value in xs:
        while value:
            bit=value.bit_length()-1
            if bit in basis:value^=basis[bit]
            else:basis[bit]=value;break
    return len(basis)


def dot(a,b):return (a&b).bit_count()&1


def rows_from_code(code):
    if type(code) is not int or not 0<=code<2**30:raise ValueError('invalid row code')
    counts=[(code>>(2*x))&3 for x in range(15)]
    zeros=20-sum(counts)
    if zeros not in (0,1):raise ValueError('invalid row weight')
    rows=[0]*zeros+[x for x in range(1,16) for _ in range(counts[x-1])]
    if rank(rows)!=4:raise ValueError('nonspanning row task')
    return rows


def load_cover(path=None):
    path=Path(path) if path else Path(__file__).with_name('row_cover.tsv')
    lines=path.read_text().splitlines()
    if lines[0]!='code\tzero\torbit_size\tsupport\ttriples':raise ValueError('cover header')
    result=[];previous=-1
    for line in lines[1:]:
        fields=list(map(int,line.split('\t')))
        if len(fields)!=5:raise ValueError('cover fields')
        code,z,size,supp,triples=fields;rows=rows_from_code(code);c=Counter(rows)
        if code<=previous or z!=c[0] or size<=0 or 20160%size or supp!=sum(x!=0 for x in c) or triples!=sum(v==3 for v in c.values()):raise ValueError('cover metadata')
        result.append(fields);previous=code
    return result


def full_support_double(rows,r=4):
    c=Counter(rows)
    return not c[0] and all(1<=c[x]<=2 for x in range(1,2**r))


class Task:
    def __init__(self,rows,b=23,r=4,known_exclusion=True):
        self.rows=list(rows);self.a=len(rows);self.b=b;self.r=r;self.n=self.a+b
        if r<2 or r>4 or b<r or any(type(x) is not int or not 0<=x<2**r for x in rows) or rank(rows)!=r:raise ValueError('invalid factors')
        self.variables=1;self.true=1;self.base=[(1,)];self.gates=[]
        self.pairs=list(combinations(range(self.n),2))
        self.internal={p:self.var() for p in self.pairs if (p[0]<self.a)==(p[1]<self.a)}
        self.labels=[[self.var() for _ in range(2**r)] for _ in range(b)]
        self.stars={x:[self.var() for _ in range(b)] for x in range(1,2**r)}
        for j,row in enumerate(self.labels):
            self.add(row)
            for v,w in combinations(row,2):self.add([-v,-w])
            for x in range(1,2**r):
                for label,v in enumerate(row):self.add([-v,self.stars[x][j] if dot(x,label) else -self.stars[x][j]])
        for x in self.stars:self.add(self.stars[x])
        for j in range(b-1):
            for x in range(2**r):
                for y in range(x):self.add([-self.labels[j][x],-self.labels[j+1][y]])
        for x in range(2**r):
            cap=2 if x==0 else 5
            for j in range(b-cap):self.add([-self.labels[j][x],-self.labels[j+cap][x]])
        if 0 in rows:
            for j in range(b):self.add([-self.labels[j][0]])
        self.affine_normal=next((x for x in self.stars if all(dot(x,a) for a in rows)),None)
        if self.affine_normal is not None:
            for x in self.stars:
                if dot(x,self.affine_normal):self.add([-v for v in self.stars[x]])
        self.known_guard=bool(known_exclusion and self.n==43 and self.a==20 and b==23 and r==4 and full_support_double(rows))
        if self.known_guard:
            occurs={x:self.gate('or',[self.labels[j][x] for j in range(b)]) for x in range(16)}
            triples={x:self.gate('or',[self.gate('and',[self.labels[j][x],self.labels[j+2][x]]) for j in range(b-2)]) for x in range(1,16)}
            self.add([occurs[0]]+[-occurs[x] for x in range(1,16)]+[triples[x] for x in range(1,16)])
        self.physical_literals={}
        for i,j in self.pairs:
            if i<self.a<=j:
                self.physical_literals[i,j]=self.stars[rows[i]][j-self.a] if rows[i] else -self.true
            else:self.physical_literals[i,j]=self.internal[i,j]

    def var(self):self.variables+=1;return self.variables

    def simplify(self,clause):
        s=set(clause)
        if self.true in s or any(-x in s for x in s):return None
        s.discard(-self.true)
        return tuple(sorted(s,key=lambda x:(abs(x),x)))

    def add(self,clause):
        c=self.simplify(clause)
        if c is not None:self.base.append(c)

    def gate(self,op,args):
        y=self.var();args=tuple(args);self.gates.append((y,op,args))
        if op=='or':
            self.add([-y]+list(args))
            for x in args:self.add([y,-x])
        elif op=='and':
            self.add([y]+[-x for x in args])
            for x in args:self.add([-y,x])
        else:raise ValueError('gate type')
        return y

    def ramsey_clauses(self):
        for q in combinations(range(self.n),5):
            literals=[self.physical_literals[p] for p in combinations(q,2)]
            for sign in (-1,1):
                c=self.simplify([sign*x for x in literals])
                if c is not None:yield c

    def primary(self,columns,internal_bits):
        if len(columns)!=self.b or any(type(x) is not int or not 0<=x<2**self.r for x in columns):raise ValueError('column list')
        if type(internal_bits) is not int or not 0<=internal_bits<2**len(self.internal):raise ValueError('internal bits')
        values={self.true:True}
        for k,v in enumerate(self.internal.values()):values[v]=bool(internal_bits>>k&1)
        for j,row in enumerate(self.labels):
            for x,v in enumerate(row):values[v]=(columns[j]==x)
        for x,row in self.stars.items():
            for j,v in enumerate(row):values[v]=bool(dot(x,columns[j]))
        def value(x):return values[abs(x)]==(x>0)
        for y,op,args in self.gates:values[y]=any(value(x) for x in args) if op=='or' else all(value(x) for x in args)
        return values

    def graph(self,columns,internal_bits):
        values=self.primary(columns,internal_bits)
        mask=sum(int(values[abs(v)]==(v>0))<<k for k,v in enumerate(self.physical_literals.values()))
        return {'n':self.n,'red_hex':format(mask,f'0{(len(self.pairs)+3)//4}x')}

    def base_holds(self,columns,internal_bits=0):
        values=self.primary(columns,internal_bits)
        return all(any(values[abs(v)]==(v>0) for v in c) for c in self.base)

    def write(self,path):
        # Stream the body once so the actual emitted clause count is authoritative.
        path=Path(path)
        if path.exists():raise ValueError('refusing to overwrite CNF')
        body=path.with_suffix(path.suffix+'.body')
        if body.exists():raise ValueError('existing temporary body')
        count=0;hist={};h=hashlib.sha256()
        with body.open('wb') as f:
            for source in (iter(self.base),self.ramsey_clauses()):
                for c in source:
                    line=(' '.join(map(str,c))+' 0\n').encode()
                    f.write(line);h.update(line);count+=1;hist[len(c)]=hist.get(len(c),0)+1
        with path.open('wb') as f,body.open('rb') as src:
            f.write(f'p cnf {self.variables} {count}\n'.encode())
            while chunk:=src.read(1024*1024):f.write(chunk)
        body.unlink()
        return {'variables':self.variables,'clauses':count,'base_clauses':len(self.base),'ramsey_clauses':count-len(self.base),
                'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'body_sha256':h.hexdigest(),
                'clause_length_histogram':hist,'known_profile_exclusion':self.known_guard,'affine_row_normal':self.affine_normal}


def target(code,cover_path=None):
    if code not in {row[0] for row in load_cover(cover_path)}:raise ValueError('row code absent from canonical cover')
    return Task(rows_from_code(code))


def parse_data(data,cover_path=None):
    if not isinstance(data,dict) or set(data)!={'row_code','columns','internal_hex'}:raise ValueError('exact task fields required')
    task=target(data['row_code'],cover_path)
    h=data['internal_hex']
    if not isinstance(h,str) or re.fullmatch('[0-9a-f]{111}',h) is None or int(h,16)>=2**443:raise ValueError('443-bit internal encoding')
    task.primary(data['columns'],int(h,16))
    return task,int(h,16)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--row-code',type=int);p.add_argument('--cnf');p.add_argument('--data');p.add_argument('--cover')
    args=p.parse_args()
    if args.data:
        data=json.loads(Path(args.data).read_text());task,bits=parse_data(data,args.cover)
        print(json.dumps({'base_filters_hold':task.base_holds(data['columns'],bits),'graph':task.graph(data['columns'],bits)},sort_keys=True))
    elif args.row_code is not None and args.cnf:
        task=target(args.row_code,args.cover);print(json.dumps(task.write(args.cnf),sort_keys=True))
    else:p.error('provide --data, or --row-code with --cnf')
