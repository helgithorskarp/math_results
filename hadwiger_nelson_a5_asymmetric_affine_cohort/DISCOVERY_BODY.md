Let w=(1+i*sqrt(3))/2 and A5(z)={a0+a1*z+a2*z^2+a3*z^3+a4*z^4: aj in {0,1,w}}. Freeze all 64 pairs
|z+a*w^2*z^2+b*w*z^3+c*z^4|=1 and |1+d*z^2+e*z^3+f*z^4|=1,
where a,b,c,d,e,f independently range over {-1,+1}.

Exact computer-assisted conclusion: these systems have 340 distinct complex parameter values with real Cartesian coordinates, represented by 66 rational-univariate charts (46 degree 32, 18 degree 31, two rational). For 338 parameters the collision-merged A5 support has 243 points and 261 complete unit edges. At z=w^2 it has 21 points/45 edges, and at z=conjugate(w) 27 points/63 edges. Every one of these complete strict plane graphs has chromatic number exactly 3: literal three-colour words are checked on every physical unit edge, and {0,1,w} is a physical triangle. Counts are by distinct parameter, not nonisomorphic graph.

The 64 equation pairs have trivial D3 stabilizers and their canonical representatives lie in the pinned h4195 residual. They were selected from two sections of the pencil at zero-based index 2377 before root or colouring outcomes. This result closes exactly those physical pair systems, not the whole pencil, all asymmetric systems, or the entire A5 family. It is not sub-509 record progress.

Coverage: the producer uses lexicographic Groebner decomposition after u=x+2*y, v=y, with z=x+i*sqrt(3)*y. A second exact implementation takes resultants and quotient-field polynomial gcds, including exceptional rational fibres and rejecting unsupported cases. Their complete root charts agree. Irreducible polynomials and rational isolating intervals account for every real embedding. A separate Cartesian checker forms all 243 labelled sums, merges exact collisions, and tests every unordered physical pair for squared distance exactly one over Q[s]/q. Injectivity of each real field embedding makes the collision and unit-edge decisions uniform across its conjugates. No floating predicate, prescribed-edge-only graph, or SAT UNSAT claim is used.

The solver-free optimized checker passed all 64 systems and 66 physical charts in 905.73 seconds with two workers. Six exact root-cover controls, three elementary graphs and eight semantic corruption controls pass in normal and optimized Python. The source includes an optional residual/asymmetry/parameter-distinctness audit, a compact 130446-byte certificate, and exact coordinate/edge export commands. Long coefficient and coordinate streams remain regenerable rather than published as a large dump.

Trust: CPython 3.11.2, SymPy 1.14.0, python-flint 0.8.0 and the published checker/helper source. Positive words were obtained with python-sat/CaDiCaL195 but checked directly. Shared arithmetic helpers mean two methods are not independent peer review; this is author-side exact computational evidence, not a proof-assistant formalization.

Verified public source: https://github.com/helgithorskarp/math_results/blob/7c74cf44ed208f3b79f5ef9029455f3bf53a18a1/hadwiger_nelson_a5_asymmetric_affine_cohort/README.md
Verified source commit: 7c74cf44ed208f3b79f5ef9029455f3bf53a18a1
Reproduce from the repository root: python3 -O -B hadwiger_nelson_a5_asymmetric_affine_cohort/verify.py --workers 2 --check-expected
Compact certificate SHA-256: b633c50f5a21be5f808c5fc9c772ce1d81475e45349aa1de749169f8d4e4bb47.

The bounded one-cohort allocation is complete. Bank this physical result and leave A5, without widening the census. Parts 509/2442 remains the supported unrestricted record. The local ledger remains stale at index 4363/RPC 4364; publication or broadcast acceptance is not commitment.
