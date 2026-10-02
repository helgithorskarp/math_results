"""Exact packed production of 54 one-family fronts and 37 sufficient cuts.

Original domains are immutable. The domain scan selects sufficient witnesses;
its failure is never used to assert feasibility of a residual target.
"""
import hashlib,json,resource,time
from itertools import combinations
from pathlib import Path
import producer_primitives as p

ROOT=Path(__file__).resolve().parent

def domains():
    for a,b in combinations(range(13),2):yield 'LOW',(1<<a)|(1<<b),0
    for a,b in combinations(range(13),2):yield 'HIGH',0,(1<<a)|(1<<b)
    for a in range(13):
        for b in range(13):
            if a!=b:yield 'MIXED',1<<a,1<<b

def conditional(prefix,lo,hi):
    columns=iter(p.s.truth_columns(11))
    values=[p.s.LOW if lo>>q&1 else p.s.HIGH if hi>>q&1 else next(columns) for q in range(13)]
    for a,b in prefix:p.s.transition(values,a,b)
    return values

def integer_word(x,word):
    for a,b in word:
        if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
    return x

def build(f):
    h21=f['prefix19']+f['maximum_word'];joint=f['joint_gate']
    words={'LOW':[p.tree_word(t,False)[0] for t in p.trees([3,4,8],[1,2])],
           'HIGH':[p.tree_word(t,True)[0] for t in p.trees([5,6,7,9,10],[11])]}
    image=sorted({integer_word(x,h21) for x in range(8192)})
    if len(image)!=246:raise ValueError('complete H21 image differs')
    columns=list(p.s.truth_columns(13))
    for a,b in h21+[joint]:columns[a],columns[b]=columns[a]&columns[b],columns[a]|columns[b]
    ranks={q:sum(1<<x for x in range(8192) if x.bit_count()>=13-q) for q in range(13)}
    roots=[];exclusions=[];unclosed=[]
    for side in ['LOW','HIGH']:
        core=list(range(2,12)) if side=='LOW' else list(range(1,11))
        held=[0,1,12] if side=='LOW' else [0,11,12]
        for i,word in enumerate(words[side]):
            prefix=h21+[joint]+word;full=list(columns)
            for a,b in word:full[a],full[b]=full[a]&full[b],full[a]|full[b]
            if any(full[q]!=ranks[q] for q in held):raise ValueError('held full-cube rank differs')
            states=sorted({sum((integer_word(x,[joint]+word)>>q&1)<<j for j,q in enumerate(core)) for x in image})
            root={'id':len(roots),'side':side,'genealogy':i,'word':word,
                  'prefix_length':len(prefix),'prefix_sha256':p.digest(prefix),
                  'remaining_budget':44-len(prefix),'held_physical_ports':held,
                  'physical_core_ports':core,'image_size':len(states),'image_sha256':p.digest(states)}
            roots.append(root);proof=None
            for family,lo,hi in domains():
                record=p.record_for(prefix,lo,hi);c=record[4]+record[5]
                base={'root_id':root['id'],'original_family':family,'original_masks':[lo,hi],
                      'record':record,'pruning':p.prune(prefix,record)} if c>=9 else None
                if c>=10:
                    proof={**base,'kind':'DELETION_COST_GE10','total_lower_bound':35+c};break
                if c!=9:continue
                values=conditional(prefix,lo,hi)
                free=[q for q,x in enumerate(values) if not isinstance(x,str)]
                for q in free:
                    cut=all(not (values[r]&~values[q]) if r<q else not (values[q]&~values[r]) for r in free if r!=q)
                    diff=full[q]^ranks[q]
                    if cut and diff:
                        witness=(diff&-diff).bit_length()-1
                        proof={**base,'kind':'TIGHT_FREE_CUT','physical_free_port':q,
                               'global_Boolean_witness':witness,'actual_bit':(full[q]>>witness)&1,
                               'sorted_bit':(ranks[q]>>witness)&1};break
                if proof is not None:break
            if proof is None:
                unclosed.append({**root,'core_states':states})
            else:exclusions.append(proof)
    if len(roots)!=54 or len(exclusions)!=37 or len(unclosed)!=17:
        raise ValueError('new sufficient 54-to-17 packet differs; no frontier inference')
    cert={'schema':'native-one-sided-forest-certificate-v1','agent':'six-sorting-2','role':'researcher',
          'n':13,'size_budget':44,'fixture_sha256':hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
          'family_words':words,'roots':roots,'exclusions':exclusions,
          'retained_root_ids':[r['id'] for r in unclosed]}
    targets={'schema':'native-one-sided-residual-targets-v1','agent':'six-sorting-2','role':'researcher',
             'scope':'Necessary literal targets only; no feasibility assertion.', 'targets':unclosed}
    return cert,targets

def main():
    start=time.monotonic();f=json.loads((ROOT/'fixture.json').read_text())
    for name,pin in f['primitive_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=pin:raise ValueError('primitive provenance differs')
    cert,targets=build(f)
    raw=json.dumps(cert,separators=(',',':'))+'\n'
    (ROOT/'certificate.json').write_text(raw)
    (ROOT/'targets.json').write_text(json.dumps(targets,separators=(',',':'))+'\n')
    print(json.dumps({'agent':'six-sorting-2','role':'researcher','status':'EXACT54_FRONTS37_OBSTRUCTIONS17_TARGETS_GENERATED',
      'fronts':54,'obstructions':37,'retained':17,'certificate_bytes':len(raw.encode()),
      'certificate_sha256':hashlib.sha256(raw.encode()).hexdigest(),
      'targets_sha256':hashlib.sha256((ROOT/'targets.json').read_bytes()).hexdigest(),
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))

if __name__=='__main__':main()
