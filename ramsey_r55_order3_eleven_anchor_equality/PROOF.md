# Two empty fixed signatures at every blue-triangle-free anchor

Let G be a red/blue complete graph on 43 vertices with no monochromatic
K5. Suppose an automorphism has type `1^10 3^11`, with **four internally
red** moving triangles and **seven internally blue** moving triangles.
Let A be any three of the red moving triangles whose nine-vertex union
contains no blue triangle. Let F be the ten fixed vertices and put

```text
z_A = |{f in F : f is blue to all nine vertices of A}|.
```

**Computer-assisted theorem: z_A >= 2.** The choice of A is arbitrary,
so the conclusion holds simultaneously for every such triple in a full
graph. It does not require a selected twelve-vertex core, fixed graph,
degree profile, or further automorphism.

The proof uses two complete 43-vertex formulas and full DRAT refutations.
It leaves the fourth red moving triangle free. It does not reuse an
eight-blue-triangle formula from the three-versus-eight branch.
No full core is excluded here: all 34 remaining four-versus-seven core
classes, both three-versus-eight cores, and the minimum moving count
eleven remain unchanged. No target graph or Ramsey lower-bound gain follows.

## Two possible anchors

Label the three selected red triangles C0,C1,C2, with vertices (i,s),
s in Z/3Z. Simultaneous rotation is the marked action. Write w_ij(d)=1
when (i,s)(j,s+d) is red. A word 111 is impossible between two red
triangles, since their union would be a red K6. Thus there are 7^3=343
possible local words. Let B_ij be the nonempty set of blue offsets.
There is a blue triangle precisely when

```text
(B_01 + B_12) intersects B_02.
```

If any B_ij has size three, a blue triangle exists. If two have size
at least two, their sum or difference is all of Z/3Z: any two subsets
of sizes at least two intersect after any translation. Again there is
a blue triangle. Hence the only possible sorted red weights are 1,2,2
and 2,2,2.

For weight one let p_ij be the unique red offset, and for weight two
let p_ij be the unique blue offset; reverse orientation negates p.
When the weights are 1,2,2 with the weight-one word on 01, absence of
a blue triangle says `p_02-p_12=p_01`. Thus
`h=p_01+p_12-p_02=0`. For weights 2,2,2 absence says `h != 0`.
Independent rotations change individual phases but preserve h. A
simultaneous inversion changes its sign. The resulting representatives,
using the indices of the existing three-triangle local catalog, are

```text
anchor11: (100,110,110), weights 1,2,2, h=0;
anchor13: (110,110,101), weights 2,2,2, h!=0.
```

This is a selected part of the existing fourteen-class local cover,
not a new classification of that whole catalog. Here the short sumset
proof and a direct census establish precisely the required subfamily.
`anchor.py` checks all 343 words by their 27 phase transversals and
supplies a relabeling for each blue-triangle-free word. There are 27
labeled words of type11 and 18 of type13. `audit.py` imports no producer:
it builds actual nine-vertex edge sets, checks every three-set, checks
every red five-set in the 45 survivors, and verifies the supplied maps
on literal vertex pairs. It also checks every blue-triangle-free
complement and every supplied map in all 34 remaining twelve-vertex
core representatives, entry by entry. There are 56 such complements
in those representatives, hence 101 literal maps altogether.

## The sharp signature equality

Each fixed vertex is uniform to each selected triangle. Write S(f) for
the indices of those to which it is red. The previously proved
[uniform-neighbor lemma](../ramsey_r55_order3_eleven_signature_bound/PROOF.md)
applies to any three disjoint red triangles, independently of the
colors or number of other moving triangles. Its short proof is repeated
to make the equality premise explicit.

For each i, the fixed vertices red to Ci form a blue clique, since a
red edge between two of them would complete a red K5 with Ci. Therefore
their number a_i is at most four and I=sum a_i<=12. There are at most
two singleton signatures {i}: three would form a blue triangle, and
would be blue to a blue edge between the other two red triangles.
That blue cross edge exists because otherwise those triangles form a
red K6. The resulting blue K5 is impossible.

Let X,Y,Z count signatures of sizes one,two,three and N=X+Y+Z. Then

```text
I=X+2Y+3Z <=12, X<=6, 2N=I+X-Z <=18.
```

So N<=9 and z_A>=1. If z_A=1, equality forces Z=0, two copies of each
singleton, one copy of each pair, and a_i=4 for every i. This equality
multiset, together with its one empty signature, is necessary; it is
not an assumed choice of fixed graph.

The equality condition is realizable locally for each anchor in the
nineteen-vertex edge-list witnesses of the cited signature lemma.
The exclusion below therefore concerns the full extension, not the
nine-vertex anchor or its fixed-vertex attachment alone.

## Full normalization with the fourth red triangle retained

Map the chosen A to cycles0,1,2 in one of the two displayed forms.
A map has `new(i,s)=old(pi(i),epsilon*s+t_i)`. Apply the SAME epsilon
to all eleven moving cycles, including the fourth red cycle and seven
blue cycles. This conjugates the marked action to itself or its inverse.
Inverting only the selected triangles would not justify the full formula.

Put the remaining red triangle at cycle3. Rotate it independently until
its word from cycle0 is one of 000,100,110,111. Rotate the seven blue
triangles similarly, and permute just those seven so their normalized
words from cycle0 are nondecreasing by weight. The anchor words on 01
and 02 are already normalized and ordered. Sort the ten fixed vertices
lexicographically by their complete eleven-bit red attachment rows.
These actions preserve the chosen anchor and the internal color split.

The accepted r=4 parent requires the word on 02 to precede the word on
03 as well. That condition need not be compatible with choosing A.
We therefore **remove exactly** its three clauses:

```text
-4 7 0
-5 8 0
-6 9 0
```

All other parent clauses remain. These three mixed-sign primary clauses
are solely the adjacent red-cycle ordering at anchor0. In particular,
no monochromatic Ramsey clause is lost: every such clause has one sign.
All counter, gate and degree clauses remain. The normalization just
described satisfies the weakened parent for every graph and every
chosen blue-triangle-free A. No twelve-vertex catalog normalization
or representative is imposed in these two formulas.

## Exact equality formulas

The accepted parent has 34,280 variables and 615,920 clauses, with SHA256
`c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f`.
After removing the three ordering clauses it has 615,917 clauses.
Append nine signed units for the selected anchor on variables
`1,2,3,4,5,6,31,32,33`.

Complete fixed-row lexicographic order also sorts their first three
coordinates. The equality multiset therefore fixes exactly these
prefixes for fixed labels33,...,42:

```text
000,001,001,010,010,011,100,100,101,110.
```

The attachment variable is `l(i,f)=211+11*(f-33)+i`. Append the thirty
signed units for these prefixes. No unit fixes the fourth red coordinate,
any of the seven blue coordinates, or any fixed-to-fixed edge. Order
within equal-prefix groups remains the ordinary full-row order.
Each final formula has **34,280 variables and 615,956 clauses**.

All 529,157 projected Ramsey clauses, both color-degree bounds, local
common-neighborhood and deficit counters, and the retained normalizations
are present. The degree window18..24 imports
[McKay and Radziszowski's R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf);
the original computation is not repeated here.

The inherited C++ auditor reconstructs the full parent from actual pair
orbits, all 962,598 five-sets and 664 gate rows. The new Python auditor
independently recovers all 320 primary edge meanings from the action on
43 vertices. It derives the three removed clauses, nine anchor units
and thirty equality units, compares every retained parent clause and
every appended unit, and checks EOF. It checks prefix order on all
2,048 full rows. Three malformed classifications and seven malformed
formulas are rejected, including restoring the incompatible ordering,
numeric-mask sorting, a lost original clause, and an extra empty clause.
Normal and optimized Python control reports agree.

## Refutations and consequence

Both complete equality formulas returned UNSAT under the fixed
60-second Kissat limit with two workers. Both full DRAT proofs passed
replay, and passed again after fresh reconstruction of the entire parent,
all classification checks, and both complete formulas. The traces use
254 and 109 RAT core lemmas, respectively; RUP-only replay is insufficient.
Exact formula and trace hashes, times, source and tool hashes are in
`result.json` and `verification.json`.

If a full graph and a chosen A had z_A=1, the normalization and equality
argument would produce a satisfying assignment of one of these two
formulas, including suitable counter and gate values. Their refutations
exclude this case. Together with z_A>=1, this proves z_A>=2.

In the original four-triangle coordinates write z for the number of
empty four-bit signatures and x_i for singleton signature {i}. A fixed
vertex is blue to the complementary triple precisely when its signature
is empty or {i}. Thus the new intrinsic consequence is

```text
z + x_i >= 2 for every i whose complementary triple has no blue triangle.
```

The 34 remaining classes cover 24,057 labeled cores. `anchors.json`
lists every applicable i in each. The preceding full-core exclusions
are needed only to assert that every remaining candidate has such an
anchor; the theorem for a specified A does not use those exclusions.
For a triple that is not the first three columns of an older canonical
formula, these inequalities do NOT authorize fixing its first two fixed
vertices. The required cardinality condition must respect that formula's
existing row order. No such further propagation test is begun here.

The parent encoding and uniform-neighbor lemma have accepted independent
reviews. The preceding 34-core sweep now also has an accepted independent
review. The later seven- and four-core closures and their empty-signature
premise remain pending, as do the new anchor normalization, equality
bridge and two refutations. Trust also includes the imported degree
theorem, unformalized combinatorics/counters, exact source semantics,
compiler/runtime/hardware, SHA256 and full DRAT checking. Internal
reconstruction is not peer review or proof-assistant formalization.
Large formulas, proofs, logs and binaries stay outside Git; hashes alone
do not replace obtaining or regenerating and replaying the proofs.
No historical-priority claim is made.
