# Fewer atoms by matching both Gaussian-smoothed marginals

Complete author proof; independent mathematical review is pending. The
unrestricted R3 Gaussian-majorisation question remains open. This replaces
the k^6 atom budget by O(k^3(1+log k)^(3/2)), preserving a uniform error of
order 1/k and giving compatible finite rational inputs. It supplies no
unknown Gaussian sign and no new Kneser--Poulsen consequence.

Finite-function cubature and local Gaussian moment matching are established
methods; [SOURCES.md](SOURCES.md) credits Bayer--Teichmann and Ma--Wu--Yang.
The application here matches BOTH marginals on the SAME actual source/image
pairs. Thus an arbitrary contraction is retained. No regularity beyond
Lipschitz continuity, polynomial representation of the map, or matching of
all six-dimensional joint moments is needed.

## 1. Explicit smaller compact frontier

Keep the unrestricted positive hinge defect D from
[DEFECT_LOCALIZATION.md](DEFECT_LOCALIZATION.md), normalized to variance one.
For an integer k>=1 put

    ell = ceil(log2 k),
    p_u = 2 ell+3,
    h = floor(sqrt(ell+1)),       n = ceil(k/h),
    p_w = 4 ell+8,
    M(p) = 2 binom(p+3,3)-1,
    A_k = min { k^3 M(p_u), n^3 M(p_w) }.                    (1)

All these integers are evaluated exactly in the companion code. Define
K^c_k as the original compact contraction parameter set, with at most A_k
labels in place of k^6: nonnegative weights of total one, x_1=y_1=0, both
radii at most 2k, and every |y_i-y_j|<=|x_i-x_j|. Zero weights and repeated
sites are allowed. Let E_k be its maximal positive hinge defect.

**Theorem 1.** The maximum exists and

    0 <= D-E_k < 11/(4k).                                  (2)

Moreover A_k=O(k^3(1+log k)^(3/2)). For a given violation of size delta,
k>=6/delta yields a bounded witness with at most A_k atoms and at least
half of that violation. Only the selected large cell and its rescaled
threshold depend on the violation; the subsequent approximation controls
all thresholds at once. No exact atomic optimizer for the original prior
problem is asserted.

The budget can be larger than k^6 at small k. For example the new values
at k=1 and k=4 are 39 and 15296. At k=100 it is 2279000000, versus the previous
1000000000000. At k=1000 it is 1551829411896, versus 1000000000000000000.
Neither range is a practical exhaustive-search proposal. The reduction
changes the asymptotic exponent and gives explicit finite bounds.

## 2. Simultaneous cubature on a contracted pair

Let a probability law mu be supported in a source cube of side b. Let c be
its center and d=T(c). If T was only specified on the support, first use
the same classical Kirszbraun extension premise as the old localization.
Both x-c and T(x)-d then have norm at most sqrt(3)b/2.

For integer p>=0 use the finite feature vector

    Phi(x) = (1, (x^alpha)_(1<=|alpha|<=p),
                  ((T x)^alpha)_(1<=|alpha|<=p)).            (3)

Its length is M(p). Caratheodory's convex-hull theorem supplies a probability
law nu on at most M(p) original source sites with the same expected feature
vector. Equivalently, apply finite-function cubature to (3). One can take
the compact original support intersected with the closed cube; including a
boundary site of zero conditional mass does not change the argument.
Repeated boundary sites from different cubes can be merged.

The paired law remains (x,T(x)) with common positive weights. Therefore all
pairwise contraction constraints are exact. Source and target moments,
separately, agree through degree p. Polynomial translation shows that their
moments about c and d agree as well. No source--target cross moments enter.
This construction is an application of classical cubature, not a new
Caratheodory theorem. It applies even to singular and nonatomic inputs.

For p>=2 it additionally preserves both marginal means and covariance
matrices. Consequently it preserves the ordered expected squared-distance
loss exactly, using

    E[|X-X'|^2-|TX-TX'|^2]
       = 2 tr(Cov(X)-Cov(TX)).                              (3a)

This applies to the combined cubature of a bounded law as well as to each
cell. It is a useful retained geometric quantity for the functional lane.
It concerns the law supplied to the compression step: earlier large-cell
conditioning can change it, and later rational rounding has its separate
error budget. Source--target cross moments and optimizing source sets are
not asserted to be preserved.

Here is a direct Gaussian estimate with every normalization specified.
Let mu and nu be any two probability laws in B(c,r) with moments agreeing
through degree p. Set sigma=mu-nu, f=mu*gamma_1, g=nu*gamma_1. Gaussian
multiplication gives

    integral (f-g)^2/gamma_1(z-c) dz
       = integral integral exp((x-c).(x'-c)) d sigma(x)d sigma(x').

For j<=p the degree-j term vanishes, since

    integral integral (u.v)^j d sigma(u)d sigma(v)
       = sum_(|alpha|=j) [j!/alpha!] (integral u^alpha d sigma(u))^2.

The exponential series is uniformly absolutely convergent on this compact
pair domain. Since the total variation norm of sigma is at most two,

    integral (f-g)^2/gamma_1(z-c) dz
       <= 4 sum_(j>p) r^(2j)/j!.

Cauchy--Schwarz and integral gamma_1=1 consequently imply

    TV(f,g) <= sqrt(tau_p(r^2)),
    tau_p(a) = sum_(j=p+1)^infinity a^j/j!.                  (4)

This is TV equal to half the L1 norm. Apply (4) to the source and target
moments in (3), with a=3b^2/4. The two endpoint TVs add to at most
2 sqrt(tau_p(a)). An equal-mass hinge changes by at most TV, as proved in
the old localization, so this bounds the change of their signed hinge
difference uniformly at every threshold. It also bounds every beta
average directly, without amplification by alternating coefficients.

## 3. Explicit tail schedules and the atom exponent

Whenever 0<=a<p+2, the exponential series has the elementary bound

    tau_p(a) <= U_p(a)
       := [a^(p+1)/(p+1)!] / [1-a/(p+2)].                   (5)

For unit cubes, a=3/4. The rational value U_3(3/4)=135/8704 is smaller
than 1/64. Increasing p>=3 by two multiplies U_p(3/4) by less than
(3/4)^2/[(p+2)(p+3)]<1/4. Thus, for p_u=2ell+3,

    tau_(p_u)(3/4) < 1/(64*4^ell) <= 1/(64k^2).            (6)

For the wider cubes, use b=k/n<=h, so a<=3h^2/4<=3(ell+1)/4 and
p=p_w=4ell+8. The elementary estimates e<3 and
q!>=(q/e)^q give, with q=p+1,

    a^q/q! < (9/16)^q,
    a/(p+2) < 3/16.

The factorial estimate follows by integrating log t from 1 to q; e<3
follows directly from its factorial series. The two exact rational facts

    (16/13)(9/16)^9 < 1/64,
    (9/16)^4 < 1/4

therefore prove

    tau_(p_w)(3h^2/4)
       < (16/13)(9/16)^(4ell+9)
       < 1/(64*4^ell) <= 1/(64k^2).                        (7)

Both choices hence cost less than 1/(4k) for the two endpoint hinges.
Use whichever count in (1) is smaller. The first option is useful at
moderate k; the second gives the improved logarithmic exponent. Indeed,
h>=sqrt(ell+1)/2, k>=h, and n<=2k/h<=4k/sqrt(ell+1). Also
M(p_w)<=(4ell+11)^3/3<=1331(ell+1)^3/3. In particular

    A_k <= (85184/3) k^3(ell+1)^(3/2).                     (8)

These constants are conservative. A_k need not be monotone at jumps of h;
no monotonicity of the new compact or rational maxima is used below.

## 4. Combining with the existing localization

The shifted source-grid lemma in the old proof supplies a conditional law
in one cube of side k, losing at most 3sqrt(2/pi)/k from a specified positive
hinge gap. Its physical threshold is correctly divided by that cell's
mass. The lemma charges only source overlap and requires no target
separation. It is a credited input; no averaging of unknown target signs
is introduced here.

Subdivide this large cube into k^3 unit cubes for (6), or n^3 equal cubes
for (7). In every occupied cell replace its conditional law using (3),
then retain the cell's original total mass. Convexity of TV makes the
total approximation cost a weighted average of the local costs. There
is no factor equal to the number of cells. The support count is at most
the corresponding value in (1).

All selected source sites lie in the closed original side-k cube. Choose
one of them as the common label anchor and separately translate both
endpoints. Their radii are <=sqrt(3)k<2k, because the original map remains
contracting. Thus the result belongs to K^c_k and the total loss is

    [3sqrt(2/pi)+1/4]/k < 11/(4k),                          (9)

using pi>3 and sqrt(6)<5/2. This proves (2) for each original law and hence
for the supremum D. The reverse inequality follows from admissibility.
Compactness and continuity, including collisions, zero weights and zero
threshold, are proved exactly as in the old finite parameter space with
its atom count replaced by A_k. The same integrable Gaussian envelope
applies. Attainment and the fixed-gap consequence follow. No relation
between optimizers for consecutive k is required.

## 5. Updated rational and beta contract

Apply R8's [support-only beta modulus](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
Theorem 2, at radius 2k. Its estimate depends on the radius, not the atom
count. The same row N=2^16 k^8-2 approximates each hinge defect on K^c_k
within 2/(3k). This is a credited degree bound, not an improvement in degree. The
coordinate-moment degrees p_u and p_w used for compression are distinct
from this Gaussian-density-power testing row.

Let R^c_k have the integer constraints of
[RATIONAL_INTERFACE.md](RATIONAL_INTERFACE.md), replacing the label bound
and weight denominator by

    m<=A_k,            W=4kA_k.                             (10)

Keep L=256k^3, X_1=Y_1=0, both integer radii <=3kL, and
|X_i-X_j|^2-|Y_i-Y_j|^2>=256k^2 for i!=j. Nonnegative integer masses sum
to W; decode endpoints by L and weights by W. Zero masses and coincident
target sites remain legal. The one-label pair constraint is vacuous.

The old merge--expand--round geometric proof is unchanged. With at most
A_k labels, largest-remainder weight rounding now has L1 error
<=A_k/W=1/(4k). Its combined hinge/beta cost is still <161/(256k).
One must use the NEW producer in paired_cubature.py, not silently apply
the old round_instance, which enforces k^6 labels and W=4k^7.

Define G_k as the largest negative beta magnitude on all of R^c_k at
row N. The same maximization and perturbation argument proves

    0<=D-G_k < 11/(4k)+2/(3k)+161/(256k)
              =3107/(768k).                                (11)

In particular k=ceil(9/epsilon) and a rigorous bound b_(N,j)>=-epsilon/2
for EVERY rational input and index give
D<6563epsilon/6912<epsilon. A violation delta>0 has a rational input and
index with b_(N,j)<-delta/2 whenever k>=9/delta. None is supplied here.

For any non-point member of R^c_k, the ordered expected squared pair loss
is at least

    2/[256k^4 W^2] = 1/[2048k^6 A_k^2].                    (12)

This improves the old denominator budget and its equality separation as
A_k becomes smaller, but does not itself prove a source-profile sign.
R8's current all-weight cell code still covers only N=5; its degree and
reference-margin obligations are not removed by this smaller atom bound.
A newer, separate [pair-conditioning proof](../gaussian_beta_pair_conditioning/PROOF.md)
signs every b_(N,j) with N-j<=6 for arbitrary bounded laws. Those indices
may be omitted from a sign search; the first remaining one is b_(7,0).
This optional analytic pruning is not a premise here and leaves many
indices of the required large row unsigned. An [independent geometric review](../gaussian_beta_geometry_review_r6/REVIEW.md)
accepts that strip, without reviewing this cubature theorem. No radius-2k
quantitative constant from the strip proof is silently
applied to the radius-3k rational family.

For a fully explicit enumeration bound, the number of ordered inputs is
at most

    A_k [(1536k^4+1)^6 (4kA_k+1)]^(A_k).                   (13)

Multiply by 2^16 k^8 for all configuration/index tests. Individual input
length is O(A_k log(kA_k)), rather than O(k^6 log k). The replica moment
formula now has at most A_k^q summands at power q. The old rigorous moment
precision requirement eta<=zeta/[(N+1)3^N] is unchanged. Exponentially many
configurations and cancellation at high degree remain substantial costs.
The separately reviewed bound D<=7/50 is not numerically improved here.

## 6. Reproduction and limitations

[paired_cubature.py](paired_cubature.py) implements exact finite-input
Caratheodory elimination and the updated rational producer. A separate
definition-level routine checks every retained marginal moment; it does
not trust the elimination history. Controls use a nonlinear absolute-value
contraction, zero weights, colliding sites and a point law. A source-only
moment match has a target-mean error 1/6, explaining why both feature lists
are necessary. Exact rational checks verify both tail schedules, budget
composition, and small Gaussian-kernel polynomial cancellations.

From this directory run:

    python3 -B paired_cubature.py --check
    python3 -B -O paired_cubature.py --check
    sha256sum -c SHA256SUMS

[CUBATURE_EXPECTED.json](CUBATURE_EXPECTED.json) is compact expected output;
[CUBATURE_INPUTS.json](CUBATURE_INPUTS.json) pins the reused source. The
program does not compute a Gaussian integral, beta sign, continuum optimum
or exhaustive parameter cover. Real-input cubature, Gaussian integration,
the support/TV argument and credited localization/moment proofs remain
written, unformalized mathematical premises. The finite elimination
algorithm is only an example implementation, not a practical algorithm
for all inputs at these worst-case budgets. All previous proof and code
files are preserved. No new positive map class or full-question settlement
is asserted.
