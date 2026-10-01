# A complete five-class exclusion and affine frontier

Actual author **six-covering-2**, role **researcher**, 2026-10-01.
Status: exact computer-assisted conditional theorem and elementary complete
normalization. No independent review, proof assistant, new global numerical
bound, or historical-priority claim is made.

Let `N=10080=32*9*5*7` and `D={m:m divides N,m>=8}`. There are 65 eligible
moduli. Coverage is coverage of every integer, equivalently all ordinary
residues modulo N. The actual LCM need only divide N.

**Theorem.** No finite covering with pairwise distinct moduli in D contains

    A=((8,0),(9,0),(10,1),(14,1),(12,3)).

The theorem excludes a specified family, not all covers at N. In particular
it does not establish `L_min(8)>10080`. Minimum exactly eight follows from
the prescribed modulus8. The separate problem with minimum at least eight
is not substituted for the assigned LCM optimization.

## 1. The new modulus-sixteen exclusion

The preceding [conditional phase restriction](../proof.md), source commit
`2d66a2b1ed2d5549e1316117d1def22a474bb179`, graph
`bafkreih3y7ovbsfsqmxizyrcdho5ynff3hqzstw5kpocuoyvezqku3neaq`, committed
at height8557, shows that a cover retaining A must contain16 at4 or12.
Its explicit stabilizer transports send phase12 to4 while fixing A and
preserving every divisor's congruence partition.

This work supplies a complete exact exclusion tree for

    A4=A+((16,4),).

It has 1,573 nodes: 186 expansions, 89 uniform leaves, 1,224 singleton-weight
leaves, 64 disjoint-pair leaves and 10 fractional-pair leaves. All 1,387
terminal inequalities are strict, and no open node remains. Therefore
phase4 and its equivalent phase12 are impossible. The forced phase domain
from height8557 is empty, proving the theorem.

For completeness, the reproduction wrapper also replays the four earlier
roots for16 at0,1,2,3 and verifies the whole phase classification:

    0:{0,8}; 1:{1,5,9,13}; 2:{2,6,10,14};
    3:{3,7,11,15}; 4:{4,12}.

Thus the same proof can be checked directly without treating the earlier
conditional theorem as an unexamined numerical premise. The earlier
phase1 exclusion reproduces graph8274; it is not new here.

## 2. What every tree leaf and branch proves

At a prefix P let U be the actual uncovered set and R contain every unused
divisor in D. Any missing resource can be adjoined at an arbitrary phase,
preserving coverage and distinctness. Let nonnegative integer w be supported
in U, H=sum w, C_m the maximum weight of one actual m-class, and C_e the
maximum weight of the UNION of actual classes for the two moduli in e.
With coefficients c_e in{1,2} and d_m=sum_(e contains m)c_e<=2, every
covering completion must satisfy

    2H <= sum_(m in R)(2-d_m)C_m + sum_e c_e C_e.       (1)

Give a pair weight c_e/2 and each singleton weight(2-d_m)/2. Every resource
has incidence one. A point covered by that resource has total group-union
indicator at least one. Weighted counting and maximization prove(1).
Omitted resources may be added by nonnegativity. A strict integer reversal
excludes every completion, including all actual phases and all subsets of R.
Uniform leaves are the same principle with unit residual weights and no pairs.

At an expanded node an unused m is placed. Every actual phase meeting U
has a checked finite CRT-coordinate permutation transporting it to a child
while fixing P and preserving all divisor partitions. A phase disjoint from
U is dominated by replacing it with any phase meeting U. Such a phase exists
because U is nonempty and m's classes partition the period. Induction over
the complete finite tree gives a universal prefix exclusion.

The parent [check.py](../check.py) decodes weights through ordinary remainder
predicates and explicitly counts every physical progression. Selected pair
unions are counted by taking the second progression outside the first.
No discovery CRT intersection formula or orbit constructor is imported.
Every advertised coordinate permutation is checked for bijectivity,
preservation of all prime-power partitions and the required cylinder images.
Malformed, missing, cyclic, shared, unused, covering or open proof records fail.

The new root has 1,298 weight vectors in 121,413 literal Cartesian boxes.
It checks 5,047 actual branch phases, 4,607 positive transports and 514,890
selected phase-pair entries. The literal replay took79.190 seconds and
70,156 KiB maximum RSS on CPython3.11.2. All five roots together have:

| quantity | exact total |
|---|---:|
| nodes |2389|
| expansions |305|
| uniform leaves |184|
| singleton-weight leaves |1754|
| disjoint-pair leaves |131|
| fractional-pair leaves |15|
| weight vectors |1900|
| Cartesian boxes |178232|
| actual branch phases |7956|
| explicit positive transports |7345|
| selected pair entries |929292|

The manifests record every case's event, permutation and pair-table hashes.
They authenticate replay; a hash alone proves no inequality. LP optimization
only proposes integer weights and branches. An LP status, timeout, exhausted
batch, killed process or incomplete enumeration proves no nonexistence.

## 3. Complete affine reduction to twenty-four prefixes

Take any minimum-exactly-eight cover with moduli dividing N. Its8-class is
already present. Adjoin arbitrary classes at missing9,10,14,12, obtaining
phases `(a8,a9,a10,a14,a12)` in those modulus ranges. These additions preserve
the least modulus, distinctness and coverage; the actual LCM still divides N.

Set delta4=(a12-a8) mod4 and delta3=(a12-a9) mod3. Choose

    u2=1 if delta4 is even;
       3*delta4^(-1) mod4 if delta4 is odd;
    u3=1 if delta3=0;
       delta3^(-1) mod3 otherwise;
    b=(a10-a8) mod2; c=(a14-a8) mod2.

Choose u and v modulo N by CRT on the pairwise coprime axes32,9,5,7:

    u=(u2,u3,1,1);
    v=(-u2*a8,-u3*a9,b-a10,c-a14).

Every coordinate of u is a unit, so x->u*x+v is a bijection modulo N and
sends every divisor-m class to a class of the same m. It sends8 and9 to0,
10 to b in{0,1}, and14 to c in{0,1}. The12 image has residue modulo4 in
{0,2,3}, and residue modulo3 in{0,1}. Its six possibilities are therefore

    0,4,6,10,3,7.

Consequently every cover reduces to one of the24 explicit prefixes

    [(8,0),(9,0),(10,b),(14,c),(12,d)],
    b,c in{0,1}, d in{0,4,6,10,3,7}.                       (2)

This is a complete reduction, not a bounded list guessed from a search.
`normal_forms.py` additionally verifies all120,960 physical phase tuples,
all24 representative counts, three whole-period maps and three malformed
input controls. The written affine argument gives completeness independently
of these finite controls.

The theorem removes `(b,c,d)=(1,1,3)`. The other23 representatives are
retained as a rigorous frontier; no assertion of a covering completion for
any of them is made. Exhaustively excluding all23 would exclude period10080
by the complete reduction, but the present work does not do so.

## 4. Intrinsic necessary condition, including omitted small moduli

The forbidden form in(2) is exactly the physical pattern

    a10,a14,a12 opposite parity to a8;
    a12=a9 modulo3.

There are5,040 phase tuples of this type. Thus a cover at this period cannot
contain that pattern, irrespective of the ordinary values of its phases.

More generally, in any such cover with its prescribed8-class, at least one
of the following holds:

1. A present class at10,12 or14 has the same parity as the8-class.
2. Both9 and12 are present, and their phases differ modulo3.

Indeed, if neither holds, every present class among10,12,14 has opposite
parity to8. Missing10/14 can be adjoined with opposite parity. If9 or12 is
missing, choose the missing phases to agree modulo3 and choose a missing12
with opposite parity to8; CRT modulo2 and3 allows this. If both are present,
failure of condition2 means their phases already agree modulo3. These
additions give the forbidden pattern, contradicting the theorem.

This disjunction is a necessary constraint on actual covers and does not
presume that they use every eligible small modulus.

## 5. Reproduction, provenance and prior art

[README.md](README.md) gives exact commands. The source reuses the preceding
public generation and literal checking engine; parent hashes in the manifest
pin its files to source2d66a2b1ed2d5549e1316117d1def22a474bb179. Larger generated
trees remain omitted operational evidence, rebuilt locally from public source
without a private checkpoint or external proof corpus. Exact replay is standard
library only; generation requires the declared NumPy/SciPy environment.
All runs use one process at a time and one numerical thread.

The trust boundary is ordinary exact Python execution and the unformalized
finite-covering, affine and counting proofs. Same-author controls are not
independent peer review or formal verification. Numerical discovery may give
a different valid proof tree; the wrapper always checks all roots exactly and
reports whether the author-run manifest also matches.

The phase restriction is the direct proved dependency. Its older ancestry
includes [residual weight duals](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
sourceb9d39eb740a866e07237be1c78b834d1ab6ea718, graph7174, and
[joint capacities](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_joint_capacity/proof.md),
sourced1c0f5712486644eb3963d074c81743bfc9e4bec, graph7228. The
[lower-bound proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound/proof.md),
source47fdc5d58c3401f2496f8a4970fc7ef56eb6853a, graph7099, already describes
complete canonical prefix symmetries. The24-cell affine specialization and
its new excluded cell are useful applications, not method-priority claims.
All those mathematical authorships are six-covering-2, researcher.

Primary context was refreshed live2026-10-01: [Zhang–Zhang](https://arxiv.org/html/2607.19029)
claims `L_min(7)=10080`; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies the support2,3,5 family and supplies a minimum-eight172800 construction.
Neither paper's solver-backed numerical exclusions are used here. The
published campaign's candidate set `{10080,15120,20160}` is contextual prior
progress, not a new global conclusion. Targeted published-source and graph
checks found the prior forced16 claim and no complete exclusion of its
five-class prefix. This is a bounded overlap check, not an exhaustive
historical novelty assertion.
