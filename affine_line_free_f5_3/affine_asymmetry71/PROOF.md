# Any 71-point line-free set in F_5^3 is affine-asymmetric

A subset of \(V=\mathbb F_5^3\) is **line-free** if it contains no complete
five-point affine line. An affine plane reflection means a nonidentity
affine involution fixing a plane pointwise.

**Theorem 1 (sharp reflection bound).** A line-free subset of \(V\)
invariant under an affine plane reflection has at most **70 points**.
This bound is attained.

**Theorem 2 (affine asymmetry).** Every line-free subset of \(V\) of
cardinality 71 has trivial affine automorphism group.

The first theorem is a complete exact computation with a short geometric
reduction. The second combines it with the earlier
[reflection-rigidity theorem](../reflection_rigidity/PROOF.md).
Neither proves or disproves existence at 71. The campaign's separate
[upper bound 71](../upper_bound71/README.md) leaves
\(70\le r_5(\mathbb F_5^3)\le71\), but is not a premise of these two
theorems. Independent peer review of this contribution is pending.

## 1. Normal form and the allowed central section

An affine involution in characteristic five has a fixed point, obtained
by averaging any point with its image. After translating this point to
zero, it is a linear map with minimal polynomial dividing
\((X-1)(X+1)\), hence diagonalizable. A two-dimensional fixed space
gives the normal form

\[
g(x,y,z)=(-x,y,z).
\]

Write \(p=(y,z)\). A \(g\)-invariant subset has planar sections, in
order \(x=0,1,2,3,4\),

\[
A,\ B,\ C,\ C,\ B.
\]

Put \(a=|A|,\ b=|B|,\ c=|C|\). Each of \(A,B,C\) must be planar
line-free, and the size is \(a+2b+2c\).

Every affine line not contained in an \(x\)-section has a unique
parametrization

\[
L(u,v)=\{(x,u+xv):x\in\mathbb F_5\},
\qquad u,v\in\mathbb F_5^2.
\]

There are 625 such lines, including the zero-slope case \(v=0\).
Define

\[
D(B,C)=\{u\in\mathbb F_5^2:
 \text{no }v\in\mathbb F_5^2
 \text{ has }u\pm v\in B,\ u\pm2v\in C\}.
\tag{1}
\]

The five sections form a line-free set **if and only if** \(A,B,C\)
are planar line-free and \(A\subseteq D(B,C)\). This covers the 150
lines within sections and the 625 transverse lines.
For the upper bound it is enough to use the relaxation

\[
|S|\le 2b+2c+|D(B,C)|,
\tag{2}
\]

without imposing line-freeness on \(D(B,C)\) itself.

## 2. Exhaustive size and symmetry reduction

The planar line-free cap is 16. For a self-contained computational
check, [catalogue.cpp](catalogue.cpp) examines all
\(\binom{25}{17}=1,081,575\) sets of size 17 and finds none line-free.
Every larger set would contain such a set. The independently generated
normal-equation lines in [direct_lines.cpp](direct_lines.cpp) confirm
that no eight-point complement meets all 30 planar lines.

Multiplying \(x\) by 2 exchanges \(B\) and \(C\), so assume \(b\ge c\).
If \(b+c\le27\), the planar cap gives

\[
|S|\le16+2\cdot27=70.
\]

For the remaining cases, \(b+c\ge28\) and \(b,c\le16\) force
\(14\le b\le16\). The following nine ordered size pairs are exhaustive:

\[
(14,14),\ (15,13),\ (15,14),\ (15,15),\
(16,12),\ (16,13),\ (16,14),\ (16,15),\ (16,16).
\tag{3}
\]

Every map \((x,p)\mapsto(x,Mp+t)\), with \(M\in GL(2,5)\), commutes
with the reflection. It acts simultaneously on all three planar sets
and carries \(D(B,C)\) to \(D(MB+t,MC+t)\). Thus \(B\) can be
normalized under the full group \(AGL(2,5)\), while \(C\) remains
arbitrary. There is no quotient of \(C\) and no assumption about its
stabilizer.

The full affine group has \(25\cdot480=12,000\) elements. The exact
planar orbit census is:

| Size of B | All subsets | Line-free subsets | Affine orbits |
|---:|---:|---:|---:|
| 14 | 4,457,400 | 961,500 | 92 |
| 15 | 3,268,760 | 252,600 | 26 |
| 16 | 2,042,975 | 28,375 | 6 |
| 17 | 1,081,575 | 0 | 0 |

[REPRESENTATIVES.txt](REPRESENTATIVES.txt) has one row
`size mask orbit_size` for each of the 124 orbits. The mask of a
planar set is \(\sum_{(y,z)\in B}2^{5y+z}\). Each representative is the
least mask in its orbit.

The catalogue generator tests every subset in each stated size.
For each first unseen line-free mask, it applies all 12,000 affine
maps, deduplicates the images, and checks their size, line-freeness,
disjointness from earlier orbits, and minimum. The orbit sizes must
sum to the full labelled census.

The Python verifier constructs the affine maps separately and acts on
the **complement** of each representative. It checks the actual
disjoint orbit sets and each multiplicity again. Their total agrees
with the independently enumerated labelled counts in the C-searches.
Consequently normalization loses no candidate.

## 3. Complete allowed-section census

For every representative \(B\), every eligible labelled \(C\) is
enumerated. The line-free \(C\) counts are:

| c | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|
| Line-free C | 3,089,000 | 2,103,000 | 961,500 | 252,600 | 28,375 |

Across (3), the computation evaluates exactly **213,309,450**
representative pairs \((B,C)\). All of them receive an entrywise
comparison between two definitions of \(D\).

The complete maxima are:

| b | c | Maximum of \(|D(B,C)|\) | \(2b+2c+\max |D|\) |
|---:|---:|---:|---:|
| 14 | 14 | 12 | 68 |
| 15 | 13 | 13 | 69 |
| 15 | 14 | 10 | 68 |
| 15 | 15 | 8 | 68 |
| 16 | 12 | 13 | 69 |
| 16 | 13 | 12 | 70 |
| 16 | 14 | 9 | 69 |
| 16 | 15 | 6 | 68 |
| 16 | 16 | 4 | 68 |

Every row is at most 70. Together with the \(b+c\le27\) case, (2)
proves the upper bound in Theorem 1.

### Paired slopes and entrywise verification

[paired_sections.cpp](paired_sections.cpp) enumerates fixed-cardinality
subsets \(C\) in increasing mask order using the next-combination
formula, and rejects any containing a planar line.

Choose the twelve nonzero vectors modulo the equivalence \(v\sim-v\).
At each center \(u\), store the 12-bit signature of those pairs
\(\{u-v,u+v\}\) contained in \(B\). For \(C\), store the signature of
\(\{u-2v,u+2v\}\). The center is forbidden precisely when the signatures
intersect or \(u\in B\cap C\), the latter handling \(v=0\).

For **every** evaluated pair, the program also constructs \(D\) directly
from the 25 slopes in (1) and checks equality of the actual 25-bit
allowed-set masks. This comparison does not depend on aggregate
histograms or a hash.

### Complement enumeration and actual line requirements

[direct_lines.cpp](direct_lines.cpp) shares no geometric input file
with the first program. It constructs the 30 planar lines by their
six normal directions and five constants, then walks all \(2^{25}\)
complement masks, retaining those of the desired size meeting every
line.

For every \(u,v\), it explicitly computes the points in the four
noncentral sections of \(L(u,v)\). Whenever the two \(B\)-points are
selected, at least one of the required \(C\)-points must be a hole.
It deliberately keeps both signs of each nonzero slope and the zero
slope. Testing these requirements gives \(D\) directly.

The two enumeration orders produce identical complete histograms,
maxima, first extremal examples, and diagnostics for all 200
representative/size records. The verifier compares these full records
before forming the nine-row summary. It also checks every histogram
total, every fixed-cardinality subset count, and every orbit partition.

For compact publication, [EXPECTED.json](EXPECTED.json) contains the
nine weighted histograms and five SHA-256 hashes of the complete
record arrays. The additional order-independent 64-bit assignment
digest is only a regression diagnostic, not a proof certificate.
No hash is substituted for the entrywise equality checks or for a
complete enumeration.

## 4. Sharpness and a third construction class

The case \(b=16,c=13\) supplies these three masks:

\[
A=25,610,005,\qquad B=1,294,078,\qquad C=19,755,466.
\]

They have sizes \(12,16,13\), respectively, and \(A=D(B,C)\).
All three are planar line-free. Hence the five sections \(A,B,C,C,B\)
give a reflected line-free set of size

\[
12+2\cdot16+2\cdot13=70.
\]

[witness70.json](witness70.json) records all 70 point indices, with
\((x,y,z)\) numbered \(25x+5y+z\). The Python verifier constructs the
full three-dimensional line geometry independently and checks all
775 lines, the five-section decoding, the cardinality, and reflection
invariance.

This example is affine-inequivalent to the paper's Figure 4 example
and to the earlier [order-three example](../odd_symmetry/witness70.json).
For each of the 31 parallel classes of affine planes, sort the five
intersection sizes. The number of classes with profile
\((6,16,16,16,16)\) is respectively:

| Construction | Number of these plane classes |
|---|---:|
| Current reflected example | 4 |
| Paper, Figure 4 | 5 |
| Earlier order-three example | 7 |

An affine bijection permutes parallel classes of planes and preserves
their profiles, so the different counts certify inequivalence.
This is a comparison with those two explicit constructions, not a
classification of all 70-point sets or a claim that no equivalent
example has ever appeared elsewhere.

The verifier also checks a geometric extremal example for each of the
nine rows of the table; all nine selected \(D\)'s are themselves
line-free and give sets of the stated upper total. A Cartesian
64-point set is a positive control, and the corresponding 80-point
set is rejected.

## 5. Deduction of complete affine asymmetry at 71

The previous [reflection-rigidity result](../reflection_rigidity/PROOF.md)
proves that a 71-point line-free set has affine automorphism group
either trivial or generated by a plane reflection. Theorem 1 excludes
the latter possibility, proving Theorem 2.

For clarity, the imported result excludes odd prime orders using the
earlier order-three enumeration and elementary order-five and
order-31 arguments. It then excludes involutions fixing a line,
central inversion, and order-four maps whose squares fix a plane.
Those prior computations are dependencies of Theorem 2, and are
**not** repeated by the current replay. They are not dependencies of
the sharp plane-reflection bound.

Thus every hypothetical 71-point line-free set has an affine orbit of
size

\[
|AGL(3,5)|=125(125-1)(125-5)(125-25)=186,000,000.
\]

No search imposing a nonidentity affine automorphism can produce a
71-point witness. An unrestricted construction may still exist.

## 6. Arithmetic, coverage, and trust boundary

All geometry is computed over integers modulo five. Planar sets occupy
25 bits of an unsigned 32-bit integer; signatures occupy 12 bits of
an unsigned 16-bit integer. Enumeration and histogram counts use
unsigned 64-bit integers. Even every labelled pair of planar subsets
would number only \(2^{50}\). The diagnostic mixer intentionally uses
unsigned arithmetic modulo \(2^{64}\).

All searches are finite, single-threaded, and have no time or conflict
cutoff. They invoke no SAT/SMT solver and use no floating-point
arithmetic. A missing partition, disagreement, failed control, or
unexpected result terminates the verifier with an error.

The complete release run covers every case in (3), all affine orbits,
both planar-cap checks, and every control. The address/undefined-behavior
sanitizer run covers the complete catalogue, both planar-cap checks,
all six \(b=c=16\) representatives, and the applicable controls.
Sanitizer coverage is not claimed for the other four \(c\)-partitions.

These algorithms and checks were authored by the same researcher.
They offer different representations and full entrywise validation,
but are not an independent peer review or a proof-assistant
formalization. Remaining trust includes the written reduction, source
inspection, compiler/runtime correctness, and, for Theorem 2 only,
the cited prior theorem.
