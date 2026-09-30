#!/usr/bin/env python3
"""Independent exact controls for a conditional Book Ramsey review.

The proofs are in review.md. Small graphs control identities; they do not
enumerate 22-vertex witnesses. No author modules, solver, or floating point.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import ast
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def choose2(n):
    return n * (n - 1) // 2


def graphs(n):
    # Bit i of a row is adjacency to vertex i. Edge order is lexicographic.
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        rows = [0] * n
        for bit, (i, j) in enumerate(pairs):
            if (mask >> bit) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        yield mask, rows


def vertices(bits, n):
    return [i for i in range(n) if (bits >> i) & 1]


def opposite(rows):
    full = (1 << len(rows)) - 1
    return [full ^ row ^ (1 << i) for i, row in enumerate(rows)]


def edges_in(rows, subset):
    return sum((rows[i] & subset).bit_count()
               for i in vertices(subset, len(rows))) // 2


def capacity_and_attachments(rows, r, s):
    """Compare literal spine budgets with degree formulas, all subsets."""
    n = len(rows)
    blue = opposite(rows)
    h = [row.bit_count() for row in rows]
    e = sum(h) // 2
    direct = sum(r - 1 - (rows[i] & rows[j]).bit_count()
                 if (rows[i] >> j) & 1
                 else s - (blue[i] & blue[j]).bit_count()
                 for i, j in combinations(range(n), 2))
    formula2 = sum((3*n + r - s - 4)*k - 3*k*k for k in h)
    formula2 += 2*(s - n + 2)*choose2(n)
    require(2*direct == formula2, 'capacity identity')
    full = (1 << n) - 1
    values = []
    for missed in range(1 << n):
        received = full ^ missed
        cost = edges_in(rows, received) + edges_in(blue, missed)
        alt = e - sum(h[i] for i in vertices(missed, n))
        alt += choose2(missed.bit_count())
        require(cost == alt, 'attachment identity')
        z = missed.bit_count()
        delta = choose2(r+1) - sum(h[i] for i in vertices(missed,n)) + choose2(z)
        factored2 = (z-r)*(z-r-1) + 2*sum(r-h[i] for i in vertices(missed,n))
        require(2*delta == factored2, 'row cost factorization')
        if max(h, default=0) <= r:
            require(delta >= 0, 'row cost sign')
        values.append(cost)
    return direct, values


def defect_and_root_controls(rows, r, s):
    """Count triangles, vertex defects and unused rooted capacities literally."""
    n = len(rows)
    blue = opposite(rows)
    d = [row.bit_count() for row in rows]
    m = sum(d)//2
    monochrome = 0
    for i, j, k in combinations(range(n), 3):
        count = ((rows[i] >> j)&1) + ((rows[i] >> k)&1) + ((rows[j] >> k)&1)
        monochrome += count in (0,3)
    require(2*monochrome == 2*(n*(n-1)*(n-2)//6)
            - sum(k*(n-1-k) for k in d), 'Goodman triple count')
    defects = [0]*n
    total = 0
    for i,j in combinations(range(n),2):
        val = r-(rows[i]&rows[j]).bit_count() if (rows[i]>>j)&1 else s-(blue[i]&blue[j]).bit_count()
        defects[i] += val
        defects[j] += val
        total += val
    require(total == r*m+s*(choose2(n)-m)-3*monochrome, 'global defects')
    for v in range(n):
        a, b = rows[v], blue[v]
        q = n-1-d[v]
        direct = r*d[v]+s*q-2*edges_in(rows,a)-2*edges_in(blue,b)
        require(direct == defects[v], 'incident defect')
        degree_difference = sum(d[u] for u in vertices(a,n)) - sum(d[u] for u in vertices(b,n))
        require(degree_difference == d[v]+2*edges_in(rows,a)-q*(q-1)+2*edges_in(blue,b), 'degree difference')
        for color, cap, othercap in ((rows,r,s),(blue,s,r)):
            other = opposite(color)
            aa, bb = color[v], other[v]
            aa_list = vertices(aa,n)
            hh = [(color[u]&aa).bit_count() for u in aa_list]
            dd, qq = len(aa_list), bb.bit_count()
            cc = used = unused = 0
            for i,j in combinations(aa_list,2):
                is_edge = (color[i]>>j)&1
                local = ((color[i]&color[j]) if is_edge else (other[i]&other[j])) & aa
                ext = ((color[i]&color[j]) if is_edge else (other[i]&other[j])) & bb
                capacity = (cap-1 if is_edge else othercap) - local.bit_count()
                cc += capacity
                used += ext.bit_count()
                unused += (cap-(color[i]&color[j]).bit_count()) if is_edge else (othercap-(other[i]&other[j]).bit_count())
            require(cc-used == unused, 'rooted exact unused capacity')
            ee = edges_in(color,aa)
            costtotal = 0
            for w in vertices(bb,n):
                zz = aa & other[w]
                costtotal += choose2(cap+1)+choose2(zz.bit_count())
                costtotal -= sum((color[u]&aa).bit_count() for u in vertices(zz,n))
            budget2 = sum((3*dd+cap-othercap-4-qq)*h-3*h*h for h in hh)
            budget2 += 2*(othercap-dd+2)*choose2(dd)+qq*cap*(cap+1)
            require(budget2 == 2*(unused+costtotal), 'rooted budget')
            require(budget2 == 2*(cc-qq*(ee-choose2(cap+1))), 'second rooted budget')
    return total, defects


def small_controls():
    stream = sha256()
    counts = {'capacity_graphs':0,'capacity_subsets_per_cap_pair':0,'defect_graphs':0,'root_color_checks':0}
    for n in range(6):
        for mask, rows in graphs(n):
            for r,s in ((3,6),(6,3),(1,2),(0,0)):
                c, costs = capacity_and_attachments(rows,r,s)
                stream.update(json.dumps([n,mask,r,s,c,costs],separators=(',',':')).encode())
            counts['capacity_graphs'] += 1
            counts['capacity_subsets_per_cap_pair'] += 1 << n
    for n in range(1,7):
        for mask, rows in graphs(n):
            val, local = defect_and_root_controls(rows,3,6)
            stream.update(json.dumps([n,mask,val,local],separators=(',',':')).encode())
            counts['defect_graphs'] += 1
            counts['root_color_checks'] += 2*n
    counts['stream_sha256'] = stream.hexdigest()
    return counts


def scalar_controls():
    # Score the remaining budget in vertex-deficit coordinates a=r-h,
    # independently of the author's direct maximum over local degrees.
    bounds = []
    for label,r,s,start in (('red',3,6,12),('blue',6,3,15)):
        for d in range(start,22):
            q = 21-d
            coefficient = 3*d+r-s-4-q
            base = d*(coefficient*r-3*r*r)+2*(s-d+2)*choose2(d)+q*r*(r+1)
            penalties = [(coefficient-6*r)*a+3*a*a for a in range(r+1)]
            upper = base-d*min(penalties)
            require(upper < 0, 'degree exclusion coverage')
            bounds.append([label,d,upper])
    equality_scores = [34*h-3*h*h for h in range(7)]
    require(equality_scores == [0,31,56,75,88,95,96], 'degree7 unique maximizer')
    survivors = []
    histogram_count = 0
    for n0 in range(12):
        for n1 in range(12-n0):
            for n2 in range(12-n0-n1):
                n3 = 11-n0-n1-n2
                histogram_count += 1
                if (n1+3*n3)%2:
                    continue
                deficits = [3]*n0+[2]*n1+[1]*n2+[0]*n3
                # Exhaust all labeled subsets; no sorted-degrees optimizer.
                twiceD = 21-sum(3*a*a-2*a for a in deficits)
                best = min((z-3)*(z-4)//2 + sum(deficits[i] for i in vertices(mask,11))
                           for mask in range(1<<11) for z in [mask.bit_count()])
                if twiceD >= 20*best:
                    require(twiceD%2 == 0, 'budget parity')
                    survivors.append([n0,n1,n2,n3,twiceD//2,best])
    expected = [[0,a,b,11-a-b] for a in (0,1) for b in (1,3,5,7)]
    remaining = [row[:4] for row in survivors if row[0]==0 and row[1]<=1]
    require(remaining == expected and len(survivors)==12, 'twelve-to-eight histograms')
    # Exhaust all degree histograms on 22 vertices with degrees 7..11.
    endpoint = []
    tested = 0
    for n7 in range(23):
        for n8 in range(23-n7):
            for n9 in range(23-n7-n8):
                for n10 in range(23-n7-n8-n9):
                    n11=22-n7-n8-n9-n10
                    tested += 1
                    ns=[n7,n8,n9,n10,n11]
                    degsum=sum((7+i)*c for i,c in enumerate(ns))
                    abs_sum=sum(abs(i-3)*c for i,c in enumerate(ns))
                    cost=sum((3*(i-3)**2+((7+i)%2))*c for i,c in enumerate(ns))
                    if degsum==194 and abs_sum<=26 and cost<=132:
                        endpoint.append(ns)
    refined=[ns for ns in endpoint if ns[0]==0]
    require(refined == [[0,k,26-2*k,k-4,0] for k in range(4,8)], '97-edge histogram refinement')
    require(all(3*x*x+(x%2)>=8*abs(x)-4 for x in range(-10,12)), 'integer absolute-value bound')
    return {'excluded_degrees':bounds,'degree7_scores':equality_scores,
            'local_histograms_tested':histogram_count,'local_scalar_survivors':survivors,
            'local_after_analytic_exclusions':remaining,'global_histograms_tested':tested,
            'edge97_histograms_before_degree7_exclusion':endpoint,
            'edge97_histograms_after_proved_degree7_exclusion':refined}


def shifted22_controls():
    """Signed identities on fixed 22-vertex examples, not valid witnesses."""
    examples = [[0]*22, [(1<<22)-1-(1<<i) for i in range(22)]]
    cycle = [(1<<((i-1)%22)) | (1<<((i+1)%22)) for i in range(22)]
    examples += [cycle, opposite(cycle)]
    examples += [[sum(1<<j for j in range(22) if (i<11)!=(j<11)) for i in range(22)]]
    results=[]
    for rows in examples:
        total, local = defect_and_root_controls(rows,3,6)
        x=[row.bit_count()-10 for row in rows]
        require(2*total==3*(44-sum(a*a for a in x)), '22-vertex shifted global identity')
        for i in range(22):
            expression=sum(x)+6-2*x[i]-x[i]*x[i]-2*sum(x[j] for j in vertices(rows[i],22))
            require(expression==local[i], '22-vertex shifted local identity')
            require((local[i]-rows[i].bit_count())%2==0, 'incident parity')
        results.append({'red_edges':sum(row.bit_count() for row in rows)//2,'signed_total_defect':total})
    return {'examples':results,'root_color_checks':len(examples)*44,
            'meaning':'signed arithmetic controls; these examples are not claimed to satisfy the book caps'}


def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def spectral_control():
    # Petersen control via outer cycle, spokes, inner pentagram; not KG(5,2).
    p=[[0]*10 for _ in range(10)]
    for i in range(5):
        for u,v in ((i,(i+1)%5),(i,i+5),(i+5,(i+2)%5+5)):
            p[u][v]=p[v][u]=1
    p2=matmul(p,p)
    p3=matmul(p2,p)
    require(all(sum(row)==3 for row in p), 'cubic control')
    require(sum(p2[i][i] for i in range(10))==30 and sum(p3[i][i] for i in range(10))==0, 'spectral moments')
    require(all(p2[i][j]+p[i][j]-2*(i==j)==1 for i in range(10) for j in range(10)), 'strong regularity identity')
    foursets = [list(c) for c in combinations(range(10),4) if all(p[i][j]==0 for i,j in combinations(c,2))]
    require(len(foursets)==5, 'independent four-set control')
    require(all(set(a)&set(b) for a,b in combinations(foursets,2)), 'intersection control')
    require(all(sum(p[w][v] for v in a)==2 for a in foursets for w in range(10) if w not in a), 'external degree two')
    m=[[int(i in c) for i in range(10)] for c in foursets for _ in range(2)]
    gram=matmul(list(map(list,zip(*m))),m)
    require(all(sum(row)==4 for row in m) and all(sum(row[j] for row in m)==4 for j in range(10)), 'incidence row/column sums')
    require(all(gram[i][j]==4*(i==j)+3-3*p[i][j]-p2[i][j] for i in range(10) for j in range(10)), 'Gram identity')
    # Exact Faddeev-LeVerrier coefficients, without eigenvalue approximation.
    b=[[int(i==j) for j in range(10)] for i in range(10)]
    coeff=[1]
    for k in range(1,11):
        b=matmul(p,b)
        tr=sum(b[i][i] for i in range(10))
        require(tr%k==0, 'characteristic polynomial integrality')
        c=-tr//k
        coeff.append(c)
        for i in range(10): b[i][i]+=c
    expected=[1]
    for root in [3]+[1]*5+[-2]*4:
        next_coeff=[0]*(len(expected)+1)
        for i,c in enumerate(expected):
            next_coeff[i]+=c; next_coeff[i+1]-=root*c
        expected=next_coeff
    require(coeff==expected, 'exact characteristic polynomial')
    return {'construction':'outer cycle / spokes / inner pentagram',
            'characteristic_coefficients_descending':coeff,
            'independent_four_sets':foursets,'Gram_entries_checked':100,
            'meaning':'arithmetic control; no catalogue or universal graph enumeration'}


def baseline_control():
    data=(Path(__file__).resolve().parent/'primary21.txt').read_bytes()
    require(sha256(data).hexdigest()=='3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55', 'primary fixture hash')
    # Primary upstream orientation is blue. Parse only its matrix literal;
    # the remaining upstream search metadata is never executed.
    text=data.decode()
    end=text.index(']]')+2
    matrix=ast.literal_eval(text[:end])
    require(len(matrix)==21 and all(len(row)==21 for row in matrix), 'matrix dimensions')
    require(all(c in (0,1) for row in matrix for c in row), 'matrix bits')
    require(all(matrix[i][i]==0 for i in range(21)) and all(matrix[i][j]==matrix[j][i] for i in range(21) for j in range(21)), 'simple undirected matrix')
    red=[sum((1-matrix[i][j])<<j for j in range(21) if i!=j) for i in range(21)]
    blue=opposite(red)
    maxima=[max((color[i]&color[j]).bit_count() for i,j in combinations(range(21),2) if (color[i]>>j)&1) for color in (red,blue)]
    require(maxima == [3,6], 'baseline book constraints')
    total, local=defect_and_root_controls(red,3,6)
    degrees=Counter(row.bit_count() for row in red)
    require(degrees=={8:4,9:16,10:1}, 'baseline degree counts')
    return {'input_sha256':sha256(data).hexdigest(),'vertices':21,'red_edges':sum(row.bit_count() for row in red)//2,
            'red_degree_counts':dict(sorted(degrees.items())), 'max_red_blue_edge_codegrees':maxima,
            'total_defect':total,'incident_defects':local,'root_color_checks':42}


def main():
    result={'agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'scope':'exact controls for analytic necessary conditions and conditional edge97 refinement; no Ramsey resolution',
            'small_controls':small_controls(),'scalar_controls':scalar_controls(),
            'shifted22_controls':shifted22_controls(),
            'spectral_control':spectral_control(),'primary21_control':baseline_control()}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
