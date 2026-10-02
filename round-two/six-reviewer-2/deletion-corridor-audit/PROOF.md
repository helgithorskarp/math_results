# Independent corridor audit and sharpness of its two scalar criteria

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Ordinary mathematical proof with exact arithmetic corroboration, unformalized.
The full defining proof of LEMMA9478 was visible and credited before this
independent audit. Its new executable, EXPECTED and RESULTS were not consulted
before the independent proof, program and complete records were sealed.

This packet audits [9478's complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/general-deletion-corridor/PROOF.md),
source ea16136611129587959bd5b9504679a6f984ec88,
ref bafkreidb5hcvtvopob3hdh6lrplkp7wbyop7eoknkdlx47nvr54efpzyfa.
It explicitly reuses the independently audited universal Schur premise in own
[REVIEW9488](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/schur-cap-audit/REVIEW.md),
source84a7d6ac9bf8e8896fabd51398032a00c4e04a06. The constructive all-order theorem
[9195](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md)
is an explicit imported sufficient premise, not independently reproved here.
No result on arbitrary H matrices or general Conjectures H/I follows.

## Original family and the two criteria

Let q>=max(4,k), k>=3 be integers. On core a,b,c and q outside points W,
include the empty set, all singletons/pairs and triples containing at least
two core points. Delete bcx for each x in any size-k subset Z of W.
Retain the exact affine type table and four-edge scalar repair of9478:
R[a,b]=R[a,c]=1; R[b,ac]=R[c,ab]=-1, symmetrically, zero elsewhere.
On nonempty members C has diagonal s-1, entries-1 on intersecting distinct
members, and Q_kappa(A,B)-1 on disjoint members, plus tR. N and s below
include the actual empty member and maximum a-star. With E's first row-1
and subsequent identity, L=J+ECE', M=(L-sI)/(N-s), U=NI-J-C.
The ordinary whole-coordinate congruences C>=0 iff L>=0 and U>=0 iff M<=I
retain the empty loop. They do not assume a symmetric certificate exists
for arbitrary H. The precise ansatz and additional cap are essential.

Put
\[
\begin{aligned}
 N&=(q^2+13q+16)/2-k,& s&=3q+4,& h&=1/(3q+5),\\
 g&=N-s=(q^2+7q+8-2k)/2,&
 d&=q(q+1)/2-k+3+2/q,\\
 w&=(3q+1-2/q)/(q-1),&
 a_0&=(2k+1)q+k-2k/q,\\
 e&=[q^2+(13-6k)q+2k^2-10k+14]/2.
\end{aligned}
\]
Here g denotes the positive gap N-s, not N-2s. The unbounded exact Schur
premise9434, independently audited in own9488, gives for feasible real
parameters kappa>=0 and
\[
 Q(\kappa)=Q_0-\kappa D_4-\kappa^2c_4\ge0,\qquad D_4,c_4>0,
\]
where
\[
 Q_0=e-\frac{a_0^2}{qg}
       -\frac{k(q-k)w^2}{qg}-\frac{4q(k-1)^2}{d},
 \quad c_4=h^2(q/g+4q/d).
\]
Writing alpha=q(q+1)/2+3(q+1)h, S=alpha-2kh, the coefficient is
D4=S-2h[a0/g+4q(1-k)/d]. No new all-order Gram derivation is claimed:
that original incidence/sign bridge is credited to9434/9488. Positive
g,d and a0>2kq ensure Q0>=0 implies e>0.

The imported9195 constructive condition is
\[
 B_0(q,k)=[q^2+(7-6k)q+2k^2-12k+8]/2>0.
\]
It supplies rational capped matrices with greatest lower/cap ranks N-1
and simple unit eigenvalue. Set
\[
 D_B=28k^2-36k+17,\quad
 r_B=(6k-7+\sqrt{D_B})/2,\quad b(k)=\lfloor r_B\rfloor.
\]
The positive cutoff is b(k)+1, not b(k). B0(k,k)=-(k-1)(3k+8)/2<0.
Thus q>=k lies between the lower root and the upper branch when B0<=0,
and B0>0 iff q>rB. The fractional part discarded by isqrt(DB) is less
than one; after division by2, an integer or half-integer cannot cross the
next integer, proving b=(6k-7+isqrt(DB))//2. At k8,q40 the discriminant
is1521 and B0=0: a strict tail endpoint is not certified by9195.

## Audit of the universal negative boundary

Hypothetical feasibility at q<=b(k)-6 forces e>0. At the domain's left
endpoint e(k,k)=(-3k^2+3k+14)/2<0. Its discriminant is
28k^2-116k+113=17+52(k-3)+28(k-3)^2>0.
Consequently q>=k and e>0 put q above the upper root rE, where e is
increasing. This branch argument must precede monotonicity; e need not
increase throughout q>=k. Since q<=rB-6, its comparison endpoint is also
above rE. Exact coefficient arithmetic gives
\[
 2e(R-6,k)-2(19k-18-3R)=2B_0(R,k),
\]
so e(q,k)<=10k-15/2-(3/2)sqrt(DB). Also rB<6k follows by squaring
positive sides: (6k+7)^2-DB=8k^2+120k+32>0.
For k>=5, DB-(5k-2)^2=(3k-13)(k-1)>0, hence
 e<(5k-9)/2. Because k>=4,q>=4,
 g<=q(q+7)/2 and d<q(q+1)/2, while a0>2kq.
The two Schur losses alone exceed
\[
 \mathcal L(k)=8k^2/(6k+7)+8(k-1)^2/(6k+1).
\]
Clearing positive denominators gives
\[
 2(6k+7)(6k+1)[\mathcal L(k)-(5k-9)/2]
 =12k^3+20k^2+269k+175>0.
\]
Thus Q0<0, contradictory, without using the nonnegative variance term.
At k4, sqrt321>17 gives e<7, while L4=7+7/775>7.
At k3, b=11, so q4,5 are the only admissible negative orders. At q4,
e=-1. At q5 the literal49 nonempty-coordinate independent reconstruction
checks all four weighted4x4 Grams, full matrices and all ten labeled Z.
The original lower z=1-Sb-Sc+Ftriangle satisfies C0z=Rz=0 and
 z'Delta z=159/10>0. The original vector
\[
 v=1-(29/155)y_Z-(97/310)y_{W\setminus Z}+(10/77)y_{extra}
\]
has v'U0v=-322737/23870, v'Delta v=939346/59675>0, v'Rv=0.
Therefore v'U_kappa,t v is strictly negative whenever kappa>=0,
for every real t. This known small-k baseline is verification, not new
finite classification. Every outside deletion set in the unbounded
argument follows by point permutation; the scalar quantities depend
only on q,k. No finite sweep substitutes for this proof.

Combining this exclusion q<=b-6 with imported construction q>=b+1
leaves at most the six integers b-5,...,b. This confirms9478 within its
exact ansatz and credited premises. No actual cutoff monotonicity,
feasibility of any corridor order, optimal parameters or arbitrary-H
exclusion is inferred.

## Strengthening and improvement opportunities

**Proved criterion sharpness.** For infinitely many k, every one of the
six corridor orders passes the complete scalar four-coordinate Schur
necessary condition for some positive real kappa and fails the imported
positive-tail criterion B0>0. Thus those two criteria, even with exact
Q rather than the coarser cubic argument, cannot uniformly replace the
six-order corridor by five orders. This is sharpness of the information
provided by these criteria. It is not sharpness of actual feasibility,
and does not assert a capped matrix exists at any of these orders.

Define positive Pell pairs by
\[
 (p_1,u_1)=(8,3),\qquad
 p_{n+1}=8p_n+21u_n,\quad u_{n+1}=3p_n+8u_n.
\]
Exact expansion preserves p^2-7u^2=1, and both coordinates increase.
For every n>=2, u>=48, p>=127. Set k=u+1. Then
DB=28u^2+20u+9, and
\[
 DB-(2p+1)^2=4(5u+1-p)>0,\qquad
 (2p+3)^2-DB=4(3p-5u+1)>0.
\]
Indeed (5/2)u<p<= (8/3)u follows from the Pell norm and u>=3.
The positive square-root bracket gives rB strictly between 3u+p and
3u+p+1. Therefore b(k)=3u+p exactly, and the six orders are
\[
 q=3u+p-5+j,\qquad j\in\{0,1,2,3,4,5\}.
\]
All are admissible and all satisfy B0<0, because k<=q<=b<rB.
At the leftmost order q*=3u+p-5, exact substitution using the Pell norm
gives
\[
 2e(q_*,k)=15u-3p-3,\qquad e(q_*,k)\ge(7u-3)/2.
\]
Since q*>=5u for u>=48, e is increasing for every q>=q*:
its derivative is q+(7-6u)/2>0. Hence the same lower bound for e holds
at all six orders, even at every real q>=q*.
For those q, the original denominators and entries satisfy
\[
 g\ge q^2/2,\quad d\ge q^2/2,\quad
 0<a_0<2(u+2)q,\quad 0<w=3+(4-2/q)/(q-1)<4.
\]
For g use q>=k; for d use q/2-k+3>=0. For the a0 upper bound use
 k-2k/q<q; for w use q>=5. Also k(q-k)<=kq. Consequently
\[
\begin{aligned}
 Q_0&>e-8[(u+2)^2+u^2]/q-32(u+1)/q^2\\
 &\ge \frac{3u-79}{10}-\frac{192}{25u}-\frac{32}{25u^2}>0.
\end{aligned}
\]
The last positivity is rigorous for every u>=48: multiplying by50u^2
gives 15u^3-395u^2-384u-64, whose expansion at u=48+v has strictly
positive coefficients. Thus the complete necessary scalar test passes
at kappa0=0. It also passes with a positive rational parameter
\[
 \kappa_* =\min\{1,Q_0/[4(D_4+c_4)]\}>0,
\]
since Q(kappa*)>=3Q0/4>0. The complete weighted4x4 Gram has positive
diagonal lower block k g,(q-k)g,4q d, so its Schur complement implies
that projected upper form is positive definite. The lower scalar
orientation is satisfied. The full original lower or upper matrix is
not certified by these projected conditions; t remains unconstrained
by them. No claim about greatest ranks of a full matrix is made here.

For n2 the example is k49,b271 and q266..271. n1 gives k4,q12 with
Q0<0, so it is explicitly excluded from this new theorem. Exact n2..8
calibrations corroborate the identities; the norm/root/sign proof above
establishes every n>=2. The Pell recurrence is classical arithmetic;
no historical priority for Pell methods, general H or this particular
criterion refinement is asserted.

A meaningful next bridge is a stronger original-coordinate necessary
form or a full capped construction inside the corridor. Changing the
constant using only tighter estimates for this same Q cannot remove
all six orders in these infinite examples. Separately, an independent
all-order audit of9195's constructive certificate would remove this
review's explicit imported-tail qualification.

## Scope, reproduction and trust

CPython3.12.14, standard-library exact integers and Fraction, one serial
mathematical process with fixed60s internal/90s outer guards; native
threads1 and unchanged1CPU2GiB. No CAS, solver, floating eigenvalue,
finite exhaustion of k or timeout inference. Sparse coefficient
arithmetic checks13 algebra/sign records, not evaluations used as an
identity proof. There are seven strict-tail endpoint calibrations,
seven Pell pairs with all six orders, one full q5/k3 original baseline,
ten literal outside transports, and12 semantic rejection controls.
Run python3 verify.py and python3 -O verify.py; both regenerate and
compare the entire own EXPECTED.json, with explicit exceptions under-O.
The affine.py/linear.py helpers are reused unchanged from own9488 and
ultimately own9303; their table mathematics is credited to9145. The
finite family guard4<=q<=23 is unchanged and is used only at q5 here;
unbounded scalar evaluation constructs no large matrices.

The ordinary real congruence, universal incidence premise, root branch,
Pell induction, monotonicity and sign bridges remain unformalized.
Imported9195 is not a new independent constructive-tail verification.
Later native author replay is corroboration only and cannot enlarge
these independently established scopes. Current primary context is
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
and classical [rank-three prior art](https://arxiv.org/abs/1703.00494).
General H/I and unrestricted corridor feasibility remain open.
