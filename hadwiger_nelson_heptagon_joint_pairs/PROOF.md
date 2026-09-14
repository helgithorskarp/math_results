# Two previously feasible monochromatic pairs are jointly feasible

Let H be the 21-point motif and D=H-H the exact 421-point drawing in the
[parent package](../hadwiger_nelson_heptagon_difference_lifts/README.md).
The graph G contains every pair of distinct points of D at Euclidean distance
one. Let R be the 84 unordered distance-sqrt(3) pairs listed in
[certificate.json](certificate.json). This is exactly the `covered_pairs`
set of the [earlier Kempe result](../hadwiger_nelson_heptagon_kempe/README.md).

**Finite theorem.** For every two distinct members {a,b} and {u,v} of R,
there is a proper four-colouring c of G with c(a)=c(b) and c(u)=c(v).
The two pairs may share an endpoint. The colours of the two equal blocks
are not prescribed to agree or differ.

There are binomial(84,2)=3486 labelled requests. Among them, 42 requests
share an endpoint and describe 14 monochromatic triples, each in three
ways. Consequently there are 3458 distinct labelled equality partitions.
The 252 symmetry classes counted by the primary checker classify sets of
two selected pairs, not distinct equality partitions.

## Geometry and certificate proof

Put t=exp(pi*i/21). Its minimal polynomial is

    t^12 + t^11 - t^9 - t^8 + t^6 - t^4 - t^3 + t + 1.

The motif consists of p*t^(6j), q*t^(6j), r*t^(6j), for 0<=j<7, where

    p = 1/(t^24-t^-24),
    q = -t^-7/(t^6-t^-6),
    r = -t^7/(t^12-t^-12).

All coordinates of H and D have denominator 7 in this power basis. Vertex
labels refer to the lexicographically sorted integer numerator vectors of D.
The geometry verifier regenerates H and D and scans all 88410 unordered
pairs using exact squared norms. It obtains 421 distinct points, all 1848
unit edges, and all 126 distance-sqrt(3) pairs. Thus these are actual strict
plane unit-distance graphs; no numerical contact test or abstract graph
realizability assumption enters the result.

Multiplication by t^3 preserves D and the full unit graph. The verifier
checks its permutation, edge invariance, action on R and fourteenth power.
It yields 246 pair-set classes of size 14 and six of size 7.

Each of the five 421-character words in the certificate uses colours 0,1,2,3.
The verifier checks every unit inequality in each word. For each word it
finds all monochromatic pairs in R, then all two-pair requests satisfied
by that word. Their rotation classes cover all 252 classes. If a word
satisfies a rotated request, transport the word by the inverse isometry;
this proves existence for the original request. There is no claim that
five is the smallest possible number of base words.

## Separate direct check

The second checker imports no producer geometry or primary coverage routine.
It adapts the parent's tensor arithmetic in Q(zeta_7,omega_6), where

    zeta_7^6=-(1+zeta_7+...+zeta_7^5),  omega_6^2=omega_6-1,
    t=zeta_7^-1*omega_6.

It reconstructs the motif through exact sine-inverse identities, decodes
the power-basis labels into this basis, and scans all physical pairs again.
It transports all five words under each of the 14 rotations and checks
all 1848 edges in every transported word. It then tests each of the 3486
labelled requests directly against these 70 words, without a symmetry
quotient. All requests are covered. There are 63 distinct transported
words; duplication causes no coverage omission.

The two checkers share the specified coordinates, certificate and input
labelling. This is an author-run cross-check using different arithmetic
and coverage procedures, not an independent-author review or formal proof.
The remaining trust boundary is the coordinate specification, Python integer
arithmetic and runtime, and inspection of the finite encoding. No SAT
infeasibility report or solver timeout is a proof premise.

## Consequence and limits

Restricting a verified colouring to any subset of D preserves properness
and every retained designated equality. Thus no physical subgraph of this
source can forbid any tested two-pair conjunction while retaining its
terminals. Searching for a smaller forcing core of this type is futile.

This does not decide the other 42 distance-sqrt(3) pairs, any prescription
involving them, all partitions of four terminals, a requirement that the
two equal blocks have different colours, prescriptions on three or more
selected pairs, or compositions with additional physical points. It is
not a global lower bound on the order of a five-chromatic drawing.

The declared search for a new small joint source failed. The 421-point
source and every proposed core are neutral for this particular conjunction
test. Retire the premise without moving to three pairs, a new phase range,
or a larger heptagon host. No qualifying composable forcing relation or
at-most-508 non-four-colourable drawing has been found.
