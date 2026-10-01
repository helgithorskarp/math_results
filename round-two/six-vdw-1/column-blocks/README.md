# Exact ordinary-column repair for W(2,7)

Author: **six-vdw-1, researcher**, 2026-10-01. W(2,7) means two colors and
seven terms. The target is a binary coloring of [1,3704] avoiding every
nonconstant monochromatic seven-term arithmetic progression. No such
coloring is supplied here and no van der Waerden bound changes.

The [elementary lemma](PROOF.md) gives a useful exact construction reduction.
In zero-based coordinates, each residue column r=2,...,616 modulo617 has six
points and intersects every interval seven-AP at most once. The conditional
cost on two columns is consequently an exact twelve-bit quadratic with
twelve linear and thirty-six cross coefficients. Its minimum requires64
left-column cases; after each case, six right-column choices are independent
apart from an optional lower edit-count requirement. Sorting six adjusted
coefficients solves that requirement exactly. Boundary columns0/1 require
higher interactions and are excluded by the kernel.

The result generalizes to prime p>k-1 and length N=(k-1)p+s with1<=s<=k-1.
It applies to arbitrary interval colorings and frozen AP weights. The
original QR reference classes enter only the prescribed construction
constraints, not the column-geometry proof.

The reproducible construction example starts with an **invalid747-violation
word** and scans every one of188805 ordinary-column pairs per sweep. Five
sweeps give counts747,681,634,607,592,576. Further descent produced the
included **invalid526-violation word**. The latter has31 edits in original
QR color class0 and34 in class1. These are local search data, with no
optimality or nonexistence conclusion about the unrestricted target.

Run from a checkout with Python3.10+ and a C++17 g++ compiler:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-vdw-1/column-blocks/reproduce.py \
  --scratch /tmp/vdw-column-block-check
```

The scratch path must be absent or empty. The script runs children
sequentially and generates all executables, checkpoints, logs and expanded
tables there. It compares the canonical result to [expected.json](expected.json).
Checks include independent complete truth tables, literal progression
counts, sanitizer agreement, corruption and boundary controls, and exact
restart comparisons. See [VALIDATION.md](VALIDATION.md).

Count either supplied word directly, without importing the search:

```sh
python3 round-two/six-vdw-1/audit_repair.py --word \
  round-two/six-vdw-1/column-blocks/fixture-invalid526.bits
```

The checker covers all1141450 integer APs, starts0..3703 and steps1..617,
and gives explicit monochromatic examples in zero-based coordinates. A
coloring certificate would need count zero. Positive counts establish only
the invalidity of those particular words.

The native [repair search](../repair3704.cpp) imposes no periodicity and fixes
no point. It uses positive dynamic AP weights, single/pair/coherent moves
and exact conditional block moves, while applying original-class edit
floors30/30 and total65 as prescribed guidance. The cited
[uniform65 QR617 theorem](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total65)
is the external context for those floors. The general bilinear lemma needs
no floor theorem. A pair sweep saves its frozen word and pair-index progress
every256 pairs; partial sweeps leave the word unchanged. Version3 search
checkpoints preserve RNG, tabu, sparse weights and active-edge ordering.
Legacy versions1/2 are accepted with the documented new strategy.

For example, compile and perform a bounded resumable sweep:

```sh
g++ -std=c++17 -O2 round-two/six-vdw-1/repair3704.cpp -o /tmp/vdw-repair
/tmp/vdw-repair /tmp/vdw-repair-state sweep 3 3704 \
  round-two/six-vdw-1/column-blocks/fixture-invalid747.bits
/tmp/vdw-repair /tmp/vdw-repair-state sweep 3 3704
```

Use the start-word argument only when the checkpoint path is fresh.
The time argument is at most55 seconds and each positive search count is
a construction diagnostic. No timeout, interrupted sweep or resource limit
establishes mathematical nonexistence.

Inspected primary context remains
[Monroe, JCMCC128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Table1 length7/two colors>3703 and Table2 modulus617, refreshed2026-10-01.
Monroe puts length before number of colors. This is bounded located-source
evidence, not an exhaustive current-record claim. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides the cyclic construction context. The prior
[order-nine product obstruction](../crt23x27/README.md) explains why coupling
or unrestricted interval repair is useful; it is not a proof dependency.
No historical priority claim or independent peer-review verdict is asserted.
