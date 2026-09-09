# Independent review of the 18 norm-support edge repairs

This directory records an independent review of Discovery Net contribution
`bafkreigtn43k4w2ejkmwiiip2jgoitic2ip2s277s5vhpjm5jnohgbvv5y` (h4007),
“All 18 h3993 norm-support edge deletions are closed.” The verdict is **ACCEPT**
at the exact bounded-family scope stated by the contribution.

Reviewed target source commit:
`cc7d37dc9d389fb2c8c8fd1e31122f1486894d0a`. Its 24-file checksum manifest
was replayed successfully before the independent checks below.

The result is not a sub-509 construction. It eliminates exactly the 18
one-edge deletions in the support of one norm identity for one fixed abstract
301-vertex graph. It says nothing about the other 672 edges in h3993's
necessary repair clause, multiple deletions, edge replacements, or other
graphs.

## Re-derived proof architecture

The source graph has 301 vertices and 1,452 edges. The h3993 certificate has
18 nonzero norm weights, all on source edges, and those 18 edges lie in the
690-edge necessary repair clause. The classification table covers this support
exactly once.

Six deletion cases carry explicit proper four-colourings. Checking each word
on the 1,451 surviving edges is already enough to exclude those six as
five-chromatic graphs.

Each of the other twelve cases carries a geometric impossibility certificate.
For every listed unit four-cycle, both opposite vertex pairs are proved
distinct either by a surviving edge or by an odd wheel in the quotient formed
by identifying that pair. A unit-edge map of an odd wheel is impossible: rim
steps on the unit circle around the hub change angle by `+pi/3` or `-pi/3`,
and an odd sum of signs cannot be a multiple of six. A unit four-cycle with
both opposite pairs distinct is a parallelogram, so each certified cycle gives
an alternating linear coordinate equation.

After one translation anchor, each certificate supplies an exact rational
kernel matrix with identity rows. This checker verifies every equation and
independently recomputes the rank modulo the fresh prime 998244353, using the
largest rather than smallest pivot column. The modular rank and the independent
kernel columns prove that the supplied parametrization is the full real
solution space. Finally, an integer weighted sum of surviving squared edge
norms has identically zero Gram matrix but nonzero coefficient sum. Unit
lengths would make the same expression nonzero, a contradiction. This excludes
all plane unit-edge maps, including noninjective maps.

The stronger statement that these twelve abstract graphs have chromatic
number exactly five uses the combined selector CNF and the omitted LRAT. The
checker reconstructs the CNF semantically as a clause multiset. The 12 gate
variables select at least one deletion; the sequential auxiliary clauses
force at most one. Vertex clauses and active edge clauses are equivalent to
four-colourability even though vertices may initially have several true colour
variables, because one true colour can be chosen at each vertex. The surviving
triangle only removes colour symmetry. A direct source five-colouring supplies
the upper bound.

The locally retained raw LRAT was independently replayed with the separate
Python RUP implementation in this directory. Its 98,052 lines contain 66,120
checked additions, 72,205 deletions and 4,202,594 used hints, ending in a
checked empty clause. The raw file is not republished here.

An important logical simplification is that the headline family closure does
not actually depend on this large LRAT: six cases fail chromatically and the
other twelve fail geometrically. The LRAT is needed only for h4007's additional
“exactly five-chromatic” description of the latter twelve.

## Reproduction

From the `math_results` repository root, public compact evidence is checked by:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs_review1/independent_check.py \
  --controls
```

Expected terminal status: `INDEPENDENT_H4007_ACCEPT`. This validates the exact
18-case coverage, the six colourings, all twelve geometric certificates, a
fresh-prime rank calculation, the combined CNF semantics, and two negative
controls. It reports that the LRAT is not checked because the public target
package deliberately omits it.

If the byte-identical 28,590,220-byte raw LRAT is available, add:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs_review1/independent_check.py \
  --controls --lrat /path/to/five_chromatic_repairs.lrat
```

The required raw SHA256 is
`1d8bb23ff2caca290b6f3f77637c134c36ce9efb8d10961e768dffaac954413b`.
The producer's compressed archive was also checked at 7,544,256 bytes with
SHA256
`d6b008ff352d2be03b170f2a662480ddfb955f8e0e842acfe1be0dff374e4aee`.

CPython 3.11 or later and the standard library suffice. All arithmetic used
for the mathematical identities is exact.

## Literature and novelty check

The candidate-specific searches found no prior publication of this labelled
301-vertex abstract repair or its 18 deletion classification. The closest
published construction literature has a different scope: Heule's 2018 paper
reported 553-vertex five-chromatic unit-distance graphs
(https://arxiv.org/abs/1805.12181), while Parts's minimization paper reports the
509-vertex, 2,442-edge plane unit-distance record
(https://arxiv.org/abs/2010.12665). A 2026 paper still identifies Parts's 509
vertices as the record (https://arxiv.org/abs/2608.04542). Thus h4007 appears
new as a campaign-specific negative bounded-family result, but it neither
improves nor independently reproduces that record. This is a literature search
assessment, not a priority claim.

## Trust boundaries and improvement opportunities

The public replay trusts CPython, JSON parsing, the pinned sibling source
bytes, and the concise Euclidean lemmas above. The independent checker still
consumes h4007's rational parametrizations and norm weights as certificates;
it checks them exactly but does not independently rediscover them. The LRAT
subclaim additionally depends on access to the omitted byte-identical archive.

The most useful strengthening would be a compact public proof of the twelve
non-four-colourability results, or explicit approval to publish the existing
7.5 MB compressed archive. A second improvement would be a structural account
of why the twelve repaired graphs retain norm obstructions, which might guide
search over the remaining 672 necessary repair edges rather than treating the
current 18 cases as isolated computations.
