# Cubic seven-point triple downsets: exact capped H classification

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.

For every simple triple collection on seven points with each point in
exactly three triples, include all pairs, singletons and the empty set.
All **ten permutation classes**, representing **11,205 labelled collections**,
have explicit rational capped H matrices with N=36, s=10, rank L=29 and
rank(I-M)=35. The latter rank gives a simple unit endpoint. Rank 29 is
maximal among all real H matrices, and the seven stars are the only maximum
intersecting families. Every finite product of arbitrary factors from this
cohort has rank 36^k-7k and precisely 7k maximum coordinate stars.

The two transitive classes are credited published baselines. The spectral
increment covers **eight nontransitive classes and 10,815 labelled inputs**.
See [PROOF.md](PROOF.md) for the precise scope, completeness arguments,
rank/equality/product bridges and prior-work credits. This does not cover
all regular seven-point triple collections. General H/I remain open; the
result is author-checked and unformalized, with no independent-review claim.

From the repository root, **CPython 3.11.2** or compatible Python 3.11+,
standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/verify_cubic_seven.py --check round-two/six-downset-3/CUBIC_SEVEN_RESULTS.json
~~~

Expected output:

~~~
exact ten-class cubic seven-point coverage, capped ranks, and 18 rejection controls match
~~~

Two complete labelled enumerations agree entry by entry. Full S7 orbits
certify canonical coverage. Both fraction-free Schur elimination and integer
characteristic polynomials check all core PSD ranks; Schur checks also cover
the full matrices. Eighteen corruption controls fail and six positive/singular
algorithm controls pass. Normal and Python -O runs passed in 8.96 and 8.08
seconds, with peak child RSS below 31 MiB, using one CPU and one thread.

The exact fixture is 13,640 bytes; no solver, floating-point package,
external catalogue or private corpus enters verification. Discovery used
NumPy 1.24.2 least squares followed by exact rational affine recovery; it
is outside the proof boundary. Compact results include every class, matrix
hash, polynomial hash and rank. Their SHA256 is

~~~
48b77c13f67dd0df27bb3e91c5f7ba2d71b1fe808acf80f6be8e29771584b310
~~~

Source checksums are in [SHA256SUMS](SHA256SUMS). The primary problem source
is [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
with its v1 record refreshed on 2026-10-01.
