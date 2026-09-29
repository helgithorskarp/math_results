# A two-pair Schur axis cannot support 54 first-column special entries

**Computer-assisted upper bound, with sharpness unresolved.** Let
`E : (Z/109Z)\{0} -> {0,1,2,3,4,5}` be reflected and modularly sum-free,
including equal summands, with colour 0 exactly at `{±1}` and colour 1
exactly at `{±2}`. Let `V : Z/109Z -> {0,2,3,4,5}` satisfy

```
V(x)=V(y)=E(y-x) is forbidden whenever x != y.
```

Then **colour 0 occurs in V at most 53 times**. This covers every axis
with those two fixed classes and every qualifying first column, with no
run-order, interval, seed or second-column restriction. The elementary
cycle bound alone is 54; this result excludes equality using all axis
and first-column constraints together.

No example attaining 53 is supplied. The existence of any such column
at modulus 109 remains unresolved in our searches. This is not an exact
capacity determination, a full 544-colouring, or a new numerical bound
on S(6). The [preceding independently reviewed axis classification](../schur6_two_pair_axis_109_review1/REVIEW.md)
classifies the relative positions of two size-two axis classes; the
present result constrains a column over its surviving doubling position.

## Reduction to one finite formula

Let `S={q:V(q)=0}`. Since `E(±1)=0`, S is an independent set in the
109-cycle. Thus `|S|<=54`. If `|S|=54`, its 54 cyclic gaps are all at least
2 and sum to 109. Exactly one gap is 3 and the other 53 are 2. Consequently
S is a translate of

```
S0 = {0,2,4,...,106}.
```

Translating **V alone** preserves its difference condition and leaves E
unchanged. We may therefore fix `S=S0`. This normalization is for the
one-column necessary condition; it is not an arbitrary translation
symmetry of the full two-column construction.

The other 55 column positions are `T={1,3,...,107,108}`. They use only
colours 2,3,4,5. The 52 positive-half axis positions `3,...,54` also use
these four colours. Give each one exactly one colour. Reflect the axis,
forbid every nonzero modular axis sum, and for every pair `x<y` in T
forbid `V(x)=V(y)=E(y-x)`. Differences `±1,±2` have fixed axis colours
0,1, so their common-colour constraints are automatically satisfied.
Colour-0 column pairs satisfy the difference condition because S0 is
cycle-independent. No other constant constraints remain.

The four common colour names are ordered by their first appearance on
the positive axis. This is valid even if a colour is unused on the axis
but used in the column: order the used axis colours first and put unused
axis colours last, permuting V simultaneously. There is no additional
symmetry restriction on the column.

The resulting formula has **428 variables and 10161 clauses** and is
UNSAT with a checked DRUP certificate. This excludes the only possible
cycle pattern at size 54, proving the stated upper bound 53.

## Encoding, verification and trust

For `q=3,...,54`, variable `4(q-3)+c+1` assigns colour `c+2` to axis
residues `±q`, where `c=0,1,2,3`. If `q` is the j-th position of T in
increasing order, variable `208+4j+c+1` assigns colour `c+2` to V(q).
Exactly-one constraints use one positive row and all pair exclusions.

`audit.py` imports neither encoder nor solver. It reconstructs **all
six colours**, substituting constants at every fixed axis and column
position. It examines all ordered nonzero axis sums, all column pairs,
and the first-appearance clauses, then compares the full clause set and
exact DIMACS hash. It checks the 109 distinct maximum-support rotations
and their gap patterns; completeness follows from the elementary gap
sum argument above. Checks remain active under Python `-O`.

The CNF has 170880 bytes and SHA-256
`ed370a49ae6f766d1c3d728d0ecbdac14d275d3d4b607c155b6339067557f061`.
Glucose 4 through `python-sat==1.9.dev15` generated a 91233941-byte text
DRUP proof with SHA-256
`0cfb50c37a7969ff795de82a2708288012924fa64232146dbb4f351ca7106579`.
DRAT-trim revision `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` accepts it;
the public auditor explicitly requests ASCII parsing and RUP-only
checking (`-I -U`). The reference proof uses zero RAT lemmas. Harmless
warnings about deleting absent clauses may appear; proof acceptance,
not a solver status or hash, is the verification gate.

The proof and logs are generated locally and omitted from Git. Full
metadata appears in `certificate.json`; `verified.json` records the
reference check. The mathematical reduction, finite literal encoding,
Python execution and C proof checker are the trust boundary. The bound
in the opening statement does **not** require the external S(4)=44
theorem: its axis conditions are encoded directly. It is not a
proof-assistant formalization. External review is pending, and no
historical priority is claimed for adapted colouring or cycle arguments.

## Reproduce

Python 3.11+ and its standard library suffice for the model audit.
Proof generation additionally needs the pinned Python package and
[DRAT-trim](https://github.com/marijnheule/drat-trim) at the cited revision.
Reference search used Python 3.12.14; the independent audit also passed
under Python 3.11.2. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 audit.py
python3 encode.py /tmp/schur-column-capacity.cnf
python3 audit.py --cnf /tmp/schur-column-capacity.cnf
python3 -m venv /tmp/schur-column-env
/tmp/schur-column-env/bin/pip install -r requirements.txt
/tmp/schur-column-env/bin/python prove.py --output /tmp/schur-column-proof \
  --drat-trim /path/to/drat-trim
```

The first two audit modes explicitly report `proof_checked: false` and
do not establish the exclusion. The final command must report
`FIRST_SPECIAL_COLUMN_UPPER_BOUND_53_VERIFIED`, `proof_checked: true`,
and `sharpness_established: false`. Its defaults allow one million
conflicts, 120 seconds for solving and 120 seconds for proof checking;
`--conflicts` and `--seconds` can change them. A proof above 128 MiB is
rejected before writing. Timeout or incomplete search is not an exclusion.
Reference generation and checking took about one minute combined.
Allow roughly 100 MiB of output space, plus solver memory.

Already generated proofs can be checked separately:

```sh
python3 -O audit.py --cnf /tmp/schur-column-proof/capacity.cnf \
  --proof /tmp/schur-column-proof/capacity.drup --drat-trim /path/to/drat-trim
```

## Full-colouring consequence and limitations

In the reflected independent-column model modulo 545, colour 0 can
occupy axis points `±5` and first-column pairs `±(5q+1)`; colour 1 can
occupy axis points `±10` and second-column pairs `±(5q+2)`. The four
common colours may occur in both columns. Every full colouring has the
displayed first-column difference condition. Hence, under this axis
normalization, its complete colour-0 class has size at most
`2+2*53=108`.

More invariantly, suppose both **physical special colours** have size-two
axis classes in this independent-column model. The reviewed axis theorem
forces them to be a doubling pair. Normalize the preceding pair to
`{±1}` by a unit modulo 109. CRT lifts it to a unit modulo 545 congruent
to 1 modulo 5 when the special labels stay fixed, or to 2 modulo 5 when
the two columns and both special labels are exchanged. Thus the special
colour whose axis pair doubles to the other has complete class size at
most 108. This last formulation uses the preceding reviewed theorem.

This does not bound the other special column in the opposite orientation,
does not cover arbitrary off-axis palettes, and does not force size-two
axis classes to occur. It leaves smaller column supports, larger special
axis classes and unrestricted 537-colourings open. No new full colouring
beyond the [established 536 baseline](https://arxiv.org/abs/2607.15034)
is asserted.
