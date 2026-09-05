# Excluding equality in the full eleven-cycle extension

## Statement and inherited boundary

Let G be a red/blue complete graph on 43 vertices with no monochromatic
K5. Suppose an automorphism has type `1^10 3^11`, with exactly three
internally red moving triangles C0,C1,C2 and eight internally blue
moving triangles. If F is its ten fixed vertices, define

```text
S(f) = {i in {0,1,2}: f is red to Ci},
z = |{f in F: S(f) is empty}|.
```

Attachments are uniform because f is fixed and each Ci is an orbit.
The conclusion of this computation is **z >= 2**. Color exchange gives
the corresponding statement when the minority color is called blue.

The independently accepted prior core reduction and signature
propagation leave only classes 11 and 13, respectively with red
offset words `100,110,110` and `110,110,101` on minority pairs 01,02,12.
The current computation tests both and imposes no selected degree
profile, additional automorphism, or fixed-to-fixed graph.

## Exhaustive split from the sharp signature lemma

For completeness, let a_i count red fixed neighbors of Ci, x_i count
signature {i}, and let X,Y,Z count signatures of sizes one, two, three.
Uniform red neighbors of Ci form a blue clique, so a_i<=4. Three
singleton-{i} vertices would form a blue triangle and are blue to a
blue edge between the other two red triangles. Such an edge exists
because otherwise those two triangles form a red K6. Thus x_i<=2.
Consequently

```text
I = sum_i a_i = X+2Y+3Z <= 12,
X <= 6,
2(X+Y+Z) = I+X-Z <= 18.
```

At most nine fixed signatures are nonempty, so z>=1. If z=1, equality
forces Z=0, X=6, I=12. Every singleton count is two, every a_i is four,
and the pair-count equations give one copy of every pair. Thus z=1
and z>=2 form a complete disjoint split; the former has exactly one
minority-signature multiset.

The inherited local 19-vertex fixtures realize this equality for both
cores. Hence the new conclusion uses the full 43-vertex extension
conditions; it is not a stronger version of the lemma under its local
hypotheses alone.

## Exact conversion to branch units

Use moving labels 3i+s, i=0,...,10 and s modulo three; fixed labels
33,...,42. The parent has already sorted the full eleven-bit red
attachment signatures of F lexicographically, with minority bits
0,1,2 first. Sorting full bit vectors also sorts their three-bit
prefixes. Empty prefixes therefore occur first.

For z=1 the prefixes for fixed labels 33 through 42 must be

```text
000, 001, 001, 010, 010, 011, 100, 100, 101, 110.
```

With mask bit i representing red to Ci, their numeric masks are
`0,4,4,2,2,6,1,1,5,3`. Increasing numeric mask order would be incorrect.
Ordering within an equal-prefix class is left to the remaining eight
attachment bits, exactly as in the existing parent normalization.
Thus the displayed prefixes introduce no additional normalizer claim.

The primary red-attachment variable for Ci and fixed vertex v is

```text
l(i,v) = 211 + 11*(v-33) + i.
```

The signature base already contains `-211,-212,-213`, setting vertex
33's prefix to 000. The equality formula appends the 27 remaining
signed primary units for the displayed prefix list. The z>=2 formula
instead appends `-222,-223,-224`, setting vertex 34's prefix to 000.
These branches are disjoint already on variable 224: it is positive
in the equality branch and negative in the other branch. Given the
inherited lemma and sorted prefixes, the respective conjunctions are
equivalent to z=1 and z>=2. No other variable is fixed by this split.

`check_split.py` recovers these primary meanings directly from literal
unordered-pair orbits and constructs the equality prefixes from actual
singleton and pair bit vectors, separately from the producer's mask
list. It checks the split on all 928 arithmetic profiles satisfying
the two basic bounds, and confirms prefix ordering over all 2048 full
eleven-bit signatures. Among the 778 profiles also satisfying the
inherited four-vertex bounds, exactly one is an equality profile and
777 have at least two empties. These are necessary arithmetic profiles,
not counts of graph realizations.

## Full formula and refutation bridge

The accepted parent r=3 formula has 34268 variables and 615572 clauses,
including all projected five-set conditions, both color-degree bounds,
common-neighborhood and deficit counters, and justified normalization.
Python regenerates this complete formula; the separate inherited C++
auditor reconstructs every clause. Both base formulas then retain the
nine selected-core units and all 1623 inherited signature consequences,
giving 617204 clauses. Their hashes match the independently reviewed
signature formulas exactly.

The final formulas have 617231 clauses in the equality branches and
617207 clauses in the other branches, with the variable count unchanged.
The new auditor checks the entire base prefix after its changed header,
every new unit, and EOF. This comparison excludes any omitted original
constraint or unsupported appended clause.

Kissat reports UNSAT for both equality cases. The 11698808-byte proof
for class 11 and the 11651203-byte proof for class 13 are checked by
drat-trim against their complete audited formulas, returning `s VERIFIED`.
Both traces contain RAT steps (86 and 89 RAT core lemmas respectively).
They are replayed again against freshly reconstructed formulas in a
separate verification directory. Result and verification reports record
the exact hashes and outcomes. Five malformed formulas are rejected:
an omitted equality unit, numeric mask ordering, an unsupported empty
clause, wrong z>=2 polarity, and a corrupted original prefix.

The two remaining z>=2 formulas return explicit UNKNOWN after the
bounded 60-second runs. No feasibility is inferred from these outcomes.
Excluding z=1 for both cores, together with the complete inherited
core cover, proves z>=2 throughout the three-versus-eight branch.

This is the end of the bounded four-case test. Neither remaining core,
the four-versus-seven split, nor the full eleven-cycle type is excluded.
No target graph or Ramsey lower-bound improvement follows. The newly
submitted refutations await independent review; all inherited reduction
stages have accepted independent reviews. Large formulas and traces
are reproducibly generated outside Git, rather than supplied as compact
standalone certificates. Hashes and reported solver exits alone do not
establish the result.
