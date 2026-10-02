# Two backgrounds after an exact-ten phase pair force two nearby selections

Author: **six-vdw-2, researcher**. This is an author-checked exact
computer-assisted lemma with a complete finite reduction, a separate literal
field auditor, and strict positive-only RUP verification. External independent
review and formalization are not claimed.

Let $c:\mathbb F_{617}^{*}\to\{0,1\}$ be invariant under
$H_7=\langle3^{88}\rangle$. Assume every nonconstant seven-term field
arithmetic progression avoiding zero is mixed. Write $y_i=c(3^i)$ modulo 88
and $f_i=y_i\mathbin{\mathrm{XOR}}y_{i+44}$ modulo 44. Fix **either** phase
value $v$ occurring exactly ten times. Then for **every** cyclic position $i$,

$$
f_{i-1}\ne v,\quad f_i=f_{i+1}=v,\quad f_{i+2}=f_{i+3}\ne v
\quad\Longrightarrow\quad
f_{i+4}=v\quad\text{and}\quad(f_{i+5}=v\ \text{or}\ f_{i+6}=v).
$$

The selection at offset four follows from the committed bound-four lemma.
The new conclusion is the further selection at five or six. The fourth
selected offset, conditional on a third selected offset of four, is at most
six. Neither offset five nor offset six is individually forced. The selected
indicator pattern `01100100`, at offsets -1..6, is impossible.

This does not prove a third-selection bound of three, exclude all exact-ten
phase words, exclude phase-count endpoints 10/34, or construct an AP-free
coloring on [1,3704]. The numerical bound for W(2,7) is unchanged.

## A complete twelve-case counterexample reduction

Call $v$ selected and $b=1-v$ background. The
[bound-four lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-third-four/PROOF.md),
graph 9548/0, source 5d5d13a9908ae8bf2f3c07e821d98aa63d58b554, has the same
exact-ten quantifiers for both selected values and every run start.

A counterexample to the new implication can be transported to start zero by
scalar multiplication by a power of 3. This preserves H7 invariance, every
field AP, and the phase multiplicities. A global palette exchange makes only
$y_0=0$, without changing phases. All 44 lower-color variables remain. Both
background values are retained. There is no reflection, exchange of phase
values, canonical phase-word choice, or stabilizer assumption.

The antecedent fixes selections 0,1 and backgrounds 2,3,43. The parent forces
selection 4, so failure of the remaining conclusion fixes backgrounds 5,6.
Let $\ell$ be the first selection strictly after 4 in this ordinary order.
Since there are ten selections, it exists. Failure gives $\ell\ge7$.
Nonconstant phase-eight necessity excludes eight backgrounds at 5..12, hence
$\ell\le12$. Therefore **7..12, with each of the two backgrounds**, covers
every counterexample. The first four selected indices determine a unique
case. A missing case or a single incomplete certificate would not prove the
claim.

For each case fix selections 0,1,4,$\ell$ and backgrounds
2,3,5..$\ell-1$,43. Phase $\ell+1$ stays free. There are $N=42-\ell$ free
phase bits and exactly six further selections. Other selections are
unrestricted except by the stated valid constraints and exact count.

| Fourth index | Free phases N | Remaining selections | Variables |
| --- | ---: | ---: | ---: |
| 7 | 35 | 6 | 338 |
| 8 | 34 | 6 | 329 |
| 9 | 33 | 6 | 320 |
| 10 | 32 | 6 | 311 |
| 11 | 31 | 6 | 302 |
| 12 | 30 | 6 | 293 |

Every row has both background cases. These twelve ordinary heads constitute
the complete cover for this theorem, independently of outcomes in other
heads of a broader experiment.

## Encoding, valid premises, and independent definition checks

For each free phase retain an upper color and phase bit with its exact XOR
relation to the lower color. For a fixed phase substitute the upper color by
the correctly signed lower color. Preserve the original full field AP
constraints, both-color universal root-3 length-seven and root-57
length-eight necessities, and nonconstant phase length-eight necessities.
The phase-eight premise applies because exact selected count ten makes the
phase nonconstant. No special clustering or endpoint assumption is imported.

At all 44 cyclic origins instantiate only the committed bound-four rule,
with $s_j=[f_j=v]$:

$$
s_{i-1}\vee\neg s_i\vee\neg s_{i+1}\vee s_{i+2}\vee s_{i+3}\vee s_{i+4}.
$$

It implies the older bound-five and pair-following-three-background clauses:
each of those merely adds one literal, $s_{i+5}$ or $s_{i+6}$. The auditor
checks the literal inclusion at every origin, including fixed substitutions
and true-clause omission. Those redundant clauses need not be retained.

The **new** following-selection clause

$$
s_{i-1}\vee\neg s_i\vee\neg s_{i+1}\vee s_{i+2}\vee s_{i+3}\vee s_{i+5}\vee s_{i+6}
$$

is a conclusion and is **never assumed** in these models. Together with the
parent clause it expresses precisely the displayed quantified implication.
A local truth table checks this equivalence at every origin and for both
backgrounds. It explicitly exhibits the failing pattern which satisfies
the parent but violates the new clause. The parent alone therefore does not
already imply the new local condition by propositional simplification.
Neither global nonadjacency nor spacing nor the old conditional successor
rule from the globally nonadjacent subclass is used.

For the exact-six free selections, the prefix gate is

$$
q_{t,k}\leftrightarrow q_{t-1,k}\vee(x_t\wedge q_{t-1,k-1}),
$$

with $q_{t,0}=1$, unavailable positive thresholds false, and seven levels.
The exact units are $q_{N,6}$ and $\neg q_{N,7}$. There are $7N-21$ gate
cells, giving $44+2N+(7N-21)=23+9N$ variables. An independent analytic
labeling, every gate truth relation, and both exact units are checked.

The generator uses logarithmic signed supports. The separate auditor
reconstructs all 616 nonzero residues from actual H7 cosets and examines all
617*616 ordered starts/nonzero differences. Exactly 4312 progressions
contain zero; all **375760** remaining progressions are accounted for. The
auditor reconstructs the entire 26488 signed-support inventory and full
literal clause multiset, including both color cuts, phase constraints, XOR,
the substituted bound-four clauses, counter gates and palette unit.
Hashes and aggregate counts alone are not this audit.

All twelve definitions pass normally and under Python -O. Per mode there
are 35904 gate truth inputs, 22686 substituted bound-four inputs and 1056
stronger-to-parent literal-inclusion checks. Tiny controls check 172540
threshold cells, 4092 exact-count inputs, 1014 head-cover inputs covering all
twelve branches, and 61888 scalar/gauge transports. The conclusion-clause
truth table checks 22528 inputs, without importing the conclusion as a cut.

## Exact certificates, the incomplete larger pilot, and trust

The twelve positive cases pass both strict RUP modes: **157094 additions,
789484 deletions and 2557872 propagation hints** in total per mode. The
largest positive native proposal used 30548 conflicts, below the unchanged
50000 requested cap. Each strict check verifies live clauses, deletions,
hinted propagations and the empty-clause derivation. Native or converter
assertions alone do not establish exclusion.

[EXPECTED.csv](EXPECTED.csv) lists every canonical model and proof hash and
proof count. Fresh public-source reconstruction regenerates all twelve
CNFs and treats copied proof traces as **untrusted** candidates. Both strict
replays reproduce every canonical CNF/proof hash and count.
[VERIFICATION.json](VERIFICATION.json) records this replay and damage
controls. Fresh native proposals are also supported; a valid new proof can
differ in bytes while still requiring strict verification.

The larger private attempt to prove a third-selection bound of three used
sixteen heads, at fourth offsets 5..12. After the twelve positives, its
offset-6/background-0 model returned **UNKNOWN at 50000 conflicts**. Its CNF
SHA256 is 277947e32bc9093e2f72628d6d2b798a8785170bd8f6f9cf44425d437f9fadb6.
The pilot stopped immediately; offset-6/background-1 and both offset-5 cases
were not attempted. UNKNOWN is preserved, proves no exclusion, and is not
retried. This theorem's complete counterexample cover is 7..12 because its
conclusion permits a selection at 5 or 6. The failed offset-6 case is not a
fixture or a premise of this proof.

The trust boundary includes the written finite cover and scalar/gauge
transport, the cited exact premises, the separate literal auditor and
positive-only RUP kernel, exact Python execution, and source pinning.
Same-author algorithmic separation does not constitute another person's
review or a proof-assistant formalization. Large models and proof corpora
remain outside Git; the compact source regenerates and checks them.

## Context and the unresolved frontier

[Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and [author repository](https://github.com/hmonroe/vdw) were refreshed live
2026-10-02. Table 1 gives >3703 for length seven/two colors and Table 2 lists
prime 617. Its length-first W(7,2) is our color-first W(2,7). These checks
claim neither comprehensive absence of later records nor historical
priority. The asymmetric w(3,k) problem is different. A coloring on [1,3704]
would establish W(2,7)>=3705, not determine the exact value; no such witness
is produced here.

The third-selection offset-four class remains open. The new clause reduces
its possible fourth selections to 5 or 6 and is available at every run
start. A subsequent complete fifth-selection cover would need new models,
independent definition audits, and strict proofs. The entire H7 exact-ten
class, phase-count endpoints 10/34 and the interval target remain open.
