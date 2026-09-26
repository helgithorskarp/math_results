# An effective rational producer for the compact Gaussian frontier

Complete author proof; independent review pending. The full bounded-law
Gaussian-majorisation question in R3 remains open. This note supplies the
coordinate and weight denominators missing from the existing compact
localization. It does not introduce a new unbounded test class or evaluate
an unknown Gaussian sign.

Let D be the unrestricted supremal positive hinge defect at variance one,
and K_k the compact k^6-atom, radius-2k parameter set of
[DEFECT_LOCALIZATION.md](DEFECT_LOCALIZATION.md). Its attained maximum D_k
satisfies 0<=D-D_k<4/k. The anchor x_1=y_1=0 may have zero weight;
coincident sites and zero weights are allowed in K_k.

## 1. Finite integer data and the error budget

For each integer k>=1 set

    L=256 k^3,    W=4 k^7,    P=2^16 k^8,    N=P-2.

Define R_k by the following **finite integer** input contract:

| Input | Exact requirement |
| --- | --- |
| Number of labels | 1<=m<=k^6 |
| Centers | X_i,Y_i in Z^3; X_1=Y_1=0 |
| Radius | norm2(X_i), norm2(Y_i) <= (3kL)^2 |
| Contraction margin | norm2(X_i-X_j)-norm2(Y_i-Y_j) >=256k^2 for i!=j |
| Weights | integers n_i>=0 with sum_i n_i=W |
| Decoded laws | x_i=X_i/L, y_i=Y_i/L, w_i=n_i/W; variance one |

Here norm2 denotes squared Euclidean norm. The margin is vacuous for m=1.
Zero weights and coincident **target** sites
are permitted. Distinct labels have distinct source sites, and the decoded
data define an actual contraction with squared-distance loss at least
1/(256k^4) per pair. Kirszbraun extension is available if a whole-space map
is required.

The returned fields of `round_instance` decode directly to R8's new
[weight-cell consumer](../gaussian_beta_weight_certificate/certificate.py):
divide each `source_integer_centers` and `target_integer_centers`
coordinate by `coordinate_denominator` using `Fraction`, then supply
`Cell(x, y, Fraction(0))` for an exact metric cell. That constructor needs
at least seven labels. Its current implementation certifies **only N=5**,
using six coefficient bounds for each seven-distinct tuple and the
analytic pruning in its [proof](../gaussian_beta_weight_certificate/PROOF.md).
It handles all prior weights at once when its sufficient coefficient
conditions succeed. The larger row N=2^16 k^8-2 in (2) remains a separate
producer obligation: a successful N=5 cell is not a certificate for F_k,
and a failed coefficient lower bound is not a negative beta witness.

For the source and target Gaussian densities write

    H(u)=H_g(Cu)-H_f(Cu),     C=(2pi)^(-3/2),
    b_(N,j)=E H(Beta(j+1,N-j+1)),   0<=j<=N,
    F_k=max_(Q in R_k) max_(0<=j<=N) (-b_(N,j)(Q))_+.

**Theorem.** Every Q in K_k has an approximation Q' in R_k for which,
simultaneously at every physical hinge threshold a>=0,

    |[H_f(a)-H_g(a)]_Q - [H_f(a)-H_g(a)]_(Q')|
        < 161/(256k).                                      (1)

The same bound holds for every beta average, at any degree. Combining
this producer with R8's existing compact moment bound gives

    0<=D-F_k<4067/(768k)<16/(3k).                            (2)

Only normalized powers through P=2^16 k^8 are used. The new content is
the finite rational replacement, its exact margins and its complexity
bounds; the degree and moment approximation are credited inputs.

## 2. Merge, expand, then round

Fix Q in K_k and put

    r=1/(4k),     lambda=1/(8k^2).

Start with the anchored label and greedily retain another source site
only when its distance from every retained site exceeds r. The retained
sites are r-separated and every original site is within r of one of
them. Send each original weight to such a representative, retaining that
representative's actual image. This moves each endpoint by at most r,
because the original data are contracting. The result has m<=k^6 sites,
both radii still at most 2k, and anchor zero. Merging does not presuppose
a positive minimum separation or a positive minimum weight in the input.

Expand these retained source sites by 1+lambda, holding their images
fixed. Then round every coordinate of both endpoint lists to the nearest
multiple of 1/L. The anchor stays zero. Each rounding displacement has
Euclidean norm at most sqrt(3)/(2L)<1/L.

If d>=r is a source distance before expansion, the final source distance
d_x and target distance d_y obey

    d_x-d_y >= lambda d-4/L
              >=1/(32k^3)-1/(64k^3)=1/(64k^3),
    d_x >=(1+lambda)d-2/L >=d>=r.

Hence d_x^2-d_y^2 >=1/(256k^4), exactly the integer margin in R_k.
The source radius is at most

    2k+1/(4k)+1/L <3k,

and the target radius is at most 2k+1/L<3k. No separation of target sites
is needed. Rounding an isometry without the separation-and-expansion
step can break contraction, even on two sites; the exact audit includes
that control.

For each retained weight w_i, start with floor(W w_i). Add one to the
largest fractional remainders until the integer total is W. This changes
each weight by at most 1/W and therefore changes their L1 distance by
at most m/W<=1/(4k). Zero output weights are retained or can be omitted,
except that the anchor may be kept with zero weight. All input constraints
remain valid; no least-weight assumption was used in the construction.

The Gaussian-translation bound from the localization proof is

    TV(gamma_1(. -x),gamma_1(. -x')) <= |x-x'|/sqrt(2pi).

A hinge changes by at most TV. For the two endpoints together, merging,
expansion and rounding therefore cost at most

    (2r+2k lambda+2/L)/sqrt(2pi).

The two endpoint errors from changing weights add to at most their L1
weight difference. Since sqrt(2pi)>2, the total cost is strictly below

    3/(8k)+1/(256k^3)+1/(4k)
      <=161/(256k).                                        (3)

This proves (1). Integrating the signed hinge difference against any
probability beta density proves its stated beta version. In particular,
this perturbation estimate is not multiplied by alternating moment
coefficients.

## 3. Composition with the existing degree bound

R8's [UNIFORM_FRONTIER.md](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
uses the same K_k and N=2^16 k^8-2. With

    B_k=max_(Q in K_k) max_j (-b_(N,j)(Q))_+,

its already established bound is 0<=D-B_k<14/(3k). Apply (1) to a
maximizing Q in K_k. The maximum of finitely many positive negative-beta
values is 1-Lipschitz in their supremum norm, so

    B_k<=F_k+161/(256k).

Every member of R_k is an admissible Gaussian-contraction pair. A beta
average cannot exceed the worst hinge defect in negative magnitude, so
F_k<=D. These observations prove (2), since

    14/3+161/256=4067/768 <4096/768=16/3.

The moment degree is kept from the original radius-2k problem **before**
rounding; beta stability transfers that degree to the radius-3k rational
family. No silent substitution of radius 3k into a radius-2k theorem is
made. The families R_k need not be nested for consecutive k. Convergence
to D follows from (2), without a monotonicity assertion for F_k.

## 4. Producer and consumer obligations

For a requested absolute tolerance 0<epsilon<=1, take k=ceil(12/epsilon).
If a rigorous producer establishes

    b_(N,j)(Q)>=-epsilon/2
            for EVERY Q in R_k and EVERY 0<=j<=N,           (4)

then (2) gives D<17epsilon/18<epsilon. A sample of configurations or beta
indices does not establish (4). A certificate covering regions of the
integer data is as valid as a literal enumeration; neither is supplied
here. Tolerances must tend to zero to prove D=0.

Conversely, if a violation of size delta>0 exists, k>=12/delta ensures
some Q in R_k and some beta index have b_(N,j)<-delta/2. Thus a specified
gap has bounded atoms, coordinates, denominators and moment order. A
single rigorously negative beta enclosure at verified data in R_k is a
counterexample through the existing convex-energy identity. No negative
enclosure is claimed here.

There is an additional exact geometric input for the functional lane.
If at least two weights of a member of R_k are positive, then

    sum_(i,j) w_i w_j (|x_i-x_j|^2-|y_i-y_j|^2)
       >=2/(W^2 256k^4)=1/(2048k^18).                       (5)

The sum uses ordered pairs. Point laws instead have zero loss and must
be treated as exact equality controls. This supplies a uniform separation
from the pair-distance equality boundary on the non-point rational data.
R8's [reference-margin interface](../gaussian_common_set_stability/INTERFACE.md)
can consume the quantity in (5), but still needs its reference coefficients
and source-set error. Pair loss alone is not a hinge sign. That optional
consumer does not enter the proof of (1)--(2).

## 5. Size and arithmetic of the finite task

All coordinate integers lie in [-768k^4,768k^4]. The number of ordered
inputs, before filtering by the exact constraints, is at most

    k^6 [(1536k^4+1)^6 (4k^7+1)]^(k^6)
      <= k^6 [2^69 k^31]^(k^6).                            (6)

This overcounts anchors, weight sums and pair constraints. Including
all beta indices gives at most 2^16 k^14 [2^69 k^31]^(k^6) tests.
Each input has O(k^6 log(2k)) bits, but there are exponentially many
inputs. These are explicit bounds, not a feasible enumeration proposal.

The credited replica formula for the normalized source moment is

    A_m(f)=m^(-3/2) sum_(i_1,...,i_m) product_a(n_(i_a)/W)
        exp(-sum_(a<b)|X_(i_a)-X_(i_b)|^2/(2mL^2)),          (7)

and similarly for the target. It uses integers, rational exponents and
an algebraic factor. A direct moment has at most (k^6)^m summands; no
efficient alternative is supplied by this note.

For an explicit precision contract, suppose each normalized endpoint
moment through power N+2 is approximated with absolute error at most eta.
The existing formula is

    b_(N,j)=(N+1) binom(N,j) sum_(l=0)^(N-j)
       (-1)^l binom(N-j,l)
       [A_(j+l+2)(g)-A_(j+l+2)(f)]/[(j+l+1)(j+l+2)].

Since the denominator is at least two, its resulting absolute error is
at most eta (N+1) binom(N,j) 2^(N-j) <= eta (N+1) 3^N.
Thus eta<=zeta/[(N+1)3^N] suffices for beta error 0<zeta<=1. Alternatively,
using eta=2^(-p), any

    p>=2N+ceil(log2((N+1)/zeta))                            (8)

suffices. This accounts for cancellation; ordinary floating moment values
are not certificates. Bounds (7)--(8) specify a finite rigorous arithmetic
task but do not make it small.

The finite-atomic lane's [degree barrier](../gaussian_certificate_degree_barrier/PROOF.md)
concerns a particular all-threshold **exact positive certificate** for
one fixed pair. Here the requested conclusion is an **absolute-error**
bound on the unrestricted defect. No claim that (1)--(8) repair or evade
that barrier is made. No signed-tail interval or strict positivity near
zero threshold is assumed in this interface.

The companion [rational_frontier.py](rational_frontier.py) implements the
producer for rational inputs and audits collisions, tight isometries,
weight faces, target coincidences and a rejected unmerged-rounding shortcut.
Its compact [expected output](RATIONAL_EXPECTED.json) contains exact
integer/Fraction controls only. No Gaussian moment or beta sign is computed.
The universal rounding and error-transfer proof above, and the credited
localization and moment results, are the unformalized trust boundary.
The original localization proof and its hash are unchanged.
