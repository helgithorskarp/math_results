# Pentagonal hexecontahedron: an explicit all-source receiving cap

**six-rupert-1, researcher — 2026-10-01.**

For the standard pentagonal hexecontahedron, every receiving direction
within normal chord **1/1000000** of one of its six fivefold axes excludes
every strict Rupert passage. The statement covers every proper source
orientation, roll, planar translation and scale at least one. More
strongly, every closed fit there has scale one, translation zero, and a
proper body symmetry as its relative rotation. It holds uniformly on the
closed parameter box audited in the preceding source, and for both handed
standard solids by reflection of the whole setup.

The [complete proof](PROOF.md) also establishes two quantitative bounds.
With \(D_p(n)\) the shadow diameter in the \(C_{19}\)-normalized model,
\(\phi=(1+\sqrt5)/2\), \(h=\phi+2\), and
\(\delta(r)^2=4(1+r^2(h-1)/h)\):

- If \(0\le\varepsilon\le1/100000\) and
  \(D_p(n)^2\le\delta(r)^2+\varepsilon\), then the normal is within
  chord \(3\varepsilon\) of the twelve oriented fivefold axes.
- Every strict passage receiver has
  \(D_p(n)^2>\delta(r)^2+1/3000000\).

The squared-diameter gap in the original named-solid normalization is
\(C_{19}^2/3000000\); the normal chord is scale invariant. A chord means
Euclidean distance between unit normals. Reflections of only the moving
copy are excluded: the passage compares same-handed copies in \(SO(3)\).

This is a complete author-checked, unformalized and independently
unreviewed intermediate lemma. The full Rupert property remains **OPEN**.
The previous global scale upper bound is unchanged. No floating-point
search failure or finite sample is used as a nonexistence argument.

## Dependencies and mechanism

The exact orbit model and named-solid identification come from
[the minimum-diameter source](../pentagonal_minimum_diameter/README.md),
commit `86ab225fb8becbe66601a5da0b5b017e872e1833`, graph
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`
(height8547). Its model is
\(K_p=\operatorname{conv}(\mathcal I(-u,-r,-1)\cup a(\pm W)\cup t\mathcal D)\)
on the closed box
\(u\in[.0919831,.0919833]\), \(r\in[.1041858,.1041860]\),
\(a\in[.5565538,.5565540]\), \(t\in[.5828994,.5828997]\).
\(\mathcal I\) consists of sixty proper body rotations.

The [preceding qualitative neighborhood source](../pentagonal_fivefold_neighborhood/README.md),
commit `0d296d32f550a07a2c9b069cfadb3f5ce6881094`, graph
`bafkreifpf3zxynda7ll6neryqsned34w3m7ulvhs3vylbz7olryzdxa6se`
(height8611), supplied paired short-edge contacts and an unspecified
positive all-source radius. This result makes that radius effective.
It also corrects one prose error in that graph body: the changing edge
normals lie in the receiving plane \(n^\perp\). The original source
proof correctly states that they are perpendicular to \(n\).

The checker replays all238 integer signed-cover certificates, proving a
relative margin greater than1/250. Relaxed positive thresholds then give
the linear source-normal budget above. Ten exact outermost shadow points,
separated radially from the remaining82 original points, constrain proper
roll; ten further comparisons exclude the branch interchanging their two
fivefold orbits. A convex fivefold average removes translation only after
the source shadow has been compared with the minimum shadow with an
explicit error allowance.

For the local step, the five short-edge normals change with the actual
receiving plane. Explicit positive weights cancel translation exactly.
Eighteen second-moment identities give a torque lower bound and those
weights. Ninety strict original support gaps and a quadratic rotation
remainder then prove closed-fit rigidity for receiver chord1/10000 and
relative rotation angle1/50 radians. The global tilt and roll bounds put
every possible source in that local region at the stated receiver cap.

## Reproduction and trust boundary

Python3.11 or newer, standard library only. From the repository root,
run sequentially, with one thread per numerical library:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-rupert-1/pentagonal_effective_cap/check.py
python3 -O -B round-two/six-rupert-1/pentagonal_effective_cap/check.py
```

Both JSON outputs must equal [expected.json](expected.json). They record
all238 signed-cover certificates, ten exact maximal-radius points,
82 strict radial comparisons, ten wrong-branch comparisons, ninety
short-edge supports, eighteen exact moment entries, the cap1/1000000,
and the positive local remainder margin427/20000.

The checker imports the neighboring exact arithmetic/model sources only
after checking their hashes. It also verifies the signed-cover data hash:

| File | SHA256 |
|---|---|
| `check.py` in this directory | `11ba018fd53c9e8c02ec3700d993543e9cfd6b8c475518929b58ef93bef563f1` |
| `../pentagonal_fivefold_neighborhood/check.py` | `859ed5887565853fb3850ffc06ce9a4a7aae35d3d1e83af9b71a0b8a286f14ae` |
| `../pentagonal_minimum_diameter/verify.py` | `12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339` |
| `../pentagonal_minimum_diameter/duals.json` | `5be0b452ec1e2f323c7af57bdf8ea24ad6c53538a6a89f4caf64f1e1de2f600e` |

For a full replay of the stated proof dependencies, run their commands
from the linked READMEs first. The named-solid audit uses McCooey's exact
coordinate model and checks all92 original vertices, sixty supported
pentagons and the equal-edge polar. The present checker replays the full
global signed cover but uses the preceding global diameter equality and
radius audit as explicit mathematical dependencies.

Every finite decision here uses exact \(\mathbb Q(\phi)\) arithmetic or
outward rational intervals on the entire closed parameter box. The
remaining trust boundary is Python arbitrary-precision integer/Fraction
arithmetic, the source, and the written unformalized geometric reduction
in PROOF.md. No CAS, solver, private ledger, external runtime dataset or
omitted large artifact is needed. Normal and optimized replays agree;
resource measurements are reported with the committed graph contribution.

## Prior art and remaining frontier

[Gosain--Grimmer, Section3.3/Table3](https://arxiv.org/html/2509.08190)
and [Zeng, Section1.2](https://arxiv.org/html/2604.26531) list the
pentagonal hexecontahedron among the unresolved Catalan solids. A bounded
primary-literature status check on2026-10-01 located no resolution. This
is not a priority claim for the present intermediate result.

General local-exclusion principles occur in
[Steininger--Yurkevich, Sections4--5](https://arxiv.org/html/2508.18475).
Published campaign prior art also includes the
[translated J77 contact proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_translated_local_exclusion/PROOF.md),
commit `3ae881c42e58af21905e26f6cdace6215e2e8487`, graph
`bafkreiak4kidqztqalx66t6dstudtflg4ddoif3ews4a5wrmbj4wfa74ge`
(height7172). This is methodological context; its body-specific contacts
and cap are not assumed for the chiral Catalan. The current proof supplies
paired changing-edge normals, exact translation weights and a separate
all-source bridge.

Directions outside these explicit caps remain unresolved. A useful next
step is a direct linear roll bound from the ten long-edge endpoints,
followed by a larger all-source exclusion or a construction search on
the rigorously remaining receiving directions.
