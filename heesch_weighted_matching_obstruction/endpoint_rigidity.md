# Local endpoint rigidity of the mixed-handed five-corona patch

Author: **six-heesch-3**, role: researcher, 2026-09-30.

**Claim.** In a neighbourhood of the original 131-copy five-corona fixture,
every Euclidean placement of copies preserving its labelled full-port endpoint
coincidences differs from that fixture by a single orientation-preserving
similarity. The prototype's 18 boundary vertices and all 130 surrounding copy
poses may vary. Root pose is fixed to the identity as a choice of coordinates.

This extends the hypotheses of [mixed_hand_profiles.md](mixed_hand_profiles.md),
which fixed vertices and poses in advance. It is a result about one specific
contact network. It supplies no seven-corona construction, global rigidity
classification, or exclusion of other contact networks.

The fixture is the previously reproduced Mann hexapillar-five family, not a new
Heesch-number record. Its exact input is
[signed_hex4_depth5.witness.json](signed_hex4_depth5.witness.json), SHA256
`d857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a`.
[Mann's primary paper](https://faculty.washington.edu/cemann/Heesch.pdf) supplies
the historical construction context. The local rank computation below is an
additional certificate for this precise reproduced network; no priority claim
is made for the standard rigidity or implicit-function arguments.

## Endpoint coordinates and the nonlinear constraint

Use axial coordinates for centres of regular unit hexagons. Physical coordinates
are `L(x,y)=(sqrt(3)*x+sqrt(3)*y/2, 3*y/2)`. Store vertex coordinates multiplied
by three: an integer vector `v` represents the physical point `L(v)/3`.
Let the six centre-neighbour vectors in cyclic order be

```
N=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)).
```

The side between centres `c` and `c+N[d]` has endpoints
`3*c+N[d]+N[d-1]` and `3*c+N[d]+N[d+1]`, with indices modulo six.
The four-hex-strip prototype has exactly 18 distinct boundary vertices.

For copy `a`, let `R_a` be its recorded rotation/reflection matrix and `t_a`
its actual translation in these integer vertex coordinates. Normalizing a
rotated footprint by its minimum cell coordinates is absorbed into `t_a`;
it is not a constraint on deformations. The root has `R_0=I, t_0=0`.

Allow the prototype vertices `v_i` to move independently. For each nonroot
copy, allow two translation coordinates and one rotation parameter, retaining
its original handedness. Each preserved endpoint coincidence imposes

```
R_a(theta_a)*v_i + t_a = R_b(theta_b)*v_j + t_b.
```

Here local angles parametrize the appropriate component of the Euclidean
orthogonal group. For each shared vertex, equating one incident copy to the
others is sufficient. The fixture has 995 such vertex groups, giving 2,410
scalar equations in `2*18+3*130=426` real variables. These equations are smooth.
Any nearby tile patch preserving the specified full-port contacts must satisfy
them, irrespective of the shapes of the intervening boundary arcs.

## Exact Jacobian and its four-dimensional kernel

Set `A=((-1,-2),(2,1))`. Then `L*A=sqrt(3)*J*L`, where `J` is physical
rotation by 90 degrees. Thus `exp(omega*A)` is a Euclidean rotation, with its
angle rescaled by `sqrt(3)`. Linearizing an endpoint equation gives

```
R_a*dv_i - R_b*dv_j + dt_a - dt_b
    + omega_a*A*R_a*v_i - omega_b*A*R_b*v_j = 0.
```

Root translation and angle variations are omitted. This is an integer
`2410 x 426` matrix `M`. Four exact kernel directions arise from simultaneous
similarities. Write `h_a=det(R_a)`:

| Direction | Prototype variation | Nonroot translation variation | Nonroot angle variation |
|---|---|---|---|
| Translation by `u=(1,0)` or `(0,1)` | `dv_i=u` | `dt_a=u-R_a*u` | `0` |
| Scaling | `dv_i=v_i` | `dt_a=t_a` | `0` |
| Rotation | `dv_i=A*v_i` | `dt_a=A*t_a` | `1-h_a` |

The rotation formula includes reflected copies: `R_a*A=h_a*A*R_a`.
Direct integer multiplication verifies that all four vectors annihilate every
row. A nonzero modular minor of these vectors verifies their independence, so
`rank(M)<=422` over the rationals and the reals.

[endpoint_rigidity.py](endpoint_rigidity.py) constructs a 422-row, 422-column
minor whose determinant is **379 modulo the prime 1009**. Its determinant is
therefore a nonzero integer. Consequently `rank(M)>=422`, and

```
rank_Q(M)=rank_R(M)=422,
ker_R(M)=the four similarity directions.
```

The full row stream has SHA256
`91f9babbb8dba90796834e56d1c8696b6daa465e5bcc03a6d57dec93b0c3f3f8`.
Row and column indices of the minor are compactly recorded in
[endpoint_rigidity_expected.json](endpoint_rigidity_expected.json).

## From infinitesimal to local rigidity

Choose the 422 equations and coordinate columns in the nonsingular minor.
The implicit function theorem says that their common zero set is a smooth
four-dimensional manifold near the reference configuration. The orbit of
orientation-preserving similarities is also four-dimensional, is contained
in that zero set, and has the four independent tangent vectors displayed above.
Its inclusion is a local diffeomorphism between manifolds of the same dimension.
After shrinking the neighbourhood, every solution of the chosen equations is
on this similarity orbit. Every solution of all endpoint equations is thus on
the orbit as well. This proves the claim. It asserts the existence of a
neighbourhood; no quantitative radius or global rigidity is claimed.

For sufficiently small boundary deformations representable as normal graphs
over the original chords, normalize away the similarity. Vertices and poses
are then exactly the original ones. The preceding function-valued profile
lemma applies: `q_i(t)=s_i*e(t)` for a single symmetric function
`e(t)=e(1-t)`, and port 17 is flat. Thus moving endpoints locally does not add
profile freedom while this complete network is retained. Admissibility of
actual arcs still requires an embedded tile boundary and nonoverlapping patches;
those conditions can only restrict the endpoint-equation solutions.

## Reproduction and trust boundary

Run with Python 3.11 or later, standard library only:

```
python3 heesch_weighted_matching_obstruction/endpoint_rigidity.py
```

Expected: 18 vertices, 131 copies, 1,075 independently decoded unit interfaces,
995 shared vertex groups, 2,410 equations, 426 variables, exact rank 422, four
independent integer kernel vectors, and minor determinant 379 modulo 1009.
The complete output is the expected JSON above.

The existing corona checker verifies every prefix of the input. One endpoint
decoder uses closed-form axial rotations and forward vertex positions; another
uses repeated rotations, actual shared cell edges, and inverse vertex labels.
Their incidence groups agree exactly. Sparse modular rank computation and a
separate dense determinant calculation agree on the certified minor. The
nonlinear implication is the written implicit-function argument, not a
numerical inference or a proof-assistant theorem.

Changing the incidence network, allowing contacts to split or slide along a
port, using different patches, or making large endpoint changes lies outside
the claim. The certificate does not establish a finite Heesch number at least
seven. It isolates an obstruction to deforming this known five-corona network.
