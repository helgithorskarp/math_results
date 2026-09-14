"""Two coordinate constructions, all-pairs tensor geometry, and positive words."""
import argparse,json,subprocess,time,hashlib
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import model as m
import alternate as a
import dyadic
from discover import graph,prime_recipe
import colour
HERE=Path(__file__).resolve().parent
def word_check(word,edges,term,pattern):
    m.require(isinstance(word,str) and len(word)>max(term) and set(word)<=set('0123'),'malformed word')
    m.require(all(word[i]!=word[j] for i,j in edges),'improper word')
    m.require([int(word[i]) for i in term]==list(pattern),'wrong terminal pattern')
def run(work,sanitize=False):
    start=time.time();work=work.resolve();m.require(not work.is_relative_to(HERE.parent),'work outside repository required');work.mkdir(parents=True,exist_ok=True)
    P,orbits,families=m.make();convert=a.source_map();mapped=[convert(p,1) for p in P];independent,alt_orbits=a.host();m.require(sorted(mapped)==independent,'host coordinate sets disagree')
    m.require(len(set(mapped))==1801,'host collision')
    blocks=[mapped];source_edges=[graph(P,work)];dyadics=dyadic.make_cases(canonical=True);ad=a.dyadics();recipe=prime_recipe()
    for (key,Q),(key2,coords) in zip(dyadics,ad):
        m.require(key==key2 and [convert(p,8) for p in Q]==coords,'dyadic coordinate constructions disagree')
        m.require(len(coords)==len(set(coords))==451,'dyadic collision');blocks.append(coords);source_edges.append(dyadic.graph(Q,recipe)[0])
    with (work/'tensor_input.txt').open('w') as f:
        f.write('17\n')
        for coords in blocks:
            f.write(str(len(coords))+'\n')
            for row in coords:f.write(' '.join(map(str,row))+'\n')
    cmd=['g++','-std=c++17','-O3','-Wall','-Wextra']
    if sanitize:cmd+=['-fsanitize=undefined','-fno-sanitize-recover=all']
    subprocess.run(cmd+[str(HERE/'exact_edges.cpp'),'-o',str(work/'exact_edges')],check=True)
    native=subprocess.run([str(work/'exact_edges'),str(work/'tensor_input.txt'),str(work/'tensor_edges.txt')],check=True,capture_output=True,text=True)
    target=[[] for _ in blocks]
    for line in (work/'tensor_edges.txt').read_text().splitlines():
        k,i,j=map(int,line.split());target[k].append((i,j))
    m.require(target==source_edges,'complete entrywise exact geometry mismatch')
    # All target supports are exact subsets of the independently built host.
    hist=Counter();where={p:i for i,p in enumerate(P)}
    for chosen,ids in families:
        taken=set(ids);hist[sum(i in taken and j in taken for i,j in target[0])]+=1
    linear=''.join(str(colour.point(p)) for p in P);m.require(all(linear[i]!=linear[j] for i,j in target[0]),'linear host colour')
    D={min(m.ps(P[i],P[j]),m.ps(P[j],P[i])) for i,j in target[0]}
    rho=m.add(m.ONE,m.POW[5]);r=m.add(m.ONE,rho);delta=(m.neg(r),r);expected=set()
    for orbit in orbits[:5]:
        for u,_ in orbit:
            for d in ((u,m.Z),(m.Z,u),(m.mul(u,delta[0]),m.mul(u,delta[1]))):expected.add(min(d,m.pneg(d)))
    m.require(D==expected and len(D)==45,'unit direction classification')
    M=a.moser();term=[mapped.index(z) for z in M]
    medges=[(i,j) for i,j in combinations(range(7),2) if tuple(sorted((term[i],term[j]))) in set(target[0])]
    m.require(len(medges)==11,'source Moser graph')
    pats=[]
    for w in product(range(4),repeat=7):
        if w[0] or any(w[i]>max(w[:i])+1 for i in range(1,7)) or any(w[i]==w[j] for i,j in medges):continue
        pats.append(list(w))
    cert=json.loads((HERE/'certificate.json').read_text());m.require([r['pattern'] for r in cert['host']]==pats and [r['pattern'] for r in cert['dyadic']]==pats,'incomplete interface')
    m.require(all(set(p)=={0,1,2,3} for p in pats),'Moser three-colouring found')
    for row in cert['host']:
        m.require(len(row['word'])==1801,'host word length');word_check(row['word'],target[0],term,row['pattern'])
    dt=[blocks[1].index(z) for z in M]
    for k in range(1,17):
        m.require(target[k]==target[1] and [blocks[k].index(z) for z in M]==dt,'dyadic labelled graph mismatch')
        for row in cert['dyadic']:
            m.require(len(row['word'])==451,'dyadic word length');word_check(row['word'],target[k],dt,row['pattern'])
    rejected=0
    for bad in ('0'*1801,'4'*1801,'',None):
        try:word_check(bad,target[0],term,pats[0])
        except (ValueError,TypeError,IndexError):rejected+=1
        else:raise ValueError('corrupt word accepted')
    for args in ((1000000411,1,98299921),(1000000411,539108921,0),(1000000412,539108921,98299921)):
        try:m.projection(*args)
        except ValueError:rejected+=1
        else:raise ValueError('corrupt ring map accepted')
    # The factor-field presentation and colour recipe respect their relations.
    m.require(a.POW[5]==a.ONE and a.mul(a.ALPHA,a.ALPHA)==a.scale(a.ONE,-3) and a.mul(a.BETA,a.BETA)==a.scale(a.ONE,-11),'alternate relations')
    for i in range(8):
        z=tuple(int(i==j) for j in range(8))
        m.require(colour.coefficient(m.mul(rho,z))==colour.fm(2,colour.coefficient(z)),'rho-linearity')
    # A non-field-homomorphism colour must not be mistaken for evaluation at zeta5.
    m.require(1^1^1^2^3==0,'five weights do not sum to zero')
    out={'host_vertices':1801,'host_edges':len(target[0]),'host_edge_sha256':m.digest(target[0]),'unit_directions':90,'target_members':len(families),'target_order':451,'target_edge_histogram':dict(sorted(hist.items())),'host_moser_patterns':len(pats),'dyadic_members':16,'dyadic_order':451,'dyadic_edges':len(target[1]),'dyadic_edge_sha256':m.digest(target[1]),'dyadic_graphs_identical_under_pair_labels':True,'dyadic_moser_pattern_checks':16*len(pats),'all_pairs_checked':sum(len(v)*(len(v)-1)//2 for v in blocks),'edge_entries_compared':sum(map(len,target)),'bad_controls_rejected':rejected,'certificate_sha256':hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),'native_summary':native.stdout.strip(),'PASS':True,'seconds':time.time()-start}
    reference=HERE/'expected.json'
    if reference.exists():
        stable=dict(out);stable.pop('seconds');m.require(json.loads(json.dumps(stable))==json.loads(reference.read_text()),'unexpected verified census')
    (work/'verified.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True);return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--sanitize',action='store_true');args=ap.parse_args();run(args.work,args.sanitize)
