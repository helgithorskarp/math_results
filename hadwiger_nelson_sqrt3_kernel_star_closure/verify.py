#!/usr/bin/env python3
"""Independent tensor-basis verifier for the paired-kernel star closure."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse,copy,hashlib,json


# Basis 1,sqrt(3),i,i*sqrt(3), independent from the producer's complex pairs.
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def neg(x): return tuple(-a for a in x)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    out=[F(0)]*4
    for m,a in enumerate(x):
        for n,b in enumerate(y):
            s=(m&1)+(n&1);j=(m>>1)+(n>>1);v=a*b
            if s>=2: v*=3;s-=2
            if j>=2: v=-v;j-=2
            out[s+2*j]+=v
    return tuple(out)
def conj(x): return x[0],x[1],-x[2],-x[3]
def norm(x,y):
    d=sub(x,y);return mul(d,conj(d))
ZERO=(F(0),)*4;ONE=(F(1),F(0),F(0),F(0));II=(F(0),F(0),F(1),F(0))
OMEGA=(F(1,2),F(0),F(0),F(1,2));ROOTS=[ONE]
for _ in range(5): ROOTS.append(mul(ROOTS[-1],OMEGA))


def enc(z):
    return [[[z[0].numerator,z[0].denominator],[z[1].numerator,z[1].denominator]],
            [[z[2].numerator,z[2].denominator],[z[3].numerator,z[3].denominator]]]
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()
def need(ok,msg):
    if not ok: raise ValueError(msg)


def base_graph():
    w5=ROOTS[5];us=(OMEGA,ONE,OMEGA,ONE);vs=(II,II,mul(II,w5),mul(II,w5))
    ds=[sub(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,sub(ds[0],ds[2]),ds[0],ds[1]);cross=((0,0),(0,1),(1,0),(1,1));roots=[]
    for (i,j),u in zip(cross,us):
        x=add(centres[i],u);roots.append((x,sub(add(centres[i],centres[2+j]),x)))
    directions=[set(),set()]
    for g in range(2):
        seeds=[sub(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,roots): seeds.extend(sub(p,centres[i if g==0 else 2+j]) for p in row)
        for seed in seeds: directions[g].update(mul(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres): points.update(add(c,u) for u in directions[h//2])
    vertices=sorted(points);edges=[e for e in combinations(range(len(vertices)),2) if norm(vertices[e[0]],vertices[e[1]])==ONE]
    return centres,vertices,edges


def move(z,source0,target0,alpha,reflected):
    d=sub(z,source0);return add(target0,mul(alpha,conj(d) if reflected else d))


def closure(centres,base,edges):
    host=set(base);hashes=set();count=0
    for s0,s1 in ((0,1),(2,3)):
        source=sub(centres[s1],centres[s0])
        for ea,eb in edges:
            for reverse in (False,True):
                ta,tb=(eb,ea) if reverse else (ea,eb);target0=base[ta];target=sub(base[tb],target0)
                for reflected in (False,True):
                    count+=1;alpha=mul(target,source if reflected else conj(source))
                    moved={move(z,centres[s0],target0,alpha,reflected) for z in base};host.update(moved)
                    hashes.add(digest([enc(z) for z in sorted(set(base)|moved)]))
    host=sorted(host);edges=[e for e in combinations(range(len(host)),2) if norm(host[e[0]],host[e[1]])==ONE]
    return count,hashes,host,edges


PATTERNS=((0,1,0,1),(0,1,0,2),(0,1,2,0),(0,1,1,0),(0,1,1,2),(0,1,2,1))
def mod3(x): return (x.numerator*pow(x.denominator,-1,3))%3


def audit(data):
    need(data.get('schema')==1 and data.get('field')=='Q(sqrt(3),i)','schema')
    need(data.get('star_interface_preserved') is True and data.get('record_improved') is False,'scope flags')
    centres,base,base_edges=base_graph()
    need((len(base),len(base_edges))==(39,102),'base counts')
    need(data.get('base_vertices')==39 and data.get('base_edges')==102,'certified base counts')
    need(data.get('base_point_sha256')==digest([enc(z) for z in base]),'base point hash')
    need(data.get('base_edge_sha256')==digest(base_edges),'base edge hash')
    count,hashes,host,edges=closure(centres,base,base_edges)
    need(count==data.get('raw_attachments')==816,'attachment count')
    need(len(hashes)==data.get('canonical_two_copy_supports')==326,'support count')
    need(data.get('support_hash_set_sha256')==digest(sorted(hashes)),'support set hash')
    need((len(host),len(edges))==(data.get('host_vertices'),data.get('host_edges'))==(587,2426),'host counts')
    need(data.get('host_point_sha256')==digest([enc(z) for z in host]),'host point hash')
    need(data.get('host_edge_sha256')==digest(edges),'host edge hash')
    ci=[host.index(z) for z in centres];pi=host.index(neg(II))
    need(ci==data.get('centre_indices') and pi==data.get('common_neighbour_index'),'terminal indices')
    edge_set=set(edges)
    need(all(tuple(sorted((pi,v))) in edge_set for v in ci),'common-neighbour spokes')
    need(tuple(sorted((ci[0],ci[1]))) in edge_set and tuple(sorted((ci[2],ci[3]))) in edge_set,'centre edges')
    need(data.get('allowed_terminal_patterns')==[list(p) for p in PATTERNS],'terminal patterns')
    words=data.get('terminal_colourings');need(isinstance(words,dict) and set(words)=={''.join(map(str,p)) for p in PATTERNS},'word keys')
    checks=0
    for pattern in PATTERNS:
        word=words[''.join(map(str,pattern))]
        need(isinstance(word,str) and len(word)==len(host) and set(word)<={'0','1','2','3'},'word domain')
        colours=list(map(int,word));need(tuple(colours[v] for v in ci)==pattern,'terminal pin')
        need(all(colours[a]!=colours[b] for a,b in edges),'word edge');checks+=len(edges)
    # A seventh canonical pattern, 0123, is impossible: its common neighbour
    # is adjacent to one vertex of every colour.  The two centre edges rule
    # out only equal colours inside their own pairs, so these seven partitions
    # exhaust all equality types up to a global colour permutation.
    need(len(set((0,1,2,3)))==4 and all(tuple(sorted((pi,v))) in edge_set for v in ci),'all-distinct obstruction')
    linear=data.get('three_colouring');need(isinstance(linear,str) and len(linear)==len(host),'linear word')
    expected=''.join(str((mod3(z[0])+mod3(z[2]))%3) for z in host)
    need(linear==expected and set(linear)<={'0','1','2'},'linear rule')
    need(all(linear[a]!=linear[b] for a,b in edges),'linear edge')
    residues=sorted({tuple(mod3(x) for x in sub(host[a],host[b])) for a,b in edges})
    need(data.get('unit_edge_residues_mod3')==[list(x) for x in residues],'edge residues')
    need(data.get('three_colouring_rule')=='a+c mod 3 for z=(a+b sqrt(3))+i(c+d sqrt(3))','rule label')
    return {'status':'PASS','base_vertices':39,'base_edges':102,'raw_attachments':count,
      'canonical_two_copy_supports':len(hashes),'host_vertices':len(host),'host_edges':len(edges),
      'host_point_pair_checks':len(host)*(len(host)-1)//2,'allowed_terminal_patterns':len(PATTERNS),
      'forbidden_all_distinct_pattern':True,'terminal_colour_edge_checks':checks,
      'linear_three_colour_edge_checks':len(edges),'unit_edge_residue_classes':len(residues),
      'host_point_sha256':data['host_point_sha256'],'host_edge_sha256':data['host_edge_sha256'],
      'record_improved':False}


def controls(data):
    cases=[]
    for key,value in [('schema',2),('canonical_two_copy_supports',325),('host_point_sha256','0'*64),
                      ('host_edge_sha256','0'*64),('star_interface_preserved',False),('record_improved',True)]:
        x=copy.deepcopy(data);x[key]=value;cases.append(x)
    x=copy.deepcopy(data);x['terminal_colourings']['0101']='0'*x['host_vertices'];cases.append(x)
    x=copy.deepcopy(data);x['three_colouring']='0'*x['host_vertices'];cases.append(x)
    x=copy.deepcopy(data);x['allowed_terminal_patterns'].append([0,1,2,3]);cases.append(x)
    rejected=0
    for x in cases:
        try: audit(x)
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError): rejected+=1
    need(rejected==len(cases),'malformed control accepted');return rejected


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'));ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
    blob=args.certificate.read_bytes();data=json.loads(blob);need(raw(data)==blob,'noncanonical certificate')
    result=audit(data);result['malformed_certificate_rejections']=controls(data);result['certificate_bytes']=len(blob);result['certificate_sha256']=hashlib.sha256(blob).hexdigest()
    if args.check_expected: need(result==json.loads(Path(__file__).with_name('expected.json').read_text()),'expected report')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
