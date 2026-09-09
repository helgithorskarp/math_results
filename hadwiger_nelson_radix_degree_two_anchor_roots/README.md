# Exact physical roots for the degree-two-anchor frontier

This package replaces the product-surface allowance by an exact real-root
census for every post-h4181 exact-five pair representative in the shared
`A5(z)` architecture that contains a degree-two event circle.

There are **400** such global pair systems. Their second curves meet the
anchor circles in 890 distinct per-pair physical roots. Exactly 272 roots lie
on already closed loci: a collision locus, a reflection axis, or the radial
unit circle. The remaining 618 roots form exactly **574** orbits under the
setwise pair stabilizers. Forty-four pair systems have no eligible physical
root and are removed from the whole frontier.

Against the h4181 baseline alone, this would change the global frontier from
**131,356 systems / 3,846,704 non-four orbit allowance** to **131,312 /
3,844,374**. HN2's h4185 anchor theorem was published while the independent
root verification was running and is strictly stronger: it three-colours all
six anchor circles and removes all 400 systems here, plus 24 at-least-six
systems. The current h4185 frontier is **130,932 / 3,843,692**. This package's
live role is therefore an exact geometric audit and refinement of h4185, not
an additional survivor reduction.

Roots shared by different pair systems are not globally deduplicated, so 574
was a conservative summed pre-h4185 allowance, not a count of global
parameters. It is not a live search allowance after h4185.

## Reproduction

From the repository root, using standard-library CPython 3.11.2:

```sh
python3 -B hadwiger_nelson_radix_degree_two_anchor_roots/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_degree_two_anchor_roots/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_degree_two_anchor_roots/controls.py
```

The independent verifier rebuilds the h4177 pair interface, the complete
2,400-row collision inventory, the rational circle pullbacks, polynomial
gcd/lcm markers, and all real-root counts using only `fractions.Fraction` and
an exact Sturm sequence.

The post-cutoff integration check proves exact row-set containment and the
allowance identity `2,330+574+108=3,012`; see [INTEGRATION.json](INTEGRATION.json)
and [HANDOFF.md](HANDOFF.md). It requires regenerating the two omitted
interfaces by the commands given there.

Optional fresh production uses SymPy 1.14.0:

```sh
python3 -B hadwiger_nelson_radix_degree_two_anchor_roots/produce.py \
  --out /tmp/hn-degree-two-anchor-certificate.json \
  --export-interface /tmp/hn-degree-two-anchor-interface.json
```

Output paths must not exist. The generated compact certificate is semantically
identical to the committed certificate (whose arrays use denser whitespace).
The 232,908-byte explicit 400-row interface is regenerated rather than
committed. Its file SHA-256 is
`94cee1fd30d8273b2631f74afcbb0d746b3fd2c9b9a3fa85b476a604648f4c1c`.
See [PROOF.md](PROOF.md) for the exact argument and [HANDOFF.md](HANDOFF.md)
for the HN2 interface.

No physical chromatic search was performed, no candidate graph is supplied,
and no improvement to the 509-vertex record is established. This is an
author-side exact computation pending independent review.
