# A translated local rigidity certificate for Johnson solid J77

Author: **six-rupert-2**, role **researcher**, 2026-09-29.

Let $P$ be the unit-edge paragyrate diminished rhombicosidodecahedron
(Johnson solid J77), with the exact vertex set in `model.py`. Set

$$
D=(0,-1,(7+\sqrt5)/2),\qquad n_0=D/\|D\|.
$$

Let $G$ be the proper fivefold symmetry about

$$
A=(0,(1+\sqrt5)/2,1)
$$

given by Rodrigues' formula with

$$
\cos(2\pi/5)=(\sqrt5-1)/4,
\qquad \sin(2\pi/5)/\|A\|=1/2.
$$

**J77 local rigidity theorem.** Let $B\in\mathbb R^{2\times3}$ have
orthonormal rows, let $n$ be either unit normal to their plane, and let

$$
\min_{0\le j<5,\ \sigma\in\{-1,1\}}
\|n-\sigma G^j n_0\|\le1/200.
$$

Let $Q\in\mathrm{SO}(3)$ have rotation angle at most $3/20$ radians.
For any $\lambda\ge1$ and any $b\in\mathbb R^2$,

$$
\lambda BQP+b\subseteq BP
\quad\Longrightarrow\quad
\lambda=1,\quad Q=I,\quad b=0.                 \tag{1}
$$

In particular, this region admits no strict Rupert passage, at unit or larger
scale, with any planar translation. The angle bound is about $8.59^\circ$;
the receiver cap has unit-normal chord radius $1/200$. There are five
unoriented receiver caps. These are restrictions on the relative full rotation
of the two projection frames, including their in-plane alignment. A bound only
on the distance between the two projection axes does not meet the hypotheses.

This is a local result. J77's global Rupert question remains unresolved.

## 1. Projection frames and the role of translation

For each orthonormal-row frame $B_i$, append the cross product of its two
rows to obtain $S_i\in\mathrm{SO}(3)$. Then

$$
Q=S_2^tS_1,\qquad B_1=B_2Q.
$$

Any additional in-plane rotation can first be included in $B_1$. Thus (1)
refers to the standard geometric projection-containment formulation. The
relative rotation is this $Q$, measured after fixing the frames.

J77 is not centrally symmetric: only 50 of its 55 vertices have antipodes in
the vertex set. Accordingly, we retain translations throughout the proof.
They disappear from specific weighted support inequalities because the
certificate makes the corresponding normal vectors sum to zero. No midpoint
or central-symmetry argument is applied to J77.

## 2. A general criterion that retains arbitrary translations

Let $K=\operatorname{conv}(V)\subset\mathbb R^3$ be a full-dimensional
convex polytope with $0\in\operatorname{int}K$ and $\|v\|\le R$ for
all $v\in V$. Fix a unit receiver normal $n_0$. Choose finitely many
vertices $v_i$ and probe normals $m_i\perp n_0$, such that

$$
m_i\cdot(v_i-w)>g>0\quad(w\in V\setminus\{v_i\}),
\qquad R\|m_i\|<M.                          \tag{2}
$$

For every Cartesian coordinate $k\in\{1,2,3\}$ and sign

$s\in\{-1,1\}$, suppose there are nonnegative weights $a_i^{k,s}$
with

$$
\sum_i a_i^{k,s}(v_i\times m_i)=s e_k,
\qquad \sum_i a_i^{k,s}m_i=0,
\qquad \sum_i a_i^{k,s}<C.                  \tag{3}
$$

Zero coefficients mean that the corresponding probe is unused. Let positive
constants $\delta,\theta_0$ satisfy

$$
2M\delta<g,\qquad
CM(\delta+\theta_0/2)<1/\sqrt3.             \tag{4}
$$

If $B$ is an orthonormal-row receiver frame with normal $n$ satisfying
$\|n-n_0\|\le\delta$, and $Q$ is a proper rotation of angle
$\theta\le\theta_0$, then

$$
\lambda BQK+b\subseteq BK,\quad\lambda\ge1
\quad\Longrightarrow\quad\lambda=1,\ Q=I,\ b=0.       \tag{5}
$$

**Proof.** Project each probe into the actual receiver plane:

$$
m_i'=m_i-(m_i\cdot n)n.
$$

Since $m_i\perp n_0$,

$$
\|m_i'-m_i\|\le\|m_i\|\delta,\qquad
\|m_i'\|\le\|m_i\|.
$$

Therefore

$$
m_i'\cdot(v_i-w)>g-2M\delta>0.             \tag{6}
$$

Each $v_i$ remains the unique supporting vertex in direction $m_i'$.
The same weights in (3) cancel translations after transport:

$$
\sum_i a_i^{k,s}m_i'
 = (I-nn^t)\sum_i a_i^{k,s}m_i=0.          \tag{7}
$$

First consider $\lambda=1$. Lift $b$ into the receiver plane as
$t=B^t b$, so $Bt=b$. Closed containment would imply

$$
m_i'\cdot(Qv_i-v_i+t)\le0                 \tag{8}
$$

for every probe. Indeed, $m_i'\perp n$, and its outer support value is
$m_i'\cdot v_i$ by (6).

For $\theta>0$, write $Q=\exp(\theta[\omega]_\times)$ with
$\|\omega\|=1$. The elementary orthogonal-exponential remainder bound is

$$
\|Q-I-\theta[\omega]_\times\|_{\rm op}\le\theta^2/2.   \tag{9}
$$

To see (9), integrate the second derivative of the exponential twice.
Its operator norm is at most one, because the exponential is orthogonal and
$\|[\omega]_\times\|_{\rm op}=1$.

Choose $k,s$ so that $s\omega_k=|\omega_k|\ge1/\sqrt3$, and use
the weights from (3). The change in their torque sum under probe transport
satisfies

$$
\left\|\sum_i a_i^{k,s}(v_i\times m_i')-s e_k\right\|
 <CM\delta.                               \tag{10}
$$

Use (7), (9), and (10) in the weighted sum of the left sides of (8). It is
strictly greater than

$$
\theta\bigl(|\omega_k|-CM\delta-CM\theta/2\bigr)
\ge\theta\bigl(1/\sqrt3-CM(\delta+\theta_0/2)\bigr)>0.
$$

The same sum must be nonpositive by (8), a contradiction. Thus a closed
unit-scale inclusion forces $\theta=0$, hence $Q=I$. A bounded set
cannot contain its nonzero translate: in direction $b$, the support value
of $BK+b$ exceeds that of $BK$ by $\|b\|^2$. Consequently $b=0$.

For $\lambda\ge1$, rescale a purported inclusion by $1/\lambda$:

$$
BQK+b/\lambda\subseteq (1/\lambda)BK\subseteq BK,
$$

where the second inclusion uses $0\in K$ and convexity. The unit-scale
case forces $Q=I$ and $b=0$. Since $BK$ has positive diameter, the
original inclusion $\lambda BK\subseteq BK$ forces $\lambda=1$.
This proves $5). The proof also applies with base normal (-n_0$, since
the same probes are perpendicular to that normal. QED.

The criterion requires no symmetry of $K$. Its finite identities live in
the five-dimensional space of three rotational and two planar translational
coordinates. The checker uses all six coordinates $(v_i\times m_i,m_i)$
to verify translation cancellation directly, without eliminating one normal
coordinate from the mathematical claim.

## 3. Exact J77 support probes

The vertex numbering in `model.py` is David McCooey's standard coordinate
order. An independent exact construction removes the two opposite pentagonal
cupolas of a rhombicosidodecahedron and restores one after a $36^\circ$
gyration. It reproduces precisely the 55 fixture vertices. The ungyrated
50-vertex core is centrally symmetric; three independent pairs, indexed

$8,29,23$, certify $0\in\operatorname{int}P$. All 55 vertices satisfy

$$
\|v\|^2=R^2=(11+4\sqrt5)/4.                \tag{11}
$$

Use this cyclic list of 17 support-vertex indices:

```text
15, 48, 32, 54, 24, 51, 30, 44, 11, 8, 41, 29, 16, 19, 31, 45, 12
```

For consecutive indices $a,b$, form the exact normalized outward normal

$$
\ell_{a,b}=
\frac{(v_b-v_a)\times D}
 {((v_b-v_a)\times D)\cdot v_a}.             \tag{12}
$$

The checker verifies the positive denominator, perpendicularity to $D$,
both endpoint support values equal to one, and

$\ell_{a,b}\cdot w\le1$ for every one of the 55 vertices.
For the vertex at position $j$ in the cycle, let

$\ell^-_j$ and $\ell^+_j$ be its incoming and outgoing normals.
Define two probes at that vertex:

$$
m_{2j}=\tfrac34\ell^-_j+\tfrac14\ell^+_j,
\qquad
m_{2j+1}=\tfrac14\ell^-_j+\tfrac34\ell^+_j. \tag{13}
$$

This specifies 34 probes in $\mathbb Q(\sqrt5)^3$. Their finite supporting
and norm inequalities are checked against every vertex. In particular,

$$
\min_{i,\,w\ne v_i}m_i\cdot(v_i-w)
  =(11-4\sqrt5)/164>1/80,                  \tag{14}
$$

and the 34 exact comparisons prove

$$
R^2\|m_i\|^2<(9/8)^2.                    \tag{15}
$$

Thus $2) holds with (g=1/80$ and $M=9/8$. There are $34\times54=1836$
unique-support gap comparisons. Every normalized probe has $m_i\cdot v_i=1$;
in a nearby receiver plane its support value remains positive, since the
change is less than $M\delta<1$.

## 4. Six exact positive combinations

For a probe define

$$
h_i=(v_i\times m_i,m_i)\in\mathbb Q(\sqrt5)^6.
$$

The table specifies the nonzero coefficients of each combination by listing
the probe columns used. All unlisted coefficients are zero. Solve

$\sum_i a_i h_i=(s e_k,0,0,0)$ over $\mathbb Q(\sqrt5)$.
The columns listed in each row are independent, and the exact solution is
unique. `exact_solve` reconstructs it and independently verifies all six
original coordinates.

| Coordinate and sign | Probe columns | Coefficient sum, approximate |
| --- | --- | --- |
| $+e_1$ | 5, 12, 25, 26 | 3.479911 |
| $-e_1$ | 7, 10, 21, 30 | 5.880379 |
| $+e_2$ | 2, 13, 18, 19, 27 | 6.006534 |
| $-e_2$ | 4, 15, 24, 32, 33 | 6.006534 |
| $+e_3$ | 1, 7, 9, 19, 23 | 5.758265 |
| $-e_3$ | 8, 10, 16, 28, 32 | 5.758265 |

Every reconstructed coefficient is strictly positive, and every sum is
strictly less than $C=61/10$, by exact field comparisons. The decimal
column is explanatory; it is not used in verification. The canonical encoding
of the complete exact coefficient solutions has a SHA256 reported by the
checker and `expected.json`.

Set $\delta=1/200$ and $\theta_0=3/20$. The remaining scalar inequalities
are rational:

$$
2M\delta=9/800<1/80=g,
$$

$$
CM(\delta+\theta_0/2)=549/1000,
\qquad 3(549/1000)^2=904203/1000000<1.      \tag{16}
$$

The latter proves the second condition in (4). The transported unique-support
gap is greater than $1/800$. Sections 2--4 prove (1) in the cap about

$\pm n_0$.

The exact checker also verifies $G\in\mathrm{SO}(3)$, $GP=P$, and that
the five directions $G^jD$ are distinct even up to sign. Conjugating the
relative rotation by $G^j$ preserves its angle; changing receiver frame by
that same symmetry preserves projection containment. This transports (1) to
the five unoriented caps in the theorem.

## 5. Reproduction, provenance, and scope

From the repository root, using Python 3.11+ and no external packages:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B convex_geometry/rupert_j77_translated_local_exclusion/verify.py --self-test
```

The output equals `expected.json`. The finite proof checks use rational
arithmetic in $\mathbb Q(\sqrt5)$, with an independent rational enclosure
audit for every strict support-gap, probe-norm and coefficient comparison. The audit
includes positive and negative small Pell conjugates. Reversed probes,
missing probes, omitted signed targets, and an inconsistent positive basis
are rejected. The mathematical criterion is a written analytic proof, not
a proof-assistant formalization or an independent review.

The exploratory calculation used NumPy 2.2.6, SciPy 1.16.2 and HiGHS 1.8.0 through
`linprog(method='highs-ds', options={'threads': 1, 'time_limit': 5})` solely
to select column indices for six linear programs. Each discovery program
minimized the sum of nonnegative coefficients with the five-coordinate
gradient equal to a signed rotational coordinate vector and zero planar
translation coordinates. The published checker reconstructs every coefficient
exactly from (11)--(13) and the small table above. Solver status, tolerances,
a floating hull, and numerical coefficients are not proof inputs. No external
instance, omitted large certificate, or exhaustive numerical search is needed.

The exact named model and base direction come from the earlier
[J77 diameter and passage-scale certificate](https://github.com/helgithorskarp/math_results/tree/main/convex_geometry/rupert_j77_projection_diameter),
by six-rupert-2. The exact receiver $n_0$ already admits no strict passage
by that minimum-diameter theorem. The new statement covers an open set of
receiver directions, bounds a full relative-rotation neighborhood, and retains
all translations by exact weighted cancellation. It does not improve the
earlier global Nieuwland bound.

Complementary team dependencies, both read before this derivation:

- **six-rupert-1**, researcher: [deltoidal hexecontahedron contact certificates](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/proof.md).
  These give a positive-combination rotation obstruction at a fixed symmetric
  receiver, with the same quadratic rotation remainder.
- **six-rupert-3**, researcher: [varying-receiver support-probe theorem for the rhombicosidodecahedron](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md).
  Its transported unique-support probes supply the varying-plane mechanism.
  The present proof adds exact normal-vector cancellation, valid for an
  asymmetric body, in place of its central-symmetry translation reduction.

A subsequent [all fixed receiver directions certificate for the deltoidal hexecontahedron](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md)
by six-rupert-1 was read during the final graph refresh. Its chamber subdivision
and exact contact-minor polynomials suggest a route to broader J77 coverage.
That all-direction result uses central symmetry and is not a hypothesis or
conclusion of the present translated J77 theorem.

Primary context checked on 2026-09-29:

- [Fredriksson, *Optimizing for the Rupert property*](https://arxiv.org/html/2210.00601).
- [Gosain--Grimmer, *Some New Insights from Highly Optimized Polyhedral Passages*, Table 4](https://arxiv.org/html/2509.08190): J72--J75 and J77 remain without passages in the reported search.
- [Zeng, 2026](https://arxiv.org/html/2604.26531): 87 of 92 Johnson solids are known Rupert; the rhombicosidodecahedron conjecture remains open.
- [Steininger--Yurkevich, *A convex polyhedron without Rupert's property*, Sections 5, 8, 9](https://arxiv.org/html/2508.18475): local and global properties differ, and central symmetry is explicitly used to remove translations in their setup.
- [Scott, *Two Sufficient Conditions for a Polyhedron to be (Locally) Rupert*](https://arxiv.org/html/2208.12912): construction criteria and the distinction between local and reverse local Rupertness.
- [McCooey's standard J77 coordinates](https://dmccooey.com/polyhedra/ParagyrateDiminishedRhombicosidodecahedron.txt), independently identified by the cupola construction.

No priority claim is made for the basic support-gradient or positive-cone
mechanism. The searched primary papers do not supply this explicit translated
J77 neighborhood certificate. The present region leaves other receiver
directions and larger relative rotations untreated; a nonlocal passage can
still exist.
