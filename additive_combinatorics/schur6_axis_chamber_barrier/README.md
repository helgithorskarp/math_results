# An axis-only barrier for unit-reseeded Schur constructions

**Theorem.** The union of the 35 axis interval-separation chambers specified
below has exact maximum modulus **107**. Consequently a reflected
six-colouring of `[1,5a-1]` whose axis lies in this union has endpoint at most
**534**, even when every off-axis position may use any of the six colours.
The bound on the **axis modulus** is attained; attainment of a full
534-point colouring in this family is not claimed.

This rules out reaching 537 through these axis chambers. It does not bound
the unrestricted sixth Schur number or exclude all independent columns.
The classical greatest-colourable-endpoint bound remains `S(6)>=536`, from
[Fredricksen and Sweet](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
also used in the [2026 shifted-template paper](https://arxiv.org/abs/2607.15034).
Repeated summands, including `x+x=z`, are included throughout.

## Axis family

The full 354-point colouring in `seed.json` is the independently
[reviewed attainer](../schur6_independent_interval_chambers_review1/REVIEW.md)
of the earlier interval-chamber result. It is reflected modulo 355 and has
class sizes `[46,50,110,56,48,44]`. Its axis word is

```
e(q) = seed(5q),  1 <= q <= 70.
```

This is a symmetric modular Schur colouring of the nonzero residues modulo
71. Apply all 70 units modulo 71. Reflection identifies multipliers `u`
and `71-u`, leaving exactly 35 representatives `1<=u<=35`. For each image,
read the maximal constant runs of its positive half, positions `1,...,35`.
Their colours and linear order are fixed. Replace each run length by its
own positive integer variable `l_j`; set `h=sum(l_j)`, `a=2h+1`, and reflect
the half-word across `q -> a-q`. There are 18 to 33 run variables.

An additional restriction retains the separating side of every axis
interval comparison described below, as selected by the unit seed. This is
an **interval-separation chamber**, not the entire family with that run
order. Different separation sides, inserted or merged runs, other seeds,
and subsequent unit reseeding after a deformation are not covered. No
upper bound on the candidate run lengths is assumed. Global permutations
of the six colour names preserve every conclusion.

There are no column variables or conditions. In particular, the result
allows arbitrary off-axis run orders, lengths, supports, colour choices,
and any equality or inequality between the two short columns. It even
allows off-axis colours outside the residue domains of the earlier
independent-column model. The restriction is solely on the axis.

## Exact interval argument

Let `Ei` be the axis support of colour `i` in `[1,a-1]`. Each support is a
union of positive-half intervals and their reflections. List the positive
intervals in order, followed by their reflections in corresponding order.
The half-axis starts at 1, and all endpoints are inclusive affine forms in
the run lengths.

The axis is modularly sum-free exactly when `(Ei+Ei)` misses `Ei` modulo
`a`, for every colour. For all constituent intervals `I,J,K` of `Ei`,
compare `I+J` with `K+t*a`, for `t=0,1`, allowing `I=J`. These two wraps
exhaust the possible sums. Two closed integer intervals `[l,r]` and `[L,R]`
are disjoint exactly when `r<=L-1` or `R<=l-1`. Retaining the seed's side
gives one affine inequality for each comparison. Add `l_j>=1`.

Each compact certificate names selected inequalities and positive rational
weights whose sum is exactly `a-B<=0`. Some certificates first bound an
integer linear expression in the run lengths by a rational number, then
replace that upper bound by its floor. Every such step is checked before
it may be used in later inequalities. There are no column-total equalities
or other hidden premises.

The 35 certificates contain **614 weighted terms and 11 integer-rounding
steps**. Their bounds are:

| Axis unit representative | Rational bound on `a` | Largest permitted odd `a` with `3` not dividing `a` |
| --- | ---: | ---: |
| the other 26 representatives | 71 | 71 |
| 6 | 97 | 97 |
| 7 | 92 | 91 |
| 8 | 81 | 79 |
| 10 | 79 | 79 |
| 11 | 104 | 103 |
| 15 | 107 | 107 |
| 17 | 95 | 95 |
| 30 | 83 | 83 |
| 32 | 101 | 101 |

The exclusion `3|a` is immediate: reflection identifies the colours at
`a/3` and `2a/3`, contradicting `a/3+a/3=2a/3`. The largest cap is 107.
The potentially decisive case `u=11` initially has a rational bound above
109. Its certificate first proves that the last run is at most `5/2`,
hence at most 2, then that the last two runs sum to at most `7/2`, hence
at most 3. These exact integer steps yield `a<=104` and remove this case.

The complete 106-entry **axis** word in `axis_witness.json`, modulo 107,
lies in chamber 15 and has class sizes `[16,2,26,20,22,20]`. The independent
checker verifies every modular sum, including doubling, and all 7,536
literal interval-order comparisons against that unit seed. This proves
that 107 is the exact axis maximum. This axis is a partial prescription
for a larger full colouring, not a full 534- or 537-point witness.

## Consequence for full colourings

If `C` is a reflected Schur colouring of `[1,5a-1]`, its restriction
`E(q)=C(5q)` is an ordinary reflected Schur colouring of `[1,a-1]`.
It is also modularly Schur: a modular violation with `x+y>a` reflects to
the ordinary violation `(a-x)+(a-y)=a-z`; a sum equal to `a` has output 0,
which is excluded. Thus every full colouring with an axis in the stated
union has `a<=107`, so `5a-1<=534`. This argument uses no information about
off-axis colours.

The construction lane's first possible endpoint above 536 has `a=109`,
namely 544. Therefore freeing only the columns, while keeping one of these
axis chambers, cannot reach the new-bound target. A continuing construction
must change the axis run pattern, at least one selected axis separation,
or the seed. The theorem does not close those alternatives.

## Reproduce and trust

Python 3.11 or later and the standard library suffice for all proof checks:

```sh
sha256sum -c SHA256SUMS
python3 -B audit.py certificate.json --witness axis_witness.json > /tmp/schur-axis-audit.json
diff -u expected.json /tmp/schur-axis-audit.json
```

The output reports complete coverage of 35 unit representatives,
`certificate_terms=614`, `integer_rounding_steps=11`,
`integer_axis_upper_bound=107`, `full_symmetric_endpoint_upper_bound=534`,
and `axis_maximum_exact=true`. Run with assertions enabled, as above.

The independent checker imports neither the generator nor an optimizer.
It reconstructs sparse affine intervals, verifies every rational identity
and integer rounding, multiplies seed positions directly, and separately
checks numeric chamber membership and full modular sums. Floating-point
linear and integer solver statuses are not proof premises.

Optional certificate and witness discovery used Python 3.12.14,
NumPy 2.5.3 and SciPy 1.18.1, pinned in `requirements.txt`:

```sh
python3 -B regenerate.py --source seed.json --output /tmp/axis-regenerated.json
python3 -B audit.py /tmp/axis-regenerated.json --witness axis_witness.json
python3 -B construct.py --source seed.json --multiplier 15 --output /tmp/axis-107.json
python3 -B audit.py certificate.json --witness /tmp/axis-107.json
```

Dual certificates and maximizing words need not be unique. Exact checking
is the acceptance criterion. Only source, complete small words, selected
rational terms, and compact expected output are published. No historical
priority is asserted for interval models or integer rounding. This is a
scoped computer-assisted construction barrier, not a numerical result
about unrestricted `S(6)`.
