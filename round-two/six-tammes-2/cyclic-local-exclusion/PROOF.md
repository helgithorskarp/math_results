# Cyclic local certificate and a completed 26-near-contact exclusion

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-10-01.

The new result is a quantified certificate for the known cyclic incumbent and
the resulting exclusion of a prescribed 26-edge near-contact pattern. The
cyclic packing, its algebraic construction, and rigidity have prior literature;
no new packing or priority for rigidity is claimed. This does not prove the
global optimality of fifteen points or improve an unconditional Tammes bound.

## 1. Exact construction and notation

Let \(\tau\) be the root of

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1
\]

in the rational interval

\[
(0.59260590292507377809642492233275,
  0.59260590292507377809642492233276).
\]

Both checkers verify the endpoint signs and a strictly positive derivative
throughout this interval. Put \(H=(1-\tau)I+\tau J\) and choose a real invertible
matrix \(B\) with \(B^TB=H\). This is possible since \(0<\tau<3/5\).
The coefficient vectors \(v_0=e_0,v_5=e_1,v_{11}=e_2\) are the first anchors.
The other three anchors satisfy

\[
(v_1\ v_2\ v_4)=H^{-1}M,\qquad
M=\begin{pmatrix}a&b&c\\c&a&b\\b&c&a\end{pmatrix},
\]

where

\[
\begin{aligned}
a&=(117\tau^4-48\tau^3+70\tau^2-6\tau-27)/2,\\
b&=(195\tau^4-106\tau^3+136\tau^2-38\tau-31)/4,\\
c&=(-429\tau^4+202\tau^3-276\tau^2+42\tau+81)/4.
\end{aligned}
\]

Construct the remaining vectors from
\(v_n=2\tau(v_i+v_j)/(1+\tau)-v_o\), using these ordered tuples
\((n,i,j,o)\):

```
(6,0,11,5) (7,0,5,11) (9,5,11,0) (14,0,6,11)
(12,5,7,0) (13,11,9,5) (3,1,4,2) (8,2,4,1) (10,1,2,4)
```

This is the previously published cyclic construction, not a symmetry assumption
on configurations to which the theorem will be applied. Exact arithmetic gives
unit points \(p_i=Bv_i\), exactly thirty inner products equal to \(\tau\), and
every other inner product less than \(17/40\). All polynomial equalities below
are checked modulo \(F\). Such equalities hold at the bracketed root without
requiring an irreducibility theorem for \(F\).

The permutation

\[
\sigma=(0\ 5\ 11)(1\ 2\ 4)(6\ 7\ 9)(14\ 12\ 13)(3\ 10\ 8)
\]

preserves the full Gram matrix. Each contact orbit has size three.

## 2. Positive stress and rank certificate

The following table gives one weight for each contact orbit. A row lists the
coefficients of \(w_e=\sum_{k=0}^4 d_k\tau^k\); all three edges in the orbit
receive that weight. The other two edges are obtained by applying \(\sigma\).

| Representative edge | \(d_0\) | \(d_1\) | \(d_2\) | \(d_3\) | \(d_4\) |
|---|---:|---:|---:|---:|---:|
| 0,5 | -97/4 | -15 | 183/2 | -66 | 559/4 |
| 0,6 | -55/4 | -5 | 59 | -36 | 351/4 |
| 0,7 | -9/2 | -3/4 | 121/4 | -65/4 | 169/4 |
| 0,14 | 1 | 0 | 0 | 0 | 0 |
| 1,2 | -1/2 | 3/2 | 3 | -1/2 | 13/2 |
| 1,3 | 3/4 | 11/2 | 15/2 | 5/2 | 39/4 |
| 1,10 | 3/4 | 11/2 | 15/2 | 5/2 | 39/4 |
| 3,7 | -2 | 11/2 | 43/2 | -5/2 | 65/2 |
| 3,14 | -1 | 9/4 | 43/4 | -5/4 | 65/4 |
| 6,14 | -3 | 1/2 | 19 | -17/2 | 26 |

Both checkers establish

\[
w_e\ge1,\qquad W=\sum_e w_e<183,\qquad
\sum_{j:ij\in E}w_{ij}(v_j-\tau v_i)=0\quad(0\le i<15).
\tag{1}
\]

In particular, \(W=-279/2+750\tau^2-378\tau^3+2223\tau^4/2\).
Multiplying equilibrium by \(B\) gives the same identity for the physical
vectors \(p_i\).

For coefficient displacements \(\delta_i\in\mathbb R^3\), let \(R\) have
fifteen rows \(v_i^TH\delta_i\), twenty-seven selected contact rows

\[
L_{ij}=v_j^TH\delta_i+v_i^TH\delta_j,
\]

and the three gauge rows \(\delta_{0,1},\delta_{0,2},\delta_{5,2}\).
The contact list, selected rows, and a rational matrix \(A\) are stored in
`certificate.json`. The row norm is the maximum absolute row sum. Exact rational
enclosures give

\[
\|A\|_\infty<46,\qquad \|I-AR\|_\infty<1/1000,
\qquad \frac{\|A\|_\infty}{1-\|I-AR\|_\infty}<46.
\tag{2}
\]

The last inequality is checked directly, rather than inferred from the first
two coarse bounds. Neumann inversion proves \(R\) invertible and
\(\|R^{-1}\|_\infty<46\). The checker `check.py` encloses \(R\), rounds it to
a rational grid, and bounds the grid residual and rounding error. The separate
checker `audit.py` forms the unreduced polynomial matrix \(I-AR\) and uses
centered Taylor enclosures; its residual is at most \(6921/40000000000\).

The full ungauged matrix of fifteen norm rows and thirty contact rows has rank
42. Indeed, the selected forty-two rows have rank 42 by (2), whereas the three
independent infinitesimal rotations lie in the full matrix's kernel. The anchor
vectors span \(\mathbb R^3\), so those rotations are independent. Equilibrium
and positive weights force all nonpositive admissible first-order contact
derivatives to vanish. Thus the packing is infinitesimally jammed, as also
consistent with the prior rigidity literature.

## 3. Explicit cyclic local inequality

Let \(q_i\) be fifteen unit vectors in the gauge

\[
q_0=p_0,\qquad q_5\in\operatorname{span}(p_0,p_5).
\]

Write \(u_i=q_i-p_i=B\delta_i\), and define

\[
\rho=\max_{i,k}|\delta_{ik}|,\quad
D=\max_i\|u_i\|,\quad
\eta=\max_{i<j}q_i\cdot q_j-\tau,\quad
\eta_+=\max(\eta,0).
\]

**Local inequality.** If \(\rho\le1/250000\), then

\[
\eta\ge\rho/16836.
\tag{3}
\]

Consequently, if \(D\le1/400000\) in this gauge, then

\[
\eta\ge D/50508.
\tag{4}
\]

To prove this, all entries of \(H\) have absolute value at most one, giving
\(\|u_i\|^2,|u_i\cdot u_j|\le9\rho^2\). The exact unit equations give
\(p_i\cdot u_i=-\|u_i\|^2/2\). Every contact therefore satisfies

\[
L_e\le\eta_++9\rho^2.
\]

With \(s_i=\sum_jw_{ij}\), equilibrium yields

\[
\sum_e w_eL_e=-\frac\tau2\sum_i s_i\|u_i\|^2
\ge-9\tau W\rho^2.
\]

Subtract the upper bounds of the other contacts. For any edge \(e\),

\[
L_e\ge-\frac{W-w_e}{w_e}\eta_+
-9\frac{\tau W+W-w_e}{w_e}\rho^2.
\]

Using \(w_e\ge1\), \(W<183\), and \(\tau<3/5\), both signs are bounded by

\[
|L_e|\le183\eta_++\frac{72}{5}\,183\rho^2.
\]

The norm rows have size at most \(9\rho^2/2\), and the gauge rows vanish.
By (2),

\[
\rho\le46\left(183\eta_++\frac{72}{5}\,183\rho^2\right).
\]

The exact scalar inequality
\((144/5)\,46\,183/250000<1\) makes the quadratic term less than \(\rho/2\)
when \(0<\rho\le1/250000\). It follows that
\(\eta_+\ge\rho/(2\cdot46\cdot183)=\rho/16836>0\), which implies
\(\eta=\eta_+\) and proves (3). If \(\rho=0\), then \(q=p\) and \(\eta=0\).

Since \(H>(2/5)I\), we have \(\rho<(8/5)D\) for \(D>0\); also
\(D\le3\rho\). These inequalities prove (4), including its radius. In
particular, a gauged configuration in this radius with maximum inner product
at most \(\tau\) equals the cyclic incumbent.

## 4. A rotation gauge costs at most ten times the initial distance

This elementary estimate is used for both incumbents. Suppose a labeled
configuration is within distance \(D_0\le1/100\) of an incumbent, whose anchors
have \(p_0\cdot p_5=\tau<3/5\). First rotate \(q_0\) to \(p_0\) in the plane
of these vectors. This rotation has operator norm distance at most \(D_0\)
from the identity, so every point is now within \(2D_0\) of its incumbent.

Project the new \(q_5\) and \(p_5\) onto \(p_0^\perp\). Their projections
differ by at most \(2D_0\); the latter projection has norm
\(\sqrt{1-\tau^2}>4/5\), so both projections are nonzero. For nonzero vectors
\(a,b\), their normalized directions differ by at most
\(2\|a-b\|/\|b\|\). Thus these directions differ by at most \(5D_0\).
Rotate about \(p_0\) to align them. This rotation's operator norm distance
from the identity equals that direction difference. The resulting gauge
satisfies

\[
\max_i\|q_i-p_i\|\le7D_0\le10D_0.
\tag{5}
\]

The case of already aligned directions uses the identity rotation. The estimate
holds after an initial orthogonal alignment, which may include a reflection.

## 5. The 26-near-contact pattern is excluded in every strict improvement

Here \(G_{26}\) is the following graph on labels \(0,\ldots,13\); label 14
has no prescribed edges:

```
(0,5) (0,6) (0,7) (0,11) (1,2) (1,3) (1,4) (1,10) (1,12)
(2,4) (2,8) (2,10) (2,13) (3,4) (4,8) (5,7) (5,9) (5,11)
(6,8) (6,11) (7,12) (8,13) (9,10) (9,11) (9,13) (10,12)
```

**26-near-contact exclusion.** Let \(t\in[14/25,\tau]\) and
\(0\le\varepsilon\le10^{-16}\). Suppose fifteen unit points satisfy

\[
q_i\cdot q_j\le t\quad(i\ne j),\qquad
t-\varepsilon\le q_i\cdot q_j\le t\quad(ij\in G_{26}).
\tag{6}
\]

Then \(t=\tau\), and up to orthogonal transformations and the stated
relabeling, the configuration is one of the two known incumbents. Thus no
strictly improved fifteen-point code contains this prescribed near-contact
pattern. No edges incident to the fifteenth point are required.

The interval includes the full improvement range for fifteen points. Deleting
one point and using the solved fourteen-point problem gives maximum inner
product at least its optimum \(t_{14}>14/25\), approximately
\(0.56395030036\). This standard domain reduction is also used in the preceding
near-contact source (height 8600), which is replayed below. Here it supplies
only the lower endpoint of the strip, not global optimality for fifteen points.

The published fourteen-point completion theorem, graph height 8670, applies
on \([14/25,593/1000]\) at tolerance at most \(10^{-13}\). It gives an
orthogonal alignment of the entire configuration within

\[
D_0\le2100000000\varepsilon
\]

of the asymmetric incumbent or its alternative completion. The alternative
completion is exactly the cyclic incumbent after the permutation mapping
common label \(i\) to cyclic label

```
1 0 11 7 5 4 10 3 9 8 6 2 14 13 12
```

That published theorem uses a full 364-active-triple avoidance-polytope
enumeration and the earlier near-contact stability theorem, not a numerical
packing search. The pinned source and its entire prerequisite chain are
replayed by `replay.py`; the cyclic Gram relabeling is checked again here.

By (5), the gauged distance for either branch is at most

\[
10\cdot2100000000\cdot10^{-16}=21/10000000<1/400000.
\]

For the asymmetric branch use its previously published local certificate,
graph height 7123, which gives \(\eta\ge D/37332\) in this radius.
For the cyclic branch use (4). In either case (6) gives
\(\eta\le t-\tau\le0\), so \(D=0\) and \(\eta=0\). It follows that
\(t=\tau\) and the configuration is the corresponding incumbent. Both known
incumbents attain (6) at equality; the cyclic one is used in the common
fourteen-point labeling above. This completes the branch left open by height
8670.

## 6. Proof status, dependencies, and scope

This is an author-checked written proof with exact computational certificates
and two arithmetic implementations. The second implementation is an internal
arithmetic audit by the same authoring researcher, not an independent team
review or a proof-assistant formalization. An incomplete search or solver
status is not used. All verification and regeneration use standard-library
Python, one sequential CPU job at a time; no solver or threaded numerical
library is needed.

The main dependencies, pinned by commit and SHA-256 in `INPUTS.json`, are:

- The two-completion and 26-near-contact reduction, height 8670, source
  `1417ab38e068f028e0cf1eae4ae0d76066d8956b`:
  [proof](https://github.com/helgithorskarp/math_results/blob/1417ab38e068f028e0cf1eae4ae0d76066d8956b/round-two/six-tammes-2/fourteen-point-completion/PROOF.md).
- The asymmetric exact local certificate, height 7123, source
  initial source `3cdc15f44977d90da550be8ce83006ef8b211808`, with the later
  literature-citation README pinned at `6dffbb940c10f415b71e275a45010a7141d1ee4e`:
  [pinned proof and checker](https://github.com/helgithorskarp/math_results/tree/6dffbb940c10f415b71e275a45010a7141d1ee4e/tammes15_exact_local_certificate).
- The earlier exact construction and forced Gram matrices of both incumbents,
  height 7170: [construction](https://github.com/helgithorskarp/math_results/tree/main/tammes15_contact_pattern_obstruction).

Primary background includes Kottwitz,
[The densest packing of equal circles on a sphere](https://doi.org/10.1107/S0108767390011370),
and the Buddenhagen–Kottwitz exact-construction manuscript cited in the preceding
construction source. Henry Cohn's
[archived spherical-code data set](https://hdl.handle.net/1721.1/153543), the live
[spherical-code table](https://spherical-codes.org/)
and [fifteen-point coordinate data](https://spherical-codes.org/data/3/15) were
refreshed on 2026-10-01. The seed
[Musin–Tarasov paper](https://arxiv.org/abs/1410.2536) proves the fourteen-point
problem. The global fifteen-point problem remains the campaign frontier.

An arbitrary improved code has not been proved to contain \(G_{26}\).
The useful next step is to combine this certified forbidden pattern with a
complete global contact-graph or near-contact covering reduction. That global
step is not supplied by this certificate.
