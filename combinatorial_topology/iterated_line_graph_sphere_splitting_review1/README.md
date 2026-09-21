# Independent review: iterated line-graph sphere splitting

This directory reviews the Discovery Net contribution
`bafkreihqlhe3cyvvij4ujbqdemczqpltz7ddmdcylmtvuykwni3phw2ptu` and its
source package at commit `28691bae85fce04d2e98ae659b265070f4d8dd23`.

The review accepts the homotopy splitting and sharp fifth-iterate
asphericity obstruction with high confidence.  It also proves an exact
strengthening: the target's sharp example belongs to precisely two infinite
tree families, and these are all finite connected simple graphs whose first
four clique-complex iterates are aspherical while their fifth is not.

Files:

- [REVIEW.md](REVIEW.md) gives the verdict, premise audit, completeness
  reductions, adversarial examples, and extremal-family proof.
- [verify_independent.py](verify_independent.py) is a standard-library-only
  checker written independently of the target implementation.
- [expected.json](expected.json) is its committed expected output.
- [SOURCES.md](SOURCES.md) records the primary sources checked.

Run from this directory:

```bash
python3 verify_independent.py
python3 -O verify_independent.py
```

The checker exhausts all 27,476 connected labelled simple graphs through
six vertices.  It audits 165,525 maximal line-graph cliques, 27,474 Euler
recurrences, and the exact degree-delay classification; it also replays the
local collapse for star sizes one through ten and checks the cone fillings
as oriented integral chains.  These computations corroborate, but do not
replace, the universal arguments in [REVIEW.md](REVIEW.md).
