# Independent-column interval deformations of a Schur colouring

This note certifies an endpoint bound of **354** for the
union of 132 explicit families of reflected six-colour constructions. Both
short columns and the axis have independent positive integer run lengths.
The families retain specified interval-separation orders from all unit
images of a supplied 334-point colouring. The bound is attained by the
complete 354-word in `witness.json`.

This does not change the classical bound `S(6)>=536` of
[Fredricksen and Sweet](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
still used in the [2026 shifted-template paper](https://arxiv.org/abs/2607.15034).
Here `S(6)` is the greatest colourable endpoint, and repeated summands count.
No 537-word or exclusion of the entire independent-column model is claimed.

## Construction and exact family

Let `a=2h+1` and `n=5a`. The positive half-axis has a colour `E(u)` for
`1<=u<=h`, also assigned to `a-u`. Two independent state words `Q1,Q2`
on `q=0,...,a-1` use `{R,2,3,4,5}`. At `5q+1`, state `R` means colour 0;
at `5q+2`, it means colour 1. A common state means its own colour. Reflect
these values to their negatives modulo `n`, and colour `5q` from the axis.
There is no column equality or additional restriction on `Qj(0)`.

`certificate.json` supplies the complete seed at `a=67`. Its class sizes
are `[44,42,110,52,42,44]`; its residual column counts are 21 and 20. Thus no
bijection of long coordinates identifies the two state columns, even with
a permutation of common colours. In particular the seed is outside every
invertible affine relation `Q2(q)=Q1(lambda*q+delta)`. This seed property
also holds for its unit images, whose residual counts may be exchanged;
it is not asserted for every subsequent length deformation.

Multiply the seed positions by each unit `u` modulo 335, exchanging colours 0
and 1 when `u mod5` is 2 or 3. This preserves the residue domains. Reflection
makes `u` and `335-u` identical, leaving 132 representatives `1<=u<=167`.
For each image, split the positive half-axis, first state column, and second
state column into maximal constant runs. First and last column runs remain
separate even when their states agree. Keep their colours and linear order,
and replace every run length by a separate positive integer variable.
Axis lengths sum to `h`; each column's lengths sum to `a=2h+1`.

An essential additional condition retains the separating side of each
interval comparison below, as selected by that unit seed. This defines its
*interval-separation chamber*. The theorem concerns the union of these 132
chambers for arbitrarily large candidate lengths. It does **not** cover all
words with the same run order. Different separating sides, split/merged
runs, changed run orders, and other seeds remain outside this family.

## Interval inequalities

Write `Ei` for the symmetric axis support of each colour `i=0,...,5`.
For common colours `i=2,...,5`, write `Ai,Bi` for the coordinate supports
in the columns, and write `R1,R2` for the residual supports. All arithmetic
here is modulo `a`; the axis omits 0.
The exact Schur conditions are

```
(Ei+Ei) misses Ei, for i=0,...,5;
(Ai+Ai) misses Bi, and -1 is absent from Ai+Bi+Bi, for i=2,...,5;
(R1-R1) misses E0, and (R2-R2) misses E1;
((Ai-Ai) union (Bi-Bi)) misses Ei, for i=2,...,5.
```

Repetitions are included. The first two off-axis equations follow from
`(5x+1)+(5y+1)=5(x+y)+2` and the common-colour condition `x+y+z=-1 mod a`
with one first-column and two second-column points. Axis/off-axis equations
give the difference conditions. Splitting all equations by residues modulo 5
gives exactly this list, as in the earlier
[independent-column source](../schur6_affine_column_normal_forms/README.md).

For integer intervals, sums and differences are intervals:
`[l,r]+[L,R]=[l+L,r+R]`, `[l,r]-[L,R]=[l-R,r-L]`.
Disjointness is exactly `r<=L-1` or `R<=l-1`. The seed satisfies one side;
its chamber keeps that linear inequality for every comparison below.

| Type | Intervals compared | Wraps |
| --- | --- | --- |
| axis sum | two intervals of `Ei` summed versus another plus `t*a` | `t=0,1` |
| two first columns | two intervals of `Ai` summed versus one of `Bi` plus `t*a` | `t=0,1` |
| one first/two second | their sum interval versus the point `t*a-1` | `t=1,2` |
| same-column difference | a difference interval versus the matching axis interval plus `t*a` | `t=-1,0` |

All pairs/triples of constituent intervals are included, with repetition.
These wraps exhaust their ranges. Axis intervals are listed as positive
intervals followed by their reflections in corresponding order; column
intervals have increasing coordinates. The half-axis starts at 1 and columns
at 0; endpoints are inclusive. Add positive-length constraints and the two
column-sum equalities. These conditions define the chamber exactly.

## Rational and integer certificates

Each certificate term names an interval comparison and a positive rational
weight. The checker reconstructs its affine inequality from the run
endpoints, dividing coefficients and constant by their positive integer gcd
when possible. Equality weights may have either sign. Their exact sum is
`a-B<=0`. Some proofs first bound a run by `length_j<=p/q`, then use the
valid integer inequality `length_j<=floor(p/q)`. Every such rounding step
is checked before later terms may use it.

The 132 certificates use 5,511 nonzero weighted terms and 15 exact integer
rounding steps. There are 86 to 160 run-length variables, with two total-length
equalities. The resulting bounds are:

| Unit representative | Axis bound `B` | Rounding steps | Largest allowed `a` |
| --- | ---: | ---: | ---: |
| the other 128 representatives | 67 | 0 | 67 |
| 3 | 70 | 1 | 67 |
| 64 | 68 | 8 | 67 |
| 131 | 69 | 2 | 67 |
| 137 | 71 | 4 | 71 |

Finally, `a` is odd, and `3|a` is impossible for a reflected modular Schur
word: with `n=5a`, reflection gives equal colours at `n/3` and `2n/3`, but
`n/3+n/3=2n/3`. Thus an axis bound below 71 implies `a<=67`.
The inclusion of equal summands is essential here. The supplied 354-word
attains `a=71` in chamber 137, proving the exact family maximum. Its class
sizes are `[46,50,110,56,48,44]` and residual column counts are 22 and 24,
so it also lies outside all invertible affine column identifications.
The independent verifier checks all 113,048 numeric interval comparisons
for its chamber membership, as well as every modular equation.

`audit.py` imports neither the model generator nor an optimizer. It checks
all unit representatives and full word equations, reconstructs every used
semantic inequality, and verifies each rational identity and integer step.
Floating-point optimizer output and integer-solver status supply no part of
the proof. The source of trust is the interval argument and these finite
exact checks. No claim of historical priority is made for interval encodings,
dual certificates, or integer rounding.

## Reproduce

Python 3.11 or later and the standard library suffice:

```sh
sha256sum -c SHA256SUMS
python3 -B audit.py certificate.json --witness witness.json > /tmp/schur-interval-audit.json
diff -u expected.json /tmp/schur-interval-audit.json
```

Optional regeneration was tested with Python 3.12.14, NumPy 2.5.3 and
SciPy 1.18.1, pinned in `requirements.txt`. Examples:

```sh
python3 -B model.py --source certificate.json --multiplier 1 --output /tmp/chamber1.json
python3 -B round.py --source certificate.json --multiplier 3 --output /tmp/chamber3-rounded.json
python3 -B regenerate.py --source certificate.json --output /tmp/regenerated-chambers.json
python3 -B audit.py /tmp/regenerated-chambers.json --witness witness.json
python3 -B construct.py --source certificate.json --multiplier 137 --output /tmp/constructed-word.json
python3 -B word.py /tmp/constructed-word.json
```

The integer optimizer may return a different maximizing word. Rational
duals need not be unique; the standalone checker is the acceptance
criterion. Only source, the complete small seed, selected rational terms,
and compact expected results are included. Constraint matrices, logs and
optimizer binaries are regenerated locally.

The seed came from freeing the two columns of the earlier
[334-point shared-column witness](../schur6_paired_prefix_obstruction/README.md)
and requiring unequal residual sizes. The earlier paired-prefix cap does
not apply to these independent run lengths. This result closes the stated
deformation family while leaving other independent-column constructions open.
