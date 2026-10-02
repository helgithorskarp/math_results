"""Independent exact projected inventories, never claimed to be packings."""
import math
from literal import require, digest


def constants(m):
    n = 18-m
    return n, 20+10*m-5*m*m, 4*n-math.comb(n,3)-120*m+740


def tables():
    # Complete at and below the three published/new ordinary thresholds.
    frontiers = {1:0, 2:3, 3:9, 4:19, 5:34}; rows = []; actual_boundary = []
    for m, frontier in frontiers.items():
        n,C,B = constants(m); kept_old = []; kept_new = []
        for P in range(frontier+1):
            W = C+2*P
            if W < 0: continue
            for T in range(math.comb(m,3)+1):
                base = B+3*P-T
                if base < 0: continue
                for tau in range(base//2+1):
                    total = base-2*tau
                    if total > 4*n: continue
                    for X in range((5*n-W)//2+1):
                        for E in range(total+1):
                            Q = total-E
                            if E < 2*X: continue
                            old = 8*E+11*Q >= 4*W and 11*E+8*Q >= 4*W+6*X
                            if old: kept_old.append([P,T,tau,X,E,Q])
                            new = 8*total >= 4*W+8*X
                            if not new: continue
                            require(old, 'new unified cut must imply both old cuts')
                            kept_new.append([P,T,tau,X,E,Q])
        rows.append({'m':m,'n':n,'C':C,'B':B,'old_count':len(kept_old),'new_count':len(kept_new),
                     'old_min_P':min((v[0] for v in kept_old),default=None),
                     'new_min_P':min((v[0] for v in kept_new),default=None),
                     'old_whole_sha256':digest(kept_old),'new_whole_sha256':digest(kept_new)})
        if m in (3,4,5):
            boundary = [v for v in kept_new if v[0] == frontier]
            require(boundary, 'necessary ordinary boundary is not an occurrence claim')
            if m in (3,4): require(all(v[1:4] == [0,0,0] for v in boundary), '3/4-hub new equality slacks')
            else: require(all(v[2] == 0 and v[1]+v[3] <= 1 for v in boundary), 'five-hub P34 boundary')
            actual_boundary.append({'m':m,'P':frontier,'count':len(boundary),'inventories':boundary})
    require([r['new_min_P'] for r in rows] == [None,3,9,19,34], 'exact new coarse threshold table')
    return {'rows':rows,'boundaries':actual_boundary,'count_profiles_are_not_realized_packings':True}


def scalar_controls():
    checked = 0; strict = 0; good = []
    # Every independent row-count parameter in this bounded box obeying
    # the exact two capacity premises, without assumed global occurrence.
    for M in range(7):
        for E in range(M, 4*M+1):
            for M0 in range(M+1):
                for QM in range(9):
                    for QU in range(9):
                        Q = QM+QU
                        for Z in range(9):
                            if 4*Z > 4*M0+3*QM: continue
                            K = Z+M-M0+QM+2*QU
                            for X in range(E//2+1):
                                W = K+E-2*X
                                left = 8*(E+Q)
                                right = 4*W+8*X+4*(E-M)+QM
                                require(left >= right, 'exact unified scalar elimination')
                                checked += 1
                                strict += 4*(E-M)+QM > 0
                                good.append([M,E,M0,QM,QU,Z,X,left-right])
    require(checked and strict, 'nontrivial scalar control box')
    return {'coupled_scalar_checks':checked,'nonzero_strengthening_corrections':strict,
            'whole_ordered_scalar_sha256':digest(good)}
