# Independent review: T375 high-contact target closure

## Verdict

**ACCEPT**, with high confidence inside the exact-computation trust boundary
below.

This reviews Discovery Net artifact
`bafkreifnpssljd3b74y33dr6wiennajxmb45uwe4ytihgvdwdpqwj3yv3m`, *All
10,012 target-sized high-contact T375 completions are four-colourable*, at
source commit `7799eabcea3409b86b4d84031e13d175be371bc4`. The stated family closure
is correct. It is an intermediate negative result, not a sub-509-vertex
five-chromatic construction.

## Exact reduction

In the stated lattice, a coordinate difference `[a,b,c,d]` represents

```text
((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

Its squared length is one exactly when

```text
3a^2 + 11b^2 + c^2 + 33d^2 = 1296,
ab + cd = 0.
```

The positive first equation bounds all four integers, so the direction search
is finite and complete. The independent checker exhausts the full resulting
817,089-row coefficient box and recovers exactly 54 oriented unit directions.
It rebuilds the 627-point source orbit by group closure, selects the pinned 375
T375 vertices, and obtains exactly 12,184 external one-step completion points.
Counting representations `q=p+d` independently gives the submitted incidence
histogram and identifies 131 core additions of T-degree at least six and 141
optional points of T-degree five.

The 647-point support has 3,626 strict unit edges. The checker constructs them
by translated-neighbour lookup rather than the target verifier's exhaustive
support-pair scan. This gives 1,661 edges on T375, 2,677 on the 506-vertex core,
868 optional-to-core incidences, and 81 optional-band edges. All canonical
point and edge hashes match.

## Colouring certificate audit

For each of the eight published core colourings, the checker directly verifies
every core edge and records each optional point's available colours as a
four-bit mask. Two optional points extend the colouring unless either mask is
empty or the points are adjacent and both masks are the same singleton. This
criterion is both necessary and sufficient: in every other case one can choose
two distinct colours when an optional edge requires it.

The eight exact pair-coverage counts are

```text
9179, 9315, 9452, 9590, 9729, 9729, 9452, 9044,
```

with successive new coverage

```text
9179, 136, 137, 138, 139, 139, 1, 1.
```

The union is all `C(141,2)=9,870` target-order graphs. As a stronger direct
check, the reviewer implementation selects a certificate row and explicit two
optional colours for every pair, then checks every optional-to-core and
optional-to-optional incidence. It separately checks all 141 singleton members
and the core. The first-cover-row hash agrees exactly. Only three optional pairs
are covered by a single row, confirming that the late certificate rows are
load-bearing rather than redundant.

The independent edge-count distribution for the 9,870 order-508 members is
recorded in [`review_result.json`](review_result.json); it ranges from 2,687 to
2,695 and sums to 9,870 members.

## Independence and reproduction

[`independent_check.py`](independent_check.py) imports no submitted module. Its
main algorithms differ from the target verifier:

- full four-coordinate enumeration rather than solving for the final square;
- representation multiplicities rather than repeated base-neighbour queries;
- direction-translation edge generation rather than all support-pair tests;
- bit-mask extension and explicit per-member colour selection rather than the
  target's tuple-based availability loop.

Fresh target runs in normal and assertion-disabled modes matched
`expected.json`, and all nine target manifest entries passed. Fresh reviewer
runs in both modes exactly matched `review_result.json`.

From this review directory, against a checkout of the verified source commit:

```bash
python3 -B independent_check.py /path/to/math_results
python3 -O -B independent_check.py /path/to/math_results
```

Python 3.11 or later and the standard library suffice for both the submitted
verifier and this independent checker. The optional SAT-based certificate
producer is not part of the verdict: the eight positive colour witnesses are
checked directly.

## Scope and trust boundary

The accepted theorem covers only the core consisting of all one-step lattice
points with at least six T375 neighbours, augmented by at most two points from
the degree-five band. It does not cover lower-incidence points, non-lattice or
multi-step completions, three or more degree-five additions, deletions from the
core, or other wrappers around T375. No graph improving the 509-vertex record is
produced.

The proof uses T375 only as a pinned exact point set and unit graph; its marked
triangle-forcing property and vertex-minimality are not premises of this family
closure. Imported trust is limited to the hash-pinned 109-row parent appendix
and retained-index list. Remaining trust includes CPython integer and file
semantics, Git/SHA-256 identity, the independent transcription, and ordinary
hardware. No floating-point predicate, SAT soundness claim, private search
state, or unpublished negative result is used.

The historical source of T375 is the Exoo--Ismailescu
[construction](https://arxiv.org/abs/1805.00157v1). Parts's
[509-vertex graph](https://arxiv.org/abs/2010.12665) supplies only the record
comparison; neither paper proves this new finite family closure.
