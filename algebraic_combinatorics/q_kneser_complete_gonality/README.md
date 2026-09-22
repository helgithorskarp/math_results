# Complete ordinary q-Kneser gonality formula

For every prime power `q` and `n>=2r>=2`, this note proves

```text
sn(qK(n,r)) = gon(qK(n,r))
            = [n choose r]_q - [n-1 choose r-1]_q
            = q^r [n-1 choose r]_q.
```

Adjacency is zero intersection of `r`-subspaces of `F_q^n`; `gon` is
divisorial graph gonality. Generalized adjacency with a larger intersection
threshold is not covered. The [proof](THEOREM.md) is universal and includes
the full binary middle-dimensional family left outside the earlier
[density theorem](../q_kneser_dense_gonality/).

## The structural bridge

For `G_r=qK(2r,r)` over `F_2`, its adjacency matrix has binary rank
`binom(2r,r)`, by its Plucker/wedge factorization. An induced graph whose
components have at most three vertices therefore has at most
`3 binom(2r,r)/2` edges. The real Hoffman bound forces more than
`2^(r(r-1))/2` edges above the EKR family size. Since
`2^(r(r-1))>3 binom(2r,r)` for every `r>=3`, the largest such family still
has size `[2r-1 choose r-1]_2`.

The four-vertex uniform scramble consequently has hitting number
`N-alpha`, while a spectral cut argument gives its exact egg-cut number
`4d-12>N`. This closes all binary ranks at once. Rank two is handled by
the edge scramble (`sn=gon=28`); rank one is complete. A general
rank--Hoffman small-component criterion is proved along the way.

## Reproduce the exact audit

Requires Python 3.10+ and its standard library only; tested with CPython
3.11.2. From this directory:

```bash
python3 verify.py --check
python3 -O verify.py --check
python3 -m unittest -v
sha256sum -c SHA256SUMS
```

Both audit commands compare against [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json)
and report `"status": "VERIFIED"`; all checks remain active under `-O`.
The eight tests include corrupted-adjacency and corrupted-Plucker rejection,
basis invariance, two different subspace generators, and invalid inputs.

The audit checks every binary `r`-subspace for `r=1,2,3` using RREF and an
independent literal span-extension enumeration. It compares disjointness
with the Plucker factorization entry by entry, computes exact binary ranks,
and checks all integer incidence actions that underlie the spectral proof.
At `r=3` this means 1,395 vertices, 973,710 unordered matrix entries including
the diagonal, and 2,943,450 incidence identities. It also audits 600 scalar
parameter records, the structural inequalities for `3<=r<=64`, and all 11
labelled graphs on one to three vertices.

The 600-record digest is
`4d32f767a822edd10429f8094a8d1e82469b1037904de105f3e621676202674c`.
Complete audits took 4.4--6.8 seconds on the campaign host; a measured replay
used 59,896 KiB peak resident memory.
No downloaded dataset, solver, numerical eigensolver, floating-point
arithmetic, or large certificate is needed or omitted.

## Status and attribution

This is a proved written theorem with a finite corroborating audit, pending
independent mathematical review. It is not a formally verified theorem.
The EKR bound, q-Kneser spectrum, exterior algebra, and general scramble
bounds are credited prior tools. The new claim is the rank--Hoffman bridge
and its application completing the gonality formula, not those classical
ingredients. [SOURCES.md](SOURCES.md) records primary inputs and the limits
of the live literature search. No absolute priority claim is made.
