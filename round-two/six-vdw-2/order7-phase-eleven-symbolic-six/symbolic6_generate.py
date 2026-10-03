"""Generate Phi_0 and Phi_1; no private gap cuts or solver imports."""
import argparse
import json
from pathlib import Path
from symbolic6_common import COMMIT, ROOT, VARIABLES, imported, pins, require, sha, write

TRUE, FALSE = 'T', 'F'


def negate(value):
    if value == TRUE:
        return FALSE
    if value == FALSE:
        return TRUE
    require(type(value) is int and value != 0, 'invalid integer literal or Boolean alias')
    return -value


def put(target, values):
    if TRUE in values:
        return
    literals = {v for v in values if v != FALSE}
    require(all(type(v) is int and 1 <= abs(v) <= VARIABLES for v in literals), 'nonliteral clause')
    if not any(-v in literals for v in literals):
        target.add(tuple(sorted(literals)))


def threshold(j, t):
    if t == 0:
        return TRUE
    if j == 0:
        return FALSE
    require(1 <= j <= 36 and 1 <= t <= 6, 'counter coordinate outside domain')
    return 132 + (j-1)*6 + t


def phase(i):
    return 89 + i % 44


def stem(background):
    return 'symbolic6-bg%d' % background


def components(background, edges):
    require(type(background) is int and background in (0,1), 'invalid background')
    rows = {name:set() for name in ['field','color','xor','phase_units','adjacency','phase8','counter','terminal','gauge']}
    for edge in edges:
        values = [i+1 for i in edge]
        put(rows['field'], values)
        put(rows['field'], [-v for v in values])
    for i in range(88):
        for length, step in [(7,1),(8,19)]:
            values = [(i+j*step)%88+1 for j in range(length)]
            put(rows['color'], values)
            put(rows['color'], [-v for v in values])
    for i in range(44):
        y,z,f = i+1,i+45,phase(i)
        for clause in [(-y,-z,-f),(y,z,-f),(y,-z,f),(-y,z,f)]:
            put(rows['xor'], clause)
    minority = lambda i: phase(i) * (1 if background == 0 else -1)
    for i in range(6):
        put(rows['phase_units'], [minority(i)])
    for i in (6,43):
        put(rows['phase_units'], [-minority(i)])
    for i in range(44):
        if i not in range(5):
            put(rows['adjacency'], [-minority(i),-minority(i+1)])
        window = [phase(i+j) for j in range(8)]
        put(rows['phase8'], window)
        put(rows['phase8'], [-v for v in window])
    for j in range(1,37):
        u = minority(j+6)
        for t in range(1,7):
            s,a,c = threshold(j,t),threshold(j-1,t),threshold(j-1,t-1)
            for clause in [(negate(a),s),(negate(u),negate(c),s),
                           (negate(s),a,u),(negate(s),a,c)]:
                put(rows['counter'], clause)
    put(rows['terminal'], [threshold(36,5)])
    put(rows['terminal'], [-threshold(36,6)])
    put(rows['gauge'], [-1])
    return rows


def main(work):
    old,new = pins()
    require(not work.exists(), 'generated or partial mathematical inputs are frozen')
    work.mkdir(parents=True)
    edges = imported('encode.py','symbolic6_scalar_edge_generator').field_edges()
    require(len(edges) == 26488, 'compressed physical edge count differs')
    records = []
    for background in (0,1):
        groups = components(background,edges)
        rows = sorted(set().union(*groups.values()),key=lambda row:(len(row),row))
        filename = work/(stem(background)+'.cnf')
        filename.write_text('p cnf %d %d\n' % (VARIABLES,len(rows))
                            + ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem(background),background=background,phase_K=11 if background==0 else 33,
            variables=VARIABLES,color_variables=88,phase_variables=44,counter_variables=216,
            clauses=len(rows),cnf_sha256=sha(filename),component_counts={k:len(v) for k,v in groups.items()},
            physical_supports=len(edges),literal_kept_APs=375760,omitted_zero_APs=4312,
            minority_profile=[6,1,1,1,1,1],normalized_minor_run=list(range(6)),
            tail_positions=list(range(7,43)),tail_weight=5,necessary_phase_heads=1876,
            maximum_background_gap=7,following_background_gap_cut=None,preceding_gap_cut=None,
            palette_gauge=[[-1]],only_global_y0_zero=True,color_zero_is_coset_of_one=True,
            threshold_definition='S(j,t) iff S(j-1,t) OR (U(j) AND S(j-1,t-1))',
            numerical_premises=[8664,8787,9069],private_gap_cut=False,foreign_family_cut=False,
            ordinary_classification_numerical_cut=False,source_commit=COMMIT,mathematical_exclusion=False))
    previous = set(old['frozen_prior_cnfs']+old['completed_previous_cnfs'])
    require(len({r['cnf_sha256'] for r in records}) == 2
            and all(r['cnf_sha256'] not in previous for r in records),'identical old native input')
    result = dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
                  producer_sha256=sha(Path(__file__)),models=2,covered_necessary_phase_heads=3752,
                  ordinary_classification='10093/index1',records=records)
    write(work/'models.json',result)
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
