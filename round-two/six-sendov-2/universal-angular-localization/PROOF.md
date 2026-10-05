# Universal real angular localization for degree nine

Actual **six-sendov-2 / researcher**, 2026-10-05, pass49.
Complete ordinary author proof; **unformalized and independently unreviewed**. Classical Rayleigh/min--max perturbation and Cauchy--Schwarz
are the mechanism. No historical priority or sharp cutoff is claimed.

Use the full grouped compression masses of7432 and the normalization from
Appendix A below: x in R8, sum x_i=0, sum x_i^2=1,
P=I-11^T/8, H=(P diag(x) P)|_{1-perp}, m_lambda=||Pi_lambda x||^2,
eta=sum m_lambda^2, D=sum x_i^4-1/8, and C=(1-eta)/D for D>0.
All original and critical multiplicities are allowed. In particular no
mu_3 or mu_5 equation is imposed.

## 1. Statement and exact improvement over the credited collar

For t=sqrt(D), 0<t<1/17, write c0=1/8. Then

    C <= F(t)=2/(c0-t)-(7/6)t^2/(c0-t)^2.                       (1)

F is strictly increasing on that interval. In particular, on the ENTIRE
balanced norm-one real sphere with 0<D<=1/676,

    C <= 5560/243 = 23-29/243 = 47/2-301/486.                    (2)

The prior continuous value16 from8753/8806 includes D=0 if desired.
The earlier source
[near-balanced angular collar](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/near-balanced-angular-collar/PROOF.md),
commit dba4b4049ea087e7fe0c358244b9ac134237b183, already supplies an
explicit bound on mu_3=mu_5=0 and D<=1/729, using a central full mass:
C<16/(1-8sqrt(D))+390625D^2. It is prior art. This argument removes both
odd-moment hypotheses and the Taylor-loss term, adds the six remaining
full masses, and enlarges the explicit numerical domain to D<=1/676.
It does NOT retain the old, stronger central-root motion O(D^(3/2)), which
uses the odd cancellations. No review of a parent transfers to this child.

## 2. The sign sector and a single separated central eigenvalue

Put a=1/sqrt(8), epsilon_i=x_i^2-c0. Then sum epsilon_i=0 and
sum epsilon_i^2=D, so |epsilon_i|<=t. Therefore

    sqrt(c0-t)<=|x_i|<=sqrt(c0+t).

These endpoints are positive. If at most three x_i are positive, balance
would require 3sqrt(c0+t)>=5sqrt(c0-t). But

    25(c0-t)-9(c0+t)=2-34t>0,

contradicts that requirement. Reflection handles the negative count.
Thus every profile in this range has exactly four positive and four
negative coordinates, with no zero. This elementary argument uses only
balance and the fourth moment; it imports no odd-moment sign theorem.

Let s_i=sign(x_i), so sum s_i=0, and set
H0=(P diag(a s) P)|_{1-perp}. On the three-dimensional sum-zero space
supported on the four positive indices, H0=aI; on the corresponding
negative space, H0=-aI. On span(s), H0=0. These orthogonal spaces exhaust
1-perp, so its spectrum is (-a,-a,-a,0,a,a,a).

On 1-perp, the symmetric perturbation H-H0 has every Rayleigh quotient
in [-e,e], where e=max_i||x_i|-a|. The min--max characterization of each
ordered eigenvalue therefore places it within e of the corresponding
ordered H0 eigenvalue. This follows directly by adding a quadratic-form
bound to the sup/inf on every subspace; no simple spectrum is assumed.

Concavity of square root, or squaring its positive two-term sum, gives

    sqrt(c0+t)-a <= a-sqrt(c0-t),
    e <= a-sqrt(c0-t),  g=a-e >= sqrt(c0-t).                      (3)

Because t<1/17<3/32=3c0/4, e<a/2. Thus exactly one eigenvalue sigma lies
in [-e,e], has a one-dimensional eigenspace, and is separated from all
six other eigenvalues. The other eigenvalues satisfy |lambda|>=g.
Repeated satellite eigenvalues and repeated original coordinates are
permitted. This central eigenvalue need not be near0 to order D^(3/2).

## 3. Full masses and the sharper angular estimate

Let Q=1-m_sigma be the sum of the remaining full grouped masses. They
have at most six distinct eigenspaces, so Cauchy--Schwarz gives

    eta >= (1-Q)^2+Q^2/6.

Furthermore Hx=P(x_i^2), whose squared norm is D. The spectral theorem
and (3) therefore give

    D=sum m_lambda lambda^2 >= g^2 Q,
    0<=Q<=q=t^2/(c0-t).

No mass is split among a basis of a repeated eigenspace. The function
2Q-7Q^2/6 is increasing for 0<=Q<=6/7. On 0<t<1/17, the scalar q is
increasing and is less than its endpoint136/2601<6/7. Hence

    1-eta <= 2Q-7Q^2/6 <= 2q-7q^2/6.

Dividing by D=t^2>0 proves(1). In particular the weaker bound
C<16/(1-8sqrt(D)) also follows by keeping the unique central mass alone;
the satellite term supplies the stronger explicit value in(2).

Direct differentiation gives

    F'(t)=[1/4-(55/24)t]/(c0-t)^3>0,

since 1/17<6/55. At t=1/26, direct rational substitution gives
F(1/26)=5560/243, proving(2). At the old endpoint t=1/27 it gives
F(1/27)=24400/1083, with margin2101/2166 below47/2. The old leading
constant16 and its full-sphere uniform limit are credited to8753/8806,
not claimed again. No optimal small-D cutoff or sharp positive-D bound
is asserted.

## 4. Combined compact counterexample band

The trace estimate proved in Appendix A applies to the entire same sphere:

    C <= U(D)=(144-224D)/(3+112D), D>0.

It gives C<=23 when D>=3/112. Consequently any strict C>T counterexample
with T>=23, including either chosen threshold47/2-q or47/2-q/2 for
0<q<=1/2, must satisfy

    1/676<D<3/112.                                              (4)

The credited sharp
[8851 moment lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/sign-count-angular-reduction/PROOF.md) and that trace estimate give
C<=412/19<23 outside strict4+4/no-zero, including every zero profile.
Thus a counterexample in(4) has exactly four coordinates of each strict
sign. On the already published
[heat/Hermite four-/six-coefficient chart](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/heat-hermite-angular-reduction/PROOF.md),
D=3/8-8E, (4) is

    39/896<E<505/10816.                                         (5)

This removes the uniform denominator singularity from the remaining
search. Original feasibility and positive denominator guards remain
mandatory. Adding (4),(5) and c>0 (the product of four positive and four
negative originals) as NECESSARY guards does not alter the existence
of a strict threshold counterexample. The primitive constant alone does
not license real roots or impose the full sign count.

This is an explicit PARTIAL angular stability result on the entire real
sphere. A full numerical gap on the exact odd locus, a full numerical
moment collar, an actual remaining-region infeasibility certificate,
and the unrestricted complex first-power target remain unpaid.

## 5. Arithmetic and proof boundary

[check.py](check.py) checks the complete rational8x8 reference
compression, all its projector identities and ranks, and every scalar
cutoff, derivative numerator, endpoint margin and E-band conversion.
The literal sign pattern4+4 is representative up to a proved permutation
conjugacy. There is no floating eigensolver or global enumeration.
Min--max, full spectral projection/Cauchy, the inequality substitutions,
and imported angular definitions/continuity are ordinary written proof,
not formalized or independently reviewed.

See [README.md](README.md) and [VALIDATION.json](VALIDATION.json) for
exact source commands, finite record custody and the ordinary proof boundary.
The separate alternate two-Bezout-matrix original-root licence is not an
input of this result and is not included in this publication.

## Appendix A. A classical full-compression trace tail

List all seven actual eigenvalues of H with their multiplicities. Assign
each FULL grouped mass to one copy of its eigenvalue, and zero to the
other copies. This bookkeeping preserves sum w_i=1, sum w_i^2=eta, and
sum w_i lambda_i^2=||Hx||^2=D; it does not split a repeated eigenspace.
For X=diag(x), Q=11^T/8, the ambient compression has one extra zero mode.
Cyclic expansion of trace((X(I-Q))^k), using sum x_i=0 and sum x_i^2=1,
gives

    tau2=sum lambda_i^2=1-2/8=3/4,
    tau4=sum lambda_i^4=mu4-4mu4/8+2/64=3/32+D/2.

In the fourth trace, the four one-Q words contribute -4mu4/8. Among
six two-Q words, four contain a mu1 factor and two have gaps(2,2),
each contributing1/64. Every three-/four-Q word contains mu1=0.
Thus no odd-moment hypothesis was hidden. These traces are classical;
the earlier six-moment Gram framework
[10105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/two-moment-parity-descent/PROOF.md)
already uses them on its simple two-odd-zero chart. No priority is claimed.

Cauchy--Schwarz applied to w_i-1/7 and lambda_i^2-3/28 gives

    eta >= 1/7+(D-3/28)^2/(3/224+D/2),
    (6/7)(3/224+D/2)-(D-3/28)^2=D(9/14-D).

The centered eigenvalue-square variance3/224+D/2 is strictly positive.
For D>0, clearing that positive denominator proves

    C <= U(D)=(144-224D)/(3+112D),
    U'(D)=-16800/(3+112D)^2<0.

At D=3/112, U(D)=23, proving the complementary tail used above.
The credited sharp8851 moment theorem gives mu4>=13/84, hence D>=5/168,
outside strict4+4/no-zero, including every zero profile. It was already
proved for ALL original levels, without odd-moment hypotheses. Thus

    C<=U(5/168)=412/19<23

on that entire sign sector, all multiplicities. This supplies the sign
restriction in Section4; the older sharp moment theorem is not claimed
again. The universal bound inside the remaining open band is unpaid.
