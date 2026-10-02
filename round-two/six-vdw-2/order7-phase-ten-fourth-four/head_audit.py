"""Independent literal-field, exact-SIX and complete sixteen-head audits."""
import argparse
from collections import Counter
import itertools,json,math,resource,time
from pathlib import Path
from common import pins,require,sha,endpoint_auditor
old=endpoint_auditor()
literal_field,expected_clauses=old.literal_field,old.expected_clauses
PARAMETERS=[(ell,b) for ell in range(10,4,-1) for b in (0,1)]
def stem_for(ell,b):return f'fourth4-fourth-{ell}-b-{b}'
def head_fixed(ell,background):
    require((ell,background) in PARAMETERS,'unsupported fourth head')
    return {i:1-background for i in (0,1,2,ell)}|{i:background for i in (*range(3,ell),43)}
def counter_check(rows, n, background, exact):
    require(exact == 6, 'wrong heterogeneous remainder')
    base, levels = 44+2*n, exact+1
    cells = {(i, k): base+(i*(i-1)//2 if i <= levels
                            else levels*(i-1)-levels*(levels-1)//2)+k
             for i in range(1, n+1) for k in range(1, min(i, levels)+1)}
    end = base+levels*n-levels*(levels-1)//2
    require(set(cells.values()) == set(range(base+1, end+1)), 'incomplete counter cells')
    units = {(cells[n, exact],), (-cells[n, levels],)}
    require({row for row in rows if len(row) == 1} == units, 'wrong heterogeneous exact-count units')
    accounted, checked = set(units), 0
    for (i, k), output in cells.items():
        a = cells.get((i-1, k), False)
        b = True if k == 1 else cells[i-1, k-1]
        value = (44+n+i)*(-1 if background else 1)
        local = {row for row in rows if len(row) > 1 and max(map(abs, row)) == output}
        domain = {abs(v) for v in (a, b, value, output) if not isinstance(v, bool)}
        require(local and all(set(map(abs, row)) <= domain for row in local),
                'wrong gate domain or missing output')
        for bits in itertools.product((0, 1), repeat=len(domain)):
            assignment = dict(zip(sorted(domain), bits))
            def ev(v):
                return v if isinstance(v, bool) else assignment[abs(v)] ^ int(v < 0)
            relation = bool(assignment[output]) == bool(ev(a) or (ev(value) and ev(b)))
            require(all(any(ev(v) for v in row) for row in local) == relation,
                    'wrong heterogeneous gate truth relation')
            checked += 1
        accounted.update(local)
    require(accounted == rows, 'unaccounted counter clause')
    return end, checked


def tiny_controls():
    thresholds = exact_inputs = 0
    for remainder in (6,):
        for length in range(1, 11):
            for bits in itertools.product((0, 1), repeat=length):
                for flip in (0, 1):
                    cells = {}
                    for i, value in enumerate(bits, 1):
                        for k in range(1, min(i, remainder+1)+1):
                            a = cells.get((i-1, k), False)
                            b = True if k == 1 else cells[i-1, k-1]
                            cells[i, k] = bool(a or ((value ^ flip) and b))
                            require(cells[i, k] == (sum(x ^ flip for x in bits[:i]) >= k),
                                    'tiny threshold differs')
                            thresholds += 1
                    require((cells.get((length, remainder), False)
                             and not cells.get((length, remainder+1), False))
                            == (sum(x ^ flip for x in bits) == remainder),
                            'tiny heterogeneous exact count differs')
                    exact_inputs += 1
    return thresholds, exact_inputs



def cover_controls():
    checked,seen=0,set()
    for length in range(12,21):
        for count in (4,5,6,7):
            for extras in itertools.combinations(range(3,length-1),count-3):
                selected={0,1,2,*extras}
                if any(all((i+j)%length in selected for j in range(8)) or
                       all((i+j)%length not in selected for j in range(8)) for i in range(length)):
                    continue
                if any((i-1)%length not in selected and i in selected and
                       (i+1)%length in selected and (i+2)%length not in selected for i in range(length)):
                    continue
                ell=sorted(selected)[3]
                if ell<5:continue  # Only failure of the proposed fourth4 rule.
                for background in (0,1):
                    require((ell,background) in PARAMETERS,'selected sequence escaped12-case failed-fourth4 cover')
                    bits=[int((i in selected)!=bool(background)) for i in range(length)]
                    fixed=head_fixed(ell,background)
                    require(all(bits[length-1 if i==43 else i]==v for i,v in fixed.items()),
                            'classification lost an ordinary fourth head')
                    seen.add((ell,background));checked+=1
    require(seen==set(PARAMETERS),'synthetic controls miss a twelve-case head')
    return checked,[list(p) for p in PARAMETERS if p in seen]
def gauge_controls():
    checked = 0
    for length in range(2, 7):
        for bits in itertools.product((0, 1), repeat=2*length):
            phase = [bits[i] ^ bits[i+length] for i in range(length)]
            for offset in range(2*length):
                rotated = [bits[(i+offset) % (2*length)] ^ bits[offset]
                           for i in range(2*length)]
                require(rotated[0] == 0 and all(rotated[i+length] ==
                        rotated[i] ^ phase[(i+offset) % length] for i in range(length)),
                        'scalar rotation or global gauge lost an orientation')
                checked += 1
    return checked



def rule_clauses(fixed,free,background):
    names={i:45+len(free)+j for j,i in enumerate(free)}
    rows,truth_inputs=set(),0
    for origin in range(44):
        positions=[(origin+j)%44 for j in (-1,0,1,2)]
        wanted=[1-background,background,background,1-background]
        true_constant=any(i in fixed and fixed[i]==v for i,v in zip(positions,wanted))
        row=None if true_constant else tuple(sorted({names[i]*(1 if v else -1)
            for i,v in zip(positions,wanted) if i not in fixed}))
        if row is not None:rows.add(row)
        domain=sorted({names[i] for i in positions if i not in fixed})
        for values in itertools.product((0,1),repeat=len(domain)):
            assignment=dict(zip(domain,values))
            selected=[(fixed[i] if i in fixed else assignment[names[i]])!=background for i in positions]
            implication=bool(selected[0] or not selected[1] or not selected[2] or selected[3])
            truth=row is None or any(assignment[abs(v)]==(v>0) for v in row)
            require(truth==implication,'substituted TWO differs from antecedent and consequence')
            truth_inputs+=1
    return rows,truth_inputs

def redundancy_controls(fixed,free,background):
    names={i:45+len(free)+j for j,i in enumerate(free)}
    def row(origin,offsets):
        points=[(origin+j)%44 for j in offsets]
        wanted=[1-background,background,background]+[1-background]*(len(offsets)-3)
        if any(i in fixed and fixed[i]==v for i,v in zip(points,wanted)):return None
        return {names[i]*(1 if v else -1) for i,v in zip(points,wanted) if i not in fixed}
    count=0
    for origin in range(44):
        strong=row(origin,(-1,0,1,2))
        for offsets in ((-1,0,1,2,3),(-1,0,1,2,4,5),(-1,0,1,2,3,4),
                        (-1,0,1,2,3,5,6),(-1,0,1,2,3,4,5),(-1,0,1,2,3,4,6)):
            weak=row(origin,offsets)
            require(weak is None or (strong is not None and strong<=weak),
                    'omitted ancestor is not a literal superset of TWO')
            count+=1
    return count

def main(work):
    began=time.monotonic();pins();premise=pins()
    models=json.loads((work/'models.json').read_text());expected=PARAMETERS
    require(models['producer_sha256']==sha(Path(__file__).with_name('head_generate.py')),
            'changed model producer')
    require([r['stem'] for r in models['records']]==[stem_for(*p) for p in expected],
            'incomplete twelve-case failed-fourth4 cover')
    require({p.name for p in work.glob('*.cnf')}=={stem_for(*p)+'.cnf' for p in expected},
            'missing or extra model file')
    slots,supports=literal_field();records=[]
    for record,(ell,background) in zip(models['records'],expected):
        fixed=head_fixed(ell,background);free=[i for i in range(44) if i not in fixed]
        require(record['minimum_distance']==1 and record['third_selected_index']==2
                and record['fourth_selected_index']==ell and record['background']==background
                and record['phase_K']==(34 if background else 10)
                and record['free_selected_count']==6 and record['selected_anchor_count']==4
                and record['selected_anchors']==[0,1,2,ell]
                and record['root57_color_cut'] is True and record['selected_run_start'] is True
                and record['proposed_FOURTH4_cut'] is False
                and record['proposed_NO_ADJACENCY_cut'] is False
                and record['redundant_ancestor_cuts'] is False
                and record['next_free_phase']==ell+1
                and record['conditional_successor_cut'] is False and record['actual_TWO_cut'] is True
                and record['two_lemma_graph']==premise['premise']['graph']
                and record['two_lemma_source_commit']==premise['premise']['source_commit'],
                'changed ordinary fourth-head semantics or false premise')
        semantic,n=expected_clauses(slots,supports,fixed,1)
        index={i:j for j,i in enumerate(free)}
        def actual_literal(point):
            i,side=slots[point]
            if not side:return i+1
            return (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
        for origin in range(88):
            point=pow(3,origin,617)
            values={actual_literal(point*pow(57,j,617)%617) for j in range(8)}
            if not any(-v in values for v in values):
                semantic.add(tuple(sorted(values)));semantic.add(tuple(sorted(-v for v in values)))
        require(n==len(free)==42-ell and record['free_phase_indices']==free
                and record['next_free_phase'] in free,'wrong free phase domain or false next neighbor')
        two,truth_inputs=rule_clauses(fixed,free,background)
        require(record['two_clauses_after_substitution']==len(two)
                and record['new_two_clauses']==len(two-semantic)>0,'missing or misstated necessary TWO clauses')
        inclusions=redundancy_controls(fixed,free,background);semantic.update(two)
        cnf=work/(record['stem']+'.cnf');text=cnf.read_text().splitlines();variables=23+9*n
        require(text[0].split()==['p','cnf',str(variables),str(record['clauses'])]
                and record['variables']==variables,'wrong SIX model dimension')
        rows=[]
        for line in text[1:]:
            values=list(map(int,line.split()))
            require(values and values[-1]==0 and all(1<=abs(v)<=variables for v in values[:-1]),
                    'invalid DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        counters={row for row in rows if any(abs(v)>44+2*n for v in row)}
        end,truth_rows=counter_check(counters,n,background,6)
        require(end==variables,'wrong analytic counter labeling')
        require(Counter(rows)==Counter(list(semantic|counters)+[(-1,)])
                and len(rows)==record['clauses'] and sha(cnf)==record['cnf_sha256'],
                'full actual-field TWO model audit differs')
        records.append(dict(stem=record['stem'],variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
            counter_truth_rows=truth_rows,substituted_TWO_truth_rows=truth_inputs,
            two_clauses_after_substitution=len(two),new_two_clauses=record['new_two_clauses'],
            ancestor_literal_inclusion_checks=inclusions,free_selected_count=6,
            free_phase_inputs_before_cuts=math.comb(n,6)))
    thresholds,exact_inputs=tiny_controls();cover_inputs,branches=cover_controls();rotations=gauge_controls()
    result=dict(agent='six-vdw-2',role='researcher',status='EXACT_K10_FOURTH4_HEAD12_AUDIT',
        records=records,literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,
        tiny_threshold_cells=thresholds,tiny_exact_counts=exact_inputs,
        synthetic_twelve_case_failed_fourth4_cover_inputs=cover_inputs,tiny_branches=branches,
        signed_rotation_controls=rotations,counter_exact_counts_tested=[6],
        synthetic_controls_not_field_theorems=True,proposed_FOURTH4_cut=False,proposed_NO_ADJACENCY_cut=False,
        conditional_successor_cut=False,actual_TWO_cut=True,ancestor_cuts_redundant=True,
        seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path=work/('audit-normal.json' if __debug__ else 'audit-optimized.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
