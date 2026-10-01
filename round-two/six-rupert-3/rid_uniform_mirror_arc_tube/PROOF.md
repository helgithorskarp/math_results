# A uniform receiving tube around the RID mirror arcs

**six-rupert-3, researcher; 2026-10-01.** Complete written geometric
intermediate proof with exactly checked polynomial hypotheses. Author-checked,
unformalized and independently unreviewed; no historical priority claim.
The global standard rhombicosidodecahedron (RID) Rupert question remains open.

## 1. Precise regions and conclusions

Let phi=(1+sqrt(5))/2. Let V be the sixty distinct independent signs and
even coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Then K=conv(V)=-K is the original standard edge-two RID, with common
original squared radius R^2=7+8phi<20. Let G be its sixty proper body
rotations, e=e_z, a=phi^2, c=2+phi and b=phi^3. Frames B are real
orthonormal-row 2-by-3 matrices, whose oriented kernel normals are the
cross products of their rows. Completing them by these normals gives
proper spatial frames. Proper planar rolls and physical translations
are retained. All normal distances below are unit-normal **chords**;
all matrix norms are Euclidean operator norms and all full rotation
angles are in radians. The parameter s is a tangent, not a chord or sine.

Put n_j(s)=(e+s e_j)/sqrt(1+s^2), j=x,y, and define

    M = union over g in G, j=x,y, 0<=s<=1/12 of g n_j(s),
    N = union over g in G, j=x,y, 1/300<=s<=1/12 of g n_j(s),
    D = 1/2000000.

Both sets are compact. The proper group includes diag(-1,-1,1), so both
signs of each mirror tilt occur. No count of distinct curve components
or redundant frame representations is asserted.

**Theorem.**

1. For every receiving frame B2 with dist(n2,N)<=D, every source frame
   B1, every physical t in R^2 and every lambda>=1,

       lambda B1 K+t subseteq B2 K
         iff lambda=1, t=0, B1=sigma B2 g (sigma=+1 or -1, g in G).

   All sources and full rolls are initially arbitrary. The receiver is
   in a tube about a continuous positive-tilt interval, with boundaries
   and reference centers included.
2. For every receiving frame with dist(n2,M)<=D, every source frame,
   every physical t and every lambda>=1,

       lambda B1 K+t is not contained in int(B2 K).

   This second conclusion is **strict exclusion only**. No classification
   of every closed fit is asserted on the near-zero remainder.
3. At any fixed reference g n_j(s), 0<s<=1/12, the separate local
   contact box has receiving chord <=s/80 **and** full relative proper
   rotation angle <=s/40. Every closed fit in this box is the identity
   relative motion, unit scale and zero translation. Both initial
   hypotheses apply to this local box. For 1/300<=s<=1/12 it contains
   the uniform box with receiving radius1/24000 and angle1/12000.

Uniform rescaling, including unit edge length, preserves all statements.
These are receiving subsets, not a full-sphere or global non-Rupert proof.
Part 1 does not enlarge the previously published endpoint cap1/15000;
its new feature is the continuous parameter interval. Part 2 increases
the previously certified whole-M strict tube1e-38 to D.

## 2. Published inputs and exact computation boundary

The direct [endpoint proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_endpoint_contact_caps/PROOF.md),
source922c24093cbd2e637bb8f0a7bcea06b28b7dcabe, graph
`bafkreibydvv4zcxs6sw73dq42unip64jsintm3hq7yrbvgnammf3yifz2i` at8903,
supplies the actual probe coordinates and the quadratic retained-normal,
summed-radial and reflected-area mechanism. The parameter certificates
and uniform nonzero-tilt bounds below are new extensions of that work.
The general support-torque method is credited to the earlier
[torque proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md),
graph7138 `bafkreig3erec7rq3afffflefrepyeb2blvwiguqw2fxj6ntte6wc7g6bfq`.

The [tube proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_arc_tube_control/PROOF.md),
source19ea97d41b421428fe3b96b24a9270fa96c09f2d, graph8853
`bafkreiern5qzomxijvp7vkbyazugkt3bzazsmxlth4xn5wduxbpyzzlsfy`, gives
actual-original matching and nearly-fixed-row geometry on both entire
mirror families. The [arc proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md),
source18e9736df5624f44a22d929699d585138f4b7483, graph8833
`bafkreia32nj6ojbdmq2ndloqbxt57h5mzspoe6wko7gwi36dlp4fxfyc3m`, proves
the whole reference-interval area/width formulae and exact center rigidity.
The [width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89, graph8732
`bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi`, is the
full-source localization premise. The [brightness source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
source58824907716016ff519f2aa5430fef92aa78c62c, graph8555
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`, supplies
original geometry, all physical Cauchy generators and proper group.

Part 2 also uses the [quadratic twofold-cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md),
source dc752d2b996ffc77ff2a24e6c05c3bbaa426f6ad, graph8613
`bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi`:
EVERY strict passage at a receiver within chord1/270 of Ge is excluded,
with arbitrary source, full roll, translation and scale>=1. Its scope
explicitly does not classify touching closed fits. Actual-original
matching credits the [fivefold proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md);
physical Cauchy/polar geometry credits the earlier
[J77 method](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).

DEPENDENCIES.json pins five mathematical endpoint files and four twofold
files. The checker first reproduces both COMPLETE expected records, with
their full transitive source fingerprints. The old uniform-local1e-16
record is inherited in this replay but its mathematical angle conclusion
is not used. A separate sequential child isolates the twofold check;
the parent waits, so only one CPU-intensive local job runs at once.
PARAMETERS.json holds compact literal actual-original probe polynomials.
All new signs and polynomial coefficients use ordered exact Q(phi) and
Fraction. The continuum proof and dependency proofs are unformalized.

## 3. Two actual four-probe families on every positive tilt

For each of the eight vertex/probe pairs in the endpoint source keep
the vertex v and the x,y probe components fixed. Replace the third
component by m_z(s)=-s m_j, j=x or y. Explicitly:

| family,index | actual v | physical m(s) |
|---|---|---|
| x,0 | (-a,-c,0) | (-phi,(13-25phi)/12,s phi) |
| x,1 | (-1,-b,1) | (1-phi,-25/12-phi,s(phi-1)) |
| x,2 | (1,-b,-1) | (phi-1,-25/12-phi,s(1-phi)) |
| x,3 | (a,-c,0) | (phi,(13-25phi)/12,-s phi) |
| y,0 | (-a,-c,0) | (-(1+11phi)/12,1-2phi,s(2phi-1)) |
| y,1 | (-1,-b,1) | (11/12-phi,-c,s c) |
| y,2 | (1,-b,1) | (phi-11/12,-c,s c) |
| y,3 | (a,-c,0) | ((1+11phi)/12,1-2phi,s(2phi-1)) |

These are perpendicular to the ACTUAL reference normal n_j(s), and
are physical spatial probes, with no unaccounted projection Jacobian.
For every actual w!=v define the affine polynomial

    g_w(s)=m(s).(v-w)-s.

The checker verifies g_w(0)>=0 and g_w(1/12)>0 for EACH of the472
original support comparisons. Affinity makes g_w(s)>0 for0<s<=1/12.
Thus all actual support gaps exceed s, including comparisons with
hidden or collinear originals. Each squared probe norm is convex in s
and is strictly below16 at both endpoints; hence ||m(s)||<4 throughout.

Put tau_i(s)=v_i cross m_i(s). Exact polynomial balancing weights are
(w0,w1,w1,w0), with

    x: w0=(phi-1)(1-s),       w1=phi^3 s;
    y: w0=1-phi^3 s,         w1=(2phi-1)s.

Each is strictly positive on0<s<=1/12; direct coefficient identities
give sum_i w_i(s) tau_i(s)=0. The oriented affine torque determinant
has strictly positive exact Bernstein coefficients over[0,1/12], so
the four torques are affinely independent, including for positive s.

For every triple of torques define N=(tau_l-tau_i) cross(tau_r-tau_i)
and h=N.tau_i. The checker expands exactly

    p(s)=h(s)^2-s^2 ||N(s)||^2.

After removing a factor s^2 where present (the other cases remove no
factor), EVERY Bernstein coefficient of the remaining polynomial on
[0,1/12] is strictly positive. The output contains the full power and
Bernstein coefficients of all eight facet inequalities and both affine
determinants, not an empirical grid or only aggregate counts.

For completeness, for p(s)=sum_k a_k s^k of degree d, write s=t/12.
The Bernstein coefficients are

    beta_i=sum_{k<=i} a_k (1/12)^k C(i,k)/C(d,k).

The exact identity p(t/12)=sum_i beta_i C(d,i)t^i(1-t)^(d-i)
follows by expanding the binomial basis. The basis functions are
nonnegative and sum to1 on[0,1]. Positive coefficients therefore prove
strict positivity on the entire closed interval. The removed s^2 is
strictly positive for the stated positive-tilt domain. Polynomial degree
and every coefficient are computed exactly; no floating sign is used.

Positive balance plus affine independence puts zero inside each torque
tetrahedron. Every facet distance exceeds s by p(s)>0. Thus its entire
closed ball of radius s is in the interior. At s=0 the balancing weights
need not all be positive and the ball bound vanishes; no rigidity at
zero is inferred from this family certificate.

## 4. Parameter-scaled closed local box

Fix0<s<=1/12 and an actual receiver n with ||n-n_j(s)||<=d0<=s/80.
Project the probes into its actual row plane:

    m'_i=m_i-(m_i.n)n,  ||m'_i||<4, ||m'_i-m_i||<4d0.

Since ||v-w||<=2R<10, each same actual original remains uniquely
supporting: m'_i.(v_i-w)>s-40d0>=s/2>0. Perturbations to both sides
of the mirror plane are included; a collapsed facet need not persist.

Let a closed fit lambda B QK+t subseteq BK have Q in SO(3),lambda>=1
and full angle0<theta<=s/40. By central symmetry, negating/averaging and
then contracting toward zero gives BQK subseteq BK without changing Q.
For its unit spatial rotation axis omega, each actual support inequality
is m'_i.(Qv_i-v_i)<=0. The exact exponential remainder has norm<=theta^2/2,
so R||m'_i||<20 gives

    omega.(v_i cross m'_i)<=20 theta/2,
    omega.tau_i <20(d0+theta/2)<=s/2<s.

This contradicts the torque ball of radius s, whose support in the unit
direction omega is at least s. Thus Q=I. Original central support
inequalities lambda h(zeta)+|zeta.t|<=h(zeta), h(zeta)>0 in every unit
planar direction, force lambda=1 and t=0. Proper body folding proves
the same result at g n_j(s), for every common planar gauge.

For s>=1/300 choose d0=1/24000 and theta0=1/12000. These are respectively
s_min/80 and s_min/40. BOTH hypotheses define this uniform local box;
the next sections prove that arbitrary sources enter it at radius D.

## 5. Full-source localization and actual matching on the whole interval

Take an actual closed fit and dist(n2,N)<=delta,0<delta<=D. Compactness
chooses a proper reference g n_j(s), s_min<=s<=s_max. Fold the receiver
by g and choose the common proper planar gauge so it differs from the
locked reference frame by at most delta. Source body folding is
independent. Put u0=s/sqrt(1+s^2)>1/301 and k!=j.

The reference physical area is

    A(n_j(s))=(A0+H_j s)/sqrt(1+s^2),
    A0=12+28phi<58, Hx=4+8phi, Hy=8+4phi, 14<H_j<17.

The actual perpendicular width direction is (phi,1,-phi s) for x
and (phi,1,-s) for y. Its squared width is

    w_j(s)^2=4(B+k_j s)^2/(S+ell_j s^2),
    B=3phi^2, S=phi+2,
    (k_x,ell_x)=(phi^2,phi^2), (k_y,ell_y)=(phi,1).

The arc proof checks its support against all originals throughout by
affinity. Area and width increase on[0,1/12]: their derivative signs
are H_j-A0 s and k_j S-ell_j B s, respectively, positive at the upper
endpoint and hence everywhere. The endpoint proof supplies the stronger
endpoint margins>1/50 below A1+1/4 and below the filter's squared-width
threshold, with A1^2=940+1520phi and w_j<9. They therefore hold on the
ENTIRE reference interval. Physical area is250-Lipschitz; transporting
one directional width changes its square by<180delta+100delta^2.
Our exact D gates preserve both filter margins. EVERY source normal
therefore folds to chord<1/8 and transverse norm<3/25 from e, with no
initial source/roll assumption.

Since D<1e-6, the tube proof Sections4–5 apply directly within their
proved receiving domain, uniformly to such references. To spell
out their finite hypotheses: receiving nonequatorial heights exceed
3/5-5delta, whose squares are>1/3>36/125; source equatorial radii squared
exceed R^2-36/125; actual equatorial support matches are within11/20;
both equatorial singular values exceed24/25. The original unequal-side
and determinant gates leave only identical or antipodal labels. Absorb
the antipodal choice by a proper planar source half-turn. Quadratic
equatorial transport plus one actual match gives full initial row-frame
error<1473/5632+(25/22)delta<4/15, including initially arbitrary roll.

For the source's nearly fixed row r, support on the four actual originals
with coordinate b and independent signs elsewhere gives

    b r_k+sum_{i!=k}|r_i|<=b+5delta.

Consequently r_k>9/10, q=||(r_i)_{i!=k}||<14delta and
||r-e_k||<16delta. Let H be shortest proper rotation sending e_k to r.
Writing nu=(n1)_k, orthogonality n1.r=0 gives |nu|<16delta and the exact
corrected normal formula

    n1'=H^t n1=n1-nu(r+e_k)/(1+r_k).

Its k coordinate vanishes, while the retained j and z coordinates change
by<120delta^2. The corrected source frame B1'=B1 H costs<16delta,
is mirror-locked, and has n1'=z'e+u'e_j, |u'|<123/1000,z'>24/25 and
normal chord<1/4. Containment of this corrected source is NOT assumed.
These implications and the parameter-free quadratic identity are proved
in the cited tube/endpoint arguments; every scalar budget is rechecked
at D and the entire reference parameter domain here.

## 6. Uniform linear lower and upper tilt bounds away from zero

Let v=|u'|. Summing all FOUR matched actual equatorial radius inequalities
cancels their mixed products and gives

    a^2(n1)_x^2+c^2(n1)_y^2 >= a^2(n2)_x^2+c^2(n2)_y^2.

This does not assume common off-arc target radii or invented preimages.
The retained coefficient squared is>6 and the other<20. Dropping the
nonnegative target k term, using |nu|<16delta and the<120delta^2 retained
correction, yields

    v^2>(n2)_j^2-1100delta^2 >=(u0-delta)^2-1100delta^2.

Since s>=1/300, u0>1/301 and u0-delta>1/302. If v<u0-delta, divide
the squared difference by u0-delta+v>1/302; otherwise the conclusion
is immediate. In either case

    v>u0-delta-332200delta^2>u0-2delta,

because1+332200D<2. This is the newly uniform positive-interval gate;
no division by an unboundedly small or zero mirror tilt occurs.

The physical Cauchy formula is A(n)=sum_{c in C}|c.n|, with31 original
paired-facet area vectors. The six with c_z=0 are reflection-even in
either transverse coordinate; the others have signed sum A0 e and
normalized z heights>1/4. Convexity and reflection give equatorial
support >=H_j |n_j|. The quadratic retained-coordinate correction
therefore gives

    F_j(v)-A(n1)<9000delta^2,
    F_j(w)=A0 sqrt(1-w^2)+H_j w.

The actual receiving equatorial j signs persist over this whole positive
interval: (n2)_j>1/301-delta, |(n2)_k|<=delta, and every exact sign gate
|c_j|(1/301-D)>|c_k|D holds. Their signed nonzero-j sum is H_j e_j;
the remaining pure-other coefficient is exactly4. Thus

    A(n2)<=F_j((n2)_j)+4delta<F_j(u0)+21delta.

On0<=w<=123/1000, F'_j(w)>6 and F'_j(w)<17. Centered unit containment
has A(n1)<=A(n2), so

    v<u0+(21delta+9000delta^2)/6<u0+4delta.

Together, |v-u0|<4delta. All source and target comparisons are physical
areas; reflection and exact target signs are needed to retain the
quadratic source correction.

## 7. Entering the contact box and recovering the original fit

Locked mirror frames are<2-Lipschitz in the sine tilt on this domain.
Negative corrected tilt is absorbed by the exact proper-body identity
C_negative=-C_positive diag(-1,-1,1). Adding corrected tilt error,
proper row correction and actual receiver transport gives some sigma,g

    ||B1-sigma B2g||<8delta+16delta+delta=25delta.

Complete the row frames to F1,F2 in SO(3) and set Q=F2^t F1. Row error h
gives completed-frame error<3h. In the positive branch use Qtilde=Qg^-1;
in the negative branch use Qtilde=J_n2 Qg^-1, with
J_n2=2n2 n2^t-I in SO(3). Since B2 J_n2=-B2 and K=-K, both branches
preserve the ACTUAL source shadow, original lambda and physical t.
The reference for the negative branch is F2 J_n2 g, a proper frame.
Hence ||Qtilde-I||<75delta and, using2sin(theta/2) and pi<4,

    full_angle(Qtilde)<150delta<=150D<1/12000.

The actual receiver is within D<1/24000 of the same positive reference.
The uniform contact box in Section4 forces Qtilde=I,lambda=1,t=0.
Undoing the proper changes gives exactly B1=sigmaB2g. Conversely gK=K=-K
gives equality for those values. Choosing positive delta=D covers exact
reference centers and all tube boundaries without taking a zero-parameter
limit. This proves part1.

## 8. Cover the complete mirror union, keeping closed and strict scopes

Suppose dist(n2,M)<=D and select a nearest reference g n_j(s). If
s>=1/300, part1 classifies every closed fit, hence excludes strict fits.
If0<=s<1/300, the reference chord from ge is at most s, so

    dist(n2,Ge)<=D+s<1/2000000+1/300<1/270.

The existing all-source twofold-cap theorem excludes every strict fit
there. Its strict conclusion is all that is used. This proves part2
with no unproved transfer of a closed-fit classification near zero.

## 9. Reproduction and remaining frontier

From the repository root, Python3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_uniform_mirror_arc_tube/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_uniform_mirror_arc_tube/check.py
```

Both must equal the entire expected.json record. All guards remain active
under optimization. The exact Bernstein tables, original support checks,
physical sign gates, full prerequisite outputs and damaged controls form
a finite certificate of the stated hypotheses. The continuum reduction
above remains a written geometric argument, not an independent review or
formal proof. No floating passage search, solver failure, timeout or
incomplete enumeration is nonexistence evidence.

Current primary seeds [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
and [Zeng](https://arxiv.org/html/2604.26531) leave the global standard RID
question unresolved. This result supplies a continuous quantified
receiving region. The macroscopic complement, nonlocal passages and a
complete receiving-sphere cover remain unresolved. A useful next step is
to identify the next actual-original support event beyond these mirror
regions and derive a new all-source reduction there, rather than merely
improve this tube constant again.
