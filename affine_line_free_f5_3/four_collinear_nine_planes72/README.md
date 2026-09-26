# A global two-arrangement reduction at 72 points

Every 72-point line-free subset of \(\mathbb F_5^3\) has at least twelve
nine-point plane sections. Four of their normals are collinear.
After projection along the common direction, four nine-lines can be
normalized to exactly two possible affine arrangements:

\[
(y=0,\ y=x,\ y=2x,\ y=3x+1)
\quad\text{or}\quad
(y=0,\ y=x,\ y=2x+1,\ y=3x+1).
\]

The [proof](THEOREM.md) adds plane-pair consistency to the prior incidence
system, then uses an elementary twelve-point argument in
\(\operatorname{PG}(2,5)\). It builds on researcher 2's
[eight-plane exclusion](../no_eight_planes72/README.md) and the previous
[weighted incidence bound](../nine_plane_frame72/README.md).

Every candidate therefore has a quotient with four parallel-class
profiles \(B=(9,15,16,16,16)\). This supplies a global filter for the
remaining lifting problem. **Neither arrangement is excluded here.**
The interval remains \(70\le r_5(\mathbb F_5^3)\le72\).

Combined with the concurrent
[quadratic moment theorem](../quadratic_moments72/README.md), this forces
exactly twelve nine-planes in both higher-rank cases. Rank two retains
only occupancies \((4,4,4)\); rank three retains only the normal pattern
\(K_6\) minus a perfect matching.

From this directory, with Python 3.10+ and a C++20 compiler:

~~~sh
python3 verify.py --out build
~~~

Expected status: FOUR_COLLINEAR_NINE_PLANES72_VERIFIED, matching
[EXPECTED.json](EXPECTED.json). Tested with Python 3.11.2 and GCC 12.2.
The replay needs no Python packages, optimizer, SAT solver, network or
external catalogue. It reuses and replays the parent planar census.
The new Farkas certificate has 72 integer multipliers, checks 463
nonnegative column sums, and has right-side scalar product \(-181596\).

The package also checks an integer solution of all 45 added plane-pair
identities and two feasible integer quotient controls. These demonstrate
specific limits of the relaxations, not the existence of a 72-point set.
All source and compact evidence hashes are in [SHA256SUMS](SHA256SUMS).

The imported no-eight-plane theorem has separate SAT proof replay
requirements; this checker does not rerun those exclusions. See
[SOURCES.md](SOURCES.md) for dependencies, discovery provenance and scope.
