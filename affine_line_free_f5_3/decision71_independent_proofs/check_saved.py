"""Independent full-formula reconstruction and stock-DRAT replay.

Reads completed author evidence without modifying it. Writes only reviewer
blocks/progress to --out. Partial runs cannot establish the exact theorem.
No reviewed point-model or evidence module is imported.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import time

COUNT=109676
DOMAIN_SHA='02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2'
SOURCE_SHA='d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'
MANIFEST_SHA='ec7fabe454c7a0e6297f3347de038028602a1aae81efd377ff4d938883af31c4'
CHUNK_SIZE=25
P3=tuple(product(range(5),repeat=3));INDEX={p:i+1 for i,p in enumerate(P3)}


def need(c,m):
    if not c:raise ValueError(m)


def sha(b):return hashlib.sha256(b).hexdigest()


def atomic(path,data):
    temp=path.with_name(path.name+f'.{os.getpid()}.tmp')
    temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(path)


def inverse(matrix):
    n=len(matrix)
    a=[[x%5 for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ValueError('singular interpolation matrix')
        a[j],a[pivot]=a[pivot],a[j]
        factor=pow(a[j][j],-1,5);a[j]=[x*factor%5 for x in a[j]]
        for i in range(n):
            if i!=j:
                factor=a[i][j];a[i]=[(x-factor*y)%5 for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]


def encode(clause):return (' '.join(map(str,clause))+' 0\n').encode('ascii')


class Formula:
    def __init__(self):
        lines={tuple(sorted(INDEX[tuple((x+t*(y-x))%5 for x,y in zip(p,q))]
                            for t in range(5))) for p,q in combinations(P3,2)}
        need(len(lines)==775,'independent line count')
        self.lines=sorted(lines)
        self.base=b''.join(encode([-v for v in L]) for L in self.lines)
        self.fibers={}
        for p in range(25):
            for n in range(5):
                # Expected subsets are found from Boolean words, independently
                # of the reviewed combinations-based cardinality generator.
                subsets=[tuple(5*p+j+1 for j,b in enumerate(bits) if b)
                         for bits in product((0,1),repeat=5)]
                upper=sorted(s for s in subsets if len(s)==n+1)
                lower=sorted(s for s in subsets if len(s)==6-n)
                clauses=[[-v for v in s] for s in upper]+[list(s) for s in lower]
                self.fibers[p,n]=(b''.join(encode(c) for c in clauses),len(clauses))

    def generate(self,word,total=71):
        need(len(word)==25 and set(word)<=set('01234') and sum(map(int,word))==total,'weight word')
        full=[i for i,c in enumerate(word) if c=='4']
        for abc in combinations(full,3):
            try:inverse([(1,p//5,p%5) for p in abc])
            except ValueError:continue
            gauge=abc;break
        else:raise ValueError('no noncollinear full-fiber triple')
        pieces=[self.base];count=778
        for p,c in enumerate(word):
            piece,n=self.fibers[p,int(c)];pieces.append(piece);count+=n
        pieces.extend(encode([-(5*p+1)]) for p in gauge)
        return f'p cnf 125 {count}\n'.encode('ascii')+b''.join(pieces),gauge,count


def check_native(checker,cnf,proof,timeout=120):
    start=time.monotonic()
    r=subprocess.run([str(checker),str(cnf),str(proof)],stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,timeout=timeout)
    accepted=r.returncode==0 and b's VERIFIED' in r.stdout.splitlines()
    return accepted,time.monotonic()-start,r.returncode,r.stdout


def case_input(index,domain,corpus,formula):
    row=domain[index];prefix=corpus/f'{index//1000:03d}'/f'case_{index:06d}'
    cnf=prefix.with_suffix('.cnf');proof=prefix.with_suffix('.drat')
    expected,gauge,clauses=formula.generate(row['weights'])
    need(cnf.read_bytes()==expected,f'CNF bytes disagree with independent geometry at {index}')
    cnf_hash=sha(expected);proof_bytes=proof.read_bytes();proof_hash=sha(proof_bytes)
    record=json.loads(prefix.with_suffix('.json').read_text())
    fields={'index':index,'type':row['type'],'weights':row['weights'],'gauge':list(gauge),
            'variables':125,'clauses':clauses,'input_catalogue_sha256':DOMAIN_SHA,
            'cnf_sha256':cnf_hash,'proof_sha256':proof_hash,'proof_bytes':len(proof_bytes),
            'status':'UNSAT_DRAT_VERIFIED'}
    need(all(record.get(k)==v for k,v in fields.items()),f'author record integrity at {index}')
    return cnf,proof,fields


def check_case(index,domain,corpus,checker,formula):
    cnf,proof,fields=case_input(index,domain,corpus,formula)
    before=(cnf.stat().st_size,cnf.stat().st_mtime_ns,proof.stat().st_size,proof.stat().st_mtime_ns)
    accepted,seconds,code,log=check_native(checker,cnf,proof)
    after=(cnf.stat().st_size,cnf.stat().st_mtime_ns,proof.stat().st_size,proof.stat().st_mtime_ns)
    need(before==after,f'input changed during check at {index}')
    need(accepted,f'stock proof checker rejected {index}, code={code}: '+log.decode(errors='replace')[-1000:])
    return {**{k:fields[k] for k in ('index','type','cnf_sha256','proof_sha256','proof_bytes')},
            'checker_seconds':seconds,'log_sha256':sha(log)}


def validate_records(records,block,domain):
    lo,hi=block['start'],block['stop']
    need(len(records)==hi-lo==block['count'],'block coverage')
    need([r['index'] for r in records]==list(range(lo,hi)),'missing, reordered or duplicated case')
    need(all(r['type']==domain[r['index']]['type'] for r in records),'case type differs')
    cnf_hash=sha(b''.join(bytes.fromhex(r['cnf_sha256']) for r in records))
    proof_hash=sha(b''.join(bytes.fromhex(r['proof_sha256']) for r in records))
    need(cnf_hash==block['ordered_cnf_hashes_sha256'] and proof_hash==block['ordered_proof_hashes_sha256']
         and sum(r['proof_bytes'] for r in records)==block['proof_bytes'],'published block differs')


def read_block(path,block,domain,code_hash,binary_hash):
    old=json.loads(path.read_text())
    need(old['status']=='INDEPENDENT_STOCK_BLOCK_VERIFIED' and old['runner_sha256']==code_hash
         and old['checker_sha256']==binary_hash and old['checker_source_sha256']==SOURCE_SHA
         and old['manifest_block']==block,'incompatible prior block')
    validate_records(old['records'],block,domain)
    counts={str(k):v for k,v in Counter(r['type'] for r in old['records']).items()}
    need(old['type_counts']==counts,'stored type counts differ')
    return old


def validate_chunk(saved,lo,hi,block,domain,corpus,formula,code_hash,binary_hash):
    need(saved['status']=='INDEPENDENT_STOCK_CHUNK_VERIFIED'
         and saved['start']==lo and saved['stop']==hi
         and saved['runner_sha256']==code_hash and saved['checker_sha256']==binary_hash
         and saved['checker_source_sha256']==SOURCE_SHA
         and saved['domain_sha256']==DOMAIN_SHA and saved['author_manifest_sha256']==MANIFEST_SHA
         and saved['manifest_block']==block,'incompatible partial checkpoint')
    records=saved['records']
    need(len(records)==hi-lo and [r['index'] for r in records]==list(range(lo,hi)),
         'partial checkpoint coverage')
    # Resumption uses only records produced by this exact frozen executable.
    # Reconstruct and hash their actual inputs again; no old author log is
    # used to infer a new proof acceptance. Complete blocks must additionally
    # match the published ordered digest, in validate_records above.
    for r in records:
        _,_,fields=case_input(r['index'],domain,corpus,formula)
        need(all(r[k]==fields[k] for k in ('index','type','cnf_sha256','proof_sha256','proof_bytes')),
             'partial checkpoint input mismatch')
        need(isinstance(r['checker_seconds'],(int,float)) and r['checker_seconds']>=0
             and len(bytes.fromhex(r['log_sha256']))==32,'malformed checker evidence')
    return records


def controls(formula,checker,corpus,out,known70):
    out.mkdir(exist_ok=True)
    original=corpus/'000'/'case_000000'
    empty=out/'empty.drat';empty.write_bytes(b'')
    false=out/'false.drat';false.write_bytes(b'a\0')
    for proof in (empty,false):
        accepted,_,_,_=check_native(checker,original.with_suffix('.cnf'),proof)
        need(not accepted,'invalid proof accepted')
    selected=set(json.loads(known70.read_text())['points'])
    need(len(selected)==70 and not any({v-1 for v in L}<=selected for L in formula.lines),'70-point input')
    word=''.join(str(sum(5*p+z in selected for z in range(5))) for p in range(25))
    data,gauge,_=formula.generate(word,70)
    heights=[next(z for z in range(5) if 5*p+z not in selected) for p in gauge]
    inv=inverse([(1,p//5,p%5) for p in gauge])
    coeff=[sum(a*b for a,b in zip(row,heights))%5 for row in inv]
    normalized={INDEX[(x,y,(z-coeff[0]-coeff[1]*x-coeff[2]*y)%5)] for x,y,z in (P3[p] for p in selected)}
    for line in data.decode().splitlines()[1:]:
        clause=list(map(int,line.split()))[:-1]
        need(any((abs(v) in normalized)==(v>0) for v in clause),'70-point assignment fails independent formula')
    sat=out/'known70.cnf';sat.write_bytes(data)
    accepted,_,_,_=check_native(checker,sat,original.with_suffix('.drat'))
    need(not accepted,'UNSAT trace accepted on checked SAT formula')
    need(not any({v-1 for v in L}<=selected for L in formula.lines),'70 control line')
    return {'known70_checked':True,'stock_negative_controls_rejected':3,
            'known70_cnf_sha256':sha(data)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--domain',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--corpus',type=Path,required=True);p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--checker-source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--start',type=int,default=0);p.add_argument('--stop',type=int,default=COUNT)
    p.add_argument('--pilot',action='store_true');p.add_argument('--known70',type=Path)
    p.add_argument('--summarize',action='store_true')
    p.add_argument('--seconds',type=float,default=0,
                   help='Stop cleanly after this runtime, at a durable 25-case boundary; 0 means unlimited.')
    args=p.parse_args();begun=time.monotonic()
    need(sha(args.domain.read_bytes())==DOMAIN_SHA,'domain provenance')
    need(sha(args.manifest.read_bytes())==MANIFEST_SHA,'complete public manifest provenance')
    need(sha(args.checker_source.read_bytes())==SOURCE_SHA,'stock checker source provenance')
    domain=json.loads(args.domain.read_text());manifest=json.loads(args.manifest.read_text())
    need(len(domain)==COUNT,'domain cardinality')
    need(0<=args.start<args.stop<=COUNT,'range')
    checker=args.checker.resolve();code_hash=sha(Path(__file__).read_bytes());binary_hash=sha(checker.read_bytes())
    args.out.mkdir(parents=True,exist_ok=True)
    if args.summarize:
        need(not args.pilot,'incompatible modes')
        blocks=manifest['blocks']
        need(blocks[0]['start']==0 and blocks[-1]['stop']==COUNT
             and all(a['stop']==b['start'] for a,b in zip(blocks,blocks[1:])),'full manifest cover')
        summaries=[];types=Counter()
        for b in blocks:
            saved=read_block(args.out/f"block_{b['start']:06d}_{b['stop']:06d}.json",b,domain,code_hash,binary_hash)
            types.update(r['type'] for r in saved['records'])
            summaries.append({**b,'summed_reviewer_checker_seconds':sum(r['checker_seconds'] for r in saved['records'])})
        need(sum(types.values())==COUNT and [types[i] for i in range(20)]==manifest['counts_by_type'],'whole-family type counts')
        result={'status':'COMPLETE_INDEPENDENT_STOCK_PROOF_REPLAY_VERIFIED','verified':COUNT,
                'complete_family':True,'independently_reconstructed_formulas':COUNT,
                'domain_sha256':DOMAIN_SHA,'author_manifest_sha256':MANIFEST_SHA,
                'runner_sha256':code_hash,'checker_sha256':binary_hash,'checker_source_sha256':SOURCE_SHA,
                'proof_bytes':sum(b['proof_bytes'] for b in blocks),'counts_by_type':[types[i] for i in range(20)],
                'blocks':summaries}
        atomic(args.out/'summary.json',result)
        print(json.dumps({k:v for k,v in result.items() if k!='blocks'},indent=2));return
    formula=Formula()
    if args.pilot:
        need(args.known70 is not None,'pilot needs 70-point control')
        control=controls(formula,checker,args.corpus,args.out,args.known70)
        chosen={0,251,252,9807,9808,20750,20807,20808,27418,27419,54837,54838,82256,82257,109675}
        types=set()
        for i,r in enumerate(domain):
            if r['type'] not in types:chosen.add(i);types.add(r['type'])
        records=[check_case(i,domain,args.corpus,checker,formula) for i in sorted(chosen)]
        first=records[0]
        tiny={'start':0,'stop':1,'count':1,'ordered_cnf_hashes_sha256':sha(bytes.fromhex(first['cnf_sha256'])),
              'ordered_proof_hashes_sha256':sha(bytes.fromhex(first['proof_sha256'])),'proof_bytes':first['proof_bytes']}
        validate_records([first],tiny,domain)
        bad_index={**first,'index':1};bad_hash={**first,'cnf_sha256':'00'*32}
        for bad in ([],[first,first],[bad_index],[bad_hash]):
            try:validate_records(bad,tiny,domain)
            except ValueError:continue
            raise ValueError('damaged review record accepted')
        control['damaged_block_controls_rejected']=4
        good={'status':'INDEPENDENT_STOCK_CHUNK_VERIFIED','start':0,'stop':1,
              'runner_sha256':code_hash,'checker_sha256':binary_hash,'checker_source_sha256':SOURCE_SHA,
              'domain_sha256':DOMAIN_SHA,'author_manifest_sha256':MANIFEST_SHA,
              'manifest_block':tiny,'records':[first]}
        validate_chunk(good,0,1,tiny,domain,args.corpus,formula,code_hash,binary_hash)
        damaged=[{**good,'records':[]},{**good,'records':[first,first]},
                 {**good,'records':[bad_index]},{**good,'records':[bad_hash]},
                 {**good,'runner_sha256':'00'*32},{**good,'checker_sha256':'00'*32},
                 {**good,'author_manifest_sha256':'00'*32},{**good,'stop':2}]
        for bad in damaged:
            try:validate_chunk(bad,0,1,tiny,domain,args.corpus,formula,code_hash,binary_hash)
            except ValueError:continue
            raise ValueError('damaged partial checkpoint accepted')
        control['damaged_chunk_controls_rejected']=len(damaged)
        result={'status':'INDEPENDENT_STOCK_REPLAY_PILOT_PASSED','cases':len(records),'records':records,
                'controls':control,'checker_sha256':binary_hash,'checker_source_sha256':SOURCE_SHA,
                'runner_sha256':code_hash,'seconds':time.monotonic()-begun,
                'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                'complete_family':False}
        atomic(args.out/'pilot.json',result)
        print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True);return
    blocks=[b for b in manifest['blocks'] if args.start<=b['start'] and b['stop']<=args.stop]
    need(blocks and blocks[0]['start']==args.start and blocks[-1]['stop']==args.stop
         and all(a['stop']==b['start'] for a,b in zip(blocks,blocks[1:])),'whole manifest blocks required')
    checked=0;fresh=0
    chunks=args.out/'chunks';chunks.mkdir(exist_ok=True)
    progress=args.out/f'progress_{args.start}_{args.stop}.json'
    for block in blocks:
        lo,hi=block['start'],block['stop'];path=args.out/f'block_{lo:06d}_{hi:06d}.json'
        if path.exists():
            read_block(path,block,domain,code_hash,binary_hash)
            checked+=hi-lo;continue
        records=[]
        for first in range(lo,hi,CHUNK_SIZE):
            last=min(first+CHUNK_SIZE,hi)
            chunkpath=chunks/f'chunk_{first:06d}_{last:06d}.json'
            if chunkpath.exists():
                saved=json.loads(chunkpath.read_text())
                part=validate_chunk(saved,first,last,block,domain,args.corpus,formula,code_hash,binary_hash)
            else:
                if args.seconds and time.monotonic()-begun>=args.seconds:
                    atomic(progress,{'status':'INCOMPLETE_DURABLE_CHECKPOINT','start':args.start,
                            'stop':args.stop,'next_index':first,'completed_block_cases':checked,
                            'current_block_checked':len(records),'fresh_checks':fresh,
                            'complete_family':False,'seconds':time.monotonic()-begun})
                    print(json.dumps({'status':'INCOMPLETE_DURABLE_CHECKPOINT','next_index':first,
                                      'fresh_checks':fresh}),flush=True)
                    return
                part=[check_case(i,domain,args.corpus,checker,formula) for i in range(first,last)]
                atomic(chunkpath,{'status':'INDEPENDENT_STOCK_CHUNK_VERIFIED','start':first,'stop':last,
                        'runner_sha256':code_hash,'checker_sha256':binary_hash,'checker_source_sha256':SOURCE_SHA,
                        'domain_sha256':DOMAIN_SHA,'author_manifest_sha256':MANIFEST_SHA,
                        'manifest_block':block,'records':part})
                fresh+=last-first
            records.extend(part)
            atomic(progress,{'status':'RUNNING','start':args.start,'stop':args.stop,'next_index':last,
                             'completed_block_cases':checked,'current_block_checked':len(records),
                             'fresh_checks':fresh,'seconds':time.monotonic()-begun})
        validate_records(records,block,domain)
        result={'status':'INDEPENDENT_STOCK_BLOCK_VERIFIED','manifest_block':block,
                'runner_sha256':code_hash,'checker_sha256':binary_hash,'checker_source_sha256':SOURCE_SHA,
                'type_counts':dict(Counter(r['type'] for r in records)),
                'summed_checker_seconds':sum(r['checker_seconds'] for r in records),'records':records}
        atomic(path,result);checked+=hi-lo
        print(json.dumps({'verified_block':[lo,hi],'completed':checked,'seconds':time.monotonic()-begun}),flush=True)
    atomic(progress,{'status':'INDEPENDENT_STOCK_RANGE_VERIFIED','start':args.start,'stop':args.stop,
                     'verified':checked,'complete_family':args.start==0 and args.stop==COUNT,
                     'fresh_checks':fresh,'seconds':time.monotonic()-begun,
                     'runner_sha256':code_hash,'checker_sha256':binary_hash})


if __name__=='__main__':main()
