# Excluding the last order-five action

**Theorem.** A graph on 43 vertices with neither a clique nor an independent
set of order five has no automorphism of order five.

The new finite result in this package excludes cycle type `1^3 5^8`.
The theorem combines it with the previously certified exclusions of the
other seven order-five cycle types. This is a computer-assisted symmetry
restriction, not a coloring construction or a Ramsey bound improvement.

## Reduction to two colorings of the fixed incidences

An order-five permutation on 43 vertices has type `1^(43-5k) 5^k`, with
`1<=k<=8`. The cases `k=1,...,7` are excluded by the four cited packages
listed in the README. It remains to consider three fixed vertices
`x=0,y=1,z=2` and eight moving cycles. Label the latter by `(i,r)`, where
`0<=i<8`, `r` is in `Z/5Z`, and the permutation sends `(i,r)` to
`(i,r+1)`. Numerically `(i,r)=3+5i+r`.

The [incidence theorem](../ramsey_r55_order5_f3_incidence/PROOF.md) says that,
after color reversal and relabeling, `xy` is red, `xz,yz` are blue, and the
moving cycles' red fixed-neighbor masks are one of

```text
h=0: 0,1,2,3,5,5,6,6;
h=1: 0,1,2,3,4,5,6,7,
```

with bit weights `x=1,y=2,z=4`. That theorem is analytic, using the
established bound `R(4,5)<=25` and elementary smaller Ramsey bounds.
It has a separately published independent review. The full extension
problem remains unrestricted apart from these necessary incidences and
the cyclic automorphism.

## Exact Boolean model

Within each moving cycle, the two unordered-distance edge orbits are
distance one and distance two. Their colors must differ: if they agreed,
the cycle's five vertices would form a monochromatic `K_5`. Let variable
`a_i=i+1` be true when its distance-one edges are red. Distance-two edges
then have red-edge literal `-a_i`.

For `i<j`, let `b_{ij,d}` mean that the edges from `(i,r)` to `(j,r+d)`
are red, independently of `r`. List the 28 pairs `(i,j)` lexicographically,
starting with index zero. The variable for pair index `t` and difference
`d` is `9+5t+d`, where `0<=d<5`. There are eight internal variables and
140 cross variables, 148 in total. The 27 fixed-edge and fixed-to-cycle
orbit colors are constants.

This parametrization covers every invariant coloring with the indicated
incidences and valid internal cycles. Conversely, every assignment defines
one such coloring. In particular, no degree restriction, hard-branch
assumption, graph catalog, or extra group action is imposed in this model.

For each of the `binom(43,5)=962598` five-sets `S`, let `L_e` be the red-edge
literal or constant of each of its ten pairs. Add

```text
OR_(e in pairs(S)) L_e        (not all blue),
OR_(e in pairs(S)) -L_e       (not all red).
```

Delete false constants and duplicate literals. Discard a clause with a true
constant or opposite literals, and deduplicate identical clauses. All of
these operations preserve equivalence. The resulting base formulas have
248,630 clauses for `h=0` and 248,610 for `h=1`.

## Normalization used only for h=1

No additional symmetry clause is imposed for `h=0`.

For `h=1`, first require `a_0=1`. If a coloring has `a_0=0`, relabel every
moving cycle by the **same** multiplier `r -> 2r`. This interchanges the
two internal distance classes on every cycle and leaves all fixed
incidences unchanged. It replaces the cyclic generator by a power that
generates the same group; hence cyclic invariance is preserved. It makes
`a_0=1`. Multiplying just one cycle would not justify this step; the
multiplier is global across all eight cycles.

Next, independently rotate each cycle `j=1,...,7`, leaving cycle zero
unchanged. Its word `(b_{0j,0},...,b_{0j,4})` is cyclically rotated by this
operation. It can be made lexicographically minimal among its rotations.
The seven choices are independent: changing the phase of cycle `j`
changes the anchor word for that cycle, not any other anchor word.
Internal distance colors and fixed incidences are unchanged.

Exactly eight of the 32 binary words of length five are lexicographically
minimal rotations. For each of the other 24 words on each of seven anchor
pairs, add the five-literal clause that forbids exactly that assignment.
Together with the single internal-orientation unit clause this gives
`7*24+1=169` additional clauses. No moving cycles of different incidence
types are interchanged. The final `h=1` formula has 248,779 clauses.

Thus every hypothetical coloring of either type yields a satisfying
assignment of its respective final formula. Refuting both formulas suffices.

## Refutations and independent reconstruction

Kissat 4.0.4 returns UNSAT for both formulas and emits binary DRAT proofs.
Both proofs were independently replayed by `drat-trim`, returning
`s VERIFIED`. `result.json` records the exact formula and proof hashes and
the tested tool revisions and binary hashes. The proof files are regenerated
outside the repository by the reproduction runner.

`independent_formula.cpp` does not import or invoke the Python encoder. It
builds all 903 unordered pairs and uses union/find under the actual
43-vertex permutation to obtain 183 edge orbits: three singletons and 180
orbits of size five. It assigns semantic literals to entire orbits using
representative edges, visits every five-set, independently substitutes
constants and complementary internal literals, and reconstructs the
normalization clauses. It compares the **complete clause multiset**, not
only counts or hashes. Both cases match. The reconstruction also passed
AddressSanitizer and UndefinedBehaviorSanitizer. The runner verifies that
deleting one clause with a corrected header, or changing a literal while
preserving the header, is rejected for each case.

`audit_normalization.py` separately checks the relabeling bridge on explicit
43-vertex graphs for all 256 internal orientation profiles, with seeded
arbitrary cross words. It imports no encoder code. It checks every edge
under the composed permutation, the preserved fixed incidences and cyclic
invariance, and all required anchor-word normal forms. These graphs are
test fixtures; they are not claimed to avoid monochromatic `K_5`.

The mathematical normalization argument is universal. The finite fixture
audit checks its implementation and does not replace that argument.
The remaining computational trust boundary is the C++/Python execution and
the DRAT checker, together with the unformalized reductions. The SAT solver
is not trusted merely for its UNSAT status. Reference hashes alone are not
proofs; a reproduction must actually replay the generated trace.

## Consequences and limits

Both possible incidence patterns of `1^3 5^8` are impossible. With the
earlier seven cycle-type exclusions, there is no order-five automorphism.
Cauchy's theorem therefore gives `5` not dividing `|Aut(G)|`. Every element
whose order is divisible by five is excluded as well, since it has a power
of order five; in particular no automorphism has a vertex cycle of length
divisible by five.

The previously established exclusions of prime orders at least seven imply
the stronger cumulative restriction `|Aut(G)|=2^a 3^b`, for nonnegative
integers `a,b`. This does not require `Aut(G)` to be trivial or construct a
target graph. The 43-vertex existence problem remains open in this campaign.
