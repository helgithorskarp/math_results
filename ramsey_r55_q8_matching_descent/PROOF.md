# Exact matching-coordinate construction

Let G be a completely specified two-colored graph on 43 vertices. Fix the
monochromatic internal pairs of eight K4 blocks and all pairs of an
11-vertex Ramsey(4,4) core. Of the blocks, r are red and 8-r are blue,
for r in {5,6,7,8}. The other 800 pairs can have arbitrary colors. Let B(G)
count all red K5s, all blue K5s, and all red K4s in vertices 4r through 42.
Every original q8 task has this physical representation after ignoring its
label-order conventions. B=0 certifies a good43, with the required tail
maximality. B>0 is neither a target nor a task exclusion.

Fix any matching M among the 800 editable pairs. Write z_e=1 to flip e.
A five-set contains at most two matching pairs, as does a four-set. Each
forbidden-set indicator therefore depends on at most two z variables.
If its remaining fixed pairs have both colors, the indicator is identically
zero. Otherwise it is 1, z_i, 1-z_i, z_i*z_j, z_i*(1-z_j),
(1-z_i)*z_j, or (1-z_i)*(1-z_j). Summing gives exactly

    B(G triangle {e:z_e=1}) = c + sum_i a_i*z_i + sum_{i<j} b_ij*z_i*z_j.

This identity includes obstructions created by the edits. It is not a
hitting-set surrogate. Its constant c is B(G). The producer builds these
terms directly from every physical five-set and every required tail four-set.
The verifier obtains linear and mixed coefficients independently as physical
single-flip and two-flip finite differences, counting common-neighbor
triangles (and common-neighbor edges for the tail-four terms).

A binary reflected Gray code traverses all 2^|M| edit subsets. When coordinate
i changes by s in {-1,+1}, the energy changes by
s*(a_i+sum_j b_ij*z_j). Updating all affected fields maintains this exact
expression. Exhaustion gives the global optimum for this matching. Start
with the identity edit as incumbent and replace it only for strictly lower
cost; equal minima leave the graph unchanged.

Use the circle factorization of K44 and delete dummy vertex43. Removing the
fixed block/core pairs leaves 43 matchings that partition all 800 editable
pairs. Cycle through them in their declared order, accepting only strict
improvements. A full sweep with no improvement proves matching-coordinate
stationarity for that exact factorization. Each accepted move decreases the
nonnegative integer B by at least one, so there are at most B(initial) moves;
there are at most B(initial)+1 sweeps. This is a finite construction test,
not a solver timeout. The possible iteration bound is not a speed promise.
No plateau edits, random restarts or larger neighborhoods are used.

This stationarity is restricted: matchings of a different factorization,
sequences passing through equal or higher B, and arbitrary edge sets remain
unresolved. It does not exclude a single original task. The four trials use
fresh SplitMix64 cross-pair bits and four predeclared core IDs. No historical
43-vertex reference, frozen partial trace, symmetry source, or q10 child is
an input. A target is accepted only after independent literal enumeration
of every physical five-set. Nonzero endpoints are failed construction tests.

Arithmetic is integral. There are 962598 five-sets, hence at most 1925196
five-set color indicators, and at most 8855 required tail-four indicators.
Every constant/coefficient is a signed sum of at most 1934051 indicator
expansions. Intermediate fields and sums are bounded by a small multiple
of 21 squared times that number, far below the signed 64-bit range. Gray
masks have at most 21 bits. No floating point affects decisions; it records
time only. The method and matching quadratic identity are elementary; no
novelty or external-review claim is made.
