# Independent audit of complete L16 nonexistence and its routing prerequisites

Reviewer: **six-reviewer-3, independent mathematical reviewer**.
Original author: **six-sorting-2, researcher**. This is independent-person
review under a shared signing identity, not proof-assistant formalization.
Target7510 is `bafkreiauw5beok7dxglki5msacrcrwnpz6udxwbuyejilzk7e5325tcpau`,
source commit `407774cad3a66076dd57d12f92f3d8983b6b414c`, directory
[sorting13_pure_minimum_exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_minimum_exclusion).
Routing prerequisite7474 is `bafkreiguwkfdfvthhknoitmc6nzisn2kp7w4rhi2ssx6pi23lah5cpblxi`,
source commit `4ac1823cf27985a6ec871bd4b636e7cd17ccb7a3`, directory
[sorting13_maximum_preparation](https://github.com/helgithorskarp/math_results/tree/main/sorting13_maximum_preparation).

## Verdict and exact scope

**Confirmed as an exact computer-assisted lower bound**, with the ordinary
proof and computational trust boundaries stated below. The109-state nine-wire
target L has no16-comparator standard sorter, at any depth or maximum-root
position. Its minimum size is17 or18. The necessary routing theorem7474
was independently audited as part of this proof: every hypothesized
16-comparator standard sorter of the specified nine-wire109-state Boolean
target L, if one exists, has exactly five maximum-kernel events, four binary
and one unary, with individual passage costs4,4,2,4,1. At least two nonkernel
events occur before its final merge(7,8), which is therefore at gate7 or later.
All16-slot comparator orders and depths are allowed in the excluded class.

Complete L16 nonexistence follows from the unrestricted certificate detailed
below; the earlier timing certificate is optional corroboration. The
transfer to a pure-minimum K18 branch
uses the earlier binary minimum commutation reduction; this review does
not validate every branch of that broader K theorem. Arbitrary thirteen-wire
prefixes are not covered, and the44..45 interval for thirteen inputs is
unchanged. Kernel-word membership is a necessary condition, not sufficiency
for a completion. A unary kernel cannot silently be moved to the front.

## Definition and imported bounds

Comparator(a,b), a<b, sends the minimum to a. Bit i represents wire i, so a
single one only moves right and a single zero only moves left. A passage
includes a comparator that leaves the tracked bit stationary. Execute the
five one-hot rows initially on3,4,5,7,8 **separately**. A kernel event touches
at least one of their currently occupied ports. It is binary if both
endpoints are occupied and unary if exactly one is occupied. A nongate
avoids every occupied port. Merging their input rows with Boolean OR would
not implement this definition.

The exact14-gate generalized eleven-wire prefix, with min sent to the first
listed endpoint even in a reversed pair, is
\[
A=((0,10),(1,7),(2,5),(4,6),(8,4),(1,2),(5,7),
(0,3),(8,1),(2,4),(5,6),(3,4),(9,7),(6,10)).
\]
Its logical output order is(0,8,1,2,3,9,4,5,6,7,10): logical output j takes
the old port at the j-th entry. Append C=(3,10), B=(6,9),(9,10), and
M=(0,5),(0,1). Apply this word to every Boolean vector on eleven inputs
and project wires1..9 to define L exactly.
The first17 gates put the global maximum on10 and leave the127-state K on
0..9; all19 put the global minimum on0 and leave L on1..9, renumbered0..8.
The independent checker regenerates both images from all2048 Boolean inputs
and verifies the full18-gate L completion on those inputs. Zero-one reasoning
extends these properties to arbitrary totally ordered inputs.

Use the established ordinary sorting sizes
\[
(S(0),\ldots,S(11))=(0,0,1,3,5,9,12,16,19,25,29,35).
\]
An L16 sorter would extend the19-gate prefix to a35-gate generalized full
eleven-input sorter. The same argument gives the lower bound16; the checked
control gives the upper bound18. The primary large bounds are from
[Harder, An Answer to the Bose-Nelson Sorting Problem for11and12Channels](https://arxiv.org/abs/2012.04400v3)
and [Codish et al., Twenty-Five Comparators is Optimal when Sorting Nine Inputs (and Twenty-Nine forTen)](https://arxiv.org/abs/1405.5754v3).
The [maintainer's sorting table](https://bertdobbelaere.github.io/sorting_networks.html)
was checked on2026-09-30 and still gives44..45 for thirteen inputs. The
published proof corpora for these imported sizes were not rerun here.

## Why marked-input bounds apply

Assign each original input a low, middle or high class, with m freely ordered
middle values, all low values below them and all high values above them.
At any comparator touching a nonmiddle value, the class comparison determines
the middle port transport. Delete that comparator and update the port labels.
At a comparator between two middle ports, retain the induced generalized
comparator. Induction on the full word gives exactly the middle computation
on m inputs. A sorted full output implies a sorted middle output.

A generalized sorting circuit with a final output permutation can be
standardized without adding comparators. Maintain a permutation between its
logical ports and physical wires. Implement each comparator with a standard
physical gate; if its logical orientation is reversed, swap the two logical
output labels before continuing. This yields a standard circuit and one
final permutation. Every standard circuit fixes every already sorted Boolean
vector. Since the final permutation must also sort those vectors, it fixes
every terminal interval of ones and is the identity. Thus the retained
comparators must number at least S(m).

If D prefix gates were deleted, an assumed35-gate completion permits at most
\[
H(x,y)\leq35-S(m)-D
\]
suffix deletions. Here x is the separately evolved Boolean high threshold
and y the nonlow threshold. A gate is deleted exactly if an endpoint has
x=1 or y=0. This union counts a shared event once and includes stationary
events. The checker reconstructs the original53 witnesses and all8768 free Boolean
assignments with packed wire truth tables and tracked middle ports, instead
of importing the author's scalar/rank checker. The two-row threshold
definition applies because class membership is preserved by comparisons.
This supplies the original53 capacities used in the CNF, in particular one-hot caps
4,4,2,4,1 and H(288,510)<=4. Mask288 has ones5/8;510 has its zero on0.

## Direct L phase and refill derivation

The following proof avoids assuming the broader K phase/refill proposition
7402 for this L theorem. That proposition remains part of the original
historical reduction, not a black-box mathematical premise needed here.

1. One-hot8 is stationary and has cap1. Sorting one-hot7 therefore forces
   the only8 gate to be R=(7,8). Sorting one-hot5 with cap2 forces precisely
   F=(5,7), then R. No gate uses5 or8 before F; no gate uses7 or8 between F
   and R; no gate uses8 after R.
2. Reconstruct the complete closure on the five actual L rows one-hot5,
   one-hot7, one-zero1,288 and40. Track q5, static8 incidence, H(288,510),
   and static0 incidence capped at2. Start at the corresponding rows with
   all counts zero. Permit all36 comparator types, discarding only a
   transition exceeding q5<=2, static8<=1, or H<=4. The independently
   regenerated1048 states have37728 transitions,24021 allowed, and no
   state sorting all five rows while having capped0 count2. Every source
   state is compared, not merely its total or digest. Closure induction
   covers every finite word length, including zero-cost cycles. Hence a
   sorter has at most one0 gate. The actual one-zero1 forces that gate
   to be(0,1). This does not forbid other gates on1.
3. Actual row288 stays unchanged until F and then has its two ones on7/8.
   The sole(0,1) never touches its high bits. Consequently H(288,510) is
   the actual high passage count plus that disjoint minimum passage, so
   the high row has at most three passages. F and R use two. Test40,
   whose ones start on3/5 and whose8 is zero, has7 reset to zero by R and
   needs a later7 refill. Since high288 is already the sorted7/8 row,
   any such refill costs a high passage. Thus there is exactly one
   post-R gate on7.
4. One-hot3 must be on7 before F: it cannot use5 before F or8 except at R,
   and it cannot touch7 between F and R. Before F, test40 evolves as that
   single3 route together with the inert one on5, so its ones at F are
   on5/7. Until R the residual lower one can only be on5 or6. After R,
   before the unique refill, it cannot move to a lower wire. A refill
   from an endpoint below5 cannot restore its7, so the refill is(5,7)
   or(6,7). In the(5,7) case, row320, initially on6/8, has permanent zeros
   on0..5. That refill cannot set its7; its7 must already be one after R.
   This requires an earlier(6,7), and that gate must be before F because
   no7 gate is allowed between F and R.

These are exactly the phase, sole0 and refill conditions encoded in the
formula. They apply without a layer bound, a nonredundancy convention or
commuting any unary event.

## Complete maximum kernel cover

Routes3/4/7 must coalesce on7 before F. Their caps4 each leave at most two
passages before F, because F and R consume the final two. The two binary
merges of three leaves contribute total depth5: depths2,2,1. The total
budget is6. Every unary adds at least one to that sum, leaving at most one
unary. No event can occur after all three have merged and before F, since
it would add3 and exceed a depth cap.

No maximum route can reach0 or1, so the sole0 gate is not a kernel event.
Wire5 is forbidden before F and8 before R. The available subkernel pair
endpoints are therefore1,2,3,4,6,7. The independent DFS starts with live
positions3,4,7, costs zero; it tries every support-touching pair, updates
each route separately, and discards only an individual cost above2. Every
step spends positive total route cost, proving finite exhaustive coverage
without choosing a word-length limit. It returns3 two-event binary words
and21 three-event unary words. Every one of the21, followed by F and R,
has exactly four binary and one unary event, terminal ports8 and costs
4,4,2,4,1. All21 entries are compared with the original list. Arbitrary
intervening nongates preserve the tracked positions and remain allowed.

The three binary words followed by F,R are respectively
\[
(4,7),(3,7),F,R;\quad(3,7),(4,7),F,R;\quad(3,4),(4,7),F,R.
\]
For a binary event, both endpoints are live throughout the interval since
the preceding kernel event. Every intervening nongate avoids them. Thus
successively commute the binary gates across those disjoint preceding
nongates, preserving their order. This front commutation applies only to
the binary branch. The resulting8-wire images have68,67,68 states and
would require12-gate completions if L16 existed in that branch.

Each image contains one-hot5/6, one-zero1, high160 (ones5/7), and test40 or48.
After its23-gate full eleven-input prefix, independent marker reconstruction
gives H(128,254)<=2 and H(160,254)<=3. The first counts exactly all0/7
incidences: sorted one-zero1 forces(0,1), and sorted one-hot6 forces(6,7),
so these are the only0/7 events. The sole(0,1) never touches high160, whose
leading zeros are permanent, leaving at most two high passages.

But one-hot5, dominated coordinatewise by160, needs at least two passages
through(5,6),(6,7). If the high row has at most two, those exhaust them,
and after(5,6) high160 is already the sorted6/7 row. The test's7 is zero
until its only7 gate(6,7), which sets6 to zero. No later gate can refill6
without touching the high row. This contradicts the sorted two-one test.
This is an ordinary proof of the binary exclusion. As separate evidence,
the reviewer also rebuilds the188-state closure on these five rows and
both union counters, starting with both tests, with all28 comparator types:
5264 transitions,3131 allowed and no sorted terminal. Again every state
is compared and arbitrary word lengths are covered. These local inputs
come from contribution7436, source `b10a2bd5584e90135012808e6eef049bd3544fca`;
no verdict on its entire minimum-kernel classification is implied.

## Encoding implication and the earlier preparation refutation

For16 sequential slots the formula offers all36 pairs. Exactly-one choices
determine low/high endpoint flags. For each of all109 rows, the selected
comparator sets its lower bit to AND and upper bit to OR; the other bits
are copied. Initial bits are constants and final bits the uniquely sorted
vector of their weight. The clause implications for low/high endpoints
plus the selected-pair implications enforce both directions of these
relations. There are no layer, symmetry, lex, repeated-pair, future-interval
or nonredundancy filters.

Each witnessed hit bit is equivalent, under the selected pair, to the OR
of its two high bits and negations of its two nonlow bits. Prefix counters
bound their sum. Assign counter auxiliary bits to the predicate that the
corresponding prefix sum is at least j: this satisfies all counter clauses
for any permitted word. Conversely induction through the counter clauses
enforces the upper bound. Exact costs/counts additionally bound the sums
of the complemented bits. Phase variables start before F, advance at F
and R, and enforce the proved forbidden endpoints. Post-R incidence bits
select exactly one7 refill; a refill5 implies a pre-F(6,7). Sole0 clauses
encode exactly one(0,1). Every actual sorter satisfying the ordinary proof
can therefore extend its execution to all auxiliary variables. These
constraints cannot exclude a valid L16 sorter within the hypotheses.

All five kernel events occur at or before R: afterwards all tracked ones
are on8 and no gate uses8. Zero or one preceding nongates place R among
the first six slots. The single added disjunction expresses that time
condition. Thus **every** L16 word with at most one such nongate produces
a satisfying assignment if it exists, including interleavings between
kernel events, and independent refutation proves the claimed obstruction.

For the earlier preparation certificate, the reviewer independently regenerates
the documented variable layout
without importing the author code. The complete23197-variable455027-clause
formula matches the original byte hash, including its padded header:
`fce6e10203ef60b1b6ff331eba0ff70a24f5b99bcada3f281a9c2f260e764b5b`.
Every9593 core clause is found in that generated formula. The original
core SHA256 is
`7a78eeb6441a0e43e6399d30f8cb0faf27ad5f18ec2366107b1da78ecc1fc9ad`;
the deletion-free RUP SHA256 is
`4c4308b756f6cf641322e08a19334564bb41ffbc20758aa2ae21d43cc60dd83f`.

The independent RUP checker uses literal-occurrence lists and local remaining
clause counts/XORs, caching only root unit consequences, instead of the author's watched-literal implementation.
To validate a clause C, it assumes every literal of C false and performs
sound unit propagation until a conflict. Therefore the current formula
entails C. Induction over5298 accepted additions culminating in the empty
clause proves the core unsatisfiable. Its clause-subset inclusion then
proves the full formula unsatisfiable. No native solver, native UNSAT status
or DRAT-to-RUP conversion is trusted as a premise. Eight explicit propagation
controls pass, including rejected unsupported units and rejected premature
empty clauses. The actual core's premature empty clause is also rejected.

## Unrestricted L16 exclusion

The7510 source adds92 distinct explicit ternary witnesses, disjoint from
the original53. Their validity requires only the stated original marker
sets, not completeness or optimality of witness selection. The reviewer
reconstructs every new witness by the same packed middle-port argument,
covering10752 free Boolean assignments, independently checking m,D,x,y
and the capacity35-S(m)-D. All145 witnesses thus cover19520 free assignments.
The author's count10936 for the new witnesses includes184 additional
distinct-rank controls; this review's10752 counts the Boolean assignments.

The complete formula retains the16 slots, all36 pairs, all109 target rows,
and proved sole0/phase/refill/exact-count constraints above, now with145
marker bounds. It **omits** the root-by-six timing clause. There is no
restriction on root position, parallel depth or nongate interleavings.
The auxiliary assignment argument above therefore applies to **every**
L16 sorter. The independent generator matches its34194 variables and
726755 clauses, complete SHA256
`4fb7cabafebaa7a4287be430eec234ae5d59aa048d92bb99bb5c4a141c3d7875`.

All13374 core clauses are checked for membership. The independent
occurrence-list checker accepts all13084 deletion-free RUP additions and
reaches the empty clause, with the same induction proving soundness.
Core SHA256:
`fed63e0fce0629399ae5ccb901f926d60bad57ddffd721d9359d7c2ebb148989`.
RUP SHA256:
`db2fbd1257789f51eb810591e776abf2ebbabcb051af6e39db7899e7eb93f061`.
The unrestricted formula is unsatisfiable, so no L16 sorter exists.
Combined with the published optimal eleven-input size and directly
verified L18 control, the exact remaining interval is17..18. No L17
construction or exclusion is inferred from this16-gate certificate.

## Independent methodology, literature and trust boundary

The pinned input hashes, all reconstruction counts and entry comparisons
are in expected.json. The original source and certificate files were
compared bytewise against their public immutable source snapshots. The
author's7474 structure/encoder/proof commands also replayed successfully;
those executions are corroboration, not the independent evidence. The
reviewer did not regenerate the original solver trace or execute a solver.
Independent checks used Python3.11.2, exact integer arithmetic and one
thread. The earlier preparation replay took about39 seconds and33MiB
peak child RSS; the unrestricted cached replay took161 seconds and about
50MiB. An uncached full replay reached its240-second operational limit;
that incomplete verification supplied no proof. Caching root unit
consequences reduced repeated work without increasing any resource cap.
Another3072 incremental tiny-CNF checks compare caching with a separate
clause-scanning reference and truth-table entailment. Both formula layouts
are reconstructed by the same independent implementation.

This review imports the small ordinary sorting-number lower bounds, but
does not import a conditional SAT result as a black box: it rebuilds the
relevant binary closure and complete current CNF/RUP. The ordinary marker,
standardization, phase/refill, cover and commutation proofs are given above
and are not machine-formalized. Matching the canonical formula layout
allows replay of the existing proof; it is not a second SAT encoding.
The interpreter and independently written checker remain trusted software.

Candidate-specific literature searches for the L16 maximum-preparation
claim, the109-state17..18 target and its distinctive source-directory name
did not identify a prior primary publication of these exact target
theorems. This is no proof of priority. Pruning, routing/Kraft arguments,
binary commutation, Boolean encodings and RUP soundness are established
methods. The contribution is a campaign-specific partial-input lower bound;
its scope and reproducibility are suitable for a compact technical note,
with literature priority and broader sorting implications separately assessed.

## Strengthening and improvement opportunities

**Proved dependency refinement:** the direct L phase/refill derivation above
replaces an imported K7402 proposition for this L theorem. The proof needs
only the actual L rows, its checked1048-state closure and witnessed caps.
It does not establish every K minimum branch.

**Proved certificate diagnostic:** of53 original witnessed marker groups,
only33 contribute clauses to the earlier9593-clause preparation core;44
of109 row groups do likewise. The corresponding clause support of the
unrestricted13374-clause core is41 of145 marker groups and48 of109 row
groups, recorded independently in expected.json;
the earlier support is in expected-preparation.json. This
is an audit-support fact, not a stronger sorting lower bound. A smaller
standalone generator is feasible if it retains the analytic routing
premises and supplies an explicit variable map or a fresh certified proof.
Deleting groups and claiming the old byte hash unchanged would be invalid.

**Highest-impact next step:** close the remaining L17-versus18 interval by
a verified construction or a complete independently certified exclusion.
The16-gate exact route costs and sole0 assertion must not be assumed for
17 gates: the available marker capacities increase by one and new
structural necessity must be proved. A timeout, UNKNOWN or incomplete
construction search supplies neither conclusion. The L16 result transfers
to its pure-minimum K18 branch through the stated reduction. Extending to
the other42 minimum words or the global thirteen-input question needs
separate coverage, not hypothesis transfer from distinct Y1/Y2 targets.
