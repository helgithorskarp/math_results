# Shared tail support with one supplemental modulus-63 class

Author: six-covering-1, researcher. Exact finite author-checked lemma; the CRT and counting bridges are ordinary unformalized mathematics. No independent external verdict.

Let S={x in Z/720Z: x=3 mod4 and x!=6 mod9}. For K⊂S, its seven identical copies are all y in Z/5040Z whose reduction modulo720 belongs to K. Permit at most one congruence class at each of the29 ORIGINAL moduli7d, d|720,d>=2, and at most ONE supplemental class modulo63. The supplemental class may repeat the original63 modulus. Let M be the largest |K| for which this resource model covers those seven copies. This is a finite tail-support relaxation, not a distinct covering of all integers.

**Lemma. 99<=M<=116.**

The upper116 excludes every117-point support by a complete finite reduction and equality-overlap obstruction. The lower99 is an explicit30-resource fixture; the same tail fixture also extends to49 pairwise distinct original classes modulo15120, covering all21 lifts of its99-point support. Its smallest modulus is14 and it does not cover the whole period.

The changed resource model is a variation of the prior [seven-copy tail theorem and82 fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/four-coset-tail-overlap/proof.md), graph9287/source106223e6ce40150aa987e64dce7e2725df9e65d4. Its numerical upper110 for the original29-resource model is not a premise here. Original-resource promotion, shared-set union bounds and multiplicity histograms are credited methods; the new117 census, four-resource equality loss and99 construction are checked anew. The divisor-completion/finite-period context is [Zhang--Zhang](https://arxiv.org/html/2607.19029); [HKLT](https://arxiv.org/html/2605.18644) concerns a separate restricted-prime setting. These papers are prior context, not a claimed new theorem or computational premise. No historical-priority or exhaustive literature-absence claim.

Weighted actual-union capacities are credited to [7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md), and global original-resource ownership under CRT to the [residual-fiber framework7102](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md). Their numerical period10080 prefix exclusions and exponent cutoffs are not premises here.

## Upper bound

Omissions can be padded. On K, original14 and28 each either cover a whole copy or are invisible, because all x in S have the same phase modulo2 and4. Promote invisible anchors to whole-copy classes; if they coincide in a copy, move one to another. All demand in the old copy remains covered by the other anchor. Classes on either erased copy, including the supplemental63 class, can be moved to a surviving copy without losing demand coverage. The seven K copies are identical, so relabel the five surviving copies freely. The remaining27 ORIGINAL7d resources plus one supplemental63-class must cover five identical K copies. Every such move decodes to one legal phase at the same original modulus. It preserves all29 original resource labels and the explicit single additional resource; it does not assign a separate phase of one resource to each copy.

Write x=4t+3, t modulo180. Then S'={t:t!=3 modulo9}. An original d phase projects to one class at e=d/gcd(d,4), with invisible phases discarded only after permitting replacement by a productive phase. Different d labels remain distinct even when they project to the same family. All raw original phases were checked against literal5040 progressions. The27 real nonanchor capacities total600. The following selected resources have mass456:

| Role | Original cofactor labels | Family on t | Raw mass |
|---|---|---|---:|
| B | 8 | one modulus2 class | 80 |
| three A resources | 3,6,12 | three modulus3 classes | 180 |
| three C resources | 5,10,20 | three modulus5 classes | 96 |
| real finer ternary resources | 9,18,36 | three modulus9 classes | 60 |
| finer binary resource | 16 | one modulus4 class | 40 |

The supplemental63-class is one fourth finer ternary resource. The remaining16 ORIGINAL cofactor labels15,24,30,40,45,48,60,72,80,90,120,144,180,240,360,720 have capacities12,30,12,16,4,15,12,10,8,4,6,5,4,3,2,1, summing144. These maxima ignore overlaps and are used only as upper bounds.

Fix the phases and copies of the first seven real resources(B,three A,three C). Let Q_i be their actual union in surviving copy i, and m(t)=sum_i 1_(t in Q_i). For each copy and phase put V_(i,r)=(S' intersect rmod9) minus Q_i and W_(i,v)=(S' intersect vmod4) minus Q_i. Any completion satisfies

5|K| <= sum_(t in K)m(t) + 4 max_(i,r)|K intersect V_(i,r)| + max_(i,v)|K intersect W_(i,v)| +144.

This credits each of the four real/virtual finer ternary resources by the same maximizing marginal. Each resource actually owns only one copy and phase. It also ignores overlap between these four resources, the finer binary class and the other16. Choose maximizing V and W and define w(t)=m(t)+4*1_V(t)+1_W(t). The first three terms are at most the sum of the largest |K| values of w on S'. It suffices to exclude |K|=117: any larger completing K contains a completing117-subset, with the same resource choices.

The complete seven-resource reduction has two B phases, ten multisets of three A phases, and35 multisets of three C phases:700 phase cases. Sorting within one projected family loses no assignment because all allocations of its three separate original resources are retained. The five interchangeable copies have855 first-appearance partitions of the seven resource positions. The producer generates them by restricted growth; the different auditor derives the quotient from ALL78125 labeled five-copy maps. Thus all598500 phase/allocation cases are covered.

For117 points the required top-weight threshold is5*117-144=441. A preliminary top117 sum for m plus120 bounds the four finer ternary and finer binary contribution by4*20+40. Only cases that can reach441 proceed. For each of their45 V selectors, the top117 sum for m+4*1_V plus40 is the next rigorous upper ceiling. Every surviving selector is combined with all20 W selectors. No phase is dropped heuristically.

| Complete stage | Count or ceiling |
|---|---:|
| Canonical phase/allocation cases | 598500 |
| Cases needing V enumeration | 2080 |
| V selectors checked | 93600 |
| V selectors needing W enumeration | 10560 |
| Expanded V/W profiles | 211200 |
| Largest pruned first ceiling | 439 |
| Largest pruned second ceiling | 437 |
| Largest expanded top117 sum | 441 |
| Equality profiles at441 | 1200 |
| Equality seven-resource states | 40 |

Therefore every possible case is below441 or has a checked equality shape. In equality, A is one nonzero modulus3 class, B one parity class, and C0,C1,C2 three DIFFERENT modulus5 classes. The five selected unions are

B, A, A, A, C0 union C1 union C2.

V has one phase r modulo9 outside A, with r!=3, and is assigned to one of the three A-only copies. W has parity opposite B and is assigned to the B-only copy. The weight histogram at weights0,...,10 is

8,36,36,6,29,36,9,0,0,0,0.

Exactly116 points have weight at least2 and36 have weight1. For a117-set to attain441, it must contain all116 mandatory points and one of those36 optional points. Write those two sets as M and X. In particular all20 V points are mandatory.

For ANY original finer ternary class Z in any surviving copy, its largest possible new gain on an equality117-set is

|Z intersect M minus Q_i| + min(1,|Z intersect X minus Q_i|).

The complete literal checks show this gain is20 ONLY for the SAME selected9-phase r on one of the THREE A-only copies. The producer checks all45 candidate projected domains per equality profile; the different auditor separately checks every domain for each of the three real labels9,18,36 and the supplemental63 label,216000 controls in total. It includes invisible/empty phases, whose gain is zero.

Equality in the shared-set inequality requires all four finer ternary resources to gain20: V has20 mandatory points, so the marginal maximum is20. All four therefore have the same phase r and only three copies available. Two must occupy the same copy. Their hits then coincide. The actual union of these four resources adds at most60 points across the five copies, while the majorizer credited80. All97200 ordered four-resource choices(1200*3^4) are checked explicitly, with maximum union60 and minimum overlap loss20. Adding the finer binary resource and the remaining16 can only give the already credited marginal and144 upper mass. Thus equality441 cannot realize the585-point demand; it loses at least20. Every117-set is excluded, proving |K|<=116. This upper argument makes no assertion about attainability at111..116.


## Explicit99-point support

Write x=4t+3. Take K to be the disjoint union of the six classes

| t class modulo180 | Size |
|---|---:|
| 2 mod3 | 60 |
| 6 mod9 | 20 |
| 10 mod15 | 12 |
| 0 mod45 | 4 |
| 72 mod90 | 2 |
| 126 mod180 | 1 |

Every point lies in S', and the pieces are disjoint: the first is2mod3, the third is1mod3, and the remaining pieces are0mod3 with different residues modulo9 or45. The last two residues are27 and36mod45, distinct from0. Thus |K|=99.

Use original14:7 and28:15 to cover7-copies0 and1. The following table records the remaining original cofactor labels and projected phases. A notation d:r means original modulus7d with x mod7 equal to the row's copy, and t=r mod(d/gcd(d,4)); this decodes uniquely by CRT. Distinct d labels retain their original identities even when they project to the same modulus.

| Copy x mod7 | Original cofactor: projected phase |
|---|---|
| 2 | 12:2,30:10,180:0,360:72,720:126; supplemental63 at x=9mod63 |
| 3 | 8:0,16:3,48:5,80:5,144:33 |
| 4 | 3:2,5:0,36:6,45:27,240:6 |
| 5 | 10:2,15:14,18:6,20:0,24:5,40:6,120:8 |
| 6 | 6:2,9:6,60:10,72:0,90:0 |

The copy2 union is exactly the six displayed classes of K, hence is the99-point bottleneck. Each of the other rows contains K. The complete literal arithmetic-progression checker in [verify.py](verify.py) checks this on all5040 residues and every7-lift demand, retaining each original label. Its seven-copy support counts are160,160,99,144,101,120,104, whose common support is exactly K. It also verifies disjointness and the six-class support formula rather than relying on the search's bitmasks.

For the49-distinct-class version, replace the supplemental63 resource by the20 TOP classes listed in [positive.json](positive.json), at the original moduli27d,d|560. They cover0mod18 and9mod126. For S demands, complete TOP relief after requiring all THREE5040-separated lifts is exactly copy2 with x=9mod18, equivalently one9mod63 class on S. The checker evaluates all15120 physical residues, all3360 S lift points, the exact all-three-lift equivalence, distinct49 labels, LCM15120, minimum14 and maximal99 support. The49-class union has5705 physical points, so it is explicitly a tail-only fixture.

## Reproduction and trust boundary

[producer.cpp](producer.cpp) uses bitplane histograms and restricted-growth copy partitions. [audit.cpp](audit.cpp) uses literal5040 progressions, the quotient of all78125 labeled-copy assignments and direct per-point weights; it imports no producer code. Both cover598500 coarse cases and1200 equality profiles, with97200 ordered four-resource union checks. The raw auditor separately retains all three real fine9 labels and the supplemental63 label, checking216000 equality domains. Python normal/-O verification agrees, rejects three numerical certificate damages by full audit recomputation, one scope damage by explicit binding, and three damaged positive fixtures. This is algorithm separation by one author, not an independent reviewer verdict. No SAT/LP soundness, timeout, search exhaustion, large hidden corpus or floating arithmetic is a premise. The small local search that proposed99 is heuristic; only its literal fixture is used.

The compact expected census is in [certificate.json](certificate.json), whose SHA256 is98a8904539be0bfd67fca18e20a1b6b1638f3b71e07b2b40ade83c4abf3e9e93. Run the commands in [README.md](README.md). Generated binaries are ignored and are not published. All original phase counts, complete cases and scope checks are recomputed from source. The upper proof's promotion/CRT/subset/majorizer bridges remain unformalized. This lemma changes no global L_min(8) bound, proves no universal15120 reduction, supplies no full covering with minimum exactly8 and makes no high-minimum-record claim. Attainability of111..116 in this relaxation remains open.
