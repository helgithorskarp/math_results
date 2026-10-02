"""Definition-level algebra, endpoint and separating-certificate controls."""
from itertools import combinations, product
from core import frame, degrees, RANK, X, SX, SY, T, CYCLE, require
from separation import TABLE, TARGET, CASES, totals, certificate, sums, relaxed_certificates


def run():
    algebra = 0
    for mode in range(4):
        adj = [set() for _ in range(22)]
        for i,j in combinations(range(22),2):
            red = (mode == 1 or (mode == 2 and (i*j+i+j) % 7 < 3)
                   or (mode == 3 and ((i-j)**2 + i*j) % 11 < 6))
            if red:
                adj[i].add(j); adj[j].add(i)
        for i,j in combinations(range(22),2):
            ground = set(range(22)) - {i,j}
            redc = len(adj[i] & adj[j])
            bluec = len((ground-adj[i]) & (ground-adj[j]))
            require(bluec == 20-(len(adj[i])-(j in adj[i]))
                    -(len(adj[j])-(i in adj[j]))+redc, 'full physical inclusion-exclusion')
            if j not in adj[i]:
                require((bluec <= 6) == (redc <= len(adj[i])+len(adj[j])-14),
                        'physical blue-spine cap')
            algebra += 1
    # Enumerate actual subsets rather than re-evaluate only the bound formula.
    minima = {}
    universe = set(range(6))
    for rowmask in range(64):
        row = {i for i in universe if rowmask >> i & 1}
        red = 0 in row
        for nmask in range(32):
            near = {i+1 for i in range(5) if nmask >> i & 1}
            key = (red,len(row),len(near))
            value = len(row & near)
            minima[key] = min(minima.get(key,6),value)
    for (red,r,h), value in minima.items():
        require(value == max(0,r+h-(6 if red else 5)), 'exact Q subset minimum')
    adj=frame()
    known_deg=degrees(adj)
    # The C/P point's precise blue SY1 obstruction, preserving degree 9.
    near={1,4,7,8,9,10,13,14}
    pages=sorted(adj[12]&near)
    dq=len(near)+2
    require(pages==[1,4,7,8,13,14] and dq==10 and known_deg[12]==9,
            'C/P named pages and actual degree')
    require(len(pages)>known_deg[12]+dq-14
            and len(pages)<=10+dq-14, 'false degree-10 tag removes essential cap')
    # A D point with M=01,p0=p1=1 violates the red SX0 cap solely after
    # retaining the internal-Q minimum, not merely its known pages.
    dnear={1,5,6,7,8,9,10,14}
    dknown=len(adj[9]&dnear)
    require(dknown==3 and max(0,RANK[9]+3-6)==1 and dknown+1>3,
            'D physical red-spine internal-Q boundary')
    # Explicit old-label input map control.
    old=(2,1,3,4,5,6,7,8,9,10)
    old_rows=((1,8,9),(0,),(6,7),(4,5),(3,7,9),
              (3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
    require(all((adj[old[i]] & set(old))=={old[j] for j in row}
                for i,row in enumerate(old_rows)), 'literal old-label adjacency')
    wrong=list(old);wrong[0],wrong[1]=wrong[1],wrong[0]
    require(any((adj[wrong[i]] & set(wrong))!={wrong[j] for j in row}
                for i,row in enumerate(old_rows)), 'wrong old-label map rejects')
    relaxed=relaxed_certificates()
    corrupted=[]
    for case,w in [('U',(0,0,1,1,0,1)),('V',(0,1,1,0,0,0))]:
        c=certificate(w,case)
        require(c['gap']<=0, 'damaged separator unexpectedly still proves exclusion')
        corrupted.append({'case':case,'weights':list(w),'gap':c['gap']})
    positive={}
    for case,roles in CASES.items():
        tuples=list(product(*(TABLE[r] for r in roles)))
        best=min(tuples,key=lambda t:(sum(abs(x-y) for x,y in zip(totals(t),TARGET)),t))
        vector=totals(best)
        require(vector!=TARGET and all(s in TABLE[r] for s,r in zip(best,roles)),
                'nearby abstract allocation accepts')
        positive[case]={'sets':list(map(list,best)),'totals':list(vector),
                        'distance':sum(abs(x-y) for x,y in zip(vector,TARGET))}
    enlarged=dict(TABLE);enlarged['C']=TABLE['C']+((0,2,3),)
    hits=[t for t in product(*(enlarged[r] for r in CASES['U'])) if totals(t)==TARGET]
    require(hits, 'relaxing U C/P should remove the obstruction')
    return {'physical_22_vertex_spines':algebra,'actual_Q_subset_minima':len(minima),
            'old_label_negative':True,'C_P_degree_nine_boundary':True,
            'D_internal_Q_boundary':True,'corrupted_separators':corrupted,
            'nearby_positive_allocations':positive,
            'U_C_P_relaxation_hit_count':len(hits),
            'U_C_P_relaxation_example':list(map(list,hits[0]))}


if __name__=='__main__':
    import json
    print(json.dumps(run(),sort_keys=True,separators=(',',':')))
