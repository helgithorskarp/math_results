# Fractional outside groups in a primitive covering budget

Actual author **six-covering-3**, researcher, 2026-10-01. Written structural
lemma and exact author checks; no independent review or formalization is
claimed. This is a reusable necessary inequality, not a numerical value
of the unrestricted exactly-eight optimum.

## Hypotheses and the existing top budget

Use the hypotheses and notation of the published
[labelled-block budget](../four-top-block-dp/proof.md):
`B=2^alpha 3^beta`, alpha,beta positive; `gcd(B,C)=1`; `N=BC`;
`T=B/6`; and `b|T`. A prescribed set P has distinct moduli dividing N.
The unused permitted divisors R are disjoint from its moduli. Every
full-B resource `S={Bd:d|C}` is prescribed or available. Top phases
already prescribed remain fixed. A completion may omit available resources.

Let u be nonnegative on residues modulo N and zero on every prescribed
class. Let v be nonnegative and periodic modulo bC, including on known
classes. Put `F=R outside S`. Write D for total demand and Phi for an
actual congruence-class footprint. No actual LCM equal to N is assumed.

For top phases `(t_d modB,r_d modd)`, set

    H(q,z)={j mod6:t_d=q+Tj and z=r_d modd for some d|C}.

Identify j with `(j mod2,j mod3)`. If H has a,c columns marked only in
binary rows 0,1 and d columns marked in both rows, use

    kappa(H)=2d+max(0,2max(a,c)-3).

The published sharp primitive lemma says that any additive grid function
`f(e,j)=x(e)+y(j)` with f>=-1 on H and f>=0 elsewhere has sum at least
`-kappa(H)`. The same published exact top budget is retained:

    K=max over legal complete top phases of
      [sum_(d|C)Phi_(Bd,a_d)(u)
       +sum_(q modT,z modC)kappa(H(q,z))*v(q modb,z)].       (1)

The u footprint of a prescribed top is zero. All prescribed top phases
participate in H. In particular no known top v footprint is subtracted
from the left side of the inequality below.

## Group theorem

Choose nonempty subsets G of F and coefficients lambda_G>=0 satisfying

    sum_(G containing n)lambda_G=1 for every n in F.      (2)

For each group there are two permitted modes. The general mode uses the
sum of its individual v footprints. The stronger union mode is permitted
under the checkable sufficient condition

    L_B(G)=lcm_(n in G)gcd(B,n) < B.                     (3)

One may use the general mode even when (3) holds. This is a sufficient
condition for union mode, not a necessary classification of all groups
or special phase configurations.

For actual phases a_n of the group let A_n be their congruence classes
and U_G their union. Define

    M_G(u,v)=max over all actual phases of the members of G
      [Phi_(U_G)(u)+Z_G(v)],                            (4)

where `Z_G(v)=Phi_(U_G)(v)` in union mode and
`Z_G(v)=sum_(n in G)Phi_(n,a_n)(v)` in general mode. Maxima in (4)
combine the two weights at the SAME phase tuple; they are not sums of
independently maximized u and v terms.

**Theorem.** Every covering completion satisfies

    D(u+v)-sum_(known outside (n,a))Phi_(n,a)(v)
       <=sum_G lambda_G M_G(u,v)+K.                     (5)

Singletons in general mode recover the published mixed bound. Every
M_G is at most the sum of its members' singleton capacities of u+v.
Thus any fixed literal grouping in (2) weakens none of those singleton
budgets. Switching a permissible group from general to union mode also
cannot increase its capacity. Neither assertion establishes an exclusion
without a strict integer comparison of the full demand and capacity.

**Proof.** Adjoin arbitrary phases for all unused permitted resources
omitted by a hypothetical cover. This preserves coverage and distinctness.
Retain all prescribed phases. Denote by g_G the union indicator in union
mode and the sum of member indicators in general mode. For each member n,
`g_G>=1_(A_n)` pointwise. Equation (2) consequently implies

    sum_G lambda_G g_G >= 1_(A_n) for every free outside n.

At every point not covered by a top class, coverage therefore gives

    h=sum_(known outside)1_(A_n)+sum_G lambda_G g_G-1 >=0.

Everywhere h>=-1. On a fixed primitive block `(q+Tj,z)` each outside
individual indicator has a proper-divisor period in j and is additive
on the 2x3 grid. In union mode the union is periodic in its B coordinate
modulo L_B(G). By (3), this number divides B/ell for ell=2 or3. A shift
`j -> j+6/ell` is therefore a period of the union on the block, including
when only some members are active at z. Its indicator is additive too.
In general mode the sum is additive without (3). Known outside indicators
are additive. Hence h is additive on each block, is nonnegative off
H(q,z), and is at least -1 on H(q,z).

Apply the sharp primitive lemma and multiply by the nonnegative block
constant v(q modb,z). Summing the blocks gives

    D(v)<=sum_knownoutside Phi(v)+sum_G lambda_G Z_G(v)
          +sum_(q,z)kappa(H(q,z))*v(q modb,z).

For the ordinary u bound, a point of positive u is outside every known
class. If a free outside class covers it, the sum of weighted group UNION
indicators is at least one by (2). Otherwise a top class covers it.
Nonnegative counting therefore yields

    D(u)<=sum_G lambda_G Phi_(U_G)(u)+sum_(d|C)Phi_(Bd,a_d)(u).

Add these two inequalities. Maximize each actual group score at its same
phase tuple, and maximize the actual complete top score only over legal
free top phases. This proves (5). QED.

The proof applies to real nonnegative weights and coefficients. The code
implements integer weights and rational pair coefficients c/scale.
For an exactly-eight application P must contain modulus8 and every
permitted modulus must be at least8. The general small controls have
lower minimum moduli and are not constructions for the assigned target.

## Exact pair oracle and a caution about union mode

For a pair m,n, let w=u+v, g=gcd(m,n), L=lcm(m,n). Its score is

    Phi_(m,a)(w)+Phi_(n,b)(w)-Phi_(A_m intersection A_n)(r),

where r=w in union mode and r=u in general mode. If a,b disagree modulo
g the intersection is empty. Otherwise they specify one class modulo L.
The L choices of its residue enumerate EVERY compatible phase pair once.
For incompatible pairs, maximize each individual footprint within each
gcd coset. For each m coset the best different n coset is among the two
best distinct n cosets. These two finite lists are complete and give an
exact maximum and actual maximizing phases. Histograms are ordinary
physical-residue sums; no orbit or floating solver is used.

`groups.py` implements this reduction, and `check_groups.py` compares it with
literal progression unions. Its overlap deduction is r, rather than
always w: omitting condition (3) can give false exclusions.

For example the distinct classes

    (2,0),(3,0),(4,1),(6,5),(12,7)

cover every residue modulo12. Take B=12,C=1,u=0,v=1 and no prescriptions.
There is one top12 resource; every singleton marked set has charge zero,
so K=0. Group all outside resources {2,3,4,6}. Their individual v footprints
sum to15. Exhaustion of all144 actual outside phase tuples shows that
their union can cover at most11 residues. Thus the unjustified union
replacement would assert `12<=11` and reject this genuine cover. Here
L_B(G)=12=B, and (3) correctly forbids that replacement. The valid general
group score is15. This counterexample concerns the general inequality,
not the existence of a minimum-eight covering.

The group count and convex maximum principles are standard. This result
combines the earlier
[joint-capacity argument](../../../number_theory/distinct_covering_joint_capacity/proof.md)
with the sharp primitive top budget and identifies a sufficient proper-period
condition for union-counting v. No historical-priority claim is made.

For a fixed group and phase tuple the score in (4) is linear in (u,v).
Hence M_G is a finite maximum of linear functions, and its epigraph can
be imposed by those actual-phase rows. The pair oracle returns a literal
maximizer and thus an exact separating row for a proposed vector. Combined
with the existing K oracle, this supplies complete separation for a FIXED
grouped relaxation. It does not certify the optimum of a floating-point
master solve, a choice of grouping, or covering feasibility.

## Reproduction and scope

The accompanying README gives the complete source dependency and commands.
The literal fixture is a budget control at period10080 with a prescribed
minimum8 class. It is not a covering witness. The test summary states
its actual strict or nonstrict comparison without interpreting a search
timeout or failure as nonexistence. The global candidates remain
{10080,15120,20160}; no new numerical lower or upper bound is asserted here.

Primary context is
[Zhang--Zhang](https://arxiv.org/html/2607.19029), which claims L_min(7)=10080,
and [HKLT](https://arxiv.org/html/2605.18644), which treats restricted prime
support. Their numerical exclusions are not proof premises. The primitive
charge and exact K dependency is source commit
2d195230df390e3f7483a00e7c4782a7ddf5fddf, graph8604; the compatible
literal adapter was added in0b3bc5f488e3b3c131596cf8b829ff1b0b7db02e.
The group-counting context is source d1c0f5712486644eb3963d074c81743bfc9e4bec,
graph7228. Neither earlier contribution has independently reviewed this one.
