#!/usr/bin/env python3
"""Small exhaustive/boundary/native/reference and analytic-bridge audits."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
import subprocess
import tempfile
import time
from pathlib import Path

def local_module(name, filename):
    path = Path(__file__).resolve().parent/filename
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

check = local_module('degree_eighteen_checker','verify.py')
gen = local_module('degree_eighteen_generator','generate.py')

def require(value, message):
    if not value:
        raise ValueError(message)

def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first,length-1):
                yield (first,)+rest

def profile_audit():
    count, accepted = 0, [0,0]
    for values in compositions(8,16):
        count += 1
        active = sum(v > 0 for v in values)
        if any(3*v > active-1 for v in values if v):
            continue
        nonzero = sorted(v for v in values if v)
        require(nonzero in ([1]*8,[1]*6+[2]),'omitted feasible degree profile')
        accepted[nonzero[-1]-1] += 1
    require(count == 490314 and accepted == [12870,80080],'deficit composition mismatch')
    return count,accepted

def graph_audit():
    count = 0
    for n in range(6):
        pairs = list(it.combinations(range(n),2))
        expected = {}
        for mask in range(1 << len(pairs)):
            edges = frozenset(e for j,e in enumerate(pairs) if mask & (1 << j))
            degrees = tuple(sum(p in e for e in edges) for p in range(n))
            expected.setdefault(degrees,set()).add(edges)
            count += 1
        for degrees,graphs in expected.items():
            require(check.degree_graphs(degrees) == graphs,'degree generator disagrees with all edge subsets')
    require(count == 1100,'small graph count mismatch')
    try:
        check.degree_graphs([3]*8,node_cap=1)
    except RuntimeError as e:
        require('INCOMPLETE' in str(e),'wrong degree cap failure')
    else:
        raise ValueError('degree guard ignored')
    return count

def swap_audit():
    plane = gen.normalization()['first_plane']
    arcs4 = [gen.word(a) for a in it.combinations(range(16),4)
             if all((gen.word(a)&line).bit_count() <= 2 for line in plane)]
    arcs5 = [gen.word(a) for a in it.combinations(range(16),5)
             if all((gen.word(a)&line).bit_count() <= 2 for line in plane)]
    require(len(arcs4) == 840 and len(arcs5) == 288,'geometric baseline mismatch')
    count = 0
    for line in plane:
        for points in it.combinations(gen.points(line),3):
            triple = gen.word(points)
            replacement = triple | (3 << 16)
            first = [b | (1 << 17) for b in plane if b != line]
            second_possible = [b | (1 << 16) for b in arcs4 if (b&triple).bit_count() <= 1]
            require(all((replacement&b).bit_count() <= 2 for b in first+second_possible+arcs5),
                    'collinear-triangle replacement is incompatible')
            count += 1
    require(count == 80,'incomplete swap domains')
    return count

def native_text(ncols,rows,excluded):
    width = len(rows[0]) if rows else 1
    lines = [f'{ncols} {len(rows)} {width}']
    lines += [' '.join(map(str,[j]+list(r))) for j,r in enumerate(rows)]
    lines += ['1',' '.join(map(str,[0,len(excluded)]+list(excluded)))]
    return '\n'.join(lines)+'\n'

def brute(ncols,rows,excluded):
    target = set(range(ncols))-set(excluded)
    answers = set()
    for mask in range(1 << len(rows)):
        selected = [j for j in range(len(rows)) if mask & (1 << j)]
        values = [p for j in selected for p in rows[j]]
        if len(values) == len(set(values)) and set(values) == target:
            answers.add(tuple(selected))
    return answers

def native_audit(engines):
    hypergraphs,rejections,incomplete = 0,0,0
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        inp,out = directory/'matrix.txt',directory/'answers.jsonl'
        fixtures = [(0,[],[]),(1,[],[]),(1,[(0,)],[]),(2,[(0,1)],[])]
        for n in range(3,7):
            full = list(it.combinations(range(n),2))[:9]
            fixtures += [(n,full,[]),(n,full[::2],[]),(n,full,[0]),(n,full,list(range(n)))]
        require(len(fixtures) == 20,'fixture count mismatch')
        for n,rows,excluded in fixtures:
            inp.write_text(native_text(n,rows,excluded))
            expected = brute(n,rows,excluded)
            for engine in engines:
                result = subprocess.run([str(engine),str(inp),str(out)],capture_output=True,text=True)
                require(result.returncode == 0,'small cover failed')
                answer = json.loads(out.read_text())
                require({tuple(a) for a in answer['covers']} == expected and
                        len(answer['covers']) == len(expected),'native covers differ from direct subsets')
            hypergraphs += 1
        malformed = ['121 0 1\n0\n','120 841 6\n','120 1 7\n',
                     '2 1 2\n0 0 0\n1\n0 0\n',
                     '2 1 2\n65536 0 1\n1\n0 0\n',
                     '2 2 1\n0 0\n0 1\n1\n0 0\n',
                     '2 1 2\n0 0 2\n1\n0 0\n',
                     '2 1 2\n0 0\n',
                     '2 1 2\n0 0 1\n1\n1 0\n',
                     '2 1 2\n0 0 1\n1\n0 2 0 0\n',
                     native_text(2,[(0,1)],[])+'trailing\n',
                     '0 0 1\n11856\n']
        for text in malformed:
            inp.write_text(text)
            for engine in engines:
                result = subprocess.run([str(engine),str(inp),str(out)],capture_output=True,text=True)
                require(result.returncode != 0,'native malformed input accepted')
                rejections += 1
        inp.write_text(native_text(2,[(0,1)],[]))
        for engine in engines:
            result = subprocess.run([str(engine),str(inp),str(out),'1'],capture_output=True,text=True)
            require(result.returncode != 0 and 'INCOMPLETE' in result.stderr,'native node guard ignored')
            incomplete += 1
            result = subprocess.run([str(engine),str(inp),str(out),'200001'],capture_output=True,text=True)
            require(result.returncode != 0,'native permitted raised node cap')
            rejections += 1
    return hypergraphs,rejections,incomplete

def witness_audit():
    path = Path(__file__).resolve().parent/'witness62.json'
    degrees = check.check_witness(path)
    witness = json.loads(path.read_text())
    mutations = []
    duplicate = dict(witness,words=witness['words'][:-1]+[witness['words'][0]])
    mutations.append(duplicate)
    bad_mask = dict(witness,words=witness['words'][:-1]+[1 << 18])
    mutations.append(bad_mask)
    mutations.append(dict(witness,y=17))
    mutations.append(dict(witness,words=witness['words'][:-1]))
    with tempfile.TemporaryDirectory() as temp:
        p = Path(temp)/'bad.json'
        for value in mutations:
            p.write_text(json.dumps(value))
            try:
                check.check_witness(p)
            except ValueError:
                pass
            else:
                raise ValueError('malformed fixture accepted')
    return degrees,len(mutations)

def reference_covers(allowed,leave):
    rows = [gen.pair_mask(b) for b in allowed]
    containing = [0]*120
    for j,row in enumerate(rows):
        for k in gen.bits(row):
            containing[k] |= 1 << j
    conflicts = []
    for row in rows:
        conflict = 0
        for k in gen.bits(row):
            conflict |= containing[k]
        conflicts.append(conflict)
    available = (1 << len(rows))-1
    for k in gen.bits(leave):
        available &= ~containing[k]
    nodes,answers = 0,set()
    started = time.monotonic()
    def visit(left,active,chosen):
        nonlocal nodes
        nodes += 1
        if nodes > 200000 or (nodes % 256 == 0 and time.monotonic()-started > 10):
            raise RuntimeError('INCOMPLETE Python reference')
        if not left:
            require(len(chosen) == 18,'invalid reference cover size')
            answers.add(tuple(sorted(allowed[j] for j in chosen)))
            return
        options,best = 0,len(rows)+1
        for k in gen.bits(left):
            choices = active&containing[k]
            count = choices.bit_count()
            if count < best:
                options,best = choices,count
                if count <= 1:
                    break
        for j in gen.bits(options):
            require(rows[j]&left == rows[j],'reference active row invalid')
            visit(left^rows[j],active&~conflicts[j],chosen+(j,))
    visit(((1 << 120)-1)^leave,available,())
    return answers,nodes

def geometric_pilot(domain_path,engines):
    expected = json.loads((Path(__file__).resolve().parent/'expected.json').read_text())
    require(hashlib.sha256(domain_path.read_bytes()).hexdigest() == expected['domain_sha256'],
            'pilot domain differs from completely checked domain')
    domain = json.loads(domain_path.read_text())
    completion = [r for r in domain['leaves'] if r[5] == 1]
    excluded = [r for r in domain['leaves'] if r[5] == 2]
    selected = completion + [excluded[i*(len(excluded)-1)//30] for i in range(31)]
    require(len(completion) == 69 and len(selected) == 100,'geometric pilot coverage mismatch')
    with tempfile.TemporaryDirectory() as temp:
        inp = Path(temp)/'geometric.txt'
        gen.matrix(inp,domain['allowed'],selected)
        native = []
        for number,engine in enumerate(engines):
            out = Path(temp)/f'geometric_{number}.jsonl'
            result = subprocess.run([str(engine),str(inp),str(out)],capture_output=True,text=True)
            require(result.returncode == 0 and not result.stderr,'native geometric pilot failed')
            records = [json.loads(s) for s in out.read_text().splitlines()]
            require(len(records) == 100 and [r['index'] for r in records] == list(range(100)),
                    'native geometric pilot missing cases')
            native.append(records)
        nodes,covers = 0,0
        profile_covers = [0,0]
        for i,row in enumerate(selected):
            answers,count = reference_covers(domain['allowed'],row[3])
            require(all({tuple(a) for a in records[i]['covers']} == answers and
                        len(records[i]['covers']) == len(answers) for records in native),
                    'geometric Python/native cover mismatch')
            require(count == native[0][i]['nodes'],'Python/native bitset node counts differ')
            for answer in answers:
                stars = [b | (1 << 17) for b in domain['plane']] + [b | (1 << 16) for b in answer]
                require(len(stars) == len(set(stars)) == 38 and
                        all(b.bit_count() == 5 for b in stars) and
                        all((a&b).bit_count() <= 2 for a,b in it.combinations(stars,2)) and
                        [sum(bool(b & (1 << p)) for b in stars) for p in [17,16]] == [20,18] and
                        not any(b & (3 << 16) == (3 << 16) for b in stars),
                        'invalid geometric star union')
            nodes += count
            covers += len(answers)
            profile_covers[row[1]] += len(answers)
    return {'cases':100,'completion_leaves':69,'exclusion_leaves':31,
            'covers':covers,'profile_covers':profile_covers,
            'reference_nodes':nodes,'exact_cover_list_agreement':True}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bitset',type=Path,required=True)
    parser.add_argument('--cover',type=Path,required=True)
    parser.add_argument('--domain',type=Path,help='optional complete checked domain for100-case geometric pilot')
    args = parser.parse_args()
    start = time.monotonic()
    compositions_count,profiles = profile_audit()
    graphs = graph_audit()
    swaps = swap_audit()
    hypergraphs,rejections,incomplete = native_audit([args.bitset.resolve(),args.cover.resolve()])
    degrees,witness_rejections = witness_audit()
    result = {'status':'PASS','deficit_compositions':compositions_count,
                      'profile_support_counts':profiles,'simple_graphs':graphs,
                      'collinear_swaps':swaps,'small_hypergraphs':hypergraphs,
                      'native_rejections':rejections,'native_incomplete_rejections':incomplete,
                      'degree_incomplete_rejections':1,'witness_rejections':witness_rejections,
              'witness_degrees':degrees}
    if args.domain:
        result['geometric_pilot'] = geometric_pilot(args.domain,[args.bitset.resolve(),args.cover.resolve()])
    result['seconds'] = time.monotonic()-start
    print(json.dumps(result))

if __name__ == '__main__':
    main()
