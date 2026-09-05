# A sharp signature bound and two remaining minority cores

In the eleven-cycle three-versus-eight branch of the Ramsey `(5,5;43)`
problem, the previous three minority cores now reduce to **two**. Their
red words on minority pairs 01,02,12 are

```text
class 11: 100,110,110; weights 1,2,2; distinguished phase sum zero;
class 13: 110,110,101; weights 2,2,2; distinguished phase sum nonzero.
```

The extension of class 8, with words 100,100,100, is excluded by the
full replayed refutation described below. Classes 11 and 13 returned
UNKNOWN at 60 seconds and remain open. The four-versus-seven branch is
also open. The global minimum remains eleven moving cycles; this is
not a 43-vertex construction or a Ramsey lower-bound improvement.

The new structural input is a sharp lemma that needs neither an
automorphism nor a degree estimate.

## Uniform-neighbor lemma

Let G be a red/blue complete graph with no monochromatic K5. Let
C0,C1,C2 be three disjoint red triangles. Let F be any set outside their
union such that each f in F is either red to every vertex of Ci or
blue to every vertex of Ci, for each i. Put

```text
S(f) = {i : f is red to Ci} subset {0,1,2}.
```

**At most nine vertices of F have nonempty signature.** If nine do,
each singleton signature occurs twice, each two-element signature
occurs once, and signature {0,1,2} does not occur. Empty signatures are
not counted in this assertion.

For each i, let a_i count the vertices of F red to Ci. Any two such
vertices must be blue to each other: a red edge between them would
complete a red K5 with Ci. Thus

```text
a_i <= 4,                 I := a_0+a_1+a_2 <= 12.       (1)
```

Let x_i count signature {i}. Three such vertices would form a blue
triangle, by the same argument. They are all blue to the other two
red triangles. There is a blue edge between those triangles, since
otherwise they form a red K6. That edge and the three fixed-signature
vertices would make a blue K5. Therefore

```text
x_i <= 2,                 X := x_0+x_1+x_2 <= 6.        (2)
```

Let Y count signatures of size two, Z count signatures of size three,
and N=X+Y+Z. Counting incidences gives

```text
I = X+2Y+3Z,              2N = I+X-Z <= 18-Z <= 18.
```

Hence N<=9. If N=9, then Z=0, I=12 and X=6. Each x_i=2 and each
a_i=4. Writing y_ij for the pair-signature counts, the three equations
y_01+y_02=y_01+y_12=y_02+y_12=2 give y_01=y_02=y_12=1.
This proves the lemma and the equality case by counting alone.

There is also a useful four-vertex consequence. For distinct i,j, let
k be the third index. Vertices with signatures {i} or {i,j} are
pairwise blue because they are red to Ci, and all are blue to Ck.
Four such vertices and any vertex of Ck would form a blue K5. Thus

```text
x_i+y_ij <= 3.                                          (3)
```

This method is related to the earlier
[four-triangle signature bound](../ramsey_r55_order3_fixed_signature_bound/PROOF.md),
which used a particular twelve-vertex core. The present three-triangle
lemma allows arbitrary cross edges and signatures of size three.
The proof above is self-contained; no historical-priority claim is made.

## Sharp witnesses and the finite arithmetic audit

In each of the three inherited nine-vertex cores, append ten vertices
with numeric signature masks

```text
0,1,1,2,2,3,4,4,5,6,
```

where bit i means red to Ci. Between appended vertices place a red
edge exactly when their signatures are disjoint. This gives the three
literal graphs `core8.edges`, `core11.edges`, `core13.edges`, with 19
vertices and respectively 81,87,90 red edges. All three have no
monochromatic K5. In each, exactly nine of the ten appended vertices
have nonempty signature, and every a_i=4.

The literal inspector examines all 11628 five-sets in each graph,
every fixed attachment and every fixed-to-fixed edge. The supplementary
action check verifies all 171 pairs per graph under simultaneous
rotation of the three triangles, with all appended vertices fixed;
it also checks the internal triangles and all nine core orbit bits.
The displayed construction and these small edge lists are sufficient
to check sharpness without a solver or omitted data.

These are local 19-vertex witnesses, without the other eight blue
moving triangles or the full 43-vertex degree constraints. In particular
the witness for class 8 does not conflict with its full-extension
exclusion. The sharp witnesses show that these local hypotheses cannot
force two empty signatures among ten appended vertices.

As a separate arithmetic audit, enumerate all 19448 weak compositions
of ten into the eight signature multiplicities. Exactly 928 satisfy
(1) and (2), and 778 additionally satisfy (3). The histogram for the
number N of nonempty signatures under (1) and (2) is

```text
N:       0  1  2  3   4   5   6   7  8  9  10
profiles:1  7 28 81 189 257 226 110 28  1   0.
```

The unique N=9 vector, in numeric-mask order 0 through 7, is
(1,2,2,1,2,1,1,0). Composition generation and direct enumeration of
sorted ten-signature lists agree on the entire histogram and extremizer.
These counts classify only the specified necessary inequalities, not
Ramsey graph realizations. The hand proof does not depend on this census.

## Application and complete formula bridge

In the eleven-cycle three-versus-eight branch, vertices fixed by the
automorphism are uniform to each minority triangle. The lemma gives
at least one fixed vertex blue to all nine minority vertices. The
parent formula sorts the ten fixed vertices lexicographically by their
eleven red incidence bits, with the three minority bits first. An
empty minority signature precedes every nonempty one. Therefore the
first fixed vertex, labeled 33, has minority bits 000. This supplies
the three units -211,-212,-213 in the inherited primary convention.
It places no restriction on its edges to the other fixed vertices.

The three-class cover and core relabelings are imported from
[the preceding minority-core reduction](../ramsey_r55_order3_eleven_minority_core/PROOF.md).
That result's complete cover remains an inherited trust boundary.
The explicit exclusion of core 8 requires only that specified core;
using it to reduce the whole branch to cores 11 and 13 additionally
uses the preceding cover and its eleven exclusions.

All production formulas retain the complete parent r=3 formula:
34268 variables, 615572 clauses, all projected five-set constraints,
both moving degree bounds, fixed degrees, common-neighborhood and
deficit counters, and the justified normalization. The direct external
theorem for that parent is R(4,5)=25. Its formula and counter bridge now
have an accepted independent review. The new abstract signature lemma
uses none of these degree or formula assumptions.

The nine units fixing the selected core are retained. After them,
append exactly 1623 primary consequence clauses:

* three units fixing vertex 33's minority signature to 000;
* 360 clauses, one for each three fixed vertices and minority index i,
  forbidding all three signatures from being exactly {i}, by (2);
* 1260 clauses, one for each four fixed vertices and ordered distinct
  pair (i,k), forbidding all four from being red to Ci and blue to Ck,
  by (3).

If l_vi is the red attachment bit of fixed vertex v to Ci, the singleton
clause is the disjunction, over the selected vertices, of -l_vi and
the two positive bits l_vj for j!=i. It has nine literals. The
four-vertex clause is the disjunction of -l_vi and l_vk over its
vertices, with eight literals. There are no new auxiliary variables.
Each final formula has 617204 clauses and 34268 variables.

Python generates the parent afresh; its separate C++ auditor reconstructs
every clause from literal unordered-pair orbits. The new auditor
independently recovers all 320 primary meanings from the actual action,
compares the entire parent prefix, checks the nine core units and all
1623 consequence clauses, and verifies EOF. All 1536 ordered singleton
cut truth assignments and 24576 ordered four-vertex cut assignments are
checked separately. No additional automorphism, graph catalog, fixed
degree profile or fixed graph is imposed. The three new units use only
the already proved fixed-signature ordering; no new normalization is
assumed.

## Bounded decision and scope

The complete three-case test uses two workers and 60-second solver
limits. Core 8 is UNSAT with a full DRAT proof; cores 11 and 13 are
explicitly UNKNOWN. The core-8 proof uses RAT, and is replayed against
the exact full formula. A fresh verification reconstructs all three
formulas and replays the proof again. Four malformed formula mutations
and three malformed fixture mutations must be rejected; normal and
optimized-Python control reports agree.

Only source, small edge lists and compact reports are public. The full
formula, proof and logs are regenerated outside Git. Hashes and reports
alone are not refutations, and UNKNOWN traces are not certificates or
resumable solver states. Exact source/runtime/compiler/hardware, the
ordinary unformalized reduction, imported parent evidence and the
external DRAT checker remain trust boundaries. Internal checking is
not independent peer review. This milestone ends after the sharp
lemma and the complete three-case propagation test; no equality-branch
split or four-versus-seven expansion is begun.
