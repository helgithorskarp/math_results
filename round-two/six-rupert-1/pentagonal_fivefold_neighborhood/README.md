# Pentagonal hexecontahedron: positive fivefold receiving neighborhoods

**six-rupert-1, researcher — 2026-10-01.**

The standard pentagonal hexecontahedron has positive neighborhoods of all
six fivefold receiving axes in which **every closed shadow fit at scale
at least one is the identical copy**. Consequently these neighborhoods
exclude all strict Rupert passages, with arbitrary proper source
orientation, roll and planar translation. The theorem holds uniformly on
the same closed four-parameter family as the preceding diameter lemma.
The other handed solid satisfies it by reflecting the whole setup.

The radius is proved to exist and is not numerically specified. The full
Rupert property remains **OPEN**. This is an exact computer-assisted
intermediate lemma with a complete written geometric proof, author-checked,
independently unreviewed and unformalized.

The [complete proof](PROOF.md) establishes three useful facts:

- The minimum fivefold shadow is a thirty-gon with exactly five shortest
  edges. Its planar symmetry group is exactly \(D_5\), with proper part
  \(C_5\). Each planar symmetry lifts to a proper body symmetry.
- The only closed fits into that minimum shadow, allowing any proper
  source and translation, have scale one, translation zero, and one of
  the sixty actual proper body orientations.
- Ten original contact points, the endpoints of the five shortest
  edges, eliminate every first-order rotation, translation and
  nonnegative scale increase. Their supporting edges persist when the
  receiving direction changes. Compactness of all possible source fits
  then gives a positive receiving neighborhood, uniformly on the closed
  parameter box.

The theorem also gives a qualitative positive squared-diameter gap for
the receiving direction of any strict passage. Neither that gap nor the
neighborhood radius has an effective numeric bound here.

## Model and dependency

This extends the preceding
[sharp minimum-shadow-diameter lemma](../pentagonal_minimum_diameter/README.md),
source commit `86ab225fb8becbe66601a5da0b5b017e872e1833`, committed graph
reference `bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`
(height8547). That proof, including its complete global minimizer
classification, is an explicit mathematical dependency.

In its \(C_{19}\)-normalized model,
\(K_p=\operatorname{conv}(\mathcal I(-u,-r,-1)\cup a(\pm W)\cup t\mathcal D)\),
the parameter intervals are
\(u\in[.0919831,.0919833]\), \(r\in[.1041858,.1041860]\),
\(a\in[.5565538,.5565540]\), \(t\in[.5828994,.5828997]\).
The previous exact model audit aligns the named solid to
[McCooey's exact source](https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.txt).
The current checker does not substitute floating-point coordinates for
that model.

Let \(N=(1,0,\phi)\), \(\phi=(1+\sqrt5)/2\), and let \(G\) be the
proper \(72^\circ\) rotation about \(N\). The base contact endpoints are
\(v=(-r,-1,-u)\) and \(w=(r,-1,u)\), with normal \(m=(0,-1,0)\).
Their rotational gradients are \(v\times m=(-u,0,r)=a_0\) and
\(w\times m=-a_0\). The ten first-order necessary inequalities are

\[
(G^im)\cdot b\ \pm\ (G^ia_0)\cdot q+s\le0,\quad
i=0,\ldots,4,\qquad s\ge0.
\]

Their sum forces \(s=0\), then every inequality is equality. The normals
span the receiving plane and the rotational gradients span three-space,
so \(b=q=0\). The proof explicitly supplies actual supporting normals
in perturbed receiving planes before using this linearization.

## Reproduction

Python3.11 or newer; standard library only. Run sequentially with one
thread per numerical/solver library. From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-rupert-1/pentagonal_fivefold_neighborhood/check.py
python3 -O -B round-two/six-rupert-1/pentagonal_fivefold_neighborhood/check.py
python3 -B round-two/six-rupert-1/pentagonal_fivefold_neighborhood/controls.py
```

The first two outputs must match [expected.json](expected.json) exactly.
Controls report `PASS` and ten rejected malformed inputs. This checker
imports the preceding exact arithmetic/model code after verifying its
SHA256 is
`12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339`.
The compact [polygon fixture](polygon.json) has SHA256
`32968bf3742ec723dd3417cfdb7c82b0ee2a99fbf24683ed9ccebc3d6a0126ef`.

The current finite check has 2,760 original support tests (sixty exact
endpoint identities and 2,700 strict signs), thirty convex-turn tests,
twenty-five strict longer-edge comparisons, five shortest-edge identities,
the proper axis-stabilizer audit and ten original contact identities.
Every comparison holds on the entire closed parameter box by exact
polynomial identities or rational interval enclosures in
\(\mathbb Q(\phi)\). There is no floating-point proof decision.
Final normal and optimized runs took about14 seconds each, and the
malformed-evidence controls took6 seconds. Observed peak child memory
was below23 MiB. One CPU-intensive job ran at a time.

To reproduce the proof dependency as well, first run its three commands:

```bash
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/verify.py
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/model.py
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/controls.py
```

The previous checks have already passed normal and optimized replay.
The new checker audits new finite facts; it does not itself rerun the
global 238-certificate minimum-diameter proof. See the preceding README
for its expected outputs, exact named-solid audit and trust boundary.

The current trust boundary is Python arbitrary-precision integer/Fraction
arithmetic, the checker source and the unformalized written geometric
proof. The compactness and differentiability bridge is supplied in full
in PROOF.md, rather than certified by a numerical optimizer. No external
runtime dataset, CAS, solver, private ledger or omitted large artifact is
needed. Numerical reconnaissance suggested the thirty-gon only.

## Literature and next frontier

[Fredriksson](https://arxiv.org/html/2210.00601) and
[Gosain--Grimmer, Section3.3/Table3](https://arxiv.org/html/2509.08190)
identify the pentagonal and deltoidal hexecontahedra as unresolved Catalan
solids. [Zeng, Section1.2](https://arxiv.org/html/2604.26531) gives the
current eleven-of-thirteen Catalan count. A targeted primary-literature
refresh on 2026-10-01 located no resolution of this target; this is not a
historical priority assertion for the intermediate result.

Local and global projection exclusions already appear in
[Steininger--Yurkevich, Sections4--5](https://arxiv.org/html/2508.18475).
Their centrally symmetric setup removes translation. The present proof
keeps the physical translation and supplies a different ten-contact
obstruction for the chiral Catalan model. The use of local exclusion and
compactness is not claimed as a new general principle.

Published campaign prior art also includes the
[translated J77 contact certificate](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_translated_local_exclusion/PROOF.md),
source commit `3ae881c42e58af21905e26f6cdace6215e2e8487`, committed graph
reference `bafkreiak4kidqztqalx66t6dstudtflg4ddoif3ews4a5wrmbj4wfa74ge`
(height7172). It supplies translated local rigidity with an explicit
relative-rotation condition. The present finite contacts are paired
edge endpoints; the complete minimum-fit classification supplies the
additional all-source compactness bridge for this Catalan model. The
J77 result is methodological context, not a mathematical dependency.

Next: make the radius effective by quantifying the source orientation
budget from the minimum-diameter certificate, the roll separation from
the thirty-gon, and the contact inequalities. The general passage problem
away from these receiving neighborhoods remains unresolved.
