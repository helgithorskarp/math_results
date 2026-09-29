# Finite residual-state reduction for a fixed coprime cofactor

Author: six-covering-3, researcher, 2026-09-29.

This is a structural reduction, not a determination of L_min(8).
The proof is mathematical; the accompanying code checks its implementation
on small instances. No exhaustive computation for the large cofactors relevant
to L_min(8) is claimed.

## Definitions and completion

Fix a prime p, a positive integer M coprime to p, and a minimum threshold m >= 2.
Write D = {d : d divides M}, k = |D| = tau(M), and

    s = min{e >= 0 : p^e >= m}.

A class with modulus p^j d is a Cartesian cylinder, under CRT:

    z = r (mod p^j),  y = b (mod d),

where z is the p-coordinate and y belongs to Z/MZ. At most one class may be
chosen for each pair (j,d). The pair is admissible exactly when p^j d >= m.
We allow admissible classes to be omitted during the construction.

If a covering with moduli dividing L and at least m exists, adding arbitrary
classes for missing admissible divisors of L preserves both covering and
distinctness. Adding L itself makes the LCM exactly L. If m divides L, adding
m makes the minimum exactly m. Thus, whenever m divides p^A M and p^A M >= m,
the completed model is equivalent to the problem with minimum exactly m and
LCM exactly p^A M. This does not equate exactly-m and at-least-m when m does
not divide L.

## Lemma 1: residual fiber capacity

Suppose chosen classes with exponents at most e have been placed. For each
p-prefix r modulo p^e, define its residual subset of Z/MZ by

    U_r = {y : (r,y) is not covered by those classes}.

Here a class of exponent j <= e tests r modulo p^j, so this definition is
well-defined. Let n_e be the number of nonempty U_r.

Let k_j be any upper bound on the number of available distinct moduli of
exponent j. If the partial system extends to a finite cover with largest
exponent A >= e, then

    n_e <= floor(sum_{j=e+1}^A k_j / p^(j-e)).                 (1)

In particular, when k_j <= k for every j, every partial stage of a finite
cover satisfies

    n_e <= floor(k * (1 - p^(-(A-e))) / (p-1)),              (2)

and consequently

    n_e <= W := floor((k-1)/(p-1)).                         (3)

**Proof.** On passing from depth t to t+1, each nonempty U_r produces p
identical nonempty residual copies. A class of exponent t+1 acts in only one
child and can make at most one child empty. There are at most k_{t+1} such
classes. Therefore

    n_{t+1} >= p n_t - k_{t+1}.

Iterating to n_A = 0 gives

    0 >= p^(A-e) n_e - sum_{j=e+1}^A p^(A-j) k_j,

which proves (1). Summing the geometric series proves (2). For every finite
A-e, its right-hand real bound is strictly less than k/(p-1). The largest
integer strictly less than k/(p-1) is floor((k-1)/(p-1)), giving (3). The case
A=e has n_e=0 and is also covered. In particular the equality boundary
n_e=k/(p-1), when integral, is forbidden; it cannot eventually terminate. QED.

## Lemma 2: the anonymous residual multiset is an exact continuation state

Discard empty fibers and sort the remaining subsets into a multiset

    S_e = multiset{U_r : U_r is nonempty}.

An exact transition from e to e+1 is as follows:

1. Replace every member U by p copies of U.
2. For each admissible d in D, either omit the modulus p^(e+1)d, or choose
   one of the current copies and a residue b modulo d, and replace its
   residual set V by V minus {y : y=b modulo d}.
3. Drop empty members and forget the labels again.

At most one operation is allowed for each d. The order of the operations
does not change their meaning: they subtract unions within the assigned
children.

**Proof.** A real collection of congruences plainly induces such a transition
by CRT. Conversely, initially give each copy its actual child prefix modulo
p^(e+1). Assign every operation to one such copy. CRT supplies a unique
residue modulo p^(e+1)d realizing the specified prefix and b. Each d is used
at most once, so all moduli remain distinct.

When two states have the same multiset, match their nonempty fibers by a
bijection. Any future choices can be transported along this bijection, and
then separately along the children of each matched fiber. Earlier classes
need not be permuted or changed: their entire effect on future coverage has
already been recorded in U_r. There is no resource attached to a parent;
the one-per-d resource is shared across the whole next level and is preserved
by the bijection. Empty fibers need no future classes. This proves equality
of their continuation possibilities.

Allowing omissions causes no problem, including when the omitted class was
redundant in an empty fiber: after a complete cover is obtained, divisor
completion can restore every missing class. QED.

## Theorem: an explicit cutoff for the unbounded exponent

Assume m/p^v divides M, where v is the largest exponent such that p^v divides m.
Let

    W = floor((tau(M)-1)/(p-1)),
    N = binomial(2^M - 1 + W, W),
    B = s + N - 1.

There exists a distinct covering with minimum exactly m and LCM p^A M for
some A >= s if and only if one exists for an exponent in [s,B]. Equivalently,
the existential question over all A is decided by a finite directed graph
of residual multisets and an initial finite computation through depth s.

**Proof.** All pairs (e,d) are admissible for e >= s. Enumerate the initial
layers 0 through s according to Lemma 2, dropping any state with more than W
members. Lemma 1 proves that no successful state is thereby lost. There are
only K=2^M-1 different nonempty subsets of Z/MZ. The number of multisets of
at most W such subsets, including the empty multiset, is

    sum_{i=0}^W binomial(K+i-1,i) = binomial(K+W,W) = N.

For later depths the transition rule is independent of the absolute depth.
Lemma 2 makes this a genuinely exact quotient, not a relaxation. Any path
from an initial state to the empty state can have its repeated states
removed. The resulting path has at most N-1 edges. Realizing those transitions
by Lemma 2 gives a covering by depth s+N-1. The divisibility assumption implies
m divides p^s M, because v <= s. Completing the constructed cover therefore
gives minimum exactly m and LCM exactly p^A M. The converse is immediate.

If a cover initially exists with A<s, completion at L=p^s M yields one at
A=s, so the same cutoff decides existence for any nonnegative exponent.
If the divisibility assumption fails, exact minimum m is impossible for
every exponent, independently of the state calculation. QED.

## Corollary: independent symmetries inside each residual fiber

Let G be any finite group of permutations of Z/MZ such that, for every d|M,
every g in G maps every residue class modulo d to a residue class modulo the
same d. Let H be the number of G-orbits of subsets of Z/MZ, including the
empty set. The theorem remains true with the sharper cutoff

    B_G = s + binomial(H - 1 + W, W) - 1.

**Proof.** Different surviving p-prefix fibers may be normalized by different
elements of G. A later class acts in only one descendant of one such fiber.
Transport its cofactor residue by that fiber's permutation. Its modulus is
unchanged and the one-per-d resources at each later depth are unchanged.
Transport further descendants in the same manner. Earlier classes stay fixed:
their effects are recorded in the residual sets. Hence the exact continuation
state is a multiset of nonempty subset-orbits. There are H-1 available types,
and the same state-counting and path-shortening proof applies. This is local
normalization of continuation data, not a claim that arbitrary independent
permutations preserve the already chosen global classes. QED.

In particular, G can be the translation group of Z/MZ. Its orbit count is

    H_M = (1/M) sum_{t=0}^{M-1} 2^gcd(M,t).

Indeed, translation by t has gcd(M,t) cycles; a subset fixed by that translation
is a union of cycles, so there are 2^gcd(M,t) fixed subsets. Averaging fixed-set
counts over the group gives the number of orbits (count pairs (g,U) with gU=U
and then use orbit-stabilizer). Thus H_M is an exact integer and effectively
computable without enumerating all subsets.

For M=q^b, with prime q different from p, there is a larger useful group:
independent permutations of the q children at every vertex of the depth-b
rooted q-ary residue tree. Digits are read from least significant to most
significant, so a residue class modulo q^j is exactly a depth-j subtree.
These permutations preserve every modulus q^j. The number h_b of subset
orbits, including the empty set, satisfies

    h_0 = 2,
    h_{b+1} = binomial(h_b + q - 1, q).

At each vertex a subset is determined up to tree automorphism by the multiset
of its q child subset-types; all such multisets are realized. Hence the
recurrence is exact. Taking H=h_b in B_G gives this stronger cutoff without
changing the width bound. For a product cofactor, one must count subset-orbits
on the product itself; multiplying the individual orbit counts would not be
justified.

## Specialization to minimum eight

For odd M and p=2, s=3, W=tau(M)-1, and the cutoff is

    A <= 2 + binomial(2^M + tau(M) - 2, tau(M)-1).

For a specified A, the stronger finite-horizon bound is

    n_e <= floor(tau(M) * (1 - 2^(-(A-e)))).

The quotient permits an exact search with bitsets of length M, rather than
bitsets of length 2^A M. Its number of states is still generally enormous.
The theorem makes an unbounded exponent question finite; it supplies neither
a practical complexity bound nor a numerical improvement to L_min(8).

The same bound can be used as a necessary pruning rule in a conventional
construction or exclusion search. A terminal reachable state proves a
construction; a complete closed set of nonterminal reachable states proves
nonexistence for every exponent with that fixed cofactor. A time limit,
memory limit, or incomplete exploration proves no such nonexistence.

For an existing full residue-choice integer program, the finite-horizon bound
gives a direct necessary cut. At a chosen depth e introduce binary variables
z_r for r modulo p^e. For each pair (r,y), with y modulo M, impose

    z_r + sum_{j<=e, d|M, p^j d>=m}
        x_{p^j d, CRT(r mod p^j, y mod d)} >= 1.

Here the CRT residue is reduced modulo p^j d. The row forces z_r=1 whenever
that fiber has an uncovered y; it allows z_r=0 for fully covered fibers.
Also impose

    sum_r z_r <= floor(sum_{j=e+1}^A k_j / p^(j-e)).

Lemma 1 proves that every genuine covering has a valid assignment to these
variables (take z_r exactly to indicate nonempty residuals). Thus this is a
safe additional constraint, not a bounded-search completeness assumption.
No optimizer implementation or numerical performance claim is made here.

For illustration, the cutoff for M=9 is 131330 before cofactor symmetries,
1832 using translations (H_9=60), and 212 using the ternary residue tree
(h_2=20). These are upper cutoffs for an existential decision procedure,
not covering constructions; in fact this small cofactor is already excluded
by the initial residual-width controls. The reductions are intended to be
reused on cofactors not already settled by such elementary controls.

## Prior work and scope

The CRT box representation and divisor completion are existing tools. See
Harrington–Klein–Lowrance–Trifonov, [arXiv:2605.18644v1](https://arxiv.org/html/2605.18644),
Sections 2–3, and Zhang–Zhang,
[arXiv:2607.19029v1](https://arxiv.org/html/2607.19029), Sections 2 and 5.
The former explicitly leaves the minimum-eight classification at fixed
prime support open. The contribution here is the residual-width argument,
its exact multiset continuation quotient, the independent within-fiber
symmetry compression, and the resulting exponent cutoff.
Targeted literature and committed graph searches found no instance of this
specific reduction; this is not a claim of priority.

No published computer-assisted lower bound is assumed in this proof. The
minimum-seven witness used by the checker is an attributed validation example,
and its direct verification does not reproduce the paper's exclusion runs.
