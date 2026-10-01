# J74: an exact conditional motion exclusion on a nonlocal receiving arc

**six-rupert-2, researcher; 2026-10-01.** J74's full Rupert property remains
**OPEN**. This is an author-checked, unformalized, independently unreviewed
intermediate result. The [written proof](PROOF.md) includes the bridge
from exact finite data to every real point of the specified arc.

For `u(t)=m+t*d`, `3/5<=t<=7/10`, with literal `m,d` in the proof,
every original scale>=1 closed fit whose proper motion is within relative
Cayley radius **1/6000** of one of

```
I, diag(-1,-1,1), M_u diag(-1,1,1), M_u diag(1,-1,1)
```

is exactly that reference motion, with scale1 and **actual translation0**.
Each center gives the identical original shadow. The receiver arc is
more than1/3 in projective unit-normal chord from all six minimum axes.
The motion radius is conditional on the source and receiver. Receiving
directions off the arc and other source motions are open.

The certificate contains36 affine positive endpoint-contact weights.
They balance physical force and torque identically in the parameter;
a5x5 minor and its Bernstein cofactor bounds give inverse norm<=6.
The exact Cayley remainder contracts by243/640. All receiver polygons
are complete original18-corner cycles, checked against all60 vertices.
The four centers use full-body symmetries, freshly checked on all60 originals.
No prototype reduction, centering assumption or source-area localizer is used.

From the repository root, with Python3.11+ and its standard library:

```sh
python3 -B round-two/six-rupert-2/nonlocal_arc_wrench/check.py
python3 -O -B round-two/six-rupert-2/nonlocal_arc_wrench/check.py
```

Both commands require the whole entrywise [expected record](expected.json)
to match. They check2160 original receiver supports,576 strict polygon
gates,8640 reference-source supports,240 full-body symmetry matches and
15 balanced polynomial coefficients. Four damaged controls reject a
wrong stress, an omitted actual receiving corner, a singular row choice,
and an unsafe motion radius. See [validation](VALIDATION.md).

Certificate SHA256:
`a2427bb6e1fdaece00a960bdaf755b4f6a456935600dfdfd0eecb7d1d99fdbca`.
The parent input pins and verified source commit are in
[DEPENDENCIES.json](DEPENDENCIES.json). The checker uses no NumPy, SciPy,
LP solver, floating approximation or discovery script. Numerical searches
helped choose this arc but are not theorem inputs and give no exclusion.

The generic equilibrium, Cayley and Bernstein mechanisms are existing
mathematics; the claim here is the explicit original-J74 receiving region
and motion exclusion. The earlier
[all-source minimum caps](../quantitative_minimum_caps/PROOF.md) address
a different receiving domain. No verdict about that extension is transferred.
