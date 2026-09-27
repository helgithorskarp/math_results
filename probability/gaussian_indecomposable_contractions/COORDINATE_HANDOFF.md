# A fully bounded rational indecomposable frontier

Complete author proof, 27 September 2026; independent review pending.
This combines [COORDINATE_HEIGHT.md](COORDINATE_HEIGHT.md) with the existing
finite frontier and chain-height reduction. No middle hinge sign is proved.

## 1. Start with the rational producer

Fix a rational `0<delta=a/b<=1` in lowest terms. Suppose a bounded-law
Gaussian contraction has an adverse hinge gap at least delta. Scale the
variance to one. Set `k=ceil(9/delta)` and use the accepted
[paired-cubature rational frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
Section 5, together with its
[rational rounding proof](../gaussian_prior_localization/RATIONAL_INTERFACE.md).
It gives an input in `R^c_k` with a beta average less than `-delta/2`.
As that average is taken against a probability density, some hinge gap is
less than `-delta/2` at this rational input.

Explicitly, let

    ell_k=ceil(log2 k), h_k=floor(sqrt(ell_k+1)), n_k=ceil(k/h_k),
    N=A_k=min{k^3[2 binom(2ell_k+6,3)-1],
              n_k^3[2 binom(4ell_k+11,3)-1]},
    L=256k^3,          W=4kN,
    B=ceil(log2(768k^4+1)).                                (1)

There are at most N prescribed source/image labels, coordinate denominator
L, integer coordinate magnitudes at most `3kL=768k^4`, and integer masses
of total W. Both supports lie in B(0,3k), and every distinct pair strictly
contracts. Thus B is a valid height bound for the coordinates and R=3k.

The order is essential. Real-valued cubature alone does not provide a
bounded rational input; the existing merge--expand--round step is used
before the rigid-mesh construction. It is not applied afterward, where
rounding could destroy the preserved distances.

## 2. The complete finite input contract

Compute M,K,H from (1)--(2) of COORDINATE_HEIGHT.md at N,B, and set V=M+3.
The [linear-height transfer](LINEAR_HEIGHT.md) and the new coordinate bound
give a noncongruent indecomposable contraction with

| Data | Bound |
| --- | --- |
| Labels | `4<=v<=V` |
| Common connected tetrahedral framework | `m<=M` nondegenerate tetrahedra |
| Each coordinate numerator and denominator | absolute numerator and positive denominator `<=2^H` |
| Supports, after common root-vertex translation | `B(0,12k)` |
| Every labelled mass | `>=m0=delta/[2(2+delta)V]` |
| Negative hinge gap magnitude | `>=gamma=delta/[4(M-1)]` |
| Fixed points | a nondegenerate root tetrahedron, with one vertex zero |

All masses can be represented with the explicit common denominator

    Q_v=2(2b+a)Wv.                                         (2)

Indeed the augmentation uses `epsilon=delta/[2(2+delta)]`. If an original
vertex has mass n_i/W (take n_i=0 at new vertices), its augmented mass is

    [(4b+a)n_i v+aW]/[2(2b+a)Wv].                          (3)

These positive integer numerators sum to Q_v. The same mass vector is
retained along the entire finite contraction chain. Coincident labels in
the extracted placement can be retained; there is no need to merge them
or alter this denominator. No dominant-atom property is retained or assumed.

Here is why the gap is gamma. The original rational input has a negative
gap greater than delta/2. Its augmentation leaves at least delta/4 at the
rescaled threshold, by the earlier mass perturbation estimate. A saturated
chain has at most m-1<=M-1 strict steps. At least one has the displayed
negative gap. This uses the linear-height author theorem, whose independent
review was still pending when this handoff was written.

This is a finite, explicitly bounded set of rational map/weight inputs:
enumerate the bounded numerators and denominators, positive integer masses
of total Q_v, and finite lists of at most M labelled tetrahedra. Test all
contraction and nondegeneracy conditions exactly. Impose equality on every
tetrahedron edge and equality on the root tetrahedron. To test that the
full distance interval has only its endpoints, enumerate the finite
root-aligned reflection choices and discard inconsistent placements and
ones outside the complete pairwise bounds. Every real intermediate
placement must preserve those tight tetrahedron edges, so none is omitted
by this rational enumeration. This is a mathematical finite input contract,
not a claim that the enumeration is computationally feasible.

The source and target of the extracted step may both be folded meshes.
They are not asserted to be embedded convex source triangulations, to
lie on the previous prescribed grid, or to have strict loss on every pair.
This distinction is the reason the new coordinate bound is useful.

## 3. Uniform signed outer intervals for this finite class

The [exposed-edge endpoint theorem](../gaussian_exposed_edge_tail/PROOF.md)
now gives uniform endpoints from the bounded input alone. It is a separate
complete author proof pending independent review. Write `R0=12k` and put

    J0=145+2 ceil(log2 V)+6 ceil(log2 R0)+(222V+30)H,
    ell=ceil(log2(1/m0)),     B0=6R0^2+2ell,
    E=16 B0^2 2^(2J0),       U=ell+12VH+4,
    tau=2^(-E),              b0=1-2^(-U).                  (4)

For every noncongruent member of the finite class, with covariance-I_3
Gaussian and positive hinge convention `H_gap(u)=H_g(Cu)-H_f(Cu)`,

    H_gap(u)>0 for 0<u<=tau,
    H_gap(u)>=0 for u>=b0.                                (5)

The middle interval `[tau,b0]` is not signed by this argument. Any
adverse witness from Section 2 must occur there.

To check (4), the least common denominator D of the at most 6v coordinate
entries is at most `2^(6VH)`. Their cleared integer magnitudes are at most
`2^((6V+1)H)`. The input-size mean-support bound from the exposed-edge
theorem therefore gives a margin at least `2^(-J0)`: the denominator
contributions are 40, `2 log2 V`, `6 log2 R0`, at most 75 from `(6*7!)^5`,
`42VH` from D^7, and `30+30(6V+1)H` from the integer-coordinate term.
The low endpoint is its geometric tail lemma with this smaller margin.

For the high endpoint, some strict pair has squared source distance at
least `D^(-2)>=2^(-12VH)`. Also m0>=2^(-ell). The source-peak loss is at
least

    m0/[8*2^(12VH)+1] >=2^(-ell-12VH-4),

which is (5) for u>=b0. There is no mean-width integration or exposed-edge
search in these uniform endpoint formulas.

Store these as compressed integer formulas: E is specified by the pair
`(16 B0^2, 2J0)`, meaning a coefficient times a power of two. Neither
`2^H`, `2^E`, nor even the fully expanded E is needed. The bounds are far
too large to be treated as a practical replay plan.

## 4. What this changes

For a fixed deficit delta, the earlier geometric test class had explicit
labels, masses, radius and surviving gap but uncontrolled rational
coordinate size. All these arithmetic parameters are now specified before
choosing the hypothetical witness. In particular, its signed outer
threshold intervals are uniform over that finite class.

The retained gap bound does not imply a sign. The remaining work is still
the actual middle comparison on indecomposable maps. The rational frontier
from the measure lane already gave another complete finite reduction; no
claim is made that this larger geometric frontier is a smaller search or
a faster algorithm. Its additional structure is the common tight framework
and indecomposability, both preserved exactly rather than by rounding.

Qualitative Brehm extension, standard determinant-height estimates, the
paired-cubature/rounding bounds, linear chain height and the geometric
low-tail lemma are credited inputs. This composition supplies no new
all-threshold class, Gaussian counterexample or Kneser--Poulsen consequence.
