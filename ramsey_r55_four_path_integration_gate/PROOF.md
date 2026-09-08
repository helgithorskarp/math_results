# The direct four-path carrier fails its size-reduction gate

This is an exact negative decision about a specified search representation.
It excludes no good43 graph. Here good43 means an order-43 graph with both
clique and independence numbers at most four. Red means edge; blue means
nonedge.

## Complete target cover and declared carrier

The accepted h3931 theorem (review h3935) forces four disjoint induced P5
or complement-P5 copies in every hypothetical good43: apply its 26-set
statement at residual orders 43, 38, 33, and 28. Label each of these four
blocks in standard path or complement-path order. In the remaining 23
vertices, greedily remove red K4s until none remains, then blue K4s until
none remains. Deletion cannot create a red K4. The residual core is an
R(4,4) graph. Since R(4,4)=18, the total number q of removed K4s lies in
2,...,5; the core order is 23-4q, in {15,11,7,3}. The number r of red K4s
can range from zero to q. Relabel the core to a listed catalog representative.

Define C to retain all choices of the four pattern colors, q, r, and core
index. For every pair of noncore blocks, retain precisely the cross matrices
for which that pair's union has no monochromatic K5. For every noncore block
and individual core vertex, independently retain precisely the stars for
which that union has no monochromatic K5. Fix the edges inside each block
and inside the catalog core. This is a physical 43-vertex edge carrier:
every free edge has exactly one coordinate. Every good43 has a relabeling
in it, using the imported catalog completeness premise.

C is a relaxation. It can contain monochromatic fives meeting three or
more noncore blocks, or involving multiple core vertices. It does not impose
degree constraints or every greedy-exhaustion consequence. The selected
all-red-K4 macro below has no blue K4 blocks, so its post-red-exhaustion
condition is exactly the already-fixed R(4,4) core. Its product count is
unaffected by that distinction.

The permitted normalization can use arbitrary internal automorphisms of
the standard noncore blocks and arbitrary permutations of equal-type blocks.
Colors, core labels and core index are retained. It may not move a vertex
between a path block, K4 block or core, or choose a different decomposition.
These restrictions define the gate; we make no claim about other possible
encodings or uses of h3931.

Success was declared to mean a complete normalized carrier strictly smaller
than the h3887 carrier P. Failure was declared to mean a rigorous lower
bound, even after all permitted relabelings, larger than P. We prove failure.

## One macro is already too large

Choose four red P5 blocks, three red K4 blocks, and an 11-vertex R(4,4)
catalog core. These orders sum to 43. This macro is included in C; it is
not asserted to contain any good43. The imported catalog supplies 546,356
distinct literal cores. Their Ramsey membership was checked upstream.
Completeness of this catalog is unnecessary for the lower bound itself;
it is used for the preceding target-cover statement and baseline interface.

Let A, B, D be the counts of admissible cross matrices for red P5/P5,
red P5/K4, and red K4/K4 pairs, respectively.

For P5/P5 there are 25 cross bits. A P5 has clique number two,
independence number three, one independent triple, and six independent
pairs. Thus the complete forbidden-five list consists of 12 blue events,
each fixing six cross bits. There are no red events. By the union bound,

    A >= A0 = 2^25 - 12*2^19 = 27,262,976.

For P5/K4 there are 20 cross bits. The complete forbidden-five list consists
of five red singleton-plus-K4 events fixing four bits and sixteen red
edge-plus-triple events fixing six bits. There are no blue events. Hence

    B >= B0 = 2^20 - 5*2^16 - 16*2^14 = 458,752.

These bounds do not assume disjoint forbidden events. The full event lists
are in CERTIFICATE.json. Two independent generation methods compare every
event including its literal vertices, color and cross-bit mask.

Exact exhaustive enumeration gives D=37,823. The producer checks the
forbidden-event masks on every 16-bit matrix. A separate checker builds
every physical eight-vertex graph and searches both colors for a K5 using
bit-set clique recursion. This rederives the imported same-color count.

A P5 plus a core vertex permits all 32 stars because a P5 contains no K4
in either color. A red K4 plus a core vertex permits 15 stars, excluding
the all-red star. Both counts are checked on physical graphs.

The selected macro has six P5/P5 pairs, twelve P5/K4 pairs, three K4/K4
pairs, 44 P5/core-vertex stars, and 33 K4/core-vertex stars. Its 790 free
edge bits split into disjoint coordinate sets of sizes 150,240,48,220,132;
the remaining 113 of the 903 vertex pairs are fixed. Therefore its raw
carrier has at least

    R = 546356 * A0^6 * B0^12 * 37823^3 * 32^44 * 15^33

elements. This is a product of independent coordinates in a single carrier,
not a multiplication of reductions with unrelated denominators.

## Every permitted block normalization is covered

Aut(P5) has order 2 and Aut(K4) has order 24. Exhausting all 120 and 24
internal permutations checks these two elementary facts. On the selected
macro the full permitted block group has order

    Gamma = (2^4 * 4!) * (24^3 * 3!) = 31,850,496.

This group acts by simultaneously relabeling all incident physical edges.
It preserves the pair and star predicates. It fixes the core pointwise
and cannot change the core index. Each orbit has at most Gamma elements,
irrespective of stabilizers or which normalization algorithm is used.
Consequently every choice of at least one representative per permitted
orbit needs at least ceil(R/Gamma) carrier elements from this macro alone.

This is an orbit-size inequality, not an assertion of a free action or an
exact orbit count. The checked automorphisms are only those of P5 and K4;
no full-graph or core-automorphism verifier is invoked. General graph
isomorphisms, core permutations, color interchange and changes of block
decomposition are outside the declared action.

## Exact comparison to h3887

For h3887 let c(3)=4, c(7)=362, c(11)=546356, c(15)=640. Its exact carrier
size is the sum, for q=7,...,10 and r=5,...,q, of

    c(n) * binom(1998+a-1,a) * binom(1931+b-1,b)
         * 37823^(binom(a,2)+binom(b,2)) * 35714^(a*b) * 15^(q*n),
    a=r-1, b=q-r, n=43-4q.

The two K4 pair-domain counts 37,823 and 35,714 and their column-orbit
counts 1,998 and 1,931 are rederived on all 131,072 physical matrices.
The producer evaluates binomial coefficients; the separate checker counts
multisets by a dynamic program adding one available symbol at a time.
The resulting sum agrees exactly with the pinned h3887 COUNTS.json value P.

All arithmetic is integral. CERTIFICATE.json records the full R, Gamma,
P and ceil(R/Gamma), and the check establishes the strict inequalities

    12 * Gamma * P < R < 13 * Gamma * P.

Thus even one macro after all permitted block relabelings needs more than
12P representatives. The whole direct four-path carrier cannot meet the
declared size-reduction gate. The interval (12,13) describes R/(Gamma P),
the certified lower-bound ratio; it is not the exact ratio of carrier sizes.

## Outcome and limits

Close this direct integration gate. Do not implement another encoder,
nearby quotient, or matrix-domain refinement on the basis of this attempt.
The accepted h3931 theorem and its immutable handoff remain valid.
This calculation makes no claim about solver time, the number of genuine
good43 survivors, the feasibility of the selected macro, or every possible
integration of h3931 into the existing h3887 search. It makes no target
solver call, decides no h3887 physical task, and proves neither existence
nor nonexistence of a good43. All 2,189,178 upstream physical tasks remain
undecided as of this pass's checkpoint; physical completion is owned by
team-r55-1.

Imported mathematical premises are h3931 (accepted at h3935), R(4,4)=18,
the listed R(4,4) cores' membership and cover, and the h3887 interface
interpretation. The finite local-domain counts and exact arithmetic are
rechecked here. The optional catalog audit checks a pinned digest and
literal uniqueness, not Ramsey membership or isomorphism completeness.
Residual computational trust includes the two Python implementations,
integer and SHA-256 semantics, operating system and hardware. No external
solver or floating-point calculation is used. No historical novelty claim
is made.
