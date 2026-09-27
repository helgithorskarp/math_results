# An averaged contraction cannot approach the full rank-six kernel extremizer

Complete author proof, 27 September 2026. Independent mathematical review
and formalization are pending. The full dimension-three Gaussian-convolution
majorisation question remains OPEN.

## 1. A global inequality and its precise limitation

Let mu be a bounded probability law on R3, let T be 1-Lipschitz on its
support, and let s>0. For iid X_i of law mu put Y_i=T(X_i) and

```
delta_ij=|X_i-X_j|^2-|Y_i-Y_j|^2 >=0,
Z_i(t)=(sqrt(1-t)X_i,sqrt(t)Y_i),  0<=t<=1,
Q_m(t)=sum_i |Z_i(t)-mean_m Z(t)|^2,
B_m=E delta_12 integral_0^1 exp(-Q_m(t)/(2s))dt.        (1)
```

For four labels define d_ij(t)=|Z_i(t)-Z_j(t)|^2 and

```
Q_D(t)=Q_123(t)+Q_124(t)-Q_12(t)
      =d_12(t)/6+[d_13(t)+d_14(t)+d_23(t)+d_24(t)]/3,
I_D=E delta_12 integral_0^1 exp(-Q_D(t)/(2s))dt.        (2)
```

Every displayed graph coefficient is nonnegative. In particular its loss
L_D=Q_D(0)-Q_D(1) is nonnegative for every tuple.

**Theorem.** There is a universal eta>0 such that, for ALL these inputs,

```
B_4 >= (8/9)^3 (1+eta) I_D,
B_2 B_4 >= (8/9)^3 (1+eta) B_3^2.                    (3)
```

An exact, but non-effective, definition is

```
eta=(5/13) min(e_graph,1/216),                         (4)
```

where e_graph>0 is the Gaussian-smoothed graph separation constant in
Section4. This is one constant independent of the measure, map, noise,
radius, number of atoms, weights and mean loss. No covariance floor is
assumed. Zero-loss inputs satisfy (3) with every term zero.

The earlier normalization of the actual endpoint hinge moments is

```
a_j=B_(j+2)/[4s(j+2)^(5/2)].                          (5)
```

Thus the first unrestricted Hankel sign would require
B2 B4>=(8/9)^(5/2) B3^2. The definition (4) gives eta<=5/2808, and

```
(1+5/2808)^2 < 9/8.                                  (6)
```

So (3) does not reach that sign. Nor does it sign a new general beta entry,
prove full majorisation, supply a zero-failure coupling or give a new
Kneser--Poulsen class. It proves that the naive six-dimensional conditional
constant cannot be approached by the FULL marked contraction average.
The amount needed to reach (8/9)^(5/2) remains a substantive open gap.

## 2. Conditional replicas and the exact Gaussian kernel

Fix t and the first two replicas. Let b=(Z_1+Z_2)/2, and let the next
two displacements from b be V,V'. They are independent copies. Direct
centering gives

```
Q_D=Q_2+(2/3)(|V|^2+|V'|^2),
Q_4=Q_2+(3/4)(|V|^2+|V'|^2)-(1/2)V.V'.              (7)
```

Write

```
r=E exp(-|V|^2/(3s))>0,
dnu=exp(-|V|^2/(3s)) dLaw(V)/r,
W=sqrt(2/(3s)) V under nu.                            (8)
```

We use nu also for the resulting law of W on R6. It is bounded for
each fixed input. Conditional averaging of (7) yields

```
E_extra exp(-Q_4/(2s))
 =exp(-Q_2/(2s)) r^2 E_(nu x nu) K(W,W'),
K(w,w')=exp[-(|w|^2+|w'|^2)/16+3w.w'/8].             (9)
```

Let gamma denote the standard Gaussian probability measure on R6, let
G~gamma be independent of W, and put

```
Pnu=Law(W/sqrt(3)+sqrt(2/3)G),
e(nu)=integral (dPnu/dgamma-1)^2 dgamma >=0.           (10)
```

The density and this finite integral exist for bounded nu. Gaussian
completion, or the classical Mehler identity at correlation 1/3, gives

```
E K(W,W')=(8/9)^3 [1+e(nu)].                         (11)
```

For clarity this identity does not assume an expansion with unsigned
cross terms. If k_w is the density of N(w/sqrt(3),(2/3)I_6), direct
integration shows

```
integral k_w(z)k_w'(z)/gamma(z) dz
 =(9/8)^3 K(w,w').                                   (12)
```

Tonelli and probability normalization prove (11). All kernels are
nonnegative; bounded centers justify the finite Gaussian integrals.

Put

```
dw=delta_12 exp(-Q_2/(2s)) dt dmu(X_1)dmu(X_2).
```

Then B2=int dw, B3=int r dw, I_D=int r^2 dw. Consequently

```
B3^2<=B2 I_D.                                       (13)
```

When I_D>0, define the probability law dOmega=r^2 dw/I_D of the base
pair and time. Equations (9)--(11) give the exact equality

```
B4/I_D=(8/9)^3 [1+E_Omega e(nu)].                    (14)
```

The rest of the proof gives a uniform positive lower bound on this
AVERAGED e(nu). It does not assert such a bound at every interpolation
time, and is compatible with the accepted instantaneous obstruction.

## 3. An elementary moment consequence of small e

Split W=(A,B) into its first and last three coordinates. The letter B
here denotes a coordinate vector, not the replica number B_m. From (10),
conditional Gaussian expectation gives

```
E_(Pnu)(|A|^2-3)=(1/3) E_nu(|A|^2-3),
E_gamma(|A|^2-3)^2=6.
```

Cauchy--Schwarz in L2(gamma), and the same calculation for B, imply

```
|E_nu |A|^2-3| <= sqrt(54 e(nu)),
|E_nu |B|^2-3| <= sqrt(54 e(nu)).                     (15)
```

In particular if e(nu)<1/216, then

```
E_nu |A|^2>5/2,  E_nu |B|^2<7/2.                   (16)
```

No entropy-to-moment continuity or unproved uniform-integrability claim
is used in (15). These are exact Gaussian polynomial identities.

## 4. A full Gaussian cannot be approached on uniformly Lipschitz graphs

For a probability law nu on R3 x R3 use (10), allowing e(nu)=infinity.
Define

```
e_graph=inf e(nu),                                   (17)
```

where the infimum ranges over probability laws concentrated on the
graph of some globally 2-Lipschitz F:R3->R3. The graph and law may vary;
there is no common bound on their supports or on F(0).

**Lemma.** One has 0<e_graph<infinity.

**Proof.** A point law on a constant graph has finite e, so the infimum
is finite. Suppose it were zero and choose nu_k with e(nu_k)->0.
Cauchy--Schwarz gives convergence of Pnu_k to gamma in L1 density.
For every xi in R6 their characteristic functions satisfy

```
nu_hat_k(xi)=exp(|xi|^2) (Pnu_k)_hat(sqrt(3)xi).
```

The right side tends to exp(-|xi|^2/2). The classical Levy continuity
theorem therefore gives weak convergence nu_k->gamma, in particular
tightness.

Let F_k be the 2-Lipschitz graph maps. Choose a fixed ball in R6 with
positive gamma mass and zero boundary mass. For all large k it has
positive nu_k mass, so its graph contains some (a_k,F_k(a_k)) in that
ball. This bounds F_k(0), because
|F_k(0)|<=|F_k(a_k)|+2|a_k|. The maps are then uniformly bounded on each
compact set and equicontinuous. Arzela--Ascoli and a diagonal subsequence
give local uniform convergence F_k->F for a 2-Lipschitz map F.

If a point is outside the closed graph of F, a sufficiently small ball
around it has bounded first projection and positive distance from that
graph. Local uniform convergence makes this ball disjoint from the graphs
of F_k eventually. By the open-set part of the Portmanteau theorem its
gamma mass is zero. A countable such cover implies gamma is concentrated
on the graph of F. That graph has six-dimensional Lebesgue measure zero
by Fubini, contradicting the positive Gaussian density. This proves the
strict lower bound. QED.

The lemma is a written compactness argument, not a computed value of
e_graph. It uses only standard weak-convergence and compactness theorems.
It is also valid for any fixed finite Lipschitz bound, but the fixed
value 2 suffices here.

For the conditional law (8), at 0<=t<1, the relation between A and B is
a map of Lipschitz constant at most sqrt(t/(1-t)). Translations by the
two base centroids and the common scaling do not alter this calculation.
If T was originally defined only on its support, Kirszbraun's theorem
first gives a global 1-Lipschitz extension, without changing any replicas.
It follows from (17) that

```
e(nu)<e_graph  implies  t>4/5.                       (18)
```

The endpoint t=1 is a null set for the time integrals and causes no issue.

## 5. The interpolation clock permits at most one unit of remaining loss

Consider the full probability law of four replicas and time with density

```
delta_12 exp(-Q_D(t)/(2s))/I_D
```

relative to dmu^4 dt. Its base/time marginal is Omega, and its two extra
replicas are conditionally independent with law (8).
Write z=1-t and set

```
U=z L_D/(2s) >=0.                                   (19)
```

Conditional on a tuple with L_D>0, let a=L_D/(2s). Since
Q_D(t)=Q_D(1)+zL_D, the law of U has density

```
exp(-u)/(1-exp(-a)),  0<=u<=a.                       (20)
```

It is an Exp(1) variable conditioned to be at most a. More explicitly,
with V uniform on (0,1),

```
U=-log[1-V(1-exp(-a))] <= -log(1-V).
```

The last variable is Exp(1). If L_D=0, U=0; such tuples have zero
delta_12 mark here anyway. Therefore, also after averaging tuples,

```
E U <=1.                                             (21)
```

Now condition instead on the base and time. Put b_X=(X1+X2)/2 and
b_Y=(Y1+Y2)/2. The diamond identity gives

```
L_D=delta_12/2+(2/3) sum_(i=3,4)
                   (|Xi-b_X|^2-|Yi-b_Y|^2).
```

Using the scaling in (8), for 0<t<1 this gives EXACTLY

```
u_bar:=E[U | base,t]
 =z delta_12/(4s)+E_nu |A|^2-(z/t)E_nu |B|^2 >=0.    (22)
```

The nonnegativity is inherited from (19), not inferred from separate
signs of the last two terms.

## 6. A uniform positive averaged remainder

Let e0=min(e_graph,1/216)>0 and let the good event in Omega be
e(nu)<e0. On that event, (16) and (18) give z/t<1/4, so (22) implies

```
u_bar >= 5/2-(1/4)(7/2)=13/8.                       (23)
```

On the complement u_bar is still nonnegative. Equations (21)--(23)
therefore imply

```
P_Omega(good)<=8/13,
E_Omega e(nu)>= e0 P_Omega(not good)>=(5/13)e0.        (24)
```

Together with (14) this proves the first inequality in (3), with (4).
Equation (13) proves the second. If I_D=0, positivity of the Gaussian
factor implies delta_12=0 almost everywhere, so every B_m=0; the proof
then needs no normalization. All integrations and conditionings above are
valid for bounded laws, and include repeated atoms and diffuse measures.

The proof retains two inputs which are lost by a pointwise rank estimate:
the deterministic graph relation of the actual source and target, and the
exact marked time distribution. An arbitrary six-dimensional cloud at one
time need not satisfy the resulting averaged restriction.

## 7. Reproducibility and remaining obligation

The standard-library checker independently reconstructs finite centering
identities from pair distances and verifies the Gaussian completion,
moment constants, time scaling and the final13/8,5/13 arithmetic. Its
seven-site rank-six fold includes zero and positive pair losses. Normal
and optimized runs compare against the same compact expected output, and
corrupted output is rejected. These exact controls are not a proof assistant
and do not calculate the compactness constant.

The useful new analytic fact is the uniform strict improvement (3), with
all input scales unrestricted. The standard Mehler identity and the
elementary graph compactness argument are not separately marketed as new
theorems. The first Hankel sign still needs a MUCH stronger lower bound,
specifically E_Omega e(nu)>=sqrt(9/8)-1, or a method retaining the
Cauchy--Schwarz surplus in (13). Our eta cannot supply that bound by (6).
No claimed beta or full-question implication is omitted from the scope
statement. See [SOURCES.md](SOURCES.md) for durable dependencies.
