"""Independent checked-arithmetic audit of the projected CNF, no producer import.

Every actual full-adder relation is exhaustively checked. Wiring is then
checked by binary-addition/count-tree induction, and every mathematical
condition is reconstructed from the pinned projection descriptor.
"""
import argparse
from collections import Counter
import copy
import hashlib
import itertools as it
import json
from pathlib import Path

PROJECTION_SHA = '0a5407af70b1711597b9bdd7a46753c78ee33a297f4812fc9b271172d6c2331a'
NEIGHBORHOOD_SHA = 'ece2f0c1a0ebf7f43fee80bd848b0ff082602e91f36bdc9946cff230e8a4ac25'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def canonical(data):
    return (json.dumps(data,sort_keys=True,indent=2)+'\n').encode()


def inverse(x):
    if type(x) is bool:
        return not x
    return -x


def literal(x,values):
    return x if type(x) is bool else values[abs(x)] == (x>0)


def normalize(rows):
    result = []
    for row in rows:
        if True in [x for x in row if type(x) is bool]:
            continue
        signs = set(x for x in row if type(x) is not bool)
        if signs & {-x for x in signs}:
            continue
        result.append(tuple(sorted(signs)))
    return result


def definitions(projection):
    upper = {}
    for block in projection['blocks']:
        upper.update({v:len(block['right']) for v in block['left']})
        upper.update({v:len(block['left']) for v in block['right']})
    margins = {}; index = 524
    for v,n in sorted(upper.items()):
        margins[str(v)] = list(range(index,index+n)); index += n
    need(index == 732,'margin allocation')
    monotone = [(-bits[i],bits[i-1]) for bits in margins.values() for i in range(1,len(bits))]
    expected = []
    for row in projection['residuals']:
        v = row['vertex']
        expected.append({'tag':f'degree-{v}','kind':'constant',
                         'left':row['subtract_variables']+margins.get(str(v),[]),'equals':row['constant']})
    for row in projection['density_equalities']:
        expected.append({'tag':f'density-{row["root"]}','kind':'constant',
                         'left':row['sum_variables'],'equals':row['equals']})
    for i,block in enumerate(projection['blocks']):
        L,R = block['left'],block['right']
        expected.append({'tag':f'balance-{i}','kind':'balance',
                         'left':[x for v in L for x in margins[str(v)]],
                         'right':[x for v in R for x in margins[str(v)]]})
        for mask,S in enumerate(block['subset_cuts'],1):
            expected.append({'tag':f'cut-{i}-{mask}','kind':'cut',
                             'left':[x for v in S for x in margins[str(v)]],
                             'right':[x for v in R for x in margins[str(v)][:len(S)]]})
    return margins,monotone,expected


def audit(meta,clauses,variables):
    need(meta['format'] == 'r55-projected-binary-backend-v1','format')
    need(meta['variables'] == variables and meta['clauses'] == len(clauses),'declared size')
    need(meta['physical_variables'] == 523 and meta['margin_variables'] == 208,'input classes')
    need(hashlib.sha256(canonical(meta['projection'])).hexdigest() == PROJECTION_SHA,'pinned entire mathematical descriptor')
    base = meta['base_clauses']; need(base == 70848,'base size')
    prefix = ('p cnf 523 70848\n'+''.join(' '.join(map(str,row))+' 0\n' for row in clauses[:base])).encode()
    need(hashlib.sha256(prefix).hexdigest() == NEIGHBORHOOD_SHA,'entire physical base')
    margins,monotone,expected = definitions(meta['projection'])
    need(meta['margins'] == margins,'literal margin variables')
    need(clauses[base:meta['monotone_end']] == normalize(monotone),'complete monotone prefix')
    claims = []
    for row in meta['constraints']:
        keys = ['tag','kind','left','equals'] if row['kind']=='constant' else ['tag','kind','left','right']
        claims.append({key:row[key] for key in keys})
    need(claims == expected and len(claims) == 93,'all 93 exact high-level constraints')
    owned = bytearray(len(clauses)); owned[:meta['monotone_end']] = b'\1'*meta['monotone_end']
    def cover(start,end):
        need(type(start) is int and type(end) is int and meta['monotone_end'] <= start <= end <= len(clauses),'valid clause interval')
        need(not any(owned[start:end]),'disjoint clause ownership')
        owned[start:end] = b'\1'*(end-start)
    truth_tests = 0
    fas = meta['fulladders']
    need(variables == 731+2*len(fas),'all auxiliary variables accounted for')
    for i,fa in enumerate(fas):
        s,c = fa['sum'],fa['carry']
        need((s,c) == (732+2*i,733+2*i),'fresh, ordered full-adder outputs')
        inputs = fa['inputs']; need(len(inputs) == 3,'ternary adder')
        need(all(type(x) is bool or (type(x) is int and 1 <= abs(x) < s) for x in inputs),'acyclic inputs')
        input_vars = sorted({abs(x) for x in inputs if type(x) is int})
        local_vars = input_vars+[s,c]; rows = clauses[fa['start']:fa['end']]
        need(all(set(map(abs,row)) <= set(local_vars) for row in rows),'local full-adder support')
        cover(fa['start'],fa['end'])
        for bits in it.product((False,True),repeat=len(local_vars)):
            values = dict(zip(local_vars,bits))
            cnf = all(any(literal(x,values) for x in row) for row in rows)
            correct = values[s]+2*values[c] == sum(literal(x,values) for x in inputs)
            need(cnf == correct,'exact full-adder relation, both directions')
            truth_tests += 1
    used_adders = set()
    def addition(record,left,right,initial=False):
        need(record['left'] == left and record['right'] == right and record['carry_in'] is initial,'word-add inputs/carry')
        indices = record['fulladders']; width = max(len(left),len(right))
        need(len(indices) == width,'word width')
        carry = initial; output = []
        for k,i in enumerate(indices):
            need(type(i) is int and 0 <= i < len(fas) and i not in used_adders,'owned full-adder')
            used_adders.add(i); fa = fas[i]
            need(fa['inputs'] == [left[k] if k<len(left) else False,
                                  right[k] if k<len(right) else False,carry],'full ripple wiring')
            output.append(fa['sum']); carry = fa['carry']
        output.append(carry)
        need(record['output'] == output,'exact addition output word')
        return output
    counts = meta['counts']; seen_inputs = set()
    for count in counts:
        inputs = count['inputs']; key = tuple(inputs)
        need(inputs == sorted(inputs) and key not in seen_inputs,'unique canonical count circuit')
        seen_inputs.add(key)
        need(all(type(x) is int and 1 <= abs(x) <= 731 for x in inputs),'count input domain')
        words = [[x] for x in inputs]; position = 0
        while len(words) > 1:
            following = []
            for k in range(0,len(words),2):
                if k+1 == len(words):
                    following.append(words[k])
                else:
                    need(position < len(count['additions']),'complete count tree')
                    following.append(addition(count['additions'][position],words[k],words[k+1]))
                    position += 1
            words = following
        need(position == len(count['additions']),'no extraneous count addition')
        need(count['output'] == (words[0] if words else []),'population count output')
    used_counts = set()
    def get_count(index,inputs):
        need(type(index) is int and 0 <= index < len(counts),'count reference')
        need(counts[index]['inputs'] == sorted(inputs),'mathematical input multiset')
        used_counts.add(index)
        return counts[index]['output']
    for row in meta['constraints']:
        A = get_count(row['left_count'],row['left'])
        if row['kind'] == 'constant':
            n = row['equals']
            tail = [[]] if not 0 <= n < (1<<len(A)) else [[x if n>>i&1 else inverse(x)] for i,x in enumerate(A)]
        else:
            B = get_count(row['right_count'],row['right']); width = max(len(A),len(B))
            left = A+[False]*(width-len(A)); right = B+[False]*(width-len(B))
            if row['kind'] == 'balance':
                tail = [clause for a,b in zip(left,right) for clause in ([inverse(a),b],[a,inverse(b)])]
            else:
                out = addition(row['comparison'],right,[inverse(x) for x in left],True)
                tail = [[out[-1]]]
        need(clauses[row['start']:row['end']] == normalize(tail),'exact terminal assertion')
        cover(row['start'],row['end'])
    need(used_adders == set(range(len(fas))) and used_counts == set(range(len(counts))),'all arithmetic used and checked')
    need(all(owned),'entire formula covered; no unexamined clause')
    return {'fulladders':len(fas),'fulladder_truth_assignments':truth_tests,'population_counts':len(counts),
            'constraint_kinds':dict(Counter(c['kind'] for c in claims)), 'monotonicity_clauses':len(monotone),
            'all_clauses_covered':len(clauses),'all_variables_covered':variables}


def controls(meta,clauses,variables):
    tests = []
    def reject(name,m,rows,v):
        try:
            audit(m,rows,v)
        except (ValueError,KeyError,IndexError):
            tests.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    rows = list(clauses); rows[meta['base_clauses']] = tuple(-x for x in rows[meta['base_clauses']])
    reject('reverse_margin_monotonicity',meta,rows,variables)
    bad = copy.deepcopy(meta); bad['constraints'].pop(); reject('omit_subset_cut',bad,clauses,variables)
    bad = copy.deepcopy(meta); bad['constraints'][2]['equals'] += 1; reject('change_degree_total',bad,clauses,variables)
    bad = copy.deepcopy(meta); bad['fulladders'][0]['sum'] += 2; reject('reuse_auxiliary',bad,clauses,variables)
    rows = list(clauses); i = meta['fulladders'][0]['start']; rows[i] = tuple(-x for x in rows[i])
    reject('corrupt_fulladder_clause',meta,rows,variables)
    rows = list(clauses); rows[-1] = tuple(-x for x in rows[-1]); reject('reverse_final_comparison',meta,rows,variables)
    bad = copy.deepcopy(meta); bad['clauses'] += 1; reject('append_unexamined_clause',bad,clauses+[(1,)],variables)
    return tests


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True); p.add_argument('--controls',action='store_true')
    a = p.parse_args(); raw = (a.work/'case.cnf').read_bytes(); lines = raw.decode().splitlines()
    header = lines[0].split(); need(header[:2] == ['p','cnf'] and len(header)==4,'header')
    variables,count = map(int,header[2:]); clauses = []
    for line in lines[1:]:
        row = list(map(int,line.split())); need(row and row[-1] == 0 and 0 not in row[:-1],'clause terminator')
        need(all(1 <= abs(x) <= variables for x in row[:-1]),'literal domain'); clauses.append(tuple(row[:-1]))
    need(len(clauses) == count,'count and EOF')
    meta = json.loads((a.work/'encoding.json').read_text())
    result = audit(meta,clauses,variables)
    comparison_tests = 0
    for width in range(1,9):
        modulus = 1<<width
        for left in range(modulus):
            for right in range(modulus):
                carry = (right+(modulus-1-left)+1)//modulus
                need(bool(carry) == (left <= right),'unsigned comparison identity')
                comparison_tests += 1
    result.update(status='EXACT_ARITHMETIC_AND_PROJECTION_CNF_AUDITED',formula_sha256=hashlib.sha256(raw).hexdigest(),
                  encoding_sha256=hashlib.sha256((a.work/'encoding.json').read_bytes()).hexdigest(),
                  unsigned_comparison_tests=comparison_tests,
                  controls=controls(meta,clauses,variables) if a.controls else [],
                  trust='pinned previously audited projection and neighborhood clause stream; current arithmetic independently checked; no solver verdict')
    with a.report.open('x') as f:
        json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()
