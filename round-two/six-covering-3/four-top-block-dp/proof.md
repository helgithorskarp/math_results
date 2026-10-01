# Optimal primitive charges and an exact budget over actual block labels

Actual author: **six-covering-3**, role **researcher**, 2026-10-01.
Status: proved structural inequalities and an exact finite optimizer, with
same-author exact checks. No independent review or formalization is claimed.
The computed examples below are budgets, not covering constructions or
exclusions of periods 10080 or 15120. The global numerical frontier is unchanged.

## 1. A sharp charge for every marked subset

Identify `Z/6` with the CRT grid `{0,1} x {0,1,2}`. Let `V` be the span of
functions having proper-divisor period; equivalently,

    f(e,j) = x(e) + y(j).

For a marked subset `H`, let `a,c` be the numbers of ternary columns
marked only in binary rows 0,1, respectively, and let `d` count columns
marked in both rows. Set

    kappa(H) = 2d + max(0, 2max(a,c)-3).                 (1)

**Lemma.** If `f in V`, `f>=-1` on H and `f>=0` outside H, then

    sum f >= -kappa(H).                                (2)

The constant is sharp for these signed-function hypotheses. In particular,
it is zero for an empty set or singleton. It is monotone under adding
marked points, and no larger than the prior distinct-point charge
`|H|` for `|H|>=2` (and zero otherwise).

**Proof.** Consider nonnegative arrays `omega` whose binary lines have
sum 2 and ternary lines have sum 3. They have the form

    omega(0,j)=1+h_j, omega(1,j)=1-h_j,
    -1<=h_j<=1, h_0+h_1+h_2=0.

Their proper-period moments equal those of the constant array one, so
`sum omega*f = sum f` for f in V. It follows that

    sum f >= -sum_(x in H) omega(x).                    (3)

The feasible h polygon has the six permutations of `(-1,0,1)` as its
vertices. To minimize its marked mass, initially set h=-1 at the a
row-zero-only columns and h=+1 at the c row-one-only columns. The other
`3-a-c` columns have coefficients zero in the objective and can balance
this choice if `|a-c|<=3-a-c`. Otherwise the unavoidable adjustment of
the marked h entries is `|a-c|-(3-a-c)=2max(a,c)-3`. Each unit of this
adjustment costs one unit of mass. Both balancing and adjustment are
attainable within [-1,1]. The minimum mass is consequently (1).

For sharpness, begin with f=-1 on each doubly marked column and zero
elsewhere, a function independent of the binary coordinate. If
`k=max(a,c)<=1`, this attains (2). If k>=2, choose the binary row e with k
singly marked columns J and add

    -1_(binary row=e) + 1_(ternary column outside J).

This is in V, has total `3-2k`, and introduces negative values only -1
at those singly marked points. At doubly marked columns its addition is
zero in row e and one in the other row, so it causes no value below -1.
It is nonnegative at every unmarked point. Its resulting total is
`-2d+3-2k=-kappa(H)`, proving sharpness. The minimum-mass description
shows monotonicity; the constant array one gives mass |H|. QED.

The same proof gives `2d+max(0,2max(a,c)-p)` on a primitive `2 x p` grid
for any odd prime p, replacing the zero-coefficient count by `p-a-c` and
the added function's total by `p-2k`. Only p=3 is needed or implemented
here. Sharpness is about signed proper-period functions, not distinct
coverings. Equation (1) takes all coincidences as a set of points.

## 2. Lift to covering completions, including prescribed top phases

Let `B=2^alpha*3^beta` with alpha,beta positive, let C>=1 be coprime to B,
put N=BC and T=B/6, and let b be a positive divisor of T. Use CRT
coordinates `(t modB,z modC)`.

Let P be prescribed distinct classes whose moduli divide N. Let R be the
eligible unused divisors, disjoint from the moduli in P. A completion
may choose any subset of R, with one phase per modulus. Every top
resource in

    S={Bd : d divides C}

must either be prescribed in P or available in R. Prescribed top phases
remain fixed. Let u>=0 on Z/N vanish on all prescribed classes, and let
v>=0 be periodic modulo bC; v may be positive on prescribed classes.
Use the ordinary demand D, class footprint Phi and actual phase capacity C_n:

    D(w)=sum_(x modN)w(x),
    Phi_(n,a)(w)=sum_(x=a modn)w(x), C_n(w)=max_a Phi_(n,a)(w).

For a complete top-phase choice write `(t_d,r_d)` for the B and d CRT
coordinates of the class at Bd, and put

    H_(q,z)={j mod6 : t_d=q+Tj, z=r_d modd, for some d|C}.
    U_d(t,r)=sum_(z=r modd)u(t,z).

Let K be the maximum, over all free top phases while retaining prescribed
ones, of

    sum_(d|C)U_d(t_d,r_d)
      +sum_(q modT,z modC) kappa(H_(q,z))*v(q modb,z).     (4)

The ordinary footprint of a prescribed top is zero by the hypothesis on u.

**Proposition.** Every completion covering every integer satisfies

    D(u+v)-sum_(known (n,a), n outside S)Phi_(n,a)(v)
       <= sum_(n in R outside S)C_n(u+v) + K.             (5)

Only known OUTSIDE footprints are subtracted. A strict reversal excludes
all completions with these permitted divisors. This is a necessary
condition; it is not a characterization of covering existence.

**Proof.** Adjoin any missing available top classes at arbitrary phases;
coverage and distinctness persist. Fix q,z and the six-point primitive
block `{q+Tj:j mod6}`. Every outside class has a proper B-part
`m=gcd(B,n)<B`. There is a prime ell in {2,3} with `m|B/ell`.
Its indicator on the block is invariant under `j -> j+6/ell`, or
identically zero. It is therefore in V.

The function f equal to the sum of all used outside indicators minus one
is in V. It is nonnegative outside H_(q,z), because no top class covers
those points, and at least -1 on H_(q,z). Equation (2), multiplied by
the block-constant value `v(q modb,z)`, bounds the block v-demand by its
actual outside footprints plus the charge in (4). The constancy follows
from b|T. Summing all q,z gives that bound for D(v), counting every known
and free outside footprint with its actual multiplicity.

Ordinary nonnegative counting for u adds the used free outside footprints
and the top footprints in (4); all known u-footprints vanish. Combine u
and v at each free outside resource's SAME actual phase before maximizing
that resource. Add nonnegative capacities of omitted outside resources,
move known outside v-footprints to the left, and maximize over the legal
top phases. This gives (5). No exact ambient-LCM equality or irredundancy
is needed. QED.

## 3. Exact subset dynamic programming over actual labels

List the k top resources d_1,...,d_k. Fix their cofactor residues r_i;
prescribed ones are fixed in this enumeration. For each ACTUAL block
label q in {0,...,T-1} and subset G of resources, let F_q(G) be the maximum

    sum_(i in G) U_di(q+Tj_i,r_i)
       +sum_(z modC)kappa({j_i:i inG,z=r_i moddi})v(q modb,z)     (6)

over j_i in Z/6. If i is prescribed, q and j_i must equal its actual
label and point. Set F_q(empty)=0 and F_q(G)=-infinity when impossible.
Thus each within-label maximum considers coincidences of points as well
as resource multiplicities. Let

    DP_0(empty)=0, DP_0(nonempty)=-infinity,
    DP_(q+1)(M)=max_(G subset M)[DP_q(M outside G)+F_q(G)].        (7)

Then K is exactly the maximum of `DP_T(all resources)` over the permitted
cofactor tuples.

Every actual phase assignment uniquely partitions its resources by
their actual labels q. Its value splits into the terms (6), so induction
on q proves the upper bound in (7). Conversely, every finite transition
is realizable: choose the within-label maximizing j_i, place different
groups at their different actual q values, and obtain each Bd class from
CRT. No resource is repeated. Prescribed phases are retained. Induction
gives realizability and hence equality. The maximum is of the budget (4),
not of the set of covering systems.

For a fixed cofactor tuple, fully free local tables visit
`sum_(G nonempty)6^|G|=7^k-1` assignments per label; (7) uses at most
3^k transitions per label. Without profile acceleration the periodic
sum in (6) adds a factor C. The cofactor tuple count in the fully free
case is `product_(d|C)d`. These are justified complete loops, not bounds
on a heuristic search. Finite small controls validate implementations;
the written partition argument supplies universal exactness.

This retains information missing from an independent sum of group
maxima: two groups cannot both claim the same label as separate groups.
The earlier distinct-point proof explicitly warned that its charge is
not superadditive under merging; simply replacing the older resource
count by a point count in a set-partition formula is only an upper
relaxation. Equation (7) resolves that specific realization gap.
The older multiplicity-based partition maximum really is attainable by
equal-label merging; no error in that differently defined theorem is
being alleged here.

**Epigraph separation corollary.** For a fixed complete legal top-phase
choice, the expression in (4) is linear in the entries of u and v.
Thus K is a finite maximum of linear functions. To decide whether a
proposed epigraph value h satisfies h>=K, run the exact optimizer. If it
does not, its maximizing phase witness supplies the violated linear
inequality h>=that phase's expression. This is an exact separation oracle
for the top-budget epigraph, with no solver premise. It permits weight
optimization to add only violated phase constraints instead of listing
all1225*B^4 full phases in advance. No such LP application is claimed here.

## 4. Four-resource cofactor profiles at the target periods

For C=35 the divisors are (1,5,7,35), so k=4 and there are1225 fully free
cofactor tuples `(0,r5,r7,s)`. For a local subset G and its j_i, let A be
the set containing j_1 when resource B is in G, otherwise empty. Define

    R=A union {j_5 if 5B is in G},
    L=A union {j_7 if 7B is in G},
    E=A union {j_5 if in G and s=r5 mod5}
         union {j_7 if in G and s=r7 mod7},
    E'=E union {j_35 if 35B is in G}.

Here subscripts refer to the cofactor divisor, not a resource count.
Let W5, W7 be the sums of the current block's v over z=r5 mod5 and
z=r7 mod7, let Wcross be its value at their unique CRT intersection,
and Ws its value at s. The periodic term in (6) is exactly

    kappa(R)W5 + kappa(L)W7
       +[kappa(R union L)-kappa(R)-kappa(L)]Wcross
       +[kappa(E')-kappa(E)]Ws.                          (8)

Away from these two cofactor cosets the active set is at most the
singleton A, whose charge is zero. Their intersection needs its actual
union charge rather than two charges; the singleton top then changes
only the residue s. This proves (8), including coincident j values and
cases where s lies on one or both cosets. The coefficients can be
precomputed for four overlap flags and every local assignment. Computing
profiles once per block permits constant-time local scoring thereafter.

| N | B | T | top moduli | actual phase tuples | local assignments in all tables |
|---:|---:|---:|---|---:|---:|
|10080|288|48|288,1440,2016,10080|8427641241600|141120000|
|15120|432|72|432,2160,3024,15120|42664933785600|211680000|

The phase-tuple count is1225*B^4 and the table count1225*T*2400. The DP
adds at most1225*T*81 transitions. Values in the phase-tuple column are
arithmetic counts, not claims that those tuples were directly enumerated.
For the assigned problem set R to every unplaced divisor at least8;
an exactly-eight anchor must be present or separately enforced. A cover
using only moduli>=8 is not automatically an exactly-eight witness.
The applicability of (5) needs no bounded-search completeness assumption.

## 5. Strict, analytically controlled fixtures

For B6,C5,b1 put u(0,z)=10 for every z, u(2,0)=20 and all other u=0,
and v=1 only at cofactor residue0. The old distinct-point maximum is72;
the new maximum is71. Ordinary top footprints total at most70, attained
only by the B-coordinate choices0 and2 for the two resources. At their
ternary-separated pair the new charge is1. Leaving either ordinary
maximizer loses at least10, while the charge is at most2. Both maxima
are achieved by actual phases. This is a strict budget improvement.

For B6,C35,b1 put u(0,z)=10 for every z, u(2,z)=20 when z=0 mod5,
and all other u=0; again v=1 only at z0. The four individual ordinary
maxima are350,140,50,20. Their sum is560 and all maximizing B-points
belong to {0,2}. At the weighted residue both points appear, so kappa=1
and the maximum is561. Any departure from the individual maxima loses
at least10, whereas the charge is at most4. The full Python DP and
compiled optimizer both recover561.

For ANY implemented B, take b=T, u(0,z)=u(B/2,z)=10 for every z, other
u=0, and v(q,z)=1 only at q=z=0. The four ordinary maxima total480.
When attained, the marked set at z0 is contained in the binary pair
{0,3} and has charge at most2, achievable, so K=482. Moving any resource
off these two B-points loses at least10 and its total charge is at most4.
But the independent group relaxation gives484: groups {B,5B} and
{7B,35B} each claim the same block q0 and the same binary pair, with
charge2 apiece. A local group costs at most2 beyond its ordinary maximum,
so this relaxation's484 is also exact. The actual-label DP removes that
unrealizable extra2. This fixture is checked at bases12,288,432.

## 6. Validation, provenance, and limits

The complete commands, arithmetic bounds and compact expected outputs
are in [README.md](README.md). Python checks every64 marked subset
against all six balanced vertices, constructs a sharp signed function
and verifies proper-period membership. It compares the DP with literal
top-phase enumeration, compares (8) with direct cofactor sums, and tests
actual-phase inequalities on genuine distinct covers with fixed known
top classes, positive known weights and negative effective demands.
Small controls have smaller minimum moduli; none is a target construction.

The C35 implementation compares full cofactor maxima with the exact
Python reference on five prescribed-top cases and the all-free561
fixture. Its maximizing target-scale phases are independently evaluated
by the literal Python definition. Four target-scale complete DP runs
have values482,482,821,810 for the explicitly generated fixtures.
Normal/optimized Python and address/undefined-behavior sanitizer controls
are required. Matching algorithms are author regression checks, not
independent mathematical review. A maximizing witness alone certifies
attainment; the written DP proof and complete loops justify the upper
maximum. No numerical solver, large corpus or private frontier is needed.

The CRT/divisor-completion context is in
[Zhang--Zhang](https://arxiv.org/html/2607.19029), whose minimum-seven
result is claimed with complete Gurobi computations, and
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644),
which studies the restricted three-prime family. Both were refreshed live
2026-10-01. Their numerical exclusions are not proof premises here.

The block framework credits six-covering-3's
[primitive-block proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420
`bafkreif6bscwv7wqq4m26wb2ryapjmbifo6f3usxbegdlj7mnzcbihn46e`.
The author's earlier
[partition realization](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_primitive_partition_realization/proof.md),
graph7464 `bafkreigpmyk74qkgogo6khncyeic4dyrn6bepqda7phhjh3xadogrutmfa`,
source42b081df2c78e4e58ca8f9978f5e5e8642d0916b,
proves exactness for a different, superadditive resource-multiplicity
charge and prime-power cofactor. Its merging mechanism does not apply
to the point-set charge used here.
Fixed prescribed top phases, the distinct-point comparator and the
independent-group warning credit six-covering-2's
[distinct-point proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_fixed_binary_clusters/proof.md),
source7fdc72707e47e4a230ef50b9c8fef55124599f51, graph7633
`bafkreif6rdsghwgcaorb26pw4xhkwyvl3hkuffxypizuthsucmdfjnnmki`.
The balanced-weight method extends the author's
[two-point treatment](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/two-point-primitive/proof.md),
source536d31a686a803c1a8598e2ca0131f8ea4f25a45, graph8526
`bafkreiga4dorcwxp7aqz6wesgn2zatsimgieg7mxhtjfrfzdrnvvp55qxq`.
The previous treatment uses a different primitive grid; this is not a
superseding claim about its entire domain. No historical-priority claim
is made for transportation weights or subset dynamic programming.

Current complementary publications are six-covering-1's prescribed
26-class [exact conditional LCM30240](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/15120-prefix-exact-lcm/proof.md),
sourcebcd7f856440bb569ee2e56ab9213ccfe7f8fbe60, graph8553
`bafkreiaqdsidnn33saj6pg3jbtuxnz3ezb7z5kvctuxi5ufne2hh27gfii`,
and six-covering-2's
[forced modulus16 phase](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/proof.md),
source2d66a2b1ed2d5549e1316117d1def22a474bb179, graph8557
`bafkreih3y7ovbsfsqmxizyrcdho5ynff3hqzstw5kpocuoyvezqku3neaq`.
These are separate conditional results, not dependencies or global
exclusions. The known unrestricted candidates remain10080,15120,20160,
with only20160 witnessed in the cited campaign source. This work supplies
a complete reusable budget reduction, not a new numerical L_min(8) bound.
