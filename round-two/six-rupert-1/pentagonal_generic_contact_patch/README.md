# Pentagonal hexecontahedron: generic receiving patch near body motions

**six-rupert-1, researcher; 2026-10-01.** Exact finite certificate and
written local rigidity proof; author checked, unformalized, independently
unreviewed. Full Rupert property: **OPEN**.

For every hull in the published pentagonal four-parameter box, at receivers
with raw direction `(1+s,2+z,3)`, `|s|,|z|<=1/1000`, closed fits with
`lambda>=1` and arbitrary actual planar translation are trivial when the
proper relative motion has Cayley infinity radius at most `1/1000000`
from a body symmetry. Proper icosahedral images of the receiving patch
and the mirror of the whole configuration have the corresponding result.
The source-motion hypothesis is essential; sources outside these
neighborhoods remain unclassified.

[PROOF.md](PROOF.md) specifies the exact family, quantifiers, six original
supports, positive stress correction and finite-motion bridge. The checker
uses only six valid supports and checks every one on all 92 original
generator points; it requires no complete exploratory hull.

From the repository root, using Python 3.11+ and the standard library:

```sh
python3 -B round-two/six-rupert-1/pentagonal_generic_contact_patch/check.py
python3 -O -B round-two/six-rupert-1/pentagonal_generic_contact_patch/check.py
python3 -B round-two/six-rupert-1/pentagonal_generic_contact_patch/validate_controls.py
```

The first two commands reproduce [expected.json](expected.json). The last
checks that record in normal and optimized Python and refuses damaged
contact, normal, correction and motion-bound inputs. Its expected summary
is [VALIDATION.json](VALIDATION.json).

The checker pins [verify.py](../pentagonal_minimum_diameter/verify.py) by
SHA-256 `12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339`,
from named-model source `86ab225fb8becbe66601a5da0b5b017e872e1833`. This
prerequisite supplies exact field/interval arithmetic, body symmetries,
generator forms and named-parameter isolation. Its
[model proof](../pentagonal_minimum_diameter/PROOF.md) supplies the
standard-solid identification. No solver, CAS, numerical library,
external dataset or large proof corpus is needed by this checker.

The mathematical use is a rigorously excluded receiving-and-motion
domain for a future global cover. The certificate establishes local
rigidity over a generic two-dimensional receiving patch and a continuous
parameter box. It supplies neither a passage nor a global non-Rupert
theorem. See the proof for complementary prior contact/Cayley work and
current primary status; generic stress techniques are not claimed as new.
