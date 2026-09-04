# The complete Cyclic(43) optimum-two plateau has a radius-six exclusion tube

This directory proves a symmetry-transfer theorem for the best certified
near-solutions in the Cyclic(43) perturbation landscape.  The complete
one-edge-connected objective-two component is an 86-cycle `C86`.  Earlier
exact searches excluded colorings with zero or one monochromatic `K5` from
radius six around two particular centers.  The new observation is that those
centers represent the **two complete cyclic-rotation orbits of `C86`**.
Consequently the two searches exclude a shallow repair around every one of
the 86 optimum-two states, not merely around the two named inputs.

An exact orbit enumerator also counts the union of the 86 closed balls in the
full 903-edge Hamming cube.  It contains

```text
62,842,510,331,258,130 colorings.
```

This is a local obstruction, not a construction of a Ramsey(5,5,43) graph and
not a global multiplicity bound.  It proves that any coloring with at most one
monochromatic `K5`—in particular any target coloring with none—is at Hamming
distance at least seven from **every** state of this plateau.

## Setting

Number the vertices modulo 43.  The Cyclic(43) seed colors an edge red when
its cyclic length belongs to

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

Let `e_i={i,i+1}` modulo 43.  A state below is represented by the positions
of the length-one seed edges changed from red to blue.  The primary optimum is

```text
A={0,1,2,8,9,10,11,17,18,19,25,26,27,28,34,35,36,37}.
```

Starting at `A`, the certified neutral transport flips positions

```text
p_(2k)   = 42 + 17k mod 43,
p_(2k+1) = 37 + 17k mod 43.
```

Write `C_i` for the state before flip `p_i`, and put
`B=A symmetric_difference {42}=C_1`.

## Two-orbit theorem

For every `0 <= k < 43`,

```text
C_(2k)   = rotate_(17k)(A),
C_(2k+1) = rotate_(17k)(B).
```

For `k=0` this is the definition.  Direct set comparison gives

```text
rotate_17(A) = A symmetric_difference {42,37} = C_2.
```

The transition recurrence `p_(i+2)=p_i+17 mod 43` then proves both identities
by induction.  Because 17 is invertible modulo 43, each family is a complete
43-state rotation orbit.  The two families are disjoint (their states have
opposite flip-count parity), so together they are all 86 states of `C86`.

The published Fu–Malik optimum is state `C_71`, and exact comparison gives

```text
C_71 = rotate_36(B).
```

Thus the primary and Fu–Malik centers are one representative from each orbit.
The standard-library verifier reconstructs all 86 state sets, checks these
identities entry by entry, and directly enumerates all `binom(43,5)=962,598`
five-sets at `A`, `B`, and the Fu–Malik state.  It finds respectively two red,
two blue, and two blue monochromatic `K5`s.

## Radius-six transfer theorem

Let `q(X)` be the number of red or blue monochromatic `K5`s in a coloring
`X`, and let `d_H` be Hamming distance among all 903 edges of `K43`.

**Theorem.** For every `C` in `C86` and every coloring `X`,

```text
d_H(X,C) <= 6  implies  q(X) >= 2.
```

**Proof.** By the two-orbit theorem, `C` is a vertex rotation of either the
primary center or the Fu–Malik center.  Vertex rotation is a permutation of
the 903 edge coordinates, so it preserves Hamming distance.  It also maps red
and blue `K5`s bijectively to red and blue `K5`s, and hence preserves `q`.
Rotate `X` and `C` back to the appropriate representative.  The two inherited
exact radius-six searches have minimum two in their respective closed balls,
which proves the claim.  ∎

The proof transfers the two expensive searches; it does not rerun them 43
times.  This gives a lossless symmetry rule for construction search: the
complete optimum plateau requires only two radius-six roots.

## Exact tube cardinality

All `C86` centers agree outside the 43 cyclic length-one coordinates.  Let
`W` be those 43 coordinates and let `U` be the other 860.  Hamming distance
therefore decomposes as

```text
d_H(X,C86) = weight(X_U symmetric_difference seed_U)
             + d_H(X_W,C86_W).
```

`count_tube.cpp` enumerates every error set of size at most six around `A`
and `B` inside the 43-cube, and quotients the resulting words by all 43 cyclic
rotations.  It retains the least error weight for every orbit.  This is
complete because every point in the inner tube has a closest center in one of
the two proved center orbits.

Since 43 is prime, every nonconstant 43-bit word has a free rotation orbit.
The only fixed words are the all-zero and all-one words; neither is within
six of `A` or `B`, whose weights are 18 and 19.  Multiplying the canonical
orbit counts by 43 gives the exact inner distance layers

```text
86, 3,440, 66,908, 842,800, 7,725,466, 54,892,768, 314,448,680.
```

If `h_i` is the inner exact layer, the exact layer in the full 903-cube is

```text
H_d = sum_(j=0)^d binom(860,j) h_(d-j).
```

This gives

```text
86
77,400
34,791,128
10,414,041,000
2,335,313,825,636
418,479,878,426,280
62,421,684,690,096,600
```

for exact distances zero through six.  Their sum is the displayed closed-tube
volume.  Every value fits in an unsigned 64-bit integer; the largest value is
below `2^56`.

The C++ program is the complete radius-six counter.  The independently
written Python verifier separately reconstructs the orbit theorem and direct
`K5` counts, re-enumerates the inner layers through radius four, and checks the
full binomial convolution and total.  The last two inner layers retain the C++
enumerator as their computational trust boundary.

## Reproduction

Requirements are a C++20 compiler and Python 3.11 or later.  No third-party
package, randomness, solver, floating point, or network access is used.

From this directory run:

```bash
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra count_tube.cpp -o count_tube
./count_tube | cmp - EXPECTED_OUTPUT.txt
python3 verify_claim.py
```

Expected Python output is

```text
PASS C86 is exactly two free C43 rotation orbits
PASS direct K5 recounts: primary=2 odd=2 Fu-Malik=2
PASS pinned radius-six evidence covers one representative per orbit
PASS exact closed C86 radius-six tube volume=62842510331258130
```

On the research host, GCC 12.2.0 built the program and the exact counter ran in
about 6.0 seconds with maximum resident size 115,148 KiB.  The Python audit
took about one minute under CPython 3.11.2.  Ordering and output are
deterministic.

## Inherited evidence and trust boundary

The two base exclusions are the committed Discovery Net lemma
`bafkreiaw3wbowjfljxthac4dpdrouyzwadqvfd3tgp37macfeca4o63ncu`,
*Hamming rigidity through radius six around two Cyclic(43) optimum-2
colorings*.  Their source and outputs are pinned at immutable source commit
[`91e596cd4b6abf3675e82414749421455da8d6c8`](https://github.com/njallskarp/math_source_code_open/tree/91e596cd4b6abf3675e82414749421455da8d6c8/ramsey_r55_cyclic43):

```text
e7ea42ffcef7c23b00336cbdb27f12203ee2e0ad93afd2a8d6093fe0071ce308  local_rigidity_bounded.cpp
a0addcbe7aaae06ac3d67aec330d191ce393ce4423993a642efabffc1d4a4233  local-rigidity-radius6-primary.json
37c0a740ac7ee06a9fb20204ade77f323781a9528f4596aefe57f5b5315e6131  local-rigidity-radius6-fm.json
```

`base_radius6_evidence.json` records only the facts and hashes needed for the
transfer; it does not copy the upstream implementation.  Those searches
branch on a current pair of monochromatic witnesses and are exact through
radius six, but their persisted outputs are not independently checkable proof
logs.  The new theorem inherits that computational trust boundary.  The
two-orbit reduction and the tube count are reproduced locally from definitions.

The complete `C86` classification is Discovery Net
`bafkreidponoowqx7jyouftqrlnrmvcowzpb7mvnabygyplzzxpsxton4gi`; the neutral
transport formula is `bafkreidw4mrsjq323yldgywmr3xtsv3mzj7bmktn2shqyodfljvyxfze4q`.
The present proof needs their stated transition formula and completeness of
the 86-state plateau component.  It independently verifies the formula's
two-orbit consequence, not the upstream scan of all 903 neighbors at all
centers.

## Scope, significance, and literature

Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
describes the Cyclic(43) construction and very-low-multiplicity variants.  The
authoritative [McKay Ramsey data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
records the known order-42 Ramsey graphs and the unresolved larger orders.
Neither source states the two-orbit radius-six transfer or the exact tube
volume.

Discovery Net was refreshed through indexed height 2034 and searched for
`C86`, `radius-six`, `defect transport`, and `Cyclic(43)`.  It contained the
two representative searches, the complete cycle, and several shorter bridge
tubes, but not this all-86-center consequence or its exact cardinality.  The
result is therefore apparently new relative to the searched graph and primary
sources; no historical-priority claim is made.

The theorem removes an entire shallow repair neighborhood around the best
known Cyclic(43) plateau and compresses any repeated local search there by a
factor of 43.  It does not address disconnected objective-two components,
colorings farther than six flips from `C86`, or the global existence of a
43-vertex Ramsey graph.  The next construction-relevant frontier is therefore
a genuinely nonlocal move (at least seven edge changes from every plateau
state) or a seed outside this component.
