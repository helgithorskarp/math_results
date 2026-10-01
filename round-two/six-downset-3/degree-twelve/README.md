# Degree-twelve seven-point triple downsets: exact capped H classification

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.

Include the full two-skeleton below any simple twelve-regular collection of
triples on seven points. All **ten permutation classes**, representing
**11,205 labelled collections**, have supplied rational capped H matrices
with N=57, s=19, rank L=50 and rank(I-M)=56. Rank 50 is maximal among all
real H matrices; the seven stars are the only maximum intersecting families.
Every supplied matrix has entries in (1/760)Z.

Two transitive classes are credited published baselines. The new finite
spectral coverage consists of **eight nontransitive classes and 10,815
labelled inputs**. Complementing the earlier cubic triple collections gives
complete enumeration, with fresh dense canonicalization and separate exact
matrix checks. See [PROOF.md](PROOF.md) for scope, completeness, ranks and
prior-work credits. General H/I remain open. This is author-checked and
unformalized, with no independent-review claim.

For arbitrary k>=0 cubic factors and l>=1 degree-twelve factors, the product
has N=36^k*57^l, largest star N/3, and rank L=N-7l. Its only maximum families
are the 7l coordinate stars belonging to degree-twelve factors. The public
[parent cubic contribution](../README.md) supplies the other factors,
the two census generators and the exact positivity helpers.

From the repository root, **CPython 3.11.2** or compatible Python 3.11+,
standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/degree-twelve/verify_degree_twelve.py --check round-two/six-downset-3/degree-twelve/DEGREE_TWELVE_RESULTS.json
~~~

Expected output:

~~~
exact ten-class degree-twelve coverage, capped ranks, and 18 rejection controls match
~~~

Two complete labelled enumerations agree entry by entry; full S7 orbits
certify canonical coverage. Fraction-free Schur elimination and integer
characteristic polynomials check both core PSD ranks, with additional full
matrix Schur checks. Eighteen corruption controls fail and six
positive/singular algorithm controls pass. Normal and Python -O replay
passed in 39.85 and 41.71 seconds, with peak child RSS below 32 MiB, using
one CPU and one thread. No additional packages are needed.

The fixed fixture is 23,106 bytes. Compact results include every class,
hole class, orbit size, denominator, rank, matrix hash and polynomial hash.
Their SHA256 is

~~~
00cb6076898dce8f500cc9157547fb83fbcb800727715f7f6a14c33d729a8e83
~~~

[SHA256SUMS](SHA256SUMS) includes the new source files, both imported parent
Python files and the parent ignore rules. Floating discovery and rational recovery choices lie outside
the exact proof boundary. No solver, external catalogue or private corpus
is required. The primary problem source is
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
whose v1 record was refreshed on 2026-10-01.
