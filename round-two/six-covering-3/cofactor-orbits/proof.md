# Exact coordinate-fiber quotients for the C35 top budget

Actual author **six-covering-3**, researcher, 2026-10-01. Proved written
symmetry reduction with exact author checks; no independent review,
formalization or improvement of L_min(8) is claimed.

We optimize the same labelled-block budget K as the published
[four-top result](../four-top-block-dp/proof.md), graph8604, source
2d195230df390e3f7483a00e7c4782a7ddf5fddf. Here C=35, the B-part is
`B=2^alpha 3^beta` with alpha,beta positive, `T=B/6` and `b|T`.
The four top resources have cofactor parts1,5,7,35. Their B coordinates
and prescribed phases remain actual coordinates; no primitive labels
are merged.

For nonnegative tables u(t,z) and v(q,z), z modulo35, let the objective of
a legal complete top-phase assignment `(t_d,r_d)` be

    A=sum_(d in{1,5,7,35}) sum_(z=r_d modd)u(t_d,z)
      +sum_(q modT,z mod35)kappa(H(q,z))*v(q modb,z),
    H(q,z)={j mod6:t_d=q+Tj and z=r_d modd for some d}.

The sharp kappa and exact dynamic program over actual labels are the
published dependencies. We change only the cofactor-tuple enumeration
used by that dynamic program.

## Certified product action

View z by its coordinates `(z mod5,z mod7)`. For p=5 or7 and the other
prime h, define the signature of a value a modulo p as the entire vector

    (u(t,a,c) for all t,c modh; v(q,a,c) for all q,c modh).

Equality is exact, not approximate or averaged. Partition coordinate
values by identical signatures. If a prescribed top with p dividing its
cofactor fixes value a, split a out as a singleton. This must include the
values of prescribed top35 as well as top5 or top7. These splits preserve
signature equality within every remaining class.

Let Gamma be the product of the symmetric groups on the resulting classes
for both coordinates. Every factor permutation preserves BOTH weight
tables. The product action consequently preserves them as well, and fixes
every prescribed top cofactor coordinate. B coordinates are untouched.

For any d in{1,5,7,35}, a cofactor class modulo d maps to another cofactor
class modulo d: it fixes exactly the coordinate predicates for primes
dividing d. Therefore top footprints transform by a bijection of z. Also
`H'(q,gamma(z))=H(q,z)` as sets of the SAME primitive j points. Their kappa
charges and v weights agree. Thus A is invariant under Gamma, with all
prescribed phases preserved. This argument does not require the action
to be an affine map on integers or to fix every prescribed outside class:
K uses outside classes only through its input tables and prescribed TOP
phases. It is a quotient of the top budget, not a normalization of the
entire covering search or its ordinary demand functional.

## Complete representatives

A cofactor tuple is specified by the ordered coordinate pairs

    (r5,s mod5), (r7,s mod7),

where s is the cofactor phase of top35; top1 has its sole cofactor value0.
For one coordinate partition, the orbit of an ordered pair has one of
these forms:

* Values in different classes: the ordered pair of their class indices.
* Equal values in one class: that class index and equality.
* Distinct values in one class: that class index and inequality.

The last form exists only if the class has at least two members. Independent
within-class permutations are transitive on each form, including distinct
ordered pairs. Hence c classes, k of them nonsingletons, give exactly
`c^2+k` ordered-pair orbits. Representatives use the first element of each
class and, for inequality in one class, its first two elements.

Combine the5- and7-coordinate representatives and obtain s by CRT. Filter
against prescribed top cofactor phases. This filtering is complete because
all fixed values were split into singleton classes: every legal orbit
retains those values, and its representative is legal. Conversely each
remaining representative is a legal actual cofactor tuple.

**Theorem.** The maximum K over all legal top phases equals the maximum
obtained by running the existing exact within-tuple dynamic program on
these representatives alone, with the same prescribed B-coordinate phases.

**Proof.** Every legal complete assignment maps under Gamma to a legal
assignment with representative cofactor tuple and identical score A.
The B phases are unchanged, so it remains feasible for that tuple's exact
labelled-block dynamic program. Every original score is bounded by the
representative maximum. Each representative is an original legal tuple,
giving the converse inequality. QED.

If all coordinate values are distinguishable, there are25 ordered pairs
at prime5 and49 at prime7: the full1225 tuples are retained. Thus weak or
absent recognized symmetry does not turn into a search cutoff. This is a
certified subgroup, not a claim to identify all joint automorphisms or the
largest possible symmetry quotient.

Signatures must be recomputed for each new input vector. The maximizing
actual phase witness is a valid row of the original K epigraph, so this
quotient can accelerate an exact separation oracle. A fixed representative
list is complete only on the domain of tables invariant under its same
group; a one-vector equality does not justify permanently dropping other
rows from an unrestricted master problem.

## Target-sized applications and controls

At the literal prefix from graph8680

    8:0,9:0,10:0,14:1,12:0, period10080,

all four tops are free. The previously checked uniform residual u and
1680-periodic projected residual v distinguish value0 at prime5 and
value1 at prime7. The other four or six coordinate values have identical
fiber signatures. Each coordinate has c=2,k=1, hence5 ordered-pair orbits.
Exactly25 tuples replace1225. Both complete and reduced optimizers give
`K=174`, and each returned witness is checked by the direct definition.
Local assignment visits fall from141120000 to2880000, exactly49-fold.
This is a reduction of the SAME budget computation, not a stricter bound
or a period10080 exclusion.

The actual-label fixtures at B=288 and432 retain value482 with25 tuples;
at B432 visits drop from211680000 to4320000. Fully uniform weights need
only4 cofactor tuples, while asymmetric u alone or v alone triggers the
full1225. Fixed top5,7,35 and simultaneous prescribed phases are checked.
Two complete-mode runs match the original published optimizer's entire
JSON, including its actual maximizing phases and visit counts.

The code is a compact derivative of the author's prior exact optimizer;
its block profiles, charge formula and dynamic-program core are reused,
not new algorithms claimed here. The new coordinate-class recognition
and complete cofactor-orbit argument are the extension. Default mode
enumerates every cofactor tuple; `--orbits` enables only the certified
quotient and reports its classes and full count.

The checker independently constructs signatures by explicit CRT fibers,
canonicalizes EVERY legal tuple, supplies full coordinate permutations,
and checks prescribed values. Selected controls additionally verify all
physical weight entries and direct budget scores under all tuple transports.
Complete and quotient C++ maxima are compared on every fixture; all
maximizing witnesses are checked literally. These finite controls check
the implementation; the group-action proof supplies universal exactness.

Reproduction and trust limits are in README.md. The source is standard
C++17/Python3.11 with one thread and the existing bounded integer domain.
Timeouts, resource kills, incomplete computations or solver statuses are
not exclusions. No new construction, global L_min(8) bound or minimum
modulus record is claimed. The current global candidates are10080,15120,20160;
the complementary published parity restriction leaves19 affine research
cases at10080. Exactly-eight remains separate from at-least-eight.

Primary context: [Zhang--Zhang](https://arxiv.org/html/2607.19029) claims
minimum-seven optimum10080; [HKLT](https://arxiv.org/html/2605.18644)
studies restricted prime support. Neither numerical exclusion is a premise.
The canonical handoff is source23565f309733c60a6ad4345bcd8189794fca7c93,
graph8680; its tree exclusions are not dependencies of the symmetry proof.
