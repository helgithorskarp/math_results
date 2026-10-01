"""Independent graph reconstruction, native search and literal certificate replay."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import random
import subprocess
from anchors import model,matrix_census
from common import require,canonical
from common import unique_object
from ordinary import product4

def graph(lengths):
    data=model(lengths)
    words=data['candidates']
    pairs=tuple(frozenset(combinations(q,2)) for q in words)
    neighbors=tuple(frozenset(j for j in range(len(words)) if i!=j and pairs[i].isdisjoint(pairs[j]))
                    for i in range(len(words)))
    # A different direct intersection test checks every graph entry.
    require(all((j in neighbors[i])==(i!=j and len(set(words[i])&set(words[j]))<=1)
                for i in range(len(words)) for j in range(len(words))),'compatibility mismatch')
    return data,neighbors

def encode(name,neighbors,target):
    return ' '.join([name,str(len(neighbors)),str(target)]+[format(sum(1<<j for j in row),'x') for row in neighbors])+'\n'

def native(binary,inputs,cap=200000):
    p=subprocess.run([str(binary),str(cap),'10'],input=inputs,text=True,capture_output=True,timeout=30)
    require(p.returncode==0 and not p.stderr,'native run incomplete or diagnostic: '+p.stderr)
    return p.stdout

def tree_check(tree,neighbors,target,available=None,depth=0):
    require(depth<target and type(tree)is list,'false negative clique leaf/malformed node')
    remaining=set(range(len(neighbors))) if available is None else set(available)
    nodes=1
    for item in tree:
        require(type(item)is list and len(item)==2 and type(item[0])is int and item[0] in remaining,'invalid branch')
        v,child=item
        nodes+=tree_check(child,neighbors,target,remaining&neighbors[v],depth+1)
        remaining.remove(v)
    # Vertex-first first-fit coloring, rebuilt rather than read from a certificate.
    groups=[]
    for v in sorted(remaining):
        for group in groups:
            if not (neighbors[v]&group): group.add(v);break
        else:groups.append({v})
    require(set().union(*groups) == remaining if groups else not remaining,'incomplete proper coloring')
    require(sum(map(len,groups))==len(remaining) and all(not(neighbors[v]&group) for group in groups for v in group),
            'invalid color classes')
    require(depth+len(groups)<target,'terminal color bound insufficient')
    return nodes

def packing(quads):
    quads=tuple(tuple(sorted(q)) for q in quads)
    require(len(quads)==len(set(quads)) and all(len(q)==len(set(q))==4 and all(type(x)is int and 0<=x<17 for x in q) for q in quads),'invalid packing blocks')
    pairs=Counter(p for q in quads for p in combinations(q,2))
    require(not pairs or set(pairs.values())=={1},'repeated pair')
    rep=tuple(sum(x in q for q in quads) for x in range(17))
    require(max(rep)<=5,'invalid replication')
    H={x for x,n in enumerate(rep) if n<5}
    leave=set(combinations(range(17),2))-set(pairs)
    e=sum(set(p)<=H for p in leave); m=sum(not(set(p)&H) for p in leave)
    return dict(blocks=len(quads),replications=rep,deficits=tuple(sorted((5-rep[x] for x in H),reverse=True)),
                high_leave=e,low_leave=m,leave_pairs=len(leave),quad_sha256=sha256(canonical(quads)).hexdigest())

def affine_all_profiles():
    original=[tuple(4*x+y for y in range(4)) for x in range(4)]
    original+=[tuple(4*x+(product4(slope,x)^offset) for x in range(4)) for slope in range(4) for offset in range(4)]
    examples=[]
    for k in range(5):
        quads=[tuple(16 if i<k and x==4*i else x for x in q) for i,q in enumerate(original)]
        examples.append(packing(quads))
    for changes in (((0,0),(4,0)),((0,0),(4,0),(8,5))):
        quads=list(original)
        for i,removed in changes:
            require(removed in quads[i],'positive switch point absent')
            quads[i]=tuple(16 if x==removed else x for x in quads[i])
        examples.append(packing(quads))
    require(len({x['deficits'] for x in examples})==7,'missing positive profile')
    for x in examples:
        require(x['blocks']==20 and x['low_leave']==0 and x['high_leave']==len(x['deficits'])-1,
                'positive all-profile identity fails')
    return examples

def controls(binary):
    rng=random.Random(832318); inputs=[]; truth=[]
    for number in range(64):
        rows=[set() for _ in range(8)]
        for u,v in combinations(range(8),2):
            if rng.randrange(2):rows[u].add(v);rows[v].add(u)
        target=1+number%9
        inputs.append(encode(str(number),rows,target))
        witnesses=[q for q in combinations(range(8),target) if all(v in rows[u] for u,v in combinations(q,2))]
        truth.append((rows,target,witnesses))
    rows=[set() for _ in range(128)];rows[126]={127};rows[127]={126}
    inputs.append(encode('64',rows,2));truth.append((rows,2,[(126,127)]))
    inputs.append(encode('65',rows,3));truth.append((rows,3,[]))
    stdout=native(binary,''.join(inputs)); lines=stdout.splitlines();require(len(lines)==66,'missing native controls')
    result=Counter()
    for i,(line,(rows,target,witnesses)) in enumerate(zip(lines,truth)):
        fields=line.split();require(fields[0]==str(i),'control id mismatch')
        require(fields[1]==('WITNESS' if witnesses else 'EMPTY'),'native/brute clique discrepancy')
        if witnesses:
            chosen=tuple(sorted(map(int,fields[3:])))
            require(len(chosen)==len(set(chosen))==target and chosen in witnesses,'invalid clique witness')
        result[fields[1]]+=1
    p=subprocess.run([str(binary),'0','10'],input=inputs[0],text=True,capture_output=True,timeout=10)
    require(p.returncode==2 and p.stderr=='INCOMPLETE: clique guard reached\n','zero guard reported a verdict/extra diagnostics')
    malformed=['bad 129 10\n','bad 1 0 0\n','bad 1 1 1\n','bad 2 2 2 0\n']
    errors=('invalid header','invalid header','invalid graph bits','asymmetric graph')
    for item,error in zip(malformed,errors):
        p=subprocess.run([str(binary)],input=item,text=True,capture_output=True,timeout=10)
        require(p.returncode==1 and p.stderr=='ERROR: '+error+'\n','malformed graph accepted/extra diagnostics')
    return dict(brute_graph_controls=64,word_boundary_controls=2,verdicts=dict(result),
                malformed_graphs_rejected=4,zero_guard_incomplete=True,stdout_sha256=sha256(stdout.encode()).hexdigest())

def audit(binary,certificate_path):
    blob=certificate_path.read_bytes()
    require(sha256(blob).hexdigest()=='2555b641beb988c70160161ffce7dcec9b1b1b9630874851949bc9e03d5fd7dc','review1certificate pin mismatch')
    certificate=json.loads(blob,object_pairs_hook=unique_object)
    require(set(certificate)=={'format','models','target'} and certificate['target']==10
            and certificate['format']=='rebuild-color-branch-v1' and len(certificate['models'])==2,'invalid global certificate')
    results=[]; inputs=[]; models=[]
    for i,lengths in enumerate(((5,),(2,3))):
        data,neighbors=graph(lengths); record=certificate['models'][i]
        require(tuple(record['cycle_half_lengths'])==lengths and record['column_count']==len(neighbors)
                and record['column_sha256']==sha256(canonical(data['candidates'])).hexdigest(),'complete model input mismatch')
        require(set(record)=={'cycle_half_lengths','column_count','column_sha256','proof','proof_nodes','nine_clique'},'bad model fields')
        nodes=tree_check(record['proof'],neighbors,10)
        require(nodes==record['proof_nodes'],'source proof count mismatch')
        nine=record['nine_clique'];require(len(nine)==len(set(nine))==9 and all(type(v)is int and 0<=v<len(neighbors) for v in nine),'invalid source sharp clique')
        require(all(v in neighbors[u] for u,v in combinations(nine,2)),'false source sharp clique')
        restored=packing(data['anchors']+tuple(data['candidates'][v] for v in nine))
        require(restored['blocks']==19 and restored['replications'][15:17]==(5,5),'source sharp packing fails')
        inputs += [encode(str(2*i),neighbors,10),encode(str(2*i+1),neighbors,9)]
        models.append((data,neighbors))
        results.append(dict(lengths=lengths,vertices=len(neighbors),edges=sum(map(len,neighbors))//2,
                            candidate_sha256=sha256(canonical(data['candidates'])).hexdigest(),
                            source_proof_nodes=nodes,source_sharp_packing=restored))
    stdout=native(binary,''.join(inputs)); lines=stdout.splitlines();require(len(lines)==4,'missing complete native graph outputs')
    for i,line in enumerate(lines):
        fields=line.split();require(fields[0]==str(i),'native graph order mismatch')
        data,neighbors=models[i//2]; record=results[i//2]
        require(fields[1]==('EMPTY' if i%2==0 else 'WITNESS'),'maxclique9 verdict fails')
        if i%2==0:record['native_ten_nodes']=int(fields[2]);require(len(fields)==3,'surplus exclusion fields')
        else:
            chosen=tuple(map(int,fields[3:]));require(len(chosen)==len(set(chosen))==9 and all(0<=v<len(neighbors) for v in chosen),'invalid native nine')
            require(all(v in neighbors[u] for u,v in combinations(chosen,2)),'native nine not a clique')
            restored=packing(data['anchors']+tuple(data['candidates'][v] for v in chosen))
            require(restored['blocks']==19 and restored['replications'][15:17]==(5,5),'native sharp restoration fails')
            record.update(native_nine_nodes=int(fields[2]),native_nine=chosen,native_sharp_packing=restored)
    graph0=models[0][1]; proof=certificate['models'][0]['proof']; bad=deepcopy(proof);bad.pop()
    mutations=[(bad,graph0,10,None,0),([],graph0,10,None,0),([[len(graph0),[]]],graph0,10,None,0),
               ([],tuple(frozenset(range(10))-{v} for v in range(10)),10,None,0),([],(),10,(),10)]
    rejected=0
    for args in mutations:
        try:tree_check(*args)
        except ValueError:rejected+=1
        else:raise ValueError('false/corrupt color certificate accepted')
    return dict(models=results,literal_source_nodes=sum(x['source_proof_nodes'] for x in results),
                native_stdout_sha256=sha256(stdout.encode()).hexdigest(),certificate_sha256=sha256(blob).hexdigest(),
                certificate_corruption_controls=rejected,native_controls=controls(binary),
                matrix_census=matrix_census(),all_seven_positive_profiles=affine_all_profiles(),
                author_executable_imports=0,old_graph_theorems_needed_for_main_proof=0)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--native',type=Path,required=True);parser.add_argument('--certificate',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(audit(args.native.resolve(),args.certificate),indent=2))
