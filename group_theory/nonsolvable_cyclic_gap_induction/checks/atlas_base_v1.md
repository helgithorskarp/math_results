# Atlas internal check of the complete B6 base

Checker: Atlas, studio-researcher-1, researcher, 2026-10-05.
Author checked: Nova, studio-researcher-3, researcher.

**Decision: ACCEPT B6**, with the explicitly stated classical classification,
order, small-isomorphism and automorphism inputs. This is an internal check of
the radical-free interface, not external peer review, a formal proof, or a
novelty claim. It does not itself check arbitrary solvable-radical extensions.

## Exact versions

The target is: if a finite nonsolvable group X has Rad(X)=1 and
c(X)/2^omega(|X|)<=6, then X is A5. Cyclic counts include the trivial subgroup.
The complete original handoff was read, including its finite-family audit,
measure argument, simple margins and socle transfer. Its immutable copy has
PROOF.md SHA256

    32cb719d41dda6b5764755dac61698a2fb20ab2859cdced294feddd5edae4a40

The original last paragraph incorrectly attributed a proof of A5 simplicity
to Iris's central-boundary artifact. Rowan identified that attribution; Iris
confirmed that her artifact proves perfectness and trivial center instead.
The corrected PROOF.md read and accepted here has SHA256

    15297f64ee862035c7438dbe244c5d5403107c06f3cb69c8e24df9c2c6b36ab0

A direct diff against the preserved original shows that attribution
paragraph changed, together with the version and checking-status headers.
The fixed handoff is base-v2; its MANIFEST.json has SHA256
7f38e83f11ffd545108efbff83648e95b1f44248a7ed840f0fafe5b9a0c47e03.
The replacement states simplicity as classical background
and gives the elementary class-size argument. Its proof is checked below.
The original mathematical argument was valid with simplicity as a classical
input; its erroneous attribution should not be published as validation.

The exact author-side computational inputs checked are:

| File in nonsolvable_cyclic_count_base | SHA256 |
|---|---|
| evidence.json | 2bd8c15067ae70e5aae74740eb7028a724386c3c0306081abff528c9f2241726 |
| catalogue.json | 623df2a1334f0ba1f6f57a0358447f6230a6e11241b940dc75a5d53d32b59f6f |

The independent standard-library implementation in this directory has SHA256

    cff37787b03c6c4e8774980b4992f74572ae26c1ae5757d6f290167576b257c0

Its deterministic BASE_BOUNDS.json has SHA256

    c3af8d1ef75e5b0ca766b2369e1b01033525b3adebe0a926860e92a6a3f05045

The implementation derives its catalogue interface, bounds, permutation
counts and structural histograms before reading either author-side comparison
file. It does not use Nova's GAP code, group models or conjugacy-class output
to generate its mathematical results.

## Measure and finite order reduction

The subgroup measure inequality is correct even when AB and C(A)C(B) are
only product sets. Their sizes are the usual intersection quotients, AB is
contained in the join, and C(A)C(B) is contained in the centralizer of the
intersection. Thus the product of the two maximal measures forces both the
intersection and join to attain the maximal measure. The finite intersection
D of all subgroups attaining it also attains it and is characteristic.
The measure of C(D) is at
least that of D; maximality puts C(D) in the same family, hence D<=C(D).
Consequently D is an abelian characteristic subgroup. Rad(X)=1 forces D=1,
and the maximal measure is |X|. This supplies the classical order estimate
self-containedly; it is not dependent on a fetched or unread Lucchini proof.

For cyclic H of order e, its measure is at least e^2, so e<=sqrt(|X|).
The generator-weight identity then gives c(X)>=sqrt(|X|). The prime-product
bound 16^omega(n)/n<=8388608/15015 is valid: each occurring prime p<16
contributes at most 16/p, each larger prime contributes at most one, and
omitted smaller primes may be inserted into this upper bound. Raising eta to
the fourth power gives eta^4>=|X|/gamma. Exact rational arithmetic yields
gamma*6^4=3623878656/5005 and the conservative ceiling B=724052. Taking a
ceiling rather than the tighter integer floor loses nothing in the argument.

## Finite-family coverage and outer primes

The proof correctly identifies its trust boundary: CFSG's family list,
standard order formulae, small derived-group isomorphisms and outer orders
are classical imports. The software iterator corroborates coverage but is
not offered as its own proof of completeness. I compared the retained
metadata with the primary CTblLib simple-by-order table and official GAP
small-simple declarations. The comparison preserves the distinct order-20160
groups A8 and PSL(3,4), the exceptional A6 outer order four, and all stated
small-group identifications. No extra isomorphism type is counted for the
low-rank orthogonal presentations.

I audited every cutoff in the proof. The independent output evaluates all
23 displayed initial bounds exactly, with integer floors used only to obtain
conservative lower bounds. The closest is the rank-three symplectic bound
725760, still above B. For clarity, the rank monotonicity implicit in the
author's paragraph can be expanded as follows. With

    N_n(q)=q^(n(n-1)/2) product_(i=2..n)(q^i-1),

the PSL lower bound is N_n(q)/n. At fixed q>=2 its ratio for consecutive
ranks is q^n(q^(n+1)-1)n/(n+1)>1. The PSU analogue replaces q^i-1 by
q^i-(-1)^i, and its consecutive ratio is
q^n(q^(n+1)-(-1)^(n+1))n/(n+1)>1. Both products also increase with q.
Thus the rank-five q=2 bounds exclude all higher ranks.

For symplectic and odd orthogonal rank l>=3 the conservative product is
q^(l^2) product_(i=1..l)(q^(2i)-1)/2. The rank ratio is
q^(2l+1)(q^(2l+2)-1)>1. For even orthogonal rank l>=4, a common lower bound
for both signs is q^(l(l-1))(q^l-1) product_(i=1..l-1)(q^(2i)-1)/4.
Its rank ratio is

    q^(2l) (q^(l+1)-1)/(q^l-1) (q^(2l)-1)>1.

These arguments cover unbounded ranks, rather than extrapolating a finite
numerical sample. The PSL3/PSU3 q>=7 bounds use center at most three; q=6 is
not a prime power. Rank-four q>=3 uses center at most four. The symplectic
rank-two q=4 order and the conservative q>=5 bound both exceed B; q=2's
derived subgroup is already A6. All low orthogonal isomorphisms return to
retained or excluded classical rows.

The exceptional-family cutoffs also hold: G2 at q=3 and 3D4 at q=2 exceed
B; F4, E6, twisted E6, E7 and E8 already do so using their q-power factors
and the stated center bounds. Suzuki's next allowed q after eight is 32;
small Ree's next after three is 27. The small derived groups return to
PSU3(3) and PSL2(8). The Tits group already has order 17971200, and the next
large Ree parameter is excluded by q^12 alone. The other 21 sporadic orders
are at least the M23 order. Alternating degrees >=10 and PSL2 q>=114 are
excluded directly by increasing order formulae.

Independent prime-power generation and row comparison match all 53 retained
names up to the stated aliases, their orders, outer orders, full Aut prime
supports and square-root exclusion flags. Multiplying order by outer order
is the correct Aut order for these centerless simple groups. The only new
primes from Out in this range are three for Sz(8) and five for PSL2(32);
both remain in the denominators. These data are checked against primary
metadata, not derived from the finite cyclic-count computation.

## Independent cyclic counts and strict margins

The square-root bound excludes exactly 37 rows using the strict test
|S|>36*4^omega(Aut(S)); all its arithmetic is exact. Eleven further PSL2
rows are excluded already by the two conjugacy classes of full tori plus
identity, giving q^2+1. Sz(8) is excluded by its three full-torus classes,
giving 8^4+1. The structural partition counts and full element-order
histograms were independently reconstructed for every residual PSL2 group
and Sz(8). The classical torus/partition structures are identified in
[BASE_CHECK.md](../BASE_CHECK.md), with direct primary sources.

A5, A6, A7 and S5 were enumerated as even/all natural permutations; each
cyclic subgroup is a literal set of powers. M11 was separately closed from
its primary ATLAS standard natural generators, checked to have order 7920,
and counted the same way. The identification of those generators imports
ATLAS data. The resulting literal counts are respectively 32, 167, 947, 67
and 2576. They do not rely on GAP's conjugacy-class calculation.

All sixteen residual simple-group counts and all sixteen complete aggregated
element-order histograms match Nova's evidence exactly. I did not independently
identify every individual split conjugacy class or its label. Those labels
are unnecessary to this count-based exclusion, and no such stronger check
is claimed. The comparator requires exact residual-row coverage and rejects
missing, duplicate, malformed or disagreeing rows. As controls, a changed
cyclic count and a missing row were each rejected in separate temporary
copies; the valid source was preserved.

The finite range therefore supplies c(S)>=4*2^omega(Aut(S)) for every
encountered simple S, and a strict value greater than 6*2^omega(Aut(S))
for every S other than A5. No unbounded stronger simple-group theorem or
threshold-four strictness extrapolation is needed.

## Socle transfer and the A5 overgroups

The product inequality follows prime by prime from
phi(lcm(u,v))<=phi(u)phi(v), so it applies without coprimality. For a
radical-free group, each minimal normal subgroup is a product of nonabelian
simple groups. The socle centralizer is normal; if nontrivial, it would
contain a minimal normal subgroup also contained in the socle center.
That center is trivial, so conjugation embeds X into Aut(socle(X)).

For the distinct simple types S_i of multiplicities m_i, the wreath-product
embedding supplies r(X)<=sum_i(a_i+omega(m_i!)), where
a_i=omega(Aut(S_i)). Since omega(m_i!)<=m_i-1 and a_i>=1,
sum_i m_i a_i>=r(X). Every factor has order at most |X|<=B, so all use
the already audited finite-range margin. Counts increase in overgroups and
multiply as lower bounds in products, yielding eta(X)>=4^(sum_i m_i).
At eta<=6 there can be only one simple factor. Every socle except A5 is
excluded even with the larger Aut denominator.

For A5, the action on the five Sylow-two Klein-four groups is faithful on
inner automorphisms. The kernel in Aut(A5) and the inner group are normal
with trivial intersection and therefore commute. An automorphism commuting
with every inner automorphism fixes every element of a centerless group.
Thus the kernel is trivial and Aut(A5) embeds in S5; conjugation by S5 gives
the reverse inclusion. This use of simplicity is valid. The corrected
paragraph can prove simplicity directly: A5 has class sizes 1,15,20,12,12,
from the double-transposition, three-cycle and five-cycle centralizers.
The possible sizes of a class union containing identity are

    1,13,16,21,25,28,33,36,40,45,48,60.

Only 1 and 60 divide 60. Lagrange's theorem excludes every proper nontrivial
normal subgroup, and the nonabelian simple group has trivial center.
The only almost-simple overgroups are A5 and S5; the independent S5 count
67 gives eta=67/8>6. This completes the claimed B6 scope.

## Reproduction and remaining scope

Use the exact command in [BASE_CHECK.md](../BASE_CHECK.md) with both comparison
arguments. CPython 3.11.2, standard library only, produced BASE_BOUNDS.json in
about 0.2 seconds with one local process. No large search or solver was run.
The classical imports remain ordinary mathematical trust inputs; the check
does not independently prove CFSG or the imported automorphism theorems.
It replaces the numerical count dependence by separate literal/structural
checks at every residual case required by B6. Extension interfaces and the
global induction have separate internal checks and must be assembled with
their exact versions before the full shared theorem is called complete.
