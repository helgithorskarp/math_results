#!/usr/bin/env python3
"""Definition-level exact checks, separate from the friendship core generator."""
from fractions import Fraction as F
from itertools import combinations
import json
import certificates as build
import deletions
import friendship
from verify import check, psd_ldl, require


def direct_matrix(k):
    members = friendship.family(k)
    size = len(members)
    denominator = 3 * k + 1
    center = 1 << (2 * k)
    matrix = [[F(0) for _ in members] for _ in members]
    matrix[0][0] = F(-2 * k, denominator)
    for i, a in enumerate(members[1:], 1):
        matrix[0][i] = matrix[i][0] = F(1, denominator)
        for j, b in enumerate(members[1:], 1):
            if i == j or a & b:
                continue
            if (a == center or b == center):
                value = F(1, denominator)
            elif bool(a & center) != bool(b & center):
                spoke, other = (a, b) if a & center else (b, a)
                leaf = (spoke ^ center).bit_length() - 1
                block = leaf // 2
                other_block = ((other & -other).bit_length() - 1) // 2
                value = F(k, (k - 1) * denominator) if block != other_block else F(0)
            elif a.bit_count() == b.bit_count() == 1:
                value = (F(k - 1, denominator)
                         if (a.bit_length() - 1) // 2 == (b.bit_length() - 1) // 2 else F(0))
            elif a.bit_count() == b.bit_count() == 2:
                value = F(1, denominator)
            else:
                value = F(0)
            matrix[i][j] = value
    return members, matrix, 2 * k + 1


def main():
    cases = []
    for k in range(1, 11):
        members, matrix, s = friendship.certificate(k)
        size = len(members)
        rank = check(members, matrix, s, upper=True)
        core = build.extract_core(matrix, s)
        require(all(sum(row) == 0 for row in core), "Friendship core is not centered")
        require(all(core[i][j] >= -1 for i in range(len(core)) for j in range(len(core)) if i != j),
                "Centered-core cap hypothesis failed")
        expected_rank = 3 if k == 1 else 5 * k
        require(rank == expected_rank, "Wrong friendship Hoffman rank")
        if k >= 2:
            require((members, matrix, s) == direct_matrix(k), "Core and direct weight formula disagree")
            schur = F(2 * k + 1) - F(7 * k, 3 * (k - 1) ** 2)
            require(schur > 0, "Friendship reduced Schur remainder is not positive")
            # Independent cap identity: I-M is the Laplacian of nonnegative weights.
            laplacian = [[F(0) for _ in members] for _ in members]
            for i in range(size):
                for j in range(i + 1, size):
                    w = matrix[i][j]
                    require(w >= 0, "Negative off-diagonal weight")
                    laplacian[i][i] += w
                    laplacian[j][j] += w
                    laplacian[i][j] -= w
                    laplacian[j][i] -= w
            require(all(laplacian[i][j] == F(int(i == j)) - matrix[i][j]
                        for i in range(size) for j in range(size)), "Cap Laplacian identity failed")
            require(psd_ldl(laplacian) == size - 1, "Upper endpoint is not simple")
            expected_rank_core = size - 3
            require(psd_ldl(core) == expected_rank_core, "Wrong friendship core rank")
        cases.append({"k": k, "N": size, "s": s, "L_rank": rank,
                      "lower_endpoint": str(F(-s, size - s)),
                      "lower_endpoint_multiplicity": size - rank})
    # Same family, two failed inherited/templates and a successful new matrix.
    removed_cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
    inherited_members, inherited_matrix, inherited_s = deletions.deletion_certificate(5, removed_cycle)
    new_members, new_matrix, new_s = friendship.certificate(2)
    # Relabel the first four coordinates so the retained matching becomes (0,1),(2,3).
    permutation = [0, 2, 1, 3, 4]
    relabel = lambda a: sum(1 << permutation[v] for v in range(5) if a & (1 << v))
    require({relabel(a) for a in inherited_members} == set(new_members)
            and inherited_s == new_s == 5, "Cycle deletion is not F_2")
    require(not deletions.cap_test(5, removed_cycle)[0], "Inherited cycle restriction is unexpectedly capped")
    check(new_members, new_matrix, new_s, upper=True)
    # The other small failure already has a capped equitable partition (N=11,s=5).
    removed_diamond = [e for e in combinations(range(4), 2) if e != (0, 1)]
    retained = deletions.deletion_certificate(5, removed_diamond)[0]
    edges = list(combinations(range(5), 2))
    mask = sum(1 << i for i, (a, b) in enumerate(edges) if ((1 << a) | (1 << b)) in retained)
    partition = build.rank_two_certificate(5, mask)
    require(partition[0] == retained and len(retained) == 11 and partition[2] == 5,
            "Wrong diamond deletion repair")
    check(*partition, upper=True)
    product = build.product_certificate([friendship.certificate(2), build.matching_certificate(2, 0, 5)])
    product_rank = check(*product, upper=True)
    for bad in (0, -1):
        try:
            friendship.certificate(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("Invalid friendship family accepted")
    print(json.dumps({"friendship_cases": cases, "friendship_N_max": 52,
                      "cycle_deletion_repaired": {"N": 12, "s": 5, "L_rank": 10},
                      "diamond_deletion_partition_repair": {"N": 11, "s": 5},
                      "mixed_capped_product": {"N": len(product[0]), "s": product[2], "L_rank": product_rank},
                      "rejection_controls": 2}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
