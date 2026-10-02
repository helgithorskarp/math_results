# Moment entry and the uniform critical-energy scale of the boundary branch

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary analytic proof with exact checks of the stated constants;
unformalized and independently unreviewed at publication.

The uniform normalized collar is the credited result
[9373](../normalized-neighborhood/PROOF.md). We prove stronger physical entry
conditions by recovering total critical moments before estimating individual
roots. The coefficient-radius exponent improves from eta13 to eta7. More
substantively, an explicit disk-rooted inward-motion family proves that
eta3 is the sharp power for **unweighted critical energy to force entry into
this fixed displayed normalized collar**, uniformly as eta tends to zero.
It gives the same necessary power for original energy; the sufficient
original-energy power here is14, so that optimal power remains open.
No statement about global concentration or a global branch minimum follows.
The fresh independent [9388 review](../../six-reviewer-3/numerical-neighborhood-audit/REVIEW.md)
confirms the older9315 numerical theorem and gives its own conservative
eta76 refinement. It explicitly gives no verdict on the stronger9373
collar; no verdict transfers to either9373 or this new entry theorem.

## 1. Conventions, credited premises and conclusions

Let `0<eta<=e=1/65536`, `a=1-eta`. The actual monic branch is

    p0'(z)=9(z-r)^6[(z-eta y0)^2+eta T0], p0(a)=0,
    r=eta x0, 1<T0<2, |x0|,|y0|<2.

Its existence and feasibility on this entire interval are credited to
[9113](../validated-boundary-branch/PROOF.md), independently confirmed in
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md). It has nine
simple original roots: the marked a, four unit roots labelled upper/lower3,4,
and four other unmarked interior roots. Their initial half-normals are
less than `-eta/4`. Define `F(p)=sum8 1/|a-zeta_j|`; multiplicities count.
A zero reciprocal denominator means infinity. All entry conditions below
keep the criticals near0 and thus have finite F.

For `0<=k<L_eta=1/2-33eta/16`, put `delta=L_eta-k>0`. Retain9373's

    b=2^-227, R=delta 2^-320, t=delta 2^-322.

For six free critical pairs and a heavy pair use the literal real coordinates

    zeta_j=eta u_j+i sqrt(eta)h_j,
    y=(u_+ +u_-)/2, T=(h_+^2+h_-^2)/2,
    V=sum_all h/eta, M=sum_all h*u.

The reference raw tuple is `(0^6,x0 1^6,y0,T0,0,0)`. These coordinates
are permutation invariant among the six small criticals; no differentiable
labels are assumed at their collision. The heavy signs are fixed by their
positive/negative imaginary parts. In9373 the four independent actual
original half-normals, slacks and normalized normals are

    alpha_k^±=(|Z_k^±|^2-1)/2, sigma_k^±=-alpha_k^±,
    beta_k=(alpha_k^+ +alpha_k^-)/(2eta),
    gamma_k=(alpha_k^+ -alpha_k^-)/(2eta^(3/2)).

Its displayed collar is the free Euclidean ball R and the normal maximum
box b, with feasibility `beta_k<=-sqrt(eta)|gamma_k|`. Its complete tail
inverse is valid on the larger target product d=2^-92 and tail s=2^-52.
Every disk-rooted monic p anchored at a whose raw maximum distance is at
most t satisfies the credited inequality

    F(p)-F(p0)>=k eta^2 D+(1/4)sum4 sigma,
    D=sum6 h_j^2+sum6(u_j-x0)^2.                         (1)

The stronger slack weight17/64 is also valid. We change the sufficient
physical entry conditions, not this previously proved inequality.

For two eight-element multisets define the squared matching energy by the
minimum over all permutations of the sum of squared complex displacements.
Let Ecrit match all criticals to those of p0, with multiplicity, and let
Eorig match the eight unmarked originals to p0, keeping the same a fixed.

**Entry theorem.** For every disk-rooted monic degree-nine p with p(a)=0,
each of the following is sufficient for(1):

    C=max0<=j<=8 |c_j(p)-c_j(p0)|
                            <=delta^6 2^-1999 eta^7;             (2)
    Ecrit                  <=delta^2 2^-664 eta^3;               (3)
    Ecrit                  <=delta^2 2^-664 eta^2,
    |Im(sum8 zeta_j)|       <=eta^(3/2)t/128;                     (4)
    Eorig                  <=[delta^6 2^-1999 eta^7/200]^2.       (5)

For real-coefficient p the trace condition in(4) is automatic. For k=1/4
simple sufficient bounds in(2),(3),(4),(5) are respectively

    C<=2^-2017 eta^7,
    Ecrit<=2^-670 eta^3,
    Ecrit<=2^-670 eta^2 with the same trace condition,
    Eorig<=2^-4050 eta^14.                                      (6)

**Uniform scale obstruction.** There is an explicit family of monic
polynomials p_v for every positive eta in the entire interval, all nine
original roots strictly inside the unit disk and still p_v(a)=0, such that
the actual normalized original normals obey

    max(|gamma3|,|gamma4|)>2b,
    (257/2)eta^3 v^2<=Ecrit(p_v)<=129eta^3 v^2,
    (20817/512)eta^3 v^2<=Eorig(p_v)<=2^29 eta^3 v^2,
    v=4096b=2^-215.                                           (7)

Consequently, for either unweighted matching energy, no fixed constant
`A>0` and exponent `q<3` can make `E<=A eta^q` universally imply entry
into9373's displayed normalized normal box for every sufficiently small
positive eta. Together with(3),(6), this identifies the critical-energy
power3; the constants are not claimed optimal. The family violates an
entry criterion, not the first-power conjecture or a stability inequality.

## 2. Exact total moments remove the balance loss

Write `p(z)=z^9+sum0..8 c_j z^j`. The monic critical polynomial p'/9 has
first two elementary critical coefficients `e1=-8c8/9`, `e2=7c7/9`.
The first two Newton sums are exactly

    S1=sum8 zeta_j=-8c8/9,
    S2=sum8 zeta_j^2=S1^2-14c7/9,
    V=Im S1/eta^(3/2), M=Im S2/(2eta^(3/2)).                    (8)

These are identities for all complex polynomials and all critical
collisions. Newton identities themselves are standard; the new use is
the scale-aware recovery in the quantified9373 chart.

On the branch S1 is real and |S1|<16eta. If C<eta, (8) gives

    |Delta S1|<=8C/9,
    |Delta S2|<[(8/9)33e+14/9]C<2C,
    |V|<C/eta^(3/2), |M|<C/eta^(3/2).                        (9)

For Delta S2 use `2|S1^0|+|Delta S1|<33eta`; the imaginary part of the
branch S2 is zero. Bounding each imaginary displacement and then dividing
its total by eta would lose a further eta power. Formula(8) avoids that.

## 3. Collision-safe eta7 coefficient entry

Set `lambda=eta t/1024`, `C7=eta lambda^6/128`, so

    C7=delta^6 2^-1999 eta^7.                              (10)

This retains the collision-circle mechanism of9373 (and credited9315);
only the balance/mixed-moment recovery changes. All branch critical moduli
are below1/32. The heavy centers have separation greater than2sqrt(eta),
and distance from r greater than sqrt(eta). Draw three disjoint lambda
circles, one about r and one about each heavy center. Their boundaries lie
in |z|<1, and lambda<eta/4. On the small circle,

    |p0'|>9lambda^6(sqrt(eta)/2)^2>eta lambda^6.

On each heavy circle,

    |p0'|>(9/64)eta^(7/2)lambda>eta lambda^6.

The last comparison is uniform since lambda^5<(9/64)eta^(5/2).
For C<=C7, on all three circles

    |p'-p0'|<=36C<eta lambda^6.

Rouche gives six small criticals with multiplicity and one in each heavy
disk, exhausting all eight. Literal real and imaginary parts then give

    |Delta u|<=t/1024, |Delta h|<=sqrt(eta)t/1024,
    |Delta y|<=t/1024, |Delta T|<5t/1024.                     (11)

For T use |h0|<2 and the exact difference of squares. On the entire
positive eta/gap window the exact positive-monomial comparison in(9),(10)
gives `|V|,|M|<t/1024`. Thus every one of the sixteen raw coordinates is
within t. Positive heavy ordering recovers the literal chart, and monicity
plus p(a)=0 recovers the same anchored p. The complete uniqueness part
of9373 identifies it with the eliminated tail; (1) follows. This uses
neither critical labels at collisions nor a real/conjugate assumption.

The previous coefficient radius was `delta^6 2^-1999 eta^13`, so(2)
strictly enlarges it by the factor eta^-6 on the entire positive interval.
For k1/4, delta>1/8, proving its bound in(6).

## 4. Critical and original energy entry

The minimizing permutation is finite and exists. Under(3) each matched
critical displacement is at most `eta^(3/2)t/1024`. Hence

    |Delta u|<=sqrt(eta)t/1024,
    |Delta h|<=eta t/1024,
    |V|<=8t/1024, |M|<40t/1024.                              (12)

The M bound uses eight terms in the exact change of h*u, each bounded
by `2|Delta h|+2|Delta u|+|Delta h Delta u|`. Heavy y and T have the
bounds in(11). The heavy and small separations identify the matched
clusters and heavy signs without extra analytic labelling. Thus raw entry
and(1) hold directly, bypassing coefficient-root Holder conversion.

Under(4) each displacement is at most `eta t/1024`. The free u bound
in(11) and h bound `sqrt(eta)t/1024` still hold, as do the T and M bounds.
The separate exact total trace now gives `|V|<=t/128=8t/1024`; this
proves raw entry for the eta2 criterion. Real coefficients imply S1 real.

For originals in the unit disk, telescope each elementary symmetric
product after matching the eight unmarked roots and leaving a fixed.
The coefficient difference is at most `binom(8,j-1)sum8 |Delta Z|`.
The largest binomial is70 and `sum|Delta Z|<=sqrt(8Eorig)`, giving

    C<200 sqrt(Eorig).                                      (13)

This elementary conversion retains9373's credit. It proves(5) from(2),
and since200<256 proves the simple eta14 original-energy bound in(6).
No energy here is measured relative to an antipodal or collapsed profile.

## 5. An explicit feasible original-root inward motion

Set v=4096b once, independently of eta and k. Leave the six free h zero
and u=x0, and take

    y=y0+8sqrt(eta)v, T=T0, V=v, M=eta v y,
    mh=eta v/2, q=sqrt(T0-eta^2 v^2/4),
    zeta_±=eta y+i sqrt(eta)(mh±q).                          (14)

Define p_v by integrating its eight critical factors and anchoring at a.
The square root is positive, the heavy pair separated, and the six-fold
small collision unchanged. We next prove all original roots interior;
feasibility is not inferred from small critical energy.

For this purpose put xi=sqrt(eta)v but treat eta and xi independently
as complex variables. Freeze the real actual branch parameters x0,y0,T0
at the chosen real eta. For `y=y0+8xi`, the entire critical polynomial is

    Q(z)=(z-eta x0)^6 [z^2-eta(2y+i xi)z
                     +eta T0+eta^2(y^2+i xi y-xi^2/2)].        (15)

This expression has no singularity in eta or xi. It is exactly(14) when
xi=sqrt(eta)v. Use the complex product

    |eta|<1/1024, |xi|<1/64,
    |x0|,|y0|<9/8, 1<T0<25/16, |y|<5/4.                    (16)

The stronger actual branch bounds in(16) follow from the unchanged
certified branch covering cube. They are checked in [checks.py](checks.py).

For transparency set h=1/1024, j=1/64, X=9/8, Y=5/4, B=25/16,
`B1=2Y+j`, `B0=Y^2+jY+j^2/2`. If E_k is the coefficient of z^(8-k)
in Q (sign irrelevant for its bound), then throughout(16)

    |E_k|/|eta| <= binom(6,k) X^k h^(k-1)
                 +binom(6,k-1) X^(k-1) B1 h^(k-1)
                 +binom(6,k-2) X^(k-2)[B h^(k-2)+B0 h^(k-1)], (17)

where impossible binomial indices and their terms are omitted. Integrate
9Q from a=1-eta. With z bound17/16 and a bound1+h, the exact anchored
majorant (including the constant term) is

    |p(eta,xi,z)-(z^9-1)| <= P |eta|, P<64.                (18)

Its complete rational value is regenerated, not fitted. On each circle
of radius1/16 about a fixed ninth root, the baseline lower bound is
`9/16-36(17/16)^7/256>1/4`, whereas `64/1024=1/16<1/4`.
Rouche therefore gives a unique simple holomorphic original-root section
in each of nine disjoint disks on the entire complex product(16).
The marked section is exactly a for all xi, by the anchor.

To define the holomorphic half-normal for a section, multiply it by its
conjugate companion section: the companion polynomial has i replaced
by -i in(15), with y=y0+8xi unchanged, and its fixed root label reversed.
For real eta,xi this product is exactly |Z|^2. Both polynomials have(18).
The companion half-normal alpha is bounded by2 and vanishes at eta0
for every xi. Removable division and the maximum-modulus principle yield

    |alpha/eta|<=2^11.

On |xi|<=1/128 its first two xi derivatives are bounded respectively by
2^18 and2^26, using the xi Cauchy radius1/128. These bounds apply to
every original label, not only the active four.

At the chosen actual branch xi=0, use the credited normalized radial
blocks J and G=diag(sin theta)O of
[9267](../radial-slack/PROOF.md), independently confirmed within its
pointwise scope by [9335](../../six-reviewer-3/radial-slack-audit/REVIEW.md).
At free h0 the conjugation parity gives beta_V=beta_M=0 and
gamma_y=gamma_T=0. Both J_y entries are strictly less than -1/3;
all entries of G have absolute value below1. The exact chain rule along
(15), since V=xi/sqrt(eta), M=sqrt(eta)xi(y0+8xi), gives

    (1/eta) d alpha_k^±/d xi at0
                =8J_(k,y)±[G_(k,V)+eta y0 G_(k,M)]<-3/2.   (19)

There is no assumed sign of an individual odd entry in this estimate.
For `0<xi=sqrt(eta)v<=v/256<2^-26`, Taylor's theorem with the full
2^26 second-derivative bound implies every active alpha is less than
`-eta xi`. Every inactive unmarked alpha varies by less than
`eta 2^18 xi<eta/8`, retaining its initial bound below `-eta/4`.
The marked a is also interior. This proves all nine roots of p_v
strictly inside the unit disk for every eta in the stated interval.

## 6. The same family leaves the displayed normal box

The credited tail inverse has maximum-norm bound800. Thus its normalized
odd block G has `max_k |G_(k,V)|>1/800`: apply the inverse to the unit
V vector. Since |G_(k,M)|<1 and |y0|<9/8,

    ||G_V+eta y0 G_M||_infty>1/800-e(9/8)>1/1024.           (20)

In the literal raw chart of9373, (14) has maximum displacement exactly
v, because `8sqrt(eta)<1` and `eta|y|<1`. Its complete segment lies
in the inner joint domain. The normalized second operator derivative
bound2^39 from9373 therefore bounds the second-order remainder by
`2^38 v^2`. The nonlinear part of M contributes at most
`8eta^(3/2)v^2`. Combining these with(20) and `2^39 v<1/2048` gives

    ||gamma(p_v)||_infty>v/1024-2^39 v^2
                       >v/2048=2b.                       (21)

This is an actual original-root normal, not a leading formal jet.
All original labels in the two joint charts agree by uniqueness in their
fixed ninth-root disks. Equation(21) proves failure of displayed collar
entry, even though the polynomial is feasible by section5.

## 7. Both physical energies are of exact order eta3

The six small criticals are unchanged. Write q0=sqrt(T0),
`Delta q=q-q0=-eta^2v^2/[4(q+q0)]`. From(14) the two heavy shifts are

    Delta zeta_±=8eta^(3/2)v+i[eta^(3/2)v/2±sqrt(eta)Delta q].

The leading real/imaginary shifts and the opposite opening shifts cancel
their cross terms after summing the two squared moduli. Hence

    Ecrit=(257/2)eta^3 v^2+2eta(Delta q)^2,
    |Delta q|<eta^2v^2/4, Ecrit<129eta^3 v^2.                (22)

This is the minimum matching energy. Each heavy shift is less than
sqrt(eta)/4, the branch heavy-small distance is greater than sqrt(eta),
and the displayed matching costs less than eta/16. Any assignment
moving a heavy critical to the wrong cluster alone costs more than
9eta/16; a heavy sign swap costs still more. Thus a minimizing matching
must use the two corresponding heavy labels and the six small labels.

For original sections let `Delta Z(eta,xi)=Z(eta,xi)-Z(eta,0)`.
It vanishes when eta0 or xi0, is holomorphic on(16), and has modulus
less than1/8 since both sections are in the same1/16 disk. Twice removable
division and maximum modulus on the product give

    |Delta Z|<=2^13 |eta xi|.

The marked shift is zero, so the eight natural labelled originals give
`Eorig<=8(2^13)^2eta^3v^2=2^29eta^3v^2`. Conversely their total trace
is independent of any matching. By(8),(14),

    Delta sum8 Z=(9/8)(16+i)eta^(3/2)v,
    Eorig>=|Delta sum8 Z|^2/8=(20817/512)eta^3v^2.           (23)

For any A>0 and q<3, choose positive eta sufficiently small so that
`129v^2 eta^(3-q)<=A` (or `2^29v^2 eta^(3-q)<=A` for originals).
Equations(21)-(23) prove the obstruction claimed after(7).
No timeout, finite eta grid or numerical minimizer is used.

## 8. Reproducibility and limits

[verify.py](verify.py) hash-checks72 unchanged public input files, exactly
reproduces the full80-predicate9373 mathematical record, and regenerates
every new budget field in [expected.json](expected.json). It checks the
uniform positive monomials, first two Newton factors, complete anchored
family majorant, inward signs, full Cauchy/Taylor remainders, true matching
separation, and entry constants. Nine semantic damages must reject.
[VALIDATION.json](VALIDATION.json) records serial native-thread1 execution,
normal/optimized agreement and external fixture rejection controls.
These are reproducibility checks, not independent review or a formal kernel.

The new ordinary proof covers all positive eta in the stated window,
all permitted positive k-gaps, all complex disk-rooted competitors in the
entry sets, and small critical collisions. Standard Newton sums,
Rouche/matching/telescoping mechanisms,9373's uniform collar and9267's
radial blocks receive explicit credit. The new contributions are their
moment-aware quantified entry and a feasible inward-motion obstruction
establishing the uniform critical-energy power3. A larger physical original
entry criterion still needs additional information. Neither the coefficient
ball nor energy conditions route every low-F competitor. No positive
physical eta0 ball, unrestricted first-power theorem, global minimum or
optimal stability endpoint is asserted.
