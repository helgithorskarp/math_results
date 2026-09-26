# Gaussian majorisation on extreme maps and rigid folded meshes

The unrestricted dimension-three conjecture is equivalent to testing
positive vertex laws on finite tetrahedral meshes of convex polytopes,
under maps that are isometries on each tetrahedron. The resulting maps
are extreme in their anchored finite Lipschitz balls, and their tight
frameworks are infinitesimally rigid at both endpoints.

This is a **reduction using classical extension theorems**, with an author
proof awaiting independent review. It does not settle the Gaussian
conjecture or prove a new Kneser--Poulsen case.

[PROOF.md](PROOF.md) gives the full quantifiers and a quantitative transfer:
an original negative hinge gap `-delta` survives auxiliary mass
`epsilon < delta/(1+delta)`. The source convex hull can remain fixed.
A uniform-mass version also holds after adding nearby sites. For any
fixed mesh, compatible maps reduce to finitely many reflection choices;
no bound on the number or complexity of the required meshes is proved.

The known simplex-flap example supplies an essential control: its tight
graph is connected and has full rigidity rank at both endpoints, yet the
classical nonliftability theorem rules out a contracting motion in `R^5`.
Extremality and rigidity cannot supply that motion by themselves.

Reproduce the small exact controls from the repository root:

```sh
python3 probability/gaussian_majorisation_extremal_maps/verify.py --check
python3 -O probability/gaussian_majorisation_extremal_maps/verify.py --check
cd probability/gaussian_majorisation_extremal_maps
sha256sum -c SHA256SUMS
```

Expected output in each Python mode:

```text
PASS: rigid flap and all eight mesh fold choices
```

Python 3.11 or later, standard library only. The largest rank calculation
is a `78 x 48` rational matrix; no heavy search, external solver, numerical
quadrature, or general Brehm-extension implementation is used. The exact
checks verify 120 flap pair inequalities, ranks 42 at both endpoints,
and a four-tetrahedron consistency control with four accepted and four
rejected fold assignments. [EXPECTED.json](EXPECTED.json) records every
small control, and [SOURCES.md](SOURCES.md) identifies prior work and
the evidence boundary.
