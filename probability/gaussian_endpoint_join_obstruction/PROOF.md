# A uniform obstruction to the proposed endpoint join

27 September 2026. Complete author proof; independent review pending.
This limits the stated certificate formulas. It asserts no adverse hinge,
failure of majorisation, or absence of other all-threshold proofs.

## 1. A geometric budget and necessary join condition

Work at variance one. Let X be an arbitrary bounded probability law and
Y=T(X) its contraction in R3. Assume

```text
|X-E X|<=R,       Cov(X)>=kappa I_3,       R,kappa>0,
d=E[|X-X'|^2-|Y-Y'|^2]>0,                K=2R^2/kappa.
```

Primes denote independent copies. A finite-cluster certificate consists of
finite center sets A={a_i}, Z={b_j}, a common cloud radius epsilon>=0, and
decompositions of the endpoint laws into positive-mass probability clouds
supported in B(a_i,epsilon), B(b_j,epsilon). Every assigned cloud mass is
at least w>0. The original map need not respect the cloud labels; the
decompositions may overlap, and individual clouds may be diffuse. Requiring
the same weights at both endpoints, as in R8's original interface, is
permitted but not needed for the budget below.

Write
`hbar(A)=integral_(S2) max_(a in A) theta.a d sigma(theta)`, where sigma
has total mass one. This is half the usual mean width and is invariant
under translations and orthogonal maps. Take ANY bounds

```text
0<delta<=hbar(A)-hbar(Z)-2epsilon.
```

Let r bound all center norms plus epsilon after arbitrary independent
translations. R8's existing finite-cluster tail schedule is

```text
B>=6r^2+2 log(1/w),             Q>=4B/delta,
H(u)>=0 for 0<u<=exp(-Q^2/2),                             (1)
```

where `H(u)=integral(g-Cu)_+-integral(f-Cu)_+`, C=(2 pi)^(-3/2).
Conservative increases of B or Q are allowed. The finite-law
case is epsilon=0, with w a positive atom-mass floor; that specialization
has independent acceptance. The incompatibility concerns the formula,
including its cloud version, and does not question the sign theorem.

**Geometric budget.** Every such input satisfies

```text
w delta^2<=Kd,             delta<=R,             r^2>=3kappa. (2)
```

Center both laws and Procrustes-align Y, transporting their cloud centers
by the same respective rigid motions. Accepted rigidity gives
`M=E|Y-X|^2<=E Delta^2/(2kappa)`. Since contraction gives
`0<=Delta<=4R^2`, it follows that M<=Kd. The average of h_A-h_Z is at
least delta+2epsilon, so there is a unit direction theta with
`h_A(theta)-h_Z(theta)>=delta+2epsilon`. Choose a source center a_i attaining
h_A(theta). For every x in its cloud ball and every y in the actual target
support,

```text
theta.(x-y)>=theta.a_i-epsilon-h_Z(theta)-epsilon>=delta.
```

That source ball has probability at least its assigned cloud mass, hence
at least w. Therefore M>=w delta^2. No relation between source and target
cloud labels, disjointness of clouds, or minimum individual atom mass is
used. This exposed-cap argument is the extension beyond the atom case.

All assigned clouds have positive mass, so the actual supports are within
Hausdorff distance epsilon of their respective center sets. Thus
`hbar(supp X)-hbar(supp Y)>=hbar(A)-hbar(Z)-2epsilon>=delta`.
In source-centered coordinates hbar(supp X)<=R. The mean support of any
nonempty set is nonnegative: fix a point a and integrate
`max theta.A>=theta.a`. Consequently delta<=R. Finally, containment of
the actual source in a radius-r ball implies
`tr Cov(X)<=r^2`, whereas `tr Cov(X)>=3kappa`. This proves (2) without
assuming that the radius center is the source mean.

**Necessary join test.** If S>0 and some application of (1) has Q<=S, then

```text
S>=72kappa/R,                                            (3)
d >= [kappa/(2R^2)] min{(72kappa/S)^2,
                       R^2 exp(9kappa-SR/8)}.            (4)
```

Failure of (3) or (4) excludes this join for every atom count, every weight
vector and every supplied mean-support gap. Passing is only necessary;
it does not certify any new sign.

Indeed (1)--(2) give, with a=72kappa/S,

```text
delta>=24r^2/S>=a,
log(1/w)<=S delta/8-3r^2,
Kd>=w delta^2>=delta^2 exp(9kappa-S delta/8).              (5)
```

If a>R no delta is possible. Otherwise the logarithm of the last expression
has second derivative -2/delta^2<0 on [a,R], so it is at least the smaller
endpoint value. At a the expression is exactly a^2, since Sa/8=9kappa;
at R it is the second term in (4). This proves the necessary test.

## 2. Non-overlap with the accepted moving window

**Theorem.** If R=1/2, kappa=2^-15 are valid bounds, m is an integer >=4,
and

```text
0<d<=2^-(44m+208),                                       (6)
```

then every tail cutoff (1) satisfies **Q>256m**.

The accepted moving-window theorem signs every u>=exp(-m^2/2) in (6).
Consequently the cutoff in (1) lies strictly below exp(-65536m^2/2).
There is a nonempty interval between the certified ranges; their negative
logarithms differ by a factor greater than 65536. The actual hinge may be
positive throughout that interval.

For a direct exact proof, suppose Q<=256m. The radius and mass terms give

```text
delta>=24r^2/(256m)>=9/(2^20 m)>2^-17/m,
log(1/w)<=Q delta/8<=16m,
w>=exp(-16m)>2^(-32m).                                  (7)
```

The last inequality uses e<4. For integer m>=4, m^2<=2^m: equality holds
at 4 and the successive ratio is at most (5/4)^2<2. Thus (7) implies

```text
w delta^2 > 2^-(32m+34)/m^2 >= 2^-(33m+34).              (8)
```

But K=2^14, and (2),(6) imply

```text
w delta^2 <=2^14 d<=2^-(44m+194).                        (9)
```

The exponent difference is 11m+160>0, a contradiction. The zero-loss
branch has isometric endpoint laws and needs no join; it is excluded in (6).

## 3. Consumer scope and the new all-threshold family

The argument already permits the exact mean-support gap, the optimal
admissible mass floor and independently chosen support centers. Improving
an exposed-edge lower bound, computing a normal fan, changing atom counts,
or searching nearby priors cannot repair this particular composition.
Rounding the low cutoff downward only shrinks its signed interval. Without
a positive delta the tail formula is unavailable in the first place.

The theorem covers arbitrary bounded laws whenever the existing tail
certificate is expressed by finitely many positive-mass clouds as above.
It does not assume a minimum individual atom mass. Grouping small atoms
into larger clouds does not evade (2): the cloud radius is paid twice in
the signed mean-support margin, and an entire exposed source cloud then
pays the displacement cost. This does not rule out a different cloud-tail
formula that avoids that loss. Accepted paired cubature supplies finite
inputs as a special case, but gains no new signs or equivalences here.

R2's new dilated-martingale theorem supplies another all-threshold family.
Its sufficient variance schedule and Jensen loss inequality are

```text
s>=4224 a R^4/((a-1)V),       a>1,       V=tr Cov(X),
D>=2(1-a^-2)V,              D=raw pair loss.             (10)
```

The coupling hypothesis is additional to contraction. Under normalized
covariance Cov(X)/s>=kappa I, (10) necessarily implies

```text
D/s > 8448 (R^2/s)^2 >= 76032 kappa^2.                  (11)
```

Indeed, put e=1-a^-1. Then eV>=4224R^4/s and
D>=2e(1+a^-1)V>2eV; also R^2>=V>=3kappa s. For kappa=2^-15 the last bound
is 297/4194304>2^-14, whereas (6) gives d<=2^-384. Thus the published
sufficient schedule (10) is also disjoint from this normalized small-loss
regime. This is a schedule compatibility calculation, not a new review of
R2's theorem or an obstruction to other martingale proofs.

Both the accepted moving window and R2's all-threshold family are preserved.
The missing join concerns the undamped, full-rank small-loss regime. A
coupled tail error decreasing with loss, a substantially stronger window,
or another sign mechanism may still close it. None is established here.

## 4. Trust boundary

The proof is (2), the calculus in (5), and the exact inequalities (7)--(11).
The checker audits rational coefficients, the universal linear-exponent
comparison, induction constants, and versioned inputs. It does not formalize
Procrustes rigidity, support-function geometry or the Gaussian input proofs.
The new obstruction has not been independently accepted.
