# Independent derivation and a stronger complete-principal relaxation

Actual six-reviewer-5, independent mathematical reviewer. Ordinary proof,
unformalized. The complete written LEMMA9793 was visible; its executable,
fixtures and provenance have not been used to write this primary derivation.
The bulk count is **G=2s-2-2K**, not T-2K when T=4s-4. The latter is a
literal typographical error in the first paragraph of the target's identity
proof; its later identities and companion compression use the correct count.

Fix n>=6 and 2<=k<=floor((n-2)/2). Use every original vertex of
D={A subset[n]: |A|<=n-2}, including the empty vertex and allowed loop.
N=2^n-n-1, s=2^(n-1)-n, h=N-s, r=n-1, Z=2s-2, T=2Z.
M is real symmetric, M1=1, zero whenever A intersects B, and
0<=sI+hM<=NI. No centering, invariance, rationality, sign, rank or gap premise.
S_k kills proper disjoint nonempty entries whose two sizes exceed k.
Let K=sum(a=2..k,C(n,a)), G=Z-2K, and
c=nh-nrs+(h-s^2/h)sum(a=2..k,a^2 C(n,a)).
All sums below over bulk vertices count both complementary members.

## Reconstructing the original compression

For F=D minus empty, B=hM_FF, C=sI-J+B and U=hI-B. Symmetry and
L1=N1 imply L-J>=0, hence C>=0. Every point-star has s entries and
its centered indicator has zero L energy, so PSD kills it. Thus each
individual star is in ker C, and Ca=0 for a_A=|A|. Original regularity
fixes L_empty,A=1-(C1)_A and L_empty,empty=1+1'C1, giving
L=J+ECE', E=[-1';I]. The cap gives U>=0.
For each bulk complement pair z_A=s-B_A,Ac=z_Ac; its original odd/even
energies give 0<=z<=Z<N. All denominators below are positive.

For any u whose low entries are |A|, substituting the cardinality kernel
into u'Uu gives

u'Uu=h sum u_A^2+2s sum (|A|-n)u_A-s sum |A|^2+n^2 s^2
       -sum_bulk (s-z_A)(|A|-u_A)(n-|A|-u_Ac)

under S_k. Without S_k append -2 sum_proper_bulk B_AB f_A f_B.
This formula follows entry by entry: low-touching shifted entries vanish,
high vertices have no disjoint high/bulk partner, and sum_F |A|=ns.
For arbitrary supported B before imposing Ca=0, retain the exact defect
(a-2u)'Ca in the combined upper/lower identity. Removing it for a free
matrix would be false. The definition-level independent program checks it.

Set v=(u_A+u_Ac)/2, t=(u_A-u_Ac)/2, x=|A|-n/2. The literal unordered
pair contribution is

-s n^2+2 phi_a(z)+2(r+z)(v-v*)^2+2(N-z)(t-t*)^2,
phi_a(z)=n^2 r z/[4(r+z)]-N x^2 z/(N-z),
v*=nz/[2(r+z)], t*=-xz/(N-z).

Each low/high pair of sizes a,n-a contributes
(h-s^2/h)a^2-sn^2 after completing the high square. The n singletons
have no n-1 partners and contribute n(N-2ns). Because G+2K=2s-2,
the global constant is nh-nrs. This proves the entire compression,
including arbitrary individual bulk/high coordinates. Scaling low entries
by any real d scales every optimum by d and the constant by d^2;
d=0 is covered. All remaining square weights are positive. Consequently
U restricted to this subspace is PSD iff E(z)=c+sum phi_a(z_A)>=0.
This is a restricted cap equivalence, not whole original feasibility.

For arbitrary original M, ell=0/1/2 on low/bulk/high gives
ell'C ell=T-sum_bulk z_A+2 sum_proper_bulk B_AB. Adding lambda times
this to the preceding identity gives precisely the target's signed identity.
Its coefficient condition w_a=f_a f_n-a<=lambda, positivity and strict
increase of f make every proper-pair rho positive and less than one.
Negative entries only lower its weighted sum. The maximum-weight conversion
to positive original mass is valid and credited to review9513.

The exact scalar identity
r v^2+N t^2+lambda z-phi_a(z)
 =(r+z)(v-v*)^2+(N-z)(t-t*)^2+z[lambda-(a-v-t)(n-a-v+t)]
proves the target's global, potentially nonconvex test-profile minimum
without invoking convexity of its quadratic constraint. Strict concavity of
phi, clipped monotone derivatives, the central-layer boundary arguments
and their multiplicities give its unique positive budget multiplier and
its exact two-test optimum. These steps are ordinary calculus, not finite
extrapolation. Positive active roots lie below Z because lambda>eps_n.
Its monotonic f proof is valid: the displayed dx/dd is positive since
lambda/m^2<=1 and z<N. The inactive regions join continuously with f=a.

## Proved refinement: optimize the whole free lower principal constraint

Under S_k the **entire** bulk/high original principal matrix is D-J:
high diagonal s and complement blocks [[s,s-z],[s-z,s]]. Odd modes have
coefficient z and are killed by J. Weighted Cauchy--Schwarz on even/high
modes proves, including z=0, that this matrix is PSD iff

Gamma(z)=sum_bulk z_A/(2s-z_A)<=2.

Its full positive definiteness requires every z_A>0 and Gamma<2. These
are the target's correct principal criterion and boundary conditions.
A violating rank-one direction is the even/high diagonal inverse times 1;
this remains a literal negative-energy witness.

Define the new relaxation

R_Gamma = max { c+sum_bulk phi_a(z_A):
  z_A=z_Ac, 0<=z_A<=Z, Gamma(z)<=2 }.

It imposes the entire free lower principal matrix AND the exact restricted
upper compression. Its nonnegative value is necessary for a capped S_k H;
it does not recover the low-row couplings or other cap/lower directions.
The feasible set is compact and convex (Gamma is strictly convex), phi is
strictly concave, and zero is feasible. Hence the maximizer is unique.

For mu>=0 each q_a(z)=phi_a(z)-mu z/(2s-z) is strictly concave. Let
z_a(mu) be its unique maximum on [0,Z]. It is zero iff
mu>=2s a(n-a), is the upper endpoint when the derivative there is
nonnegative, and otherwise is the unique root

phi'_a(z)=mu*2s/(2s-z)^2.

Clearing its positive denominators gives a quartic; the monotone derivative
selects the root unambiguously. Its deficit mass Gamma(mu) is continuous
and decreases strictly whenever an uncapped active layer is present.
At mu=0 the independent-maximizer total deficit exceeds T by the target's
verified central-layer inequalities (even n: central z=Z with multiplicity
>2; odd n: central z=N r^2/(N+nr)>=r^2/2 and the binomial lower bound).
Such a profile has Gamma>2 by the Jensen budget derived below. At
mu=2s n^2/4 every root is zero. At Gamma=2 no layer can be at Z:
each multiplicity is at least20 and its contribution would be at least
20(s-1)>2. Thus there is a unique mu*>0 with Gamma(mu*)=2.
The root vector is complementary. Summing the scalar maxima proves

R_Gamma=c+2mu*+sum_bulk [phi_a(z_a(mu*))-mu* gamma(z_a(mu*))].

This is exact algebraic one-multiplier optimization; no numerical duality
assumption is required. For ANY positive rational mu the same expression
with scalar maxima is a rigorous upper bound and can exclude S_k when
negative. Exact derivative brackets and supporting tangents give rational
upper certificates for those maxima. Floating scouts only select mu.

Let m=sum_bulk z_A. Jensen gives Gamma>=Gm/(2sG-m), so
m<=B=4sG/(G+2)=T-4K/(s-K)<T. This budget is sharp for the free principal
criterion, with equality only for the constant deficit z=4s/(G+2).
Every Gamma-feasible profile belongs to the target's two-test polytope.
The target's unique optimum saturates m=T and is therefore excluded.
Compactness and uniqueness prove **R_Gamma is strictly smaller than the
old two-test optimum for EVERY allowed n,k**. This is a strict improvement
of necessary relaxation values, not a proved actual support improvement.

The new R_Gamma is strictly increasing with the allowed integer cutoff.
Put a=k+1. Restrict the old optimum after removing layers a,n-a; Gamma
only decreases. The constant increases by C(n,a)*rN a^2/h. The scalar
square identity at lambda=0 and v=Na/(2h),t=ra/(2h),w=0 proves
phi_a(z)<=rN a^2/(2h). Equality requires the scalar minimizers and hence
phi'_a(z)=0; it cannot occur at an active old optimum with mu*>0, and
at an inactive z=0 the positive bound is strict. Thus the new objective
strictly increases after removal. This proves strict monotonicity without
an asserted H construction or an assumed invariant original matrix.

The independent rational certificates give negative R_Gamma upper bounds
at (24,5),(32,7),(40,10),(48,13),(64,18),(96,30), and positive feasible
partial energies at (24,6),(32,8),(40,11),(48,14),(64,19),(96,31).
Every positive schedule has every z>0 and Gamma<2, hence whole free-lower
positive definiteness and positive restricted cap compression. Monotonicity
proves the same exact first-positive cutoffs for this stronger relaxation.
These schedules are not M matrices. Neither actual existence at48/64/96
nor an actual optimum, gap, rank, historical priority or general H/I follows.
