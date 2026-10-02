# All-source closed J74 fits on a nonminimal receiving cap

**six-rupert-2, researcher; 2026-10-02.** Exact finite covering certificate
and ordinary geometric proof. Author-checked, unformalized and independently
unreviewed. The global Rupert property of J74 remains **OPEN**.

## 1. Named solid, receiving domain and complete statement

Let `s=sqrt(5)>0`, and let `K=conv(V)` be the original unit-edge,
60-vertex **metabigyrate rhombicosidodecahedron, J74**, constructed in
[model.py](../model.py) by two nonopposite 36-degree cupola gyrations.
The original [geometry proof](../PROOF.md), source
`25fc9695745b6832d068d18544452b7852b5847f`, committed LEMMA8551,
identifies the named body and proves its complete original geometry.
Every original has squared radius `R^2=(11+4s)/4<81/16`.
Three independent actual antipodal pairs put zero in the interior of K.
The whole body is not assumed centrally symmetric.

For a unit normal n put `P_n=I-n n^t` and `M_n=I-2n n^t`.
Define

    u0=((16s-26)/44, (53-15s)/44, (-11-s)/44),
    n0=u0/||u0||, delta=1/1000000000.

This is the raw receiver `(m+10d)/11` in the earlier receiving strips:
`m=(1,-phi,-phi^2)/(2phi)`, `phi=(1+s)/2`, and
`d=((-5+3s)/8,(11-3s)/8,-1/4)`. The receiving set C is the ENTIRE
closed projective unit-normal chord cap

    min(||n-n0||,||n+n0||)<=delta.                 (1)

The radius is a unit-normal chord, not a raw coordinate or angle.
Every cap boundary and both choices of oriented normal are included.
Every receiver in C has projective chord greater than1/3 from ALL six
global minimum-area axes. Thus this is a nonminimal receiving cap.

Set `a=(s-1)/4`, `b=(s+1)/4`, `c=1/2`, and give matrices by ROWS:

    H=diag(-1,-1,1),
    A=(( b, a, c), (-a,-c, b), ( c,-b,-a)),
    B=((-a,-c,-b), ( c,-b, a), (-b,-a, c)),
    F={I,H,A,AH,B,BH},  Mx=diag(-1,1,1).

All six members of F are proper. Mx preserves all original vertices
of K and is improper. For each receiving n define

    E(n)=F union {M_n g Mx: g in F}.               (2)

Every motion in(2) is proper; there are exactly twelve distinct motions
throughout C. Some preserve the full body; the finite proof also uses
poses that preserve its shadow on this cap.

**Theorem.** For EVERY receiving n in C, EVERY proper Q, EVERY actual
physical translation `T in n^perp`, and EVERY scale `lambda>=1`,

    lambda P_n(QK)+T subseteq P_n K
        iff lambda=1, T=0, Q in E(n).             (3)

All these fits are equal shadows. No initial source-normal, roll,
relative-rotation, quaternion-component or translation bound is imposed.
No strict standard Rupert passage uses a receiver in C. The cap does
not cover the receiving sphere and(3) does not decide global J74.

Current primary literature was refreshed on2026-10-02. The five open
Johnson entries J72,J73,J74,J75,J77 occur in
[Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190).
[Zeng, Sections1.1--1.2](https://arxiv.org/html/2604.26531) gives the
proper strict-projection convention and still states RID non-Rupertness
as a conjecture. The distinct
[Steininger--Yurkevich Noperthedron result, v2](https://arxiv.org/abs/2508.18475)
does not settle these Johnson solids. No published theorem is claimed
as new here and no historical priority for the methods below is asserted.

## 2. Actual supports, equal shadows and exact local duals

The exact monotone hull of ALL sixty projected originals at n0 is

    16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20.   (4)

Let `i->j` traverse(4), `E_i=Vj-Vi`,
`h_i(n)=(E_i cross n).Vi`, and `N_i(n)=(E_i cross n)/h_i(n)`.
At n0, the checker rebuilds all1020 original support comparisons,
positive heights, endpoint equalities and the complete hull. Each
actual spatial edge E_i has length one, and

    h_i(n0)>1/10,  R^2||N_i(n0)||^2<9/4.           (5)

The exact matrices in F are reconstructed from the certificate, checked
proper, and tested against all sixty original source vertices. Each
receiving corner in(4) has a LITERAL spatial preimage `g Vk=Vi`.
For each g and edge, every other source image p apart from its two
literal endpoints satisfies

    (E_i cross n0).(Vi-p)>1/10000.                 (6)

These are5916 strict normalized offendpoint comparisons, evaluated
without approximating n0: the raw gap is positive and its square exceeds
`||u0||^2/10000^2`. Source images have the same radius R. Variation of
the left side in(6) is less than `(9/2)||n-n0||`. Thus all supports and
their literal corner preimages persist throughout C. This proves

    P_n(gK)=P_n K, g in F, n in C.                 (7)

For each g, six exact nonnegative five-contact duals at n0 target the
three signed spatial coordinates. Their actual source labels and
weights are in [certificate.json](certificate.json). If `p=g Vk` is
an actual contact and `N=N_i(n0)`, the finite identities are

    sum w(p cross N)=+/-e_j,
    sum w N=0,  w>0.                              (8)

All SIX spatial components are checked directly. Each of the36 selected
five-by-five bases, using columns `(p cross N,N_x,N_y)`, has its full
inverse product checked. Seven different exact bases occur. The finite
bounds, with no floating or solver premise, are

    ||basis_inverse||infinity<=32,
    min w>1/160,
    sum w<(6,7,8)_j-1/10.                         (9)

## 3. The local duals remain valid on the entire receiving cap

Write `d=||n-n0||<=delta`. From(5), R<9/4 and d<=1/1000,
`h_i(n)>1/20`. Direct subtraction of the normalized supports gives

    ||N_i(n)-N_i(n0)||<500d.                       (10)

Indeed the numerator changes by at most d, the height by at most Rd,
and the two reciprocal-height bounds are20 and10. The resulting
coefficient is at most `20+200R<470<500`.

Every five-component column changes by less than1200d: the torque
change is at most `R*500d<1125d`, and either force-coordinate change is
at most500d. The whole basis infinity perturbation is therefore at
most6000d. The Neumann inequality `32*6000d<1/2` gives perturbed inverse
norm at most64. If w0 is a point weight vector, `||w0||infinity<8`.
Solving the SAME exact target in the nearby real basis changes each
weight by at most

    ||w(n)-w0||infinity<=96000*32*d.                (11)

This is at most0.003072, strictly less than half of1/160. The weights
stay positive. Their mass changes by at most
`480000*32*d<=0.01536<1/10`. Thus their masses remain bounded by6,7,8.
Since every N_i(n) is perpendicular to n and n_z remains nonzero,
zero x/y force coordinates imply zero z force also. The repaired duals
cancel every ORIGINAL physical translation.

Moreover(5),(10) give `R||N_i(n)||<8/5`. At any actual contact
`N.p=1`, the elementary product-of-linear-forms bound yields

    (N.q)(p.q)-||q||^2 >= -(13/10)||q||^2.         (12)

For clarity, the smallest eigenvalue of the symmetric product form
`(Np^t+pN^t)/2` is `(N.p-||N||||p||)/2`; subtracting `N.p=1` proves(12).

Suppose an actual closed fit has `Q=R(q)g`, `g in F`, with finite
ordinary Cayley vector q, where

    R(q)=I+2([q]_cross+[q]_cross^2)/(1+q.q).

Multiply its actual contact inequalities by a repaired dual. Force
balance gives `lambda sum w N.R(q)p<=sum w`. With lambda>=1, their
unit-scale weighted support change is nonpositive. The exact Cayley
formula and(12) therefore imply

    |q_x|<=6(13/10)||q||^2,
    |q_y|<=7(13/10)||q||^2,
    |q_z|<=8(13/10)||q||^2.                        (13)

Hence `||q||<=(13/10)sqrt(149)||q||^2`. On the CLOSED Euclidean gate
`||q||<=1/16`, any nonzero q would give the contradiction

    1<=(13/10)sqrt(149)/16<1,
    squared factor=25181/25600<1.                 (14)

Thus q=0 there. This is a conditional local lemma; section4 derives
entry into its gate for EVERY source on the receiving cap.

The other six motions follow through proper companions. For
`gbar(n)=M_n g Mx`, replacing Q by `Q'=M_n Q Mx` preserves its ENTIRE
projected source, because `Mx K=K` and `P_n M_n=P_n`. It is proper,
and the actual scale and physical translation are retained. Its
relative rotation is the reflection conjugate of `Q gbar(n)^t`, so
the relative Cayley Euclidean norm is identical. No single improper
body placement is substituted for a proper passage.

## 4. A complete four-chart source cover, including half-turns

Every proper spatial rotation has a nonzero real homogeneous quaternion
`z=(h,v)` and

    R(z)=[(h^2-v.v)I+2vv^t+2h[v]_cross]/(h^2+v.v).

Choose a largest absolute quaternion component, change the common sign
if needed, and divide by that component. This places z in one of FOUR
closed charts `z_j=1`, with the remaining three coordinates in[-1,1].
The construction covers ALL of SO(3), including h=0. It neither assumes
a source chart near an equality pose nor discards a degenerate face.

At n0 the checker constructs168 exact positive two/three-support force
circuits `(mu_i,N_i^0)`, with `sum mu=1`, `sum mu N_i^0=0`. For each
cut leaf, the certificate chooses actual original source indices k_i.
Define the symmetric four-by-four form

    L(N,p) = ((N.p, (p cross N)^t),
              (p cross N, Np^t+pN^t-(N.p)I)),
    D=sum mu_i L(N_i^0,V_ki)-I4.

The formula gives the literal identity below. The code additionally
checks a second homogeneous-matrix monomial derivation on three exact
vector pairs:

    z^t D z=(z.z)[sum mu_i N_i^0.R(z)V_ki-1].      (15)

The compact dyadic forest has8899 leaves, distributed over the four
charts as2381,2253,2078,2187, with maximum depth22. At depth d its
binary path splits coordinate `d mod3`. Exact sorted prefix intervals
verify complete, gapless, nonoverlapping interiors in EACH whole cube.
Closed cube faces are retained. Each leaf has one of the following
two EXACT certificates:

* **8855 cut leaves:** all27 tensor-Bernstein coefficients of(15),
  after affine conversion of the closed cube, exceed1/1000000.
* **44 local-pose leaves:** all27 coefficients of
  `(z.z)[trace(R(z) gbar0^t)-t0]` are strictly positive, for one of the
  twelve actual equality poses at n0, where
  `t0=(3-(4/75)^2)/(1+(4/75)^2)`.

The tensor degree is(2,2,2). Its basis functions are nonnegative on
the whole real cube and sum to one, so the coefficient signs certify
the full continuum, not sampled orientations. There are240273 exact
coefficient sign checks. Every coefficient of every leaf, with its
original labels, feeds the canonical stream digest
`ae58255e24d95a17244cbc37200701c1c60c61652256aa4e2c92737bde9f8185`.

On a cut leaf `z.z<=4`, so the unit weighted support violation at n0
exceeds1/4000000. On a local-pose leaf, the proper relative rotation
has finite Cayley norm STRICTLY less than4/75. This entry bound is a
consequence of the complete source cover.

## 5. Transporting all cut leaves to the receiving cap

Keep a cut leaf's positive weights and point normals, and for any
receiver n use the actual planar support polars

    Ntilde_i=P_n N_i^0, Htilde_i=h_K(Ntilde_i).

Projection preserves FORCE BALANCE: `sum mu_i Ntilde_i=0`. The new
polars need not be silhouette edges. They are valid support directions
against the ENTIRE original K. Since `N_i^0` is perpendicular to n0,

    ||Ntilde_i-N_i^0||<=d||N_i^0||.

Support functions of a body in the radius-R ball are R-Lipschitz.
Equation(5) therefore bounds the total change in its weighted unit
violation by

    2R d sum mu_i||N_i^0||<3d.

On the entire cap the violation is consequently greater than

    1/4000000-3/1000000000=247/1000000000>0.        (16)

For an actual scaled fit, translation cancels. Because zero belongs
to K, `sum mu_i Htilde_i>=0`; the positive unit violation in(16)
remains contradictory for EVERY lambda>=1. This excludes every source
in every cut leaf at EVERY cap receiver, without a translation bound.

A local-pose leaf around a fixed g in F already has Cayley norm<4/75
relative to g, inside the gate1/16 in(14). For a companion, its reference
moves from `M_n0 g Mx` to `M_n g Mx`. Reflection matrices satisfy
`||M_n-M_n0||op<=2d`. Thus its new relative operator distance from I
is less than `8/75+2d<11/100`. The exact comparison

    (11/100)^2<4/257

derives relative Cayley norm<1/16. The local lemma applies to this
ACTUAL proper motion also. Every source is therefore one of(2).

The twelve point poses have exact pairwise squared Frobenius separation
greater than1/100. Each companion moves in Frobenius norm by less than
3d, and `6delta<1/10`; all twelve remain distinct on the closed cap.

## 6. Recovering original scale and translation; sufficiency

The original source projection now equals the receiver by(7) and the
companion identity. A positive width of the full-dimensional receiver
in the ORIGINAL inclusion(3) gives `lambda<=1`. Thus lambda=1. Equal
shadow support inequalities give `a.T<=0` for every planar direction a;
choosing a in the direction of T forces the ORIGINAL T=0. Conversely
all motions in(2) give equality, proving the iff in(3).

The exact center has chord>3/8 from every global minimum axis. The
triangle inequality gives chord>`3/8-delta>1/3` throughout C. Negative
oriented normals have the same P_n and M_n, so both parts of(1) and
every boundary obey the same statement.

## 7. Evidence, dependencies and remaining frontier

[check.py](check.py), [collar.py](collar.py) and
[certificate.json](certificate.json) are a standard-library exact
replayer, finite collar checker and compact8899-leaf certificate.
[DEPENDENCIES.json](DEPENDENCIES.json) pins the original model and
ordered arithmetic BEFORE import. The arithmetic is credited to the
prior [J77 diameter source](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/q5.py).
[expected.json](expected.json) contains the complete compact mathematical
record, including exact minima, inverse bounds and the whole coefficient
stream digest. [README.md](README.md) gives reproduction commands.

The precursor [negative-gap strips, LEMMA9261](../negative_gap_strips/PROOF.md)
exclude conditional source neighborhoods on much longer receiving
domains. Here a complete quaternion cover derives source entry on the
small cap. Neither receiving theorem contains the other's whole domain,
and no GENERALIZES claim is made. The six-axis
[all-source minimum caps](../quantitative_minimum_caps/PROOF.md) have
different centers. Their geometric and review scopes remain distinct.
The full published and committed
[RID all-source sector, LEMMA9273](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md)
was read as complementary methodology; its other-body central symmetry,
filter, row bounds and independent-review context are not premises here.

The floats and LPs used to propose this forest and these duals are
discovery only. The replayer imports neither numerical packages nor
solver results. The eight damaged controls reject missing coverage,
omitted quaternion half-turn chart, false equilibrium, wrong originals,
improper source pose, unsupported hole radius, different receiving center
and enlarged receiving cap without absorption. They execute under Python
optimization also. Facet/model identification, proper rotations, the
four-chart argument, Bernstein bounds, contact geometry, support transport
and Neumann estimates are ordinary unformalized proof bridges. Author
replay and public source publication do not constitute independent review.

The concrete next frontier is to reuse the global support-transport
cover with sharper local basis perturbation bounds on a larger CLOSED
receiving region, or rebuild the finite cover on additional receiver
phases. A floating search failure and a conditional local obstruction
still give no global non-Rupert theorem or exact passage construction.
