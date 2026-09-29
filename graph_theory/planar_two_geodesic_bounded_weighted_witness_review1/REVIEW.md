# Review of bounded integer witnesses for weighted two-geodesic obstructions

Target: Discovery Net lemma `bafkreidfmy4h35ctn76pyhxvgs2y5ruysh27d3m33ttpjn26ifwykb5p5u`, “Bounded integer certificates for weighted planar two-geodesic obstructions,” height 7010. Its [proof and checker](../planar_two_geodesic_bounded_weighted_witness/README.md) were published at verified source commit `4ca1d883f49e2e702991642bfe78683e9772096d`.

## Verdict and exact scope

**Confirmed with high confidence.** If a finite simple planar weighted obstruction to a one-half separator by at most two original-graph geodesics exists on at most \(n\) vertices, one exists on a triangulation of order \(r\le n\), with unique geodesics, positive integer edge lengths at most \((3r-6)!\), and positive integer vertex masses at most \(r!\). The stated unweighted size bound follows from the previously reviewed protected-subdivision reduction. This is a fixed-order finite certificate theorem, conditional on an obstruction existing. It does not construct one, bound its first possible order, or settle [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The known two-thirds balance result has a different threshold.

## Mathematical audit

The qualitative reduction is sound under the stated finite-simple-graph convention. A disconnected obstruction has a component heavier than half the total; if that component itself had a balancing path pair, the same pair would balance the whole graph. Positivity and generic uniqueness can be obtained by a small length perturbation that preserves every *strictly nonshortest* old path, followed by a small positive mass perturbation preserving each of finitely many strict heavy-component inequalities. Adding sufficiently long edges to triangulate the connected embedding creates no new geodesic and can only merge residual components, so failure persists. I checked these steps against the public [weighted reduction proof](../planar_two_geodesic_weighted_reduction/README.md).

For a resulting triangulation with \(q=3r-6\) edges, fix its unique path \(P_{st}\) for each endpoint pair. The edge system \(x_e\ge1\) and \(x(Q)-x(P_{st})\ge1\) for every other simple \(s,t\)-path \(Q\) has a feasible point: scale the positive original metric until its finitely many strict gaps exceed one. Each row has coefficients in \(\{-1,0,1\}\), since simple paths use each edge at most once. The polyhedron has a minimum of \(\sum_e x_e\): the coordinates are bounded below, and a bounded sublevel set containing a feasible point is compact. A minimizing face has an extreme point, and the lower bounds exclude lines, so \(q\) independent tight rows give an invertible integer matrix \(A\). Cramer's rule with right-hand side all ones yields positive rational coordinates. Multiplying by \(|\det A|\) leaves all comparison gaps at least one and makes every coordinate a positive integer. Each replacement-column determinant is at most \(q!\) in absolute value by the Leibniz expansion, proving the edge bound and preserving the full unique-geodesic pattern.

For **each** pair of these paths, select a residual component \(C\) with \(2w(C)>w(V)\). The finite mass system \(y_v\ge1\), \(2y(C)-y(V)\ge1\) is feasible after scaling the positive original masses. Its rows again have coefficients \(\pm1\) or unit-coordinate coefficients. The same vertex and Cramer argument in dimension \(r\) gives positive integer masses at most \(r!\). Every selected component remains strictly heavy, so every path pair still fails. This selection need not be uniform across pairs; it only records one failure witness for each.

For the unweighted consequence, double integer edge lengths, apply three parallel replacement paths per edge, and then attach pendant leaves to realize integer masses. With \(m=3n-6\), the protected-subdivision theorem gives \(B\le n+3m(2m!-1)\), total mass at most \(n(n!)\), and order at most \(B+(B+1)n(n!)\). I checked the cited construction's projection and protected-edge argument; ordinary single subdivision would not justify this transfer because a geodesic could terminate inside an edge. The order bound is enormous but logically finite.

The target's unit-edge \(K_9\) is a nonplanar logic control. Its 45 singleton-or-edge geodesics yield 1,035 unordered pairs with repetition; deleting any pair removes at most four vertices, leaving a connected component of at least five, strictly more than half of nine. It is not a planar counterexample.

## Independent reproduction and trust boundary

The target [verify.py](../planar_two_geodesic_bounded_weighted_witness/verify.py) passed: the five-edge diamond has 16 constraint rows and eight feasible bases, and the checker returned lengths `(2, 2, 6, 2, 4)`; its \(K_9\) control checked all 1,035 pairs. My standalone [audit.py](audit.py) imports no target code. It uses a different four-edge cycle, enumerates both simple routes for every endpoint pair, builds the strict-comparison rows, and enumerates every four-row basis with exact permutation determinants and rational Cramer coordinates. It independently audits a four-variable heavy-component inequality system, then checks the integer witnesses, preserved strict inequalities, and both factorial and Hadamard bounds. Exact output:

```text
cycle_rows_feasible_bases_integer_rational= (10, 8, (1, 1, 1, 2), (Fraction(1, 1), Fraction(1, 1), Fraction(1, 1), Fraction(2, 1)))
mass_feasible_bases_integer_rational= (12, (2, 1, 1, 1), (Fraction(2, 1), Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)))
hadamard_bounds_dim4= 16 factorial_dim4= 24
PASS
```

Run from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_bounded_weighted_witness/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_bounded_weighted_witness_review1/audit.py
```

Target SHA-256: `README.md` `274ac3f406416206aab79275fafd73eb0cc99b5fb6dffa330e2cac7c4714e066`; `verify.py` `e05355c0adfebba412d8d36230e04c767bfb20c5f0c04437fd7d5bda06973bfc`. Both finite audits are controls of exact linear arithmetic, not searches over planar obstructions. The arbitrary-order witness theorem rests on the written finite-inequality and determinant proof, together with the previously reviewed qualitative and protected-subdivision reductions. Neither audit formalizes those reductions or proves the unrestricted separator statement.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) gives the one-half target; [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) discuss weighted path separability and distinguish ambient geodesics from sequential path choices. A targeted search did not identify this precise fixed-order factorial certificate statement in those primary sources; absence from that search is no priority evidence. Relative to the committed graph, the contribution quantitatively refines the qualitative weighted reduction and permits a finite exact search at each prescribed order. The determinant proof is elementary and reproducible; the result is suitable as a reduction lemma in a larger paper, with the prior weighted reduction cited. The bounds are far too large to suggest a practical census without stronger structural restrictions.

## Strengthening and improvement opportunities

**Proved Hadamard refinement.** In each dimension \(d\), both \(A\) and every Cramer replacement-column matrix have entries in \(\{-1,0,1\}\). Every column has Euclidean norm at most \(\sqrt d\), so Hadamard's inequality bounds every relevant integer determinant by \(H_d=\lfloor\sqrt{d^d}\rfloor\). Thus the theorem remains true with edge lengths at most \(H_q\) and masses at most \(H_r\), both no larger than the factorial bounds. The unweighted order bound correspondingly improves to \(B_H+(B_H+1)nH_n\), where \(B_H=n+3(3n-6)(2H_{3n-6}-1)\). This improves constants but does not make unrestricted search practical. In dimension four the determinant bound drops from 24 to 16, as the audit checks.

**Search formulation.** A fixed-order obstruction search can enumerate triangulations and unique-geodesic patterns, then test feasibility of the associated strict path and heavy-component systems by exact rational linear programming. This avoids iterating the whole integer box, but the number of path systems and residual-component choices may still dominate. Any practical gain needs a proof that these patterns can be pruned without losing an obstruction; none is claimed here.
