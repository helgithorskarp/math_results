# Defect-18 rigidity for a hypothetical 29-word code in `Q_7`

## Result

Let `C` be a minimum locating-dominating code of cardinality 29 in the
binary 7-cube.  Use the Honkala--Laihonen--Ranto partition into excess-zero
points, codeword couples, and father/son families.  Write

\[
p=\#\{x:|I(x)|=1\},\qquad
D=\sum_F (|I(f_F)|-2),
\]

and let `a` and `q` be the number of isolated codewords and codeword
couples.  Then

\[
\boxed{D\geq18.}
\]

Consequently

\[
p\geq42,\qquad a\geq13.
\]

The same conclusion needed by the size-29 search holds if the true minimum
is 28: adding any non-codeword to the previously analyzed hypothetical
size-28 code gives a 29-word code with at least 42 singleton signatures and
15 isolated codewords.  Thus every possible code of cardinality at most 29
leads, losslessly, to an exact-cardinality-29 search instance satisfying

\[
p\geq42,\quad a\geq13,
\quad e(Q_7[C])\leq32,
\quad A_2(C)\geq26.
\]

This strengthens the earlier bounds `41`, `12`, `33`, and `24`.  It does not
prove that a 29-word code is impossible.

## The defect-17 frontier

For a family of defect `d=i-2`, its maximum cardinality is

\[
h(d)=1+\binom{d+2}{2},
\qquad (h(1),\ldots,h(5))=(4,7,11,16,22).
\]

The standard partition identities for a minimum 29-code are

\[
p=24+D,
\qquad a\geq D-5,
\qquad 2q\leq34-D,
\qquad M=104-D-2q,
\]

where `M` is the number of vertices in families.  Exhausting the integer
partitions of `D=17` subject to

\[
\sum_F h(d_F)\geq M
\]

leaves exactly the following ten rows.  The column `delta` is the total
number of absent sons relative to full capacity.

| `q` | `M` | defects | `delta` |
|---:|---:|:---|---:|
| 7 | 73 | `(5,5,5,2)` | 0 |
| 8 | 71 | `(5,5,5,2)` | 2 |
| 7 | 73 | `(5,5,5,1,1)` | 1 |
| 8 | 71 | `(5,5,5,1,1)` | 3 |
| 8 | 71 | `(5,5,4,3)` | 0 |
| 8 | 71 | `(5,5,4,2,1)` | 0 |
| 8 | 71 | `(5,5,4,1,1,1)` | 1 |
| 8 | 71 | `(5,5,3,1,1,1,1)` | 0 |
| 8 | 71 | `(5,5,2,1,1,1,1,1)` | 0 |
| 8 | 71 | `(5,5,1,1,1,1,1,1,1)` | 1 |

## Near-full `F_7` rigidity

Call a family with `|I(f)|=7` an `F_7` family.

First, every `F_7` father in the table is a non-codeword.  Indeed, if an
`F_7` father `x` were a codeword, `I(x)` would consist of `x` and six
codeword neighbors.  For a neighbor `c`, the only possible son assigned to
the pair `{x,c}` is `c` itself, because

\[
B_1(x)\cap B_1(c)=\{x,c\}.
\]

If at most `delta` sons are absent, that family therefore contains at least
`7-delta` codewords.  But the total number of codewords in all families is at
most

\[
29-(D-5)-2q=17-2q,
\]

which is at most 3 in the two `q=7` rows and at most 1 in every `q=8`
row.  The displayed values of `delta` make a codeword `F_7` father
impossible.

Now let `x` be a non-codeword `F_7` father.  Its seven neighbors are the
codewords in `I(x)`.  Each of its 21 possible sons corresponds to one pair
of these neighbors and is the other common radius-one neighbor of that
pair.  If all six pair-sons incident with a codeword $c\in I(x)$ are
present, every neighbor of `c` is a non-codeword, so `c` is isolated.
Consequently an `F_7` family missing `t` sons guarantees at least

\[
7-2t
\]

isolated codewords.

These guaranteed isolated sets can be added over distinct `F_7` fathers.
The only way two radius-one balls in a cube share codewords is for their
centers to be at distance two.  In that case the two shared codewords form
the pair whose other common neighbors are the two fathers; neither father
is a son of the other.  Hence that pair is missing in both families, and
the shared codewords are excluded from both guaranteed sets.  Thus `k`
non-codeword `F_7` families with total capacity deficit at most `delta`
force at least

\[
7k-2\,\mathit{delta}
\]

distinct isolated codewords.

This lower bound contradicts the maximum `29-2q` isolated codewords in
eight of the ten rows.  Only

```text
q=8, defects=(5,5,4,1,1,1), delta=1
q=8, defects=(5,5,1,1,1,1,1,1,1), delta=1
```

remain.  In either row, both `F_7` families would be full unless their
unique missing son belongs to one of them, and two full families already
force 14 isolated codewords although `q=8` permits at most 13.  Therefore
one `F_7` family is full and the other is missing exactly the son assigned
to a pair `{c_1,c_2}`.

Let `y` be the other common neighbor of `c_1,c_2`.  If `y` were a
non-codeword, then `c_1` and `c_2` would also be isolated, again giving 14
isolated codewords.  Hence `y` is a codeword.  Both `c_1` and `c_2` have
exactly the codeword neighbor `y`, so

\[
I(c_i)=\{c_i,y\}\quad(i=1,2),
\qquad |I(y)|\geq3.
\]

Thus `y` is a father and `c_1,c_2` are its codeword sons.  These are three
codewords in a family, contradicting the global allowance of at most one
family codeword.  The last two rows are impossible, proving `D>=18`.

## Search consequences

At most 16 codewords are nonisolated.  The standard binary-layer
edge-isoperimetric recurrence gives

\[
E_7(16)=32,
\]

so the induced code has at most 32 edges.  The orphan double count from the
predecessor now gives at least `p-29>=13` orphan-isolated codewords and

\[
A_2(C)\geq2(p-29)\geq26.
\]

`search_q7_ld29_d18.py` regenerates the predecessor's exact orphan-local
SAT search with these sharper bounds.  By default it builds the compact
singleton/isolation/edge encoding.  `--pair-bounds` adds the static
distance-two bound, and `--dynamic-pair-bound` also adds the sharper
relation `A_2(C)>=2p-58`.  CNFs and solver traces are restricted to
`/scratch`.

## Reproduction

The structural verifier uses only the Python standard library:

```bash
python3 verify_defect18.py
```

Build a canonical branch, for example:

```bash
python3 search_q7_ld29_d18.py \
  --local-graph-index 0 --build-only \
  --write-cnf /scratch/q7-ld29-d18-branch000.cnf
```

The SAT generator depends on the exact encoding and local-graph enumeration
in `../q7_ld29_family_reduction` and on `python-sat[pblib]==1.9.dev15`.

## Status and sources

The `D>=18` statement is a hand-checkable theorem.  Integer enumeration is
used only to list the ten defect-17 rows and is reconstructed by the
standard-library verifier.  SAT runs are downstream applications and do not
prove the structural theorem.

The family partition is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  The published
small-dimension context is V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming
Spaces*, Designs, Codes and Cryptography 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>.

The argument was prompted by the Discovery Net review's explicit request to
classify the defect-17 frontier.  Targeted searches through 2026-09-01 found
no prior size-29 defect-18 statement.  It is apparently new relative to the
searched sources and graph, not a historical-priority claim.
