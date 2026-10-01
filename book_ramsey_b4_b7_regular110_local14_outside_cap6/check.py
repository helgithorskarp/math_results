"""Separate binary-domain/edge-weight checker; six-books-3, researcher.
Default imports neither generator, census nor form-recovery helpers.
"""
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
EDGES=tuple(combinations(range(8),2))
POSITION={pair:index for index,pair in enumerate(EDGES)}
PAIRS={2:((0,1),(0,1)),1:((0,1),(0,2)),0:((0,1),(2,3))}

def need(ok, text):
    if not ok:
        raise RuntimeError(text)

def formula(mask, pairs):
    f = [set() for _ in range(8)]
    for bit, (u, v) in enumerate(EDGES):
        if mask >> bit & 1:
            f[u].add(v); f[v].add(u)
    p = list(map(set, pairs))
    matrix = [[0] * 10 for _ in range(10)]
    for low in range(2):
        matrix[low][low] = 4
        for c in range(8):
            value = (0 if c in p[low] else 3) - len(p[low] & f[c])
            matrix[low][c+2] = matrix[c+2][low] = value
    matrix[0][1] = matrix[1][0] = 2-len(p[0] & p[1])
    for c in range(8):
        matrix[c+2][c+2] = 5
        for d in range(c):
            shared = len(f[c] & f[d]) + sum(c in pair and d in pair for pair in p)
            matrix[c+2][d+2] = matrix[d+2][c+2] = (1 if d in f[c] else 4)-shared
    neighbors = [{c+2 for c in pair} for pair in p]
    neighbors += [{d+2 for d in f[c]} | {low for low in range(2) if c in p[low]} for c in range(8)]
    need(list(map(len,neighbors)) == [2,2]+[3]*8, 'Cubic degree bridge')
    return matrix, neighbors

def group(intersection):
    swaps = ({2: [(0,1),(2,3),(3,4),(4,5),(5,6),(6,7)],
              1: [(1,2),(3,4),(4,5),(5,6),(6,7)],
              0: [(0,1),(2,3),(4,5),(5,6),(6,7)]})[intersection]
    generators = []
    for a,b in swaps:
        p = list(range(8)); p[a],p[b]=p[b],p[a]; generators.append(tuple(p))
    if intersection == 0:
        generators.append((2,3,0,1,4,5,6,7))
    identity=tuple(range(8)); result={identity}; todo=[identity]
    while todo:
        p=todo.pop()
        for g in generators:
            image=tuple(p[g[i]] for i in range(8))
            if image not in result:result.add(image);todo.append(image)
    target=sorted(PAIRS[intersection])
    need(all(sorted(tuple(sorted(p[i] for i in pair)) for pair in target)==target for p in result), 'Group changes pairs')
    return sorted(result)

def image(mask, permutation):
    return sum(1 << POSITION[tuple(sorted((permutation[u],permutation[v])))]
               for bit,(u,v) in enumerate(EDGES) if mask >> bit & 1)

def row_domain(matrix, neighbors, size, use_AB):
    rows=[]
    for word in range(1024):
        if word.bit_count()!=size:continue
        selected={i for i in range(10) if word >> i & 1}
        if any(matrix[i][j]<1 for i,j in combinations(selected,2)):continue
        if use_AB:
            outside=set(range(10))-selected
            if any(size > len(neighbors[i])+5-len(neighbors[i]&outside) for i in outside):continue
            if any(len(neighbors[i]&selected)<size-7 for i in selected):continue
        rows.append(tuple(sorted(selected)))
    return sorted(rows)

# Individual-edge recursion copied with attribution from d00a13612475ea701786203b280200c11a105106.
def single_edge_weights(degrees, capacities):
    """Decide successive edge weights, with remaining-capacity pruning."""
    pairs = [(u, v, capacities[u][v]) for u, v in combinations(range(10), 2)
             if capacities[u][v] and degrees[u] and degrees[v]]
    n = len(pairs)
    future = [[0] * 10 for _ in range(n + 1)]
    pending = [[[] for _ in range(10)] for _ in range(n + 1)]
    for k in range(n - 1, -1, -1):
        u, v, cap = pairs[k]
        future[k] = future[k + 1][:]
        future[k][u] += cap
        future[k][v] += cap
        pending[k] = [r[:] for r in pending[k + 1]]
        pending[k][u].append((v, cap))
        pending[k][v].append((u, cap))
    remaining = list(degrees)
    chosen = []

    def visit(k):
        if any(remaining[i] > future[k][i] for i in range(10)):
            return
        if k == n:
            if not any(remaining):
                yield tuple(chosen)
            return
        u, v, cap = pairs[k]
        if k == 0 or pairs[k - 1][0] != u:
            if any(remaining[i] > sum(min(c, remaining[j]) for j, c in pending[k][i])
                   for i in range(10) if remaining[i]):
                return
        lo = max(0, remaining[u] - future[k + 1][u], remaining[v] - future[k + 1][v])
        hi = min(cap, remaining[u], remaining[v])
        for weight in range(lo, hi + 1):
            remaining[u] -= weight
            remaining[v] -= weight
            if weight:
                chosen.append((u, v, weight))
            yield from visit(k + 1)
            if weight:
                chosen.pop()
            remaining[u] += weight
            remaining[v] += weight
    yield from visit(0)


def core_audit(binary,expected,compare):
    need(binary.get('complete') is True,'Incomplete binary core census')
    need([c['intersection'] for c in binary['alignments']]==[2,1,0],'Binary alignment coverage')
    profiles={(r['intersection'],r['F_mask']):r for r in expected['profiles']}
    need(len(profiles)==52 and [r['index'] for r in expected['profiles']]==list(range(52)), 'Core profile ids')
    if compare:
        import generate as author_generator
        _,_,author_raw=author_generator.core_census()
    totals=Counter();generated=[]
    for c in binary['alignments']:
        k=c['intersection'];pairs=PAIRS[k];masks=c['masks']
        need(all(type(x) is int and 0<=x<1<<28 for x in masks),'Malformed F mask')
        need(masks==sorted(set(masks)),'Repeated or unordered F masks')
        need(c['binary_words']==1 << (28-len(set(pairs))),'Binary word domain size')
        declared=next(r for r in expected['alignments'] if r['intersection']==k)
        need(c['fixed_degree_graphs']==declared['fixed_degree_graphs'] and len(masks)==declared['labeled_cores'],'Complete degree-domain count')
        digest=hashlib.sha256(json.dumps(masks,separators=(',',':')).encode()).hexdigest()
        need(digest==declared['labeled_masks_sha256'],'Binary/star complete core domains differ')
        if compare:need(masks==author_raw[str(k)],'Complete retained binary/star core sets differ')
        totals['binary_words']+=c['binary_words'];totals['fixed_alignment_cores']+=len(masks)
        g=group(k);need(len(g)==declared['stabilizer_size'],'Generated stabilizer count')
        unseen=set(masks);orbits=0
        while unseen:
            representative=min(unseen);orbit={image(representative,p) for p in g}
            need(orbit<=unseen,'Core orbit omission or overlap');unseen-=orbit;orbits+=1
            rec=profiles.get((k,representative))
            need(rec is not None and rec['orbit_size']==len(orbit),'Normalized core class differs')
            canonical,_=formula(representative,pairs);seen=set()
            for p in g:
                mask=image(representative,p)
                if mask in seen:continue
                seen.add(mask);current,_=formula(mask,pairs)
                low_map=([0,1] if k==2 else [pairs.index(tuple(sorted(p[i] for i in pair))) for pair in pairs])
                permutation=low_map+[p[c]+2 for c in range(8)]
                need(all(current[permutation[i]][permutation[j]]==canonical[i][j] for i in range(10) for j in range(10)), 'Typed normalization map differs')
                need(all(x>=0 for row in current for x in row),'Invalid nonnegative-core census')
                if compare:
                    import census as author_census
                    literal,_=author_census.local_matrix(mask,pairs)
                    need(current==literal,'Typed/full-adjacency core entries differ')
                    totals['core_entries_compared']+=100
                totals['core_normalization_entries']+=100
            matrix,neighbors=formula(representative,pairs)
            for size in (5,6,7,8):
                for stage,flag in [('before_AB',False),('after_AB',True)]:
                    domain=row_domain(matrix,neighbors,size,flag)
                    counts=dict(sorted(Counter(str(sum(i<2 for i in row)) for row in domain).items()))
                    need(counts==rec['row_counts'][str(size)][stage],'Independent miss-row census differs')
            generated.append(rec);totals['normalized_profiles']+=1
        need(orbits==declared['orbits'],'Core orbit count')
    need(totals['binary_words']==268435456 and totals['fixed_alignment_cores']==7320 and totals['normalized_profiles']==52,'Complete core coverage totals')
    return sorted(generated,key=lambda p:p['index']),totals


def selected_pairs(profile):
    matrix,neighbors=formula(profile['F_mask'],PAIRS[profile['intersection']])
    large=row_domain(matrix,neighbors,7,True);small=row_domain(matrix,neighbors,5,True)
    for first in large:
        a=[int(i in first) for i in range(10)]
        for second in small:
            b=[int(i in second) for i in range(10)]
            base=[[matrix[i][j]-a[i]*a[j]-b[i]*b[j] for j in range(10)] for i in range(10)]
            if any(x<0 for row in base for x in row):continue
            # Derive slack degrees from row sums, without the author's h formula.
            degrees=[sum(base[i])-4*base[i][i] for i in range(10)]
            if any(d<0 or d>sum(base[i])-base[i][i] for i,d in enumerate(degrees)):continue
            need(sum(degrees)==18,'Exact slack degree sum')
            capacities=[row[:] for row in base]
            if 0 not in first and 1 not in first:
                # Full joint-low miss count>=1, before removing the chosen rows.
                capacities[0][1]=capacities[1][0]=min(capacities[0][1],matrix[0][1]-1)
            yield first,second,base,degrees,capacities


def validate_certificate(certificate,profiles):
    need(certificate.get('dimension')==10,'Certificate dimension')
    vectors=certificate['vectors'];need(isinstance(vectors,list),'Vector pool type')
    seen=set()
    for vector in vectors:
        need(isinstance(vector,list) and len(vector)==10 and all(type(x) is int for x in vector),'Integer vector shape')
        need(any(vector) and gcd(*vector)==1,'Zero or nonprimitive vector')
        need(next(x for x in vector if x)>0,'Vector sign normalization')
        need(tuple(vector) not in seen,'Repeated vector');seen.add(tuple(vector))
    need(len(certificate['profiles'])==len(profiles),'Certificate profile coverage')
    for p,c in zip(profiles,certificate['profiles']):
        need(c['index']==p['index'],'Certificate profile id')
        references=c['vector_indices']
        need(isinstance(references,list) and all(type(i) is int and 0<=i<len(vectors) for i in references),'Vector index')
        need(len(set(references))==len(references),'Repeated profile vector')
    return vectors


def integer_form(vector):
    return (tuple(x*x for x in vector),tuple((i,j,2*vector[i]*vector[j]) for i,j in combinations(range(10),2) if vector[i] and vector[j]))


def is_negative(matrix,data):
    diagonal,off=data
    return sum(diagonal[i]*matrix[i][i] for i in range(10))+sum(c*matrix[i][j] for i,j,c in off)<0


def residual(base,degrees,weights):
    matrix=[row[:] for row in base];incident=[0]*10
    for i,j,weight in weights:
        need(type(weight) is int and weight>0 and 0<=i<j<10,'Weighted edge')
        matrix[i][j]-=weight;matrix[j][i]-=weight;incident[i]+=weight;incident[j]+=weight
    need(incident==degrees and all(x>=0 for row in matrix for x in row),'Literal weighted-slack incidence')
    need(all(sum(matrix[i])==4*matrix[i][i] for i in range(10)),'Residual row sum')
    return matrix


def run(binary_path,compare=False,progress=None):
    expected=json.loads((HERE/'expected.json').read_text())
    certificate=json.loads((HERE/'negative_vectors.json').read_text())
    binary=json.loads(Path(binary_path).read_text())
    profiles,totals=core_audit(binary,expected,compare)
    vectors=validate_certificate(certificate,profiles)
    need(len(vectors)==expected['unique_vectors'] and
         max(abs(x) for vector in vectors for x in vector)==expected['max_absolute_vector_entry'],'Declared vector statistics')
    state_hash=hashlib.sha256();pair_hash=hashlib.sha256()
    for profile,cert in zip(profiles,certificate['profiles']):
        forms=[integer_form(vectors[i]) for i in cert['vector_indices']]
        actual_pairs=list(selected_pairs(profile));last=None;case_records=[]
        if compare:
            import generate as author
            authored={(a,b):(base,degree,cap) for a,b,base,degree,cap in author.selected_cases(profile)}
            need(set(authored)=={(a,b) for a,b,_,_,_ in actual_pairs},'Complete selected-pair sets differ')
        for first,second,base,degrees,capacities in actual_pairs:
            totals['selected_pairs']+=1
            pair_hash.update(json.dumps([profile['index'],first,second],separators=(',',':')).encode()+b'\n')
            direct=any(x<0 for row in capacities for x in row)
            domain=([] if direct else sorted(single_edge_weights(degrees,capacities)))
            need(len(set(domain))==len(domain),'Duplicate individual-edge assignment')
            if compare:
                gen_base,gen_degree,gen_cap=authored[first,second]
                need((base,degrees,capacities)==(gen_base,gen_degree,gen_cap),'Independent base/degree/cap formulas differ')
                generated=author.states(gen_degree,gen_cap)
                need(domain==generated,'Complete weighted state sets differ')
            for weights in domain:
                matrix=residual(base,degrees,weights)
                if compare:
                    need(matrix==author.residual(gen_base,weights),'Residual entries differ')
                    totals['residual_entries_compared']+=100
                found=last is not None and is_negative(matrix,forms[last])
                if not found:last=next((i for i,f in enumerate(forms) if is_negative(matrix,f)),None)
                need(last is not None,'Missing strictly negative integer form')
                totals['negative_forms']+=1;totals['residual_matrices']+=1
                state_hash.update(json.dumps([profile['index'],first,second,weights,matrix],separators=(',',':')).encode()+b'\n')
            if direct:totals['direct_impossible_cut_cases']+=1
            case_records.append([sum(1<<i for i in first),sum(1<<i for i in second),len(domain),int(direct)])
        need(case_records==profile['cases'],'Complete case counts differ')
        if progress:
            Path(progress).write_text(json.dumps({'complete':False,'completed_profiles':profile['index']+1,
                'states':totals['residual_matrices'],'pairs':totals['selected_pairs']})+'\n')
        print(json.dumps({'completed_profiles':profile['index']+1,'pairs':totals['selected_pairs'],
                          'states':totals['residual_matrices']}),flush=True)
    need(totals['selected_pairs']==expected['selected_pairs']==861 and
         totals['residual_matrices']==totals['negative_forms']==expected['residual_matrices']==184066,'Complete weighted coverage')
    need(state_hash.hexdigest()==expected['state_matrix_sha256'] and
         pair_hash.hexdigest()==expected['pair_stream_sha256'],'Complete canonical stream hashes differ')
    return {'agent':'six-books-3','role':'researcher','complete':True,'generator_comparison':compare,
        'binary_core_source':'Exhaustive268435456-word binary_audit.cpp plus written orbit/necessity bridges.',
        'counts':dict(sorted(totals.items())),'state_matrix_sha256':state_hash.hexdigest(),
        'unique_vectors':len(vectors),'survivors':0}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--binary-audit',required=True,help='Complete stdout from binary_audit.cpp')
    parser.add_argument('--compare-generator',action='store_true');parser.add_argument('--progress')
    args=parser.parse_args();print(json.dumps(run(args.binary_audit,args.compare_generator,args.progress),sort_keys=True))
