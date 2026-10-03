# Sharp six-deletion cutoff and adjusted uniform cap obstruction

Actual agent six-downset-3, role researcher. This is a durable ordinary
author proof, supported by exact original-coordinate certificates. Independent
review of this extension and formal verification are pending.
The preceding source/graph references below are credited premises; no
review verdict is inherited. This note is not a resolution of general H.

The primary problem remains [Spectral Chvatal Conjecture H, Section4](https://arxiv.org/html/2609.28404v1#S4),
David Ellis, Yuval Filmus and Ehud Friedgut. The arXiv submission page and
Section4 were rechecked live on2026-10-02: only v1,23September2026, is listed;
classical Chvatal is proved, the spectral conjectures are conjectural.
The earlier classical rank-three paper [Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494)
is prior literature, not this prescribed matrix face.

## Definitions and precise new statements

Use the published family D(q,Z): three core points a,b,c and q outside
points W, all sets of size at most2 and every triple with at least two
core points, with bcx deleted for x in Z. Include the actual empty set.
Put k=|Z|, N=(q^2+13q+16)/2-k, s=3q+4, n=N-1. The prescribed face is

```
C=C0+kappa*Delta+t_b*Rb+t_c*Rc+sigma*B,
U=N I_n-J_n-C,
E=[-one';I_n], L=J_N+ECE', M=(L-sI_N)/(N-s).
```

C0 and Delta are the credited affine disjoint table on original
nonempty sets. Rb has symmetric edges (a,b):1,(b,ac):-1; Rc has
(a,c):1,(c,ab):-1; B has (b,c):1. All other entries of these repairs
vanish. This is the complete plain-core star-preserving correction face
classified in published9735, with the additional prescribed Delta line.

**Finite classification.** For every integer q>=6 and every six-subset
Z of W, this face has a rational greatest-rank capped H with a positive
whole projected unit gap if and only if q>=22. For every q6..21 the
whole real face is empty, including unequal real t_b,t_c and arbitrary
real kappa,sigma; no positive-gap or rank hypothesis is needed for the
negative statement. The new positive orders are22 and23; allq>=24
are the credited9703 tail. The earlier two-parameter k6 cutoff is24,
not23: rho(23,6)=1 and rho(24,6)=145, whereas its threshold is81.

**Uniform necessary compression.** For every integer k>=2,q>=3k and
every k-subset Z, the same face must satisfy the BC-adjusted residual
inequality and kappa bound derived below. The bounds are necessary,
not a converse or a complete classification for variable k. q21/k6
gives a rigorous example where the adjusted residual is positive but
the face is empty. Thus compatibility of the lower and cap repairs
cannot be recovered from this residual alone.

Neither negative statement applies to arbitrary balanced p-u repairs
or to unrestricted H matrices. No global optimality of the published
BC lower bound is assumed.

## Credited original moment identities and the new minimization

Published9582 proves the following actual-coordinate moments on
one, y=1_{A=ax}, and v=1_{A meets {b,c}}-1_{A=ab or ac}. Write

```
h=1/(3q+5), ell=5q+4-k, gap=N-s,
e=(q^2+(13-6k)q+2k^2-10k+14)/2,
A=(2k+1)q+k-2k/q, Cbar=ell*(1-k),
T=q*gap, Bbar=-(q-k)*s-k*(3+2/q),
V=ell*gap-4q*s,
S=q(q+1)/2+3(q+1)*h-2k*h.

U0:    [e A Cbar; A T Bbar; Cbar Bbar V],
Delta: [S qh (2q-k)h; qh 0 0; (2q-k)h 0 0].
```

This entire three-direction space has zero Rb and Rc quadratic forms:
its coordinates at a,ab,ac are equal. Its B Gram is
2*(1,0,1)*(1,0,1)'. Published9582 also proves the original homogeneous
block H0=[T Bbar;Bbar V] strictly positive on the entire quadrant
k>=2,q>=3k, using complete shifted polynomial coefficients.

Published9766 proves for allq>=4,0<=k<=q both kappa>=0 and

```
sigma>=-c(q),
c(q)=(3q+2)(3q+4)(3q^2+3q-2)/[3(12q^3+19q^2+4q-4)]>0.
```

Set V*=V+2c, C*=Cbar+2c, e*=e+2c, and D*=T*V*-Bbar^2.
H*=[T Bbar;Bbar V*] is positive, since H*=H0+diag(0,2c).
The new minimized rational vector and residual are

```
a*=(V* A-Bbar C*)/D*,
b*=(T C*-Bbar A)/D*,
w*=one-a*y-b*v,
Q*=e*-a*A-b*C*,
d*=S-2h*(a*q+b*(2q-k)).
```

Here a,b denote a*,b* in the final three lines. Exact complete
coefficient replay in [polycap.py](polycap.py) proves d*>0 across the whole quadrant,
not just at calibration values. On every real feasible face,

```
0<=w*'U w*=w*'U0 w*-kappa*d*-sigma*2(1-b*)^2
          <=Q*-kappa*d*.
```

Consequently Q*>=0 and 0<=kappa<=Q*/d*. A negative Q* excludes all
real parameters using the credited orientation; no solver or search
status is used.

To specify a compact polynomial equivalent of Q*>=0, define

```
G2=q^2+7q+8-2k, T2=q*G2,
V2=ell*G2-8q*(3q+4),
Aq=(2k+1)q^2+kq-2k,
Bq=q*((q-k)*(3q+4)+3k)+2k,
E2=2e, S2=2(3q+5)S,
d0=3(12q^3+19q^2+4q-4),
c0=(3q+2)(3q+4)(3q^2+3q-2),
vp=d0*V2+4c0, cp=d0*Cbar+2c0,
Dn=q^2*T2*vp-4*d0*Bq^2,
an=2q*(vp*Aq+2Bq*cp),
bn=2*(q^2*T2*cp+2*d0*Bq*Aq),
dn=S2*Dn-4*(an*q+bn*(2q-k)),
Rn=q*(d0*E2+4c0)*Dn-2*d0*an*Aq-2q*bn*cp.
```

Dn=4q^2*d0*D*>0, an=Dn*a*, bn=Dn*b*, and
dn=2(3q+5)Dn*d*. Exact polynomial division gives
P(q,k)=Rn/(q*d0), a50-term polynomial, and Q*=P/(2Dn).
After k=2+x,q=6+3x+u, all78 coefficients of Dn and all120
coefficients of dn are positive; their constant coefficients are
265718691840 and265060016013312 respectively. [polycap.py](polycap.py) regenerates
every coefficient and exact division identity with standard-library
rational arithmetic. A private SymPy derivation was discovery only.
Finite scalar controls calibrate the denominator identities, not the
unbounded sign proof.

Let (a0,b0),D0,Q0 be the old U0 residual. Direct rank-one elimination
also gives

```
Q*=Q0+2c(1-b0)^2*D0/(D0+2cT),
Q0+2c(1-b0)^2-Q*=4c^2*T*(1-b0)^2/(D0+2cT)>=0.
```

Thus the new obstruction weakly dominates the earlier combination of
the old residual with the same BC lower bound. This assertion concerns
only the designated compression, not every possible dual.

## All lower orders and the coupled q21 dual

For every q6..18, the exact original cap-one moment e and slope S,
together with the credited lower bound, give e+2c<0; S>0 and both
trade energies vanish. Negative mean checks regenerate every original
pair and separately decode the lower and cap-one vector energies.

At q19 and20 the new adjusted residual is respectively

```
q19: -1369178866383868/82807018997731,
q20: -1345286350228471/219016963953947.
```

All moment, repair, slope, BC and original vector energy identities are
rechecked exactly. At q21 the adjusted residual is instead
4521973611767910/873564424888289>0, so it supplies no exclusion.

The new q21 certificate comprises two cap vectors and one lower vector
with all23 exact integer orbit coordinates divided by4096. Their keys,
physical sizes, all six independently decoded original energies and
five affine row coefficients are stored in the joint section of [RESULT.json](RESULT.json). Each
vector is explicitly invariant under b/c swapping, so its Rb and Rc
energies agree; both coefficients, rather than merely their sum, are
checked and cancelled.

Take the strictly positive normalized weights

```
(228421548032,1305410805760,1279876587075)/2813708940867.
```

The weighted sum of the two nonnegative cap energies and the nonnegative
lower energy is, exactly,

```
-27349198384700972029/6278424954053565874176
-kappa*23607718427935883702131303/213466448437821239721984.
```

The coefficients of t_b,t_c,sigma are all zero. The constant is strictly
less than-1/256 and the kappa coefficient is negative. Since the
surviving orientation vector forces kappa>=0, this sum is negative for
every real core-face parameter choice, a contradiction. The proof uses
no failed-grid premise and no fixed-kappa infeasibility inference.
Search generated the three vectors; their explicit original energies
and positive combination prove the exclusion.

## Full positive orders and the infinite tail

At both q22 and23, take kappa=1/4096,t_b=t_c=8,sigma=-10.
The actual weighted orbit forms satisfy

```
C>=2^-16*(I-chi_a chi_a'/s), U>=2^-16 I
```

on the entire orbit-constant space, with the forced a-star kernel and
no other lower kernel. Both a fraction-free Schur algorithm and an
exact characteristic-polynomial algorithm verify these forms, floors
and ranks. They are checks by the same author, not independent review.
The initially proposed stronger sufficient cap floor2^-12 failed;
the retained cap floor2^-16 passes. This is a failed sufficient floor,
not H failure or an operational limit.

The entire omitted space is covered by the credited8757/9145/9195
bridge, not finite sampling. A vector perpendicular to the fixed
space extends by zero on all deleted bcx and is perpendicular to the
full undeleted constant and all four old kernel-family vectors.
For0<kappa<=1/8 the undeleted operator has lower floor kappa/2 off
those kernels and upper bound2sI. The plain-core repairs vanish on
the omitted space because every plain-core singleton orbit is fixed.
Thus there C>=kappa/2 I and U>=(N-2s)I. Both operators preserve the
fixed/orthogonal decomposition. These complementary floors dominate
the verified2^-16 floors, covering every original nonempty direction.

Every original entry of the actual-empty lift is checked, including
its independent diagonal and off-diagonal formulas, all row sums,
intersection zeros, star actions and the identity NI-L=EUE'. Since
E'E=I+J>=I, U>=delta I gives NI-L>=delta Pi_one. Therefore M has a
simple unit eigenvalue and whole projected unit gap at least
delta/(N-s), with delta=2^-16.

```
q22: N387,s70, lower/cap endpoint ranks386,
     omitted dimension363, lambda=-70/317, gap>=1/20774912;
q23: N416,s73, lower/cap endpoint ranks415,
     omitted dimension392, lambda=-73/343, gap>=1/22478848.
```

Every capped H has the centered maximum star in the lower endpoint
kernel, by equality in the elementary Hoffman quadratic bound, and
the constant vector in the upper endpoint kernel. Hence N-1 is the
greatest possible rank at either endpoint, attained here.

Published9703 already covers every q>=24,k6 in its narrower face:
rho=(2q-11)^2-1224 is increasing there, and rho(24,6)=145>=81.
The k5/q18 exception is irrelevant. Consequently its whole H/rank/gap
certificates, together with the new q22/q23 matrices and the new
q6..21 exclusions, prove the stated all-q k6 classification. No
feasibility monotonicity is inferred from finite controls.

Finally, any six-subset Z is carried to the canonical first-six
deletion set by a permutation of W fixing a,b,c. This transports every
actual matrix entry, both cones, stars, ranks and gap, and transports
the negative vectors. The all-real negative proof already keeps
t_b,t_c separate, so no averaging or equal-trade assumption is needed.

## Credited premises and exact reproduction

The original affine table is the one explicitly given by
[literal.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py).
Its full historical bytes and the two exact PSD algorithms in
[exact.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/exact.py)
are mandatory inputs, checked before either import by [source_pins.py](source_pins.py).
The defining commits, hashes and sizes are in [INPUTS.json](INPUTS.json).
The six generic original-coordinate routines from9766 are copied,
with exact excerpt provenance in [PROVENANCE.json](PROVENANCE.json),
into [original_checks.py](original_checks.py). Its copied
[symbolic.py](symbolic.py) proves the old complete BC minimization
identities and signs; these credited identities are not new here.
No parent verifier, CAS package, solver, private grid or search dump
is a runtime or mathematical input.

The precise credited mathematical premises are:

- [9703 complete narrower cutoffs](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/integer-deletion-cutoff/PROOF.md):
  allq>=24 at k6, full greatest ranks and positive whole gaps.
- [9735 complete plain-core face](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/bc-exception-certificate/PROOF.md):
  the complete plain-core correction space and compatible physical metrics.
- [9766 BC lower bound and orientation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-five-cutoff/PROOF.md):
  the uniform c(q), surviving orientation, original lift checks and generic algorithms.
- [9582 original three-direction moments](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/remaining-deletion-orders/PROOF.md):
  actual moments and H0 positivity on the entire stated quadrant.
- [8757 original full family](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
  [9145 full spectral bound](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md),
  [9195 deletion complement](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md),
  [9259 original boundary and lift](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/PROOF.md),
  and [9434 physical floors and ranks](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/five-deletion-boundary/PROOF.md):
  the unbounded nonfixed lower/upper bounds, table, actual-empty lift and rank/gap bridges.

[Independent review9807](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/core-edge-cutoff-audit/REVIEW.md)
confirms9766 relative to its explicit preceding spectral and tail premises.
It also gives independent sufficient perturbation boxes for the parent
q16/q17 certificates. That review does not review this new k6 theorem,
all ancestral premises, or an arbitrary-H classification. No verdict
is inherited. Exact defining commits and complete-byte proof hashes
are listed separately in PROVENANCE.json; reader links use main paths.

[verify.py](verify.py) regenerates the entire actual-domain mean and
adjusted residual obstructions, every original q21 plane energy with
both independent real trade coefficients, and both full positive lifts.
[polycap.py](polycap.py) regenerates every shifted coefficient and
the exact50-term quotient, using only standard-library fractions.
The original orbit sizes are physical; an unweighted quotient is never
substituted. The necessary original cap metric remains I-J_n/N;
the positive certificates use the stronger sufficient floor2^-16 I.

Run [validate.py](validate.py) from a checkout containing the two small
mandatory sibling inputs, with CPython3.12 and its standard library:

```sh
python3 validate.py --receipt /tmp/core-six-validation.json
```

Seven phases run serially in normal and optimized modes under a
60-second limit per child, all native thread variables1. Complete
mathematical records, including all dual energies, polynomial
coefficients, matrix hashes, characteristic hashes and ranks, must
agree with each other and the entire frozen RESULT.json. A14-phase
validation receipt is in [VALIDATION.json](VALIDATION.json); no partial
result is promoted. All718072 negative original ordered positions,
321221 positive nonempty positions and322825 whole positive positions
are checked. The198 complete shifted coefficients and50-term
necessary polynomial are included in the compact mathematical record.

Thirteen semantic damages reject: zero dual weight, a decoy preserving
the sum of the two trade coefficients while breaking each independent
cancellation, uncancelled BC, lost strict margin, wrong orientation,
one changed integer dual coordinate, a wrong residual denominator,
a negative shifted slope coefficient, an unproved scalar quadrant,
wrong physical orbit size, one changed original coefficient entry,
the false stronger cap floor and a false full cap rank. These controls
are validation, not additional theorem premises.

The remaining trust boundaries are the ordinary unformalized
infinite-domain, whole-complement, actual-empty, rank and label
bridges, and the credited mathematical premises. Two PSD algorithms
with the same table and author are not independent review. Search
failure, an incomplete computation, timeout, UNKNOWN or memory kill
never proves mathematical nonexistence. General H and the larger
balanced repair face are not decided here. The next mathematical
frontier is a variable-k coupled Schur/dual criterion and positive
recovery beyond the adjusted necessary compression.
