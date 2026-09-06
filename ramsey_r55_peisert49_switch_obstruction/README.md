# The Peisert(49) switching family is excluded at order 43

**Theorem, using the published Hill–Love classification.** Every graph
obtained by selecting any 43 vertices of Peisert(49) and applying an
arbitrary Seidel switch contains a clique or independent set of order five.
The result covers all six deletions, all switch sets, all relabelings, and
global color reversal. It imposes no degree profile, resulting graph
automorphism, catalog parent, or neighborhood data.

The new obstruction concerns the **opposite switch class** of a 22-point
four-arc. Peisert(49) actually has Ramsey(5,5) induced subgraphs of order 22:
[fixture22.json](fixture22.json) supplies one with a literal edge list.
Thus the earlier Paley(49) lemma that every 22-point subset contains a
monochromatic five-set is false for this construction. The proof below
closes the new family through its attachments instead.

There is no 43-vertex Ramsey graph or improvement of a Ramsey-number bound
in this package. The order-42 boundary is left open. No historical-priority
claim or exclusion of arbitrary binary-rank-26 graphs is made.

## 1. Definition and imported geometric premise

Work in F49 = F7[t]/(t²−3), with x+yt labeled x+7y. The element g=1+t,
labeled 8, has multiplicative order 48. Peisert(49) has red edge uv when

    u−v = g^j,   j = 0 or 1 modulo 4.

This is the standard Peisert construction; see §0.4 of
[A. E. Brouwer's primary notes](https://aeb.win.tue.nl/preprints/paleyclique-v2.pdf)
and their reference to W. Peisert, *All self-complementary symmetric graphs*,
Journal of Algebra 240 (2001), 209–229. Those notes also explain its different
maximal-clique behavior from Paley(49). No clique classification from the
notes is a proof premise here.

The 24 red differences are precisely the nonzero vectors in the four
directions of slopes {0,1,5,infinity}. The code checks this from the 48
distinct powers of g and independently using the character criterion

    z^12 in {1, g^12} = {1, 3t}.

Every affine F7-line is monochromatic: all its nonzero differences differ
by a nonzero F7 scalar, and F7* = <g^8> lies in the fourth powers.
Multiplication by g² reverses every color. The choice of red versus blue
therefore creates no extra case.

The sole imported classification is the theorem of Ray Hill and Chris P.
Love that PG(2,7) has exactly three projective-equivalence classes of
22-point sets meeting every line in at most four points. Source:
[On the (22,4)-arcs in PG(2,7) and related codes](https://www.sciencedirect.com/science/article/pii/S0012365X02008129),
Discrete Mathematics 266 (2003), 253–261,
DOI [10.1016/S0012-365X(02)00812-9](https://doi.org/10.1016/S0012-365X(02)00812-9).
**Its completeness, including the MAGMA part, is imported, not recomputed.**

The three literal representatives in [arcs.json](arcs.json) are reused from
the accepted [Paley(49) arc package](../ramsey_r55_paley49_arc_obstruction/).
The present checker independently validates all 57 projective lines and
obtains these profiles; entry j counts lines containing j points:

| Arc | j=0 | j=1 | j=2 | j=3 | j=4 |
|---|---:|---:|---:|---:|---:|
| 0 | 7 | 1 | 0 | 21 | 28 |
| 1 | 6 | 2 | 3 | 16 | 30 |
| 2 | 4 | 4 | 9 | 6 | 34 |

Distinct profiles prove projective inequivalence, so the imported theorem
makes these three representatives complete. No claim about the full
automorphism groups of the arcs is needed.

## 2. Why every switch class has order at most 22

Within a switch-bit class, all colors are unchanged. A class in a hypothetical
Ramsey graph thus has at most four points on each affine line, and its
projective completion has an empty line at infinity: it is a four-arc.

Each displayed representative is saturated. For every one of its 35 other
projective points, the checker finds a line containing that point and four
of the representative's points. These are 3·35 = 105 exact extension
obstructions. Therefore none of the three representatives extends to a
23-point four-arc. By the imported classification, no 23-point four-arc
exists: deleting a point from one would give a listed 22-point type and
an impossible extension. A larger four-arc would contain a 23-point one.

Hence a hypothetical switched Ramsey graph on 43 points has switch classes
of sizes 22 and 21. Complement all switch bits if necessary and call its
22-point class A, with switch bit zero.

## 3. All affine positions of the 22-point class

Choose a projective isomorphism from a displayed representative C to A.
Pull the line at infinity back to L. This L is disjoint from C, giving
7+6+4 = 17 choices over the three representatives.

For L=(l0,l1,l2), let k be the largest index with lk nonzero, and i<j the
other coordinate indices. Use the canonical chart

    p -> (pi/(L·p), pj/(L·p)).

The three coordinate forms pi,pj,L are independent. Thus this chart carries
L to infinity and maps its other 49 projective points bijectively to F7².
Any other projective embedding with the same pulled-back infinity differs
by an invertible affine map Mx+b.

Translations preserve all differences. Pulling back Peisert colors by M
therefore changes only the subset of its red directions. The two independent
columns of M have 48·42 = 2,016 possibilities. Enumerating all of them gives
exactly 28 distinct pulled-back direction masks. All 2,016 maps are retained
when deriving this set; no arbitrary linear map is assumed to preserve the
Peisert graph. Matrices giving the same mask give literally the same
color to every pair in F7², including pairs involving outside vertices.

Consequently the complete affine family has

    17 empty-line charts · 28 direction masks = 476 cases.

The producer derives these masks using field multiplication and quartic
cosets. The checker derives them separately from independent vector columns
and the slope set {0,1,5,infinity}. Controls check every one of the 96,768
nonzero displacement transports and all 98,784 point images.

## 4. Seven forbidden opposite-switch vertices in every case

Each case has 22 fixed selected points and 27 other affine points. The
[certificate](certificate.json) gives seven distinct outside points w.
For each w it supplies a color c and four distinct anchor indices Q such
that all six pairs in Q have original color c, while the four pairs from
w to Q have original color 1−c. Selecting w with switch bit one would
reverse those four pairs and make Q union {w} a physical monochromatic K5.

The seven points must therefore be omitted. This leaves at most 20 of the
27 outside points available for the required opposite class of size 21.
Equivalently, at least seven deletions are forced although selecting 43
of 49 allows only six. This contradiction proves the theorem.

Each certificate row is

    [arc_index, projective_line_index, direction_mask,
     [[outside_field_label, color, q0, q1, q2, q3], ... seven stars ...]].

Projective lines are lexicographically ordered canonical triples with first
nonzero coordinate 1. Direction bits 0..6 represent slopes 0..6; bit 7 is
infinity. Anchor indices refer to the ordered representative. The checker
reconstructs all five physical vertices and their switch bits, verifies
all ten pairs, checks distinctness of the seven outside exclusions, and
requires every expected case exactly once. This is 3,332 explicit physical
five-set witnesses and 33,320 checked pairs. No SAT verdict is used.

The direct exhaustive control, which ignores the supplied star witnesses
and enumerates all four-subsets of each anchor, finds the stronger
single-vertex capacities below. They are exact for avoidance of K5s using
four anchor vertices, not claims of joint feasibility of the surviving
outside vertices. Only the weaker bound 20 is needed by the compact
seven-star certificate.

| Individually admissible opposite points | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Affine cases | 80 | 24 | 8 | 80 | 64 | 8 | 120 | 84 | 8 |

Every one of the 476 anchors is itself Ramsey(5,5). This is checked through
the direct four-subset census and its possible fifth neighbors; it is not
needed for the exclusion. It demonstrates why an attachment argument is
needed instead of transferring the previous Paley 22-point lemma.

## 5. Reproduction and scope

Python 3.11 or later, standard library only, from the repository root:

```sh
python3 -B ramsey_r55_peisert49_switch_obstruction/reproduce.py
python3 -O -B ramsey_r55_peisert49_switch_obstruction/reproduce.py
```

Both print `VERIFIED_PEISERT49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE`.
The main proof certificate can be checked without replaying the producer
or the broader implementation controls:

```sh
cd ramsey_r55_peisert49_switch_obstruction
python3 -B check.py certificate.json
python3 -B verify_graph.py fixture22.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) imports neither producer code nor the control program.
[verify_graph.py](verify_graph.py) knows no Peisert or projective geometry:
it validates the literal edge list and checks all five-subsets directly.
The 22-vertex fixture is not a new Ramsey bound or a target candidate.

Controls compare three color definitions on all 2,401 ordered field pairs,
all 57 complete charts, and all 2,016 linear maps. A direct census of
3,481,940 four-subsets replaces the producer's bitset search and checks the
entire attachment-capacity distribution. Eight deliberately malformed or
false certificates are rejected. Normal and assertion-disabled runs agree.
No network, solver, compiler, private trace, or external data file is
required for replay. `SHA256SUMS` fixes all source and compact evidence.

The exact Peisert binary adjacency ranks are 24 in both colors. A Seidel
switch changes its binary adjacency matrix by s1ᵀ+1sᵀ, of rank at most two;
taking a principal submatrix cannot increase rank. Thus both ranks of
every family member are at most 26. The known seven-defect cyclic graph
has ranks 40 and 42, excluding rediscovery under relabeling or color reversal.
The prior package's rank comparisons with the cyclic seed, primary optimum
and supplied catalog parents transfer through this same rank bound.
This does not inspect every state of every old cyclic basin.

The literal Ramsey22 fixture and the prior Paley22 obstruction also show
that the two 49-point base graphs are not isomorphic. The deleted switching
families are not asserted disjoint. The new proof concerns every member
of the Peisert family, regardless of any overlap with already closed work.

The principal inherited trust boundary is the Hill–Love completeness theorem.
Other trust is in the displayed geometric and switching reductions, exact
Python integer semantics, the finite checking implementations and ordinary
hardware. This is author validation; no external review or formalization of
this Peisert application is claimed. Team-r55-3's global degree-profile
frontier is unchanged and is not a premise of this result.
