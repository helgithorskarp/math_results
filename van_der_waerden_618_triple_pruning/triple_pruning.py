"""Exact minority-row pruning for three-column moves in the period618 model.

The bound uses literal finite differences; residual scores use independent
truth-row bitsets. Generated model and detailed summaries are kept in build/.
No coloring in cases.json is progression-free. No solver is required.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import resource
import time

ROOT = Path(__file__).resolve().parent
MODEL_SHA256 = '093dd57840c2e9de0eb17dd3aa90df45cb9361e3dee72809a20c942145713986'
if not __debug__:
    raise RuntimeError('Run without -O: exact validation assertions are required.')


def model_edges():
    # Starts outside [0,308] globally complement; steps above309 reverse.
    edges = set()
    for a in range(309):
        for d in range(1,310):
            literals = set()
            for j in range(7):
                t = (a+j*d) % 618
                literals.add((t % 309+1)*(1 if t<309 else -1))
            if any(-v in literals for v in literals):
                continue
            edges.add(min(tuple(sorted(literals)),tuple(sorted(-v for v in literals))))
    edges = sorted(edges)
    raw = '309 94657\n'+''.join(' '.join(map(str,e))+' 0\n' for e in edges)
    assert len(edges) == 94657 and hashlib.sha256(raw.encode()).hexdigest() == MODEL_SHA256
    return edges


def profiles(edges, word):
    n = len(word)
    groups = [edge for edge in edges if len(edge) == 3]
    assert groups and len(groups)*3 == n
    group_of = {}
    for g, triple in enumerate(groups):
        assert len({abs(v) for v in triple}) == 3
        assert len({word[abs(v)-1] ^ int(v < 0) for v in triple}) == 2
        for lit in triple:
            assert abs(lit)-1 not in group_of
            group_of[abs(lit)-1] = g
    assert len(group_of) == n
    long = [edge for edge in edges if len(edge) != 3]
    assert all(len(edge) == 7 and len({group_of[abs(v)-1] for v in edge}) == 7 for edge in long)
    width = (len(long)+7)//8
    one = [bytearray(width) for _ in range(n)]
    zero = [bytearray(width) for _ in range(n)]
    count_rows = [bytearray(width) for _ in range(8)]
    for e, edge in enumerate(long):
        byte, bit = divmod(e,8)
        truth = [word[abs(v)-1] ^ int(v < 0) for v in edge]
        count_rows[sum(truth)][byte] |= 1 << bit
        for lit, value in zip(edge,truth):
            (one if value else zero)[abs(lit)-1][byte] |= 1 << bit
    one = [int.from_bytes(rows,'little') for rows in one]
    zero = [int.from_bytes(rows,'little') for rows in zero]
    counts = [int.from_bytes(rows,'little') for rows in count_rows]
    mono = counts[0] | counts[7]
    choices = []
    neutral = []
    single_hist = {}
    for g, triple in enumerate(groups):
        choices.append([])
        for mask in range(1,8):
            next_word = word[:]
            o = z = 0
            changed = []
            for i, lit in enumerate(triple):
                if mask & (1 << i):
                    variable = abs(lit)-1
                    next_word[variable] ^= 1
                    o |= one[variable]
                    z |= zero[variable]
                    changed.append(variable)
            if len({next_word[abs(v)-1] ^ int(v < 0) for v in triple}) != 2:
                continue
            assert o & z == 0
            f = o | z
            create = (counts[1] & o) | (counts[6] & z)
            after = (mono & ~f) | create
            score = mono.bit_count()-after.bit_count()
            single_hist[score] = single_hist.get(score,0)+1
            entry = {'group':g,'mask':mask,'ones':o,'zeros':z,'flipped':f,'create':create,
                     'changed_variables':changed,'score':score,'word':next_word}
            choices[-1].append(entry)
            if score == 0:
                neutral.append({'group':g,'mask':mask,'changed_variables':changed,
                                'halfword':''.join(map(str,next_word))})
        assert len(choices[-1]) == 5
    return choices, counts, mono, neutral, single_hist, long


def paired(rows, mono, a, b):
    return ((mono & ~(a['flipped'] | b['flipped']))
            | (a['create'] & ~b['flipped']) | (b['create'] & ~a['flipped'])
            | (rows[2] & a['ones'] & b['ones']) | (rows[5] & a['zeros'] & b['zeros']))




def row_controls():
    pairs_checked = triples_checked = 0
    for bits in itertools.product([0,1],repeat=7):
        q = sum(bits)
        V = lambda count:int(count in [0,7])
        for i,j in itertools.combinations(range(7),2):
            a,b = 1-2*bits[i],1-2*bits[j]
            K = V(q+a)+V(q+b)-V(q)-V(q+a+b)
            classified = (-1 if q in [0,7] else
                          1 if q in [1,6] and bits[i]!=bits[j] else
                          -1 if q in [2,5] and bits[i]==bits[j]==int(q==2) else 0)
            assert K == classified
            pairs_checked += 1
        for i,j,k in itertools.combinations(range(7),3):
            a,b,c = (1-2*bits[v] for v in [i,j,k])
            T = V(q)-V(q+a)-V(q+b)-V(q+c)+V(q+a+b)+V(q+a+c)+V(q+b+c)-V(q+a+b+c)
            positive = (q in [0,7] or
                        (q in [2,5] and sum(bits[v]==int(q==2) for v in [i,j,k])==2))
            assert T in [-1,0,1] and (T>0) == positive
            triples_checked += 1
    assert pairs_checked == 2688 and triples_checked == 4480
    return {'pair_curvatures':pairs_checked,'third_positive_classes':triples_checked,
            'all128_truth_words':True,'status':'COMPLETE_SEVEN_LITERAL_ROW_CONTROLS_PASSED'}


def triple_bad(rows, mono, a, b, c):
    fa, fb, fc = a['flipped'], b['flipped'], c['flipped']
    oa, ob, oc = a['ones'], b['ones'], c['ones']
    za, zb, zc = a['zeros'], b['zeros'], c['zeros']
    return ((mono & ~(fa | fb | fc))
            | (a['create'] & ~(fb | fc)) | (b['create'] & ~(fa | fc))
            | (c['create'] & ~(fa | fb))
            | (rows[2] & oa & ob & ~fc) | (rows[2] & oa & oc & ~fb)
            | (rows[2] & ob & oc & ~fa)
            | (rows[5] & za & zb & ~fc) | (rows[5] & za & zc & ~fb)
            | (rows[5] & zb & zc & ~fa)
            | (rows[3] & oa & ob & oc) | (rows[4] & za & zb & zc))


def triple_oracle_controls():
    rng = random.Random(618103125)
    checked = 0
    for trial in range(5):
        triples = [[3*g+1,-3*g-2,3*g+3] for g in range(7)]
        word = [0]*21
        for triple in triples:
            truth = rng.randrange(1,7)
            for i, lit in enumerate(triple):
                word[abs(lit)-1] = int(bool(truth & (1 << i))) ^ int(lit < 0)
        long = [[(3*g+rng.randrange(3)+1)*rng.choice([-1,1]) for g in range(7)] for _ in range(20)]
        for q in range(8):
            long.append([(3*g+1)*(1 if word[3*g] == int(g < q) else -1) for g in range(7)])
        choices, rows, mono, neutral, hist, long = profiles(triples+long,word)
        assert all(count.bit_count() for count in rows)
        for ga,gb,gc in itertools.combinations(range(7),3):
            for a in choices[ga]:
                for b in choices[gb]:
                    for c in choices[gc]:
                        candidate = word[:]
                        for v in a['changed_variables']+b['changed_variables']+c['changed_variables']:
                            candidate[v] ^= 1
                        direct = sum(len({candidate[abs(v)-1] ^ int(v < 0) for v in edge}) == 1 for edge in long)
                        assert triple_bad(rows,mono,a,b,c).bit_count() == direct
                        checked += 1
    assert checked == 21875
    return {'status':'MINORITY_ROW_TRIPLE_LITERAL_CONTROLS_PASSED',
            'triples_checked':checked,'explicit_initial_truth_counts':list(range(8)),
            'random_seed':618103125}


def analyze(edges, word, cutoff, seconds, start):
    choices, rows, mono, neutral, single_hist, long = profiles(edges,word)
    assert len(choices) == 103 and len(long) == 94554
    groups = [e for e in edges if len(e) == 3]
    group_of, position = {}, {}
    for g,e in enumerate(groups):
        for p,lit in enumerate(e):
            group_of[abs(lit)-1],position[abs(lit)-1] = g,p
    matrix = {(a,b):[0]*9 for a,b in itertools.combinations(range(103),2)}
    third_positive = {}
    row_hist = {}

    def budget():
        if time.monotonic()-start >= seconds-1:
            raise RuntimeError('Incomplete computation: no neighborhood exclusion.')

    def add_pair(va,vb,weight):
        ga,gb = group_of[va],group_of[vb]
        pa,pb = position[va],position[vb]
        if ga>gb:
            ga,gb,pa,pb = gb,ga,pb,pa
        assert ga<gb
        matrix[ga,gb][3*pa+pb] += weight

    def add_third(columns):
        t = tuple(sorted(columns))
        assert len(set(t)) == 3
        third_positive[t] = third_positive.get(t,0)+1

    for edge in long:
        variables = [abs(v)-1 for v in edge]
        truth = [word[abs(v)-1] ^ int(v<0) for v in edge]
        q = sum(truth)
        row_hist[q] = row_hist.get(q,0)+1
        if q in [0,7]:
            for va,vb in itertools.combinations(variables,2):
                add_pair(va,vb,-1)
            for cols in itertools.combinations([group_of[v] for v in variables],3):
                add_third(cols)
        elif q in [1,6]:
            minority = [v for v,t in zip(variables,truth) if t==int(q==1)]
            assert len(minority) == 1
            for v in variables:
                if v != minority[0]:
                    add_pair(minority[0],v,1)
        elif q in [2,5]:
            minority = [v for v,t in zip(variables,truth) if t==int(q==2)]
            assert len(minority) == 2
            add_pair(*minority,-1)
            for v in variables:
                if v not in minority:
                    add_third([group_of[minority[0]],group_of[minority[1]],group_of[v]])
        budget()
    for group in choices:
        group.sort(key=lambda a:(-a['score'],a['mask']))
    order = sorted(range(103),key=lambda g:(-choices[g][0]['score'],g))
    max_single = [max(a['score'] for a in group) for group in choices]
    max_pair, conditional, pair_hist = {}, {}, {}
    checked = 0
    for ga,gb in itertools.combinations(range(103),2):
        values = []
        to_b, to_a = [[] for _ in range(5)], [[] for _ in range(5)]
        for ia,a in enumerate(choices[ga]):
            for ib,b in enumerate(choices[gb]):
                K = sum(matrix[ga,gb][3*i+j] for i in range(3) if a['mask']&(1<<i)
                        for j in range(3) if b['mask']&(1<<j))
                to_b[ia].append(b['score']+K)
                to_a[ib].append(a['score']+K)
                independent_score = mono.bit_count()-paired(rows,mono,a,b).bit_count()
                assert a['score']+b['score']+K == independent_score
                pair_hist[independent_score] = pair_hist.get(independent_score,0)+1
                values.append(K)
                checked += 1
        max_pair[ga,gb] = max(values)
        conditional[ga,gb] = [max(values) for values in to_b]
        conditional[gb,ga] = [max(values) for values in to_a]
        budget()
    assert checked == 131325
    selected, bound_hist = [], {}
    coarse_remaining = 0
    for rank,t in enumerate(itertools.combinations(order,3)):
        a,b,c = sorted(t)
        positive = third_positive.get((a,b,c),0)
        coarse = (max_single[a]+max_single[b]+max_single[c]+max_pair[a,b]
                  +max_pair[a,c]+max_pair[b,c]+positive)
        anchors = []
        if coarse >= cutoff:
            coarse_remaining += 1
            anchors = [
                max(choices[a][i]['score']+conditional[a,b][i]+conditional[a,c][i] for i in range(5))+max_pair[b,c]+positive,
                max(choices[b][i]['score']+conditional[b,a][i]+conditional[b,c][i] for i in range(5))+max_pair[a,c]+positive,
                max(choices[c][i]['score']+conditional[c,a][i]+conditional[c,b][i] for i in range(5))+max_pair[a,b]+positive]
        upper = min([coarse]+anchors)
        bound_hist[upper] = bound_hist.get(upper,0)+1
        if upper >= cutoff:
            selected.append((rank,(a,b,c),upper))
        if rank % 1000 == 0:
            budget()
    total = math.comb(103,3)
    assert sum(bound_hist.values()) == total == 176851
    assert 0 < len(selected)*125 <= 200000, 'split a larger residual domain; no exclusion'
    residual_hist, best_moves = {}, []
    best_score = None
    for rank,columns,upper in selected:
        a,b,c = columns
        for ma,mb,mc in itertools.product(choices[a],choices[b],choices[c]):
            # Independent from the finite-difference bound: exact truth-row sets.
            score = mono.bit_count()-triple_bad(rows,mono,ma,mb,mc).bit_count()
            assert score <= upper
            residual_hist[score] = residual_hist.get(score,0)+1
            if best_score is None or score > best_score:
                best_score, best_moves = score, []
            if score == best_score:
                candidate = word[:]
                for v in ma['changed_variables']+mb['changed_variables']+mc['changed_variables']:
                    candidate[v] ^= 1
                best_moves.append({'rank':rank,'columns':list(columns),
                                   'masks':[ma['mask'],mb['mask'],mc['mask']],
                                   'score':score,'halfword':''.join(map(str,candidate))})
        budget()
    assert sum(residual_hist.values()) == len(selected)*125
    for move in best_moves:
        candidate = list(map(int,move['halfword']))
        direct = sum(len({candidate[abs(v)-1]^int(v<0) for v in e})==1 for e in long)
        assert direct == mono.bit_count()-move['score']
        assert all(len({candidate[abs(v)-1]^int(v<0) for v in e})==2 for e in groups)
        budget()
    selection = f'{total} {len(selected)}\n'+''.join(str(rank)+'\n' for rank,_,_ in selected)
    attained_cutoff = best_score >= cutoff
    return {'initial_long_cost':mono.bit_count(),'cutoff_score':cutoff,
            'columns':103,'single_moves_checked':515,'pair_moves_checked':checked,
            'all_pair_entries_matrix_vs_bitset_match':True,
            'total_triples':total,'total_moves':total*125,
            'coarse_remaining_triples':coarse_remaining,
            'pruned_below_cutoff_triples':total-len(selected),
            'pruned_below_cutoff_moves':(total-len(selected))*125,
            'remaining_triples':len(selected),'remaining_moves':len(selected)*125,
            'residual_moves_independently_checked':sum(residual_hist.values()),
            'maximum_selected_score':best_score,'cutoff_attained':attained_cutoff,
            'selection_sha256':hashlib.sha256(selection.encode()).hexdigest(),
            'selected_original_ranks':[rank for rank,_,_ in selected],
            'bound_histogram':bound_hist,'selected_score_histogram':residual_hist,
            'single_score_histogram':single_hist,'pair_score_histogram':pair_hist,
            'long_row_truth_count_histogram':row_hist,'best_selected_moves':best_moves,
            'basis_file_sha256':hashlib.sha256((''.join(map(str,word))+'\n').encode()).hexdigest(),
            'model_sha256':MODEL_SHA256,'complete_threshold_coverage':True,
            'no_template_family_exclusion':True,'length3704_witness':False}


def compact_evidence(document):
    """Canonical summaries; complete histograms stay in generated build output."""
    out = json.loads(json.dumps(document))
    results = out['results']
    for key in ['bound_histogram','selected_score_histogram','single_score_histogram',
                'pair_score_histogram']:
        histogram = results.pop(key)
        raw = json.dumps(histogram,sort_keys=True,separators=(',',':')).encode()
        results[key+'_summary'] = {'entries':sum(histogram.values()),
                                   'minimum':min(map(int,histogram)),
                                   'maximum':max(map(int,histogram)),
                                   'sha256':hashlib.sha256(raw).hexdigest()}
    for move in results['best_selected_moves']:
        halfword = move.pop('halfword')
        move['halfword_file_sha256'] = hashlib.sha256((halfword+'\n').encode()).hexdigest()
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case',choices=['preferred584','gate585'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--seconds',type=float,default=30)
    args = parser.parse_args()
    assert 0 < args.seconds <= 30
    assert not args.output.exists(), 'preserve previous evidence'
    start = time.monotonic()
    case = json.loads((ROOT/'cases.json').read_text())[args.case]
    word = list(map(int,case['halfword']))
    assert len(word)==309 and all(v in [0,1] for v in word)
    assert hashlib.sha256((case['halfword']+'\n').encode()).hexdigest()==case['file_sha256']
    controls = {'row_cases':row_controls(),'residual_bitset':triple_oracle_controls()}
    edges = model_edges()
    result = analyze(edges,word,case['cutoff_score'],args.seconds,start)
    assert result['initial_long_cost']==case['initial_long_cost']
    mathematical = {'agent':'six-vdw-1','role':'researcher','case':args.case,
                    'controls':controls,'results':result}
    if args.expected:
        expected = json.loads(args.expected.read_text())[args.case]
        assert compact_evidence(mathematical) == expected, 'deterministic expected evidence differs'
    word_output = args.output.with_suffix('.bits')
    assert not word_output.exists(), 'preserve previous word'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(mathematical,indent=2,sort_keys=True)+'\n')
    word_output.write_text(case['halfword']+'\n')
    print(json.dumps({'status':'COMPLETE_CHECKED_REDUCTION','case':args.case,
                      'initial_long_cost':result['initial_long_cost'],
                      'total_moves':result['total_moves'],
                      'pruned_moves':result['pruned_below_cutoff_moves'],
                      'selected_moves':result['remaining_moves'],
                      'maximum_selected_score':result['maximum_selected_score'],
                      'cutoff_score':result['cutoff_score'],
                      'cutoff_attained':result['cutoff_attained'],
                      'seconds':time.monotonic()-start,
                      'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=='__main__':
    main()
