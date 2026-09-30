"""Full independent census, cross-language witnesses, and exact matrix replay."""
from pathlib import Path
from itertools import permutations,combinations
from hashlib import sha256
import argparse,importlib.util,json,os,subprocess

BASE=Path(__file__).resolve().parent

def need(c,m):
    if not c:raise ValueError(m)

def downset(f,n):
    return all(not(f>>a&1) or all(not(a>>i&1) or (f>>(a^(1<<i))&1)
               for i in range(n)) for a in range(1<<n))

def orbit(f,n):
    return {sum(1<<sum(1<<p[i] for i in range(n) if a>>i&1)
                for a in range(1<<n) if f>>a&1) for p in permutations(range(n))}

def partition_valid(f,bins,n):
    if not downset(f,n):return False
    needed={a for a in range(1,1<<n) if f>>a&1};actual=[]
    s=max((sum(a>>i&1 for a in needed) for i in range(n)),default=0)
    if len(bins)!=s:return False
    for binmask in bins:
        if binmask<0 or binmask>>(1<<n):return False
        members=[a for a in range(1<<n) if binmask>>a&1]
        if not members or any(a&b for a,b in combinations(members,2)):return False
        actual.extend(members)
    return set(actual)==needed and len(actual)==len(needed)

def controls(work,census):
    # Independent exhaustive definition test on every 16-bit family.
    families={f for f in range(1<<16) if downset(f,4)};reference={}
    while families:
        f=min(families);images=orbit(f,4);need(images<=families,'overlapping reference orbit')
        families-=images;reference[f]=len(images)
    rows=[list(map(int,line.split())) for line in (work/'n4-witnesses.txt').read_text().splitlines()]
    need({r[0]:r[1] for r in rows}==reference and len(rows)==len(reference),'small full orbit mismatch')
    for f,o,s,nodes,*bins in rows:need(partition_valid(f,bins,4),'invalid small witness')
    f,o,s,nodes,*bins=next(r for r in rows if r[0]==65535)
    mutations=[bins[:-1],bins+[bins[0]],[bins[0]|bins[1]]+bins[1:],[bins[0]|1]+bins[1:]]
    need(all(not partition_valid(f,m,4) for m in mutations),'corrupt certificate accepted')
    # Authenticate all 720 byte-table permutation maps on all 64 basis bits.
    expected=bytes(sum(1<<p[i] for i in range(6) if a>>i&1)
                   for p in permutations(range(6)) for a in range(64))
    need((work/'n6-maps.bin').read_bytes()==expected,'permutation basis-map mismatch')
    counted=exceptions=trivial=0;previous=-1;records=0
    for line in (work/'n6-witnesses.txt').read_text().splitlines():
        f,o,s,nodes,*bins=map(int,line.split());need(f>previous and downset(f,6),'invalid family stream')
        previous=f;records+=1
        if f<=1:
            need(s==0 and not bins and o==1,'trivial normalization');trivial+=1
        elif nodes==-1:
            need(f==1991589575991295 and s==11 and o==12 and not bins,'unknown exception')
            exceptions+=1
        else:
            need(partition_valid(f,bins,6),'invalid full-census positive witness')
            need(s==len(bins) and 0<nodes<=2000000,'search metadata');counted+=1
    need((records,counted,exceptions,trivial)==(census['classes'],census['partition_certified'],1,2),
         'cross-language witness coverage mismatch')
    return {'n4_all_family_masks_tested':65536,'n4_classes':len(reference),
            'n4_labeled':sum(reference.values()),'permutation_basis_maps_checked':len(expected),
            'cross_language_full_witnesses_checked':counted,'rejected_partition_corruptions':4}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--record',action='store_true');args=parser.parse_args();work=args.work.resolve()
    need(work!=BASE.parent and BASE.parent not in work.parents,'generated work must be outside source repository')
    work.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    compiler=os.environ.get('CXX','g++');binary=work/'audit'
    subprocess.run([compiler,'-std=c++17','-O2','-Wall','-Wextra','-Wshadow','-Werror',
                    str(BASE/'audit.cpp'),'-o',str(binary)],check=True,env=env,timeout=60)
    def run(n):
        cmd=[str(binary),str(n),str(work/f'n{n}-witnesses.txt')]
        if n==6:cmd.append(str(work/'n6-maps.bin'))
        r=subprocess.run(cmd,check=True,capture_output=True,text=True,env=env,timeout=180)
        (work/f'n{n}.json').write_text(r.stdout);return json.loads(r.stdout)
    small=run(4);census=run(6)
    spec=importlib.util.spec_from_file_location('review5_exception',BASE/'exception.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    matrix=module.main();checks=controls(work,census)
    result={'agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'small_census':small,'six_census':census,'exception':matrix,'controls':checks,
            'fresh_full_witness_sha256':sha256((work/'n6-witnesses.txt').read_bytes()).hexdigest(),
            'permutation_map_sha256':sha256((work/'n6-maps.bin').read_bytes()).hexdigest(),
            'input_sha256':sha256((BASE/'input.json').read_bytes()).hexdigest()}
    if args.record:(BASE/'expected.json').write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads((BASE/'expected.json').read_text()),'expected evidence mismatch')
    print(json.dumps(result,indent=2)+'\n',end='')

if __name__=='__main__':main()
