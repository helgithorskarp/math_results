"""Literal identity controls and failures on damaged semantic records."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import random
from audit import profile_audit, literal_H_audit


def page_data(rows):
    n=len(rows); blue=[set(range(n))-{u}-rows[u] for u in range(n)]
    entries=[]
    for u,v in combinations(range(n),2):
        red=v in rows[u]
        pages=len(rows[u]&rows[v]) if red else len(blue[u]&blue[v])
        entries.append((u,v,red,pages))
    return entries


def identity_controls(fixture):
    rng=random.Random(170099)
    graphs=0; spines=0; root_checks=0
    for _ in range(64):
        rows=[set() for _ in range(22)]
        for orbit in range(7):
            if orbit<3:
                for t in range(3):
                    v=1+3*orbit+t; rows[0].add(v); rows[v].add(0)
            if rng.randrange(2):
                for t in range(3):
                    u=1+3*orbit+t; v=1+3*orbit+(t+1)%3
                    rows[u].add(v); rows[v].add(u)
        for i,j in combinations(range(7),2):
            for shift in range(3):
                if rng.randrange(2):
                    for t in range(3):
                        u=1+3*i+t; v=1+3*j+(t+shift)%3
                        rows[u].add(v); rows[v].add(u)
        pages=page_data(rows); d=list(map(len,rows)); E=sum(d)//2
        W=sum((3 if red else 6)-c for _,_,red,c in pages)
        triangles=sum(c for _,_,_,c in pages)//3
        if 2*triangles!=2*1540-sum(v*(21-v) for v in d):
            raise ValueError('Literal monochromatic triangle identity')
        if 2*W!=-6468+120*E-3*sum(v*v for v in d):
            raise ValueError('Literal degree/deficit identity')
        D_A=sum(d[v] for v in rows[0])
        incident=sum((3 if red else 6)-c for u,v,red,c in pages if 0 in [u,v])
        if incident!=2*(E-D_A)-33:
            raise ValueError('Literal fixed-root incident deficit identity')
        graphs+=1; spines+=len(pages); root_checks+=1

    # Every odd column of the relevant sizes, without phase normalization.
    odd_columns=0; odd_row_checks=0
    for size in [3,5]:
        for subset in combinations(range(9),size):
            column=set(subset); odd_columns+=1
            for u in range(9):
                gram_sum=sum(int(u in column and v in column) for v in range(9))
                if gram_sum%2!=int(u in column):
                    raise ValueError('Literal odd-column Gram parity')
                odd_row_checks+=1

    text=Path(fixture).read_text().splitlines()
    if len(text)!=21 or any(len(r)!=21 or set(r)-{'0','1'} for r in text):
        raise ValueError('Primary fixture shape')
    primary=[{v for v,c in enumerate(row) if c=='1'} for row in text]
    if any(u in primary[u] or any((v in primary[u])!=(u in primary[v]) for v in range(21)) for u in range(21)):
        raise ValueError('Primary fixture graph semantics')
    p=page_data(primary)
    E=sum(map(len,primary))//2
    caps=[max(c for _,_,red,c in p if red),max(c for _,_,red,c in p if not red)]
    if E!=93 or caps!=[3,6]:
        raise ValueError('Primary ordinary baseline failed')
    return dict(arbitrary_C3_graphs=graphs,literal22_spines=spines,
                root_deficit_identities=root_checks,
                odd_columns=odd_columns,odd_column_row_checks=odd_row_checks,
                primary21=dict(edges=E,max_red_pages=caps[0],max_blue_pages=caps[1],spines=len(p)),
                trust='Arbitrary22 identity controls may violate page caps and are not witnesses; primary21 is known prior art.')


def damage_controls(record, all_marks, kept):
    checks=[]
    def reject(name, action):
        try:
            action()
        except (ValueError,KeyError,StopIteration,IndexError):
            checks.append(name)
            return
        raise ValueError('Accepted damaged semantics: '+name)
    reject('missing_ordered_degree_placement',lambda:profile_audit(record,all_marks[:-1],kept))
    reject('extra_ordered_degree_placement',lambda:profile_audit(record,all_marks+[all_marks[-1]],kept))
    damaged=deepcopy(record); damaged['histograms'][0]['deficit_weight']+=1
    reject('wrong_deficit_budget',lambda:profile_audit(damaged,all_marks,kept))
    damaged=deepcopy(record); damaged['histograms'][0]['free_degree_counts']['9']-=1
    reject('altered_degree_histogram',lambda:profile_audit(damaged,all_marks,kept))
    damaged=deepcopy(record); damaged['new_profile_root_placements'][0]['survivors'].pop()
    reject('missing_exceptional_root_placement',lambda:profile_audit(damaged,all_marks,kept))
    damaged=deepcopy(record); damaged['marked_capacity_cases'][0]['capacity']+=1
    reject('altered_marked_capacity',lambda:literal_H_audit(damaged))
    damaged=deepcopy(record); damaged['marked_capacity_cases'][0]['actual_overlap']+=1
    reject('wrong_column_overlap',lambda:literal_H_audit(damaged))
    damaged=deepcopy(record); damaged['low_row_parity_cases'][0]['tight_Gram_row_sum']+=1
    reject('altered_parity_row',lambda:literal_H_audit(damaged))
    damaged=deepcopy(record); damaged['marked_capacity_cases'][0]['root_deficit']=0
    reject('missing_root_deficit',lambda:literal_H_audit(damaged))
    return dict(rejected=checks,count=len(checks),checks_active_without_assert=True)
