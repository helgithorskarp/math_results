# A changed thirteen-input prefix reduces to a 177-state eleven-wire target

Author and executing agent: **six-sorting-1**, role **researcher**,
2026-10-02. Complete author proof with two computational representations;
unformalized, with no external independent-review verdict.

Use physical ports0..12 and standard comparators(a,b), a<b, which send
the smaller value to a. Define the literal words

~~~text
N19 = (0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
      (0,2),(3,6),(4,12),(5,7),(8,10),
      (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
      (0,1),(2,10).
B21 = N19 ; (4,8) ; (3,6).
B23 = B21 ; (9,11) ; (11,12).
~~~

The ordered [fixture](fixture.json) is authoritative. The complete
Boolean image of B23 has179 thirteen-bit states. Its projection onto
physical ports1..11 has177 eleven-bit states, called I. Logical core
port j corresponds to physical port j+1; bit j of a listed integer is
the value at that logical port. The complete I, with original-input
multiplicities, is in [certificate.json](certificate.json).

**Theorem.** A standard thirteen-input sorter of total size at most44
beginning with literal B21 exists if and only if a standard eleven-wire
word of at most21 comparators sorts every state in I. The equivalence
covers arbitrary order, repetitions, depth and intervening preparation
comparators. In a hypothetical B21 completion its first maximum-route
events are necessarily(9,11),(11,12); they can be commuted to the suffix
front. Physical ports0 and12 are then frozen.

The six-history maximum-only reduction is credited to six-sorting-2's
[Section0](../../six-sorting-2/native24-kernel-cover/P21.md), source
dce3955b2880381edb2884b7446d282bf7bdeda5, actually committed lemma9207
bafkreigyiwnzlza2aetdtlaoctzrvsare6jh6onf5mxb7yzftmmm7xqk4u.
We apply its general structural lemma to a different literal prefix,
reconstruct its premises here and spell out the application below.
The native P21 and P22 exclusions are not premises for this changed
prefix. The new claim is this concrete reduction and complete target,
not priority for the generic maximum, pruning or Huffman mechanism.

There is no44-comparator witness or exclusion of B21 here. The global
minimum remains44..45 in the [primary table](https://bertdobbelaere.github.io/sorting_networks.html),
checked2026-10-02. I is a restricted image, not all2048 eleven-bit inputs;
the21-comparator question for I remains unresolved.

## 1. Ordinary mass and anchored touch budgets

Fix an original placement of two distinct values below all eleven
free inputs (LOW), or above them (HIGH), and retain the full free
Boolean cube. Let D count gates meeting a mark, once for stationary
touches and once when a gate meets both marks. Marked configurations
and these touch increments do not depend on the free Boolean values.

For any fixed selected subset T of original placements, group by
current unordered marked pair z, put d_T(z)=max D in that class and
W_T=sum_z 2^d_T(z), omitting empty classes. A comparator's unordered
pair map has at most two preimages per output configuration. Both
preimages of a double fibre are touched. The inequality

~~~text
2^(1+max(d1,d2)) >= 2^d1 + 2^d2
~~~

and nonnegative increments on single fibres prove that W_T never
decreases. Original conditional domains stay separate before maxima
are formed; equal marked configurations do not identify their Boolean
images. This applies to the six selected histories as well as to the
full78-placement family.

At the end of a total-m sorter all two-LOW configurations are{0,1},
and all two-HIGH configurations are{11,12}. Removing the marked paths
leaves a generalized eleven-input sorter with at most m-D gates.
Standardization adds no comparators. Imported S(11)>=35 implies
D<=m-35 and consequently W_T<=2^(m-35) at every prefix. For m<=44
the ceiling is512. These are the established pruning principles of
[Harder, Section3.2](https://arxiv.org/html/2012.04400v3#S3.SS2),
and the credited campaign [pruning proof](../../six-sorting-2/semantic-pruning/PROOF.md),
actual8539. The large S(11) lower-bound corpus is imported, not rerun.

For a reachable unary extreme at p, define its ordinary pair anchor
M_p=sum_(z contains p)2^d(z) using the corresponding LOW or HIGH family.
A gate avoiding the unary route preserves p-membership, so the fibre
argument gives nondecrease. If the gate meets p, the pair map restricted
to old pairs containing p is injective, every such pair is charged,
and all their images contain the new unary port. Hence the anchor
at least doubles. Thus t future touches, including stationary touches,
give 2^t M_p<=512 in a total-size-at-most44 completion. This is the
ordinary case of the credited [anchor transport](../../six-sorting-2/semantic-pruning/ANCHORS.md),
actual8604. No semantic identity deletions are needed below; R and its
mask are nevertheless fully reconstructed as auxiliary certificate fields.

## 2. The complete maximum-route alternatives at B21

The full unary and pair data give exactly these maximum-route ports:

| HIGH port | Ordinary anchored mass | Future-touch upper bound |
|---:|---:|---:|
|9|64|3|
|11|80|2|
|12|192|1|

Every unary-HIGH route must end at12. Three distinct routes need two
binary merges. Route12 can join only at the final merge, without a
singleton event, since it has only one touch available. Routes9 and11
must merge first. Route11's two required merges exhaust its capacity.
Route9 can have at most one extra singleton event, before that merger.

The first maximum event is therefore either the direct merge(9,11),
or g_r=(min(r,9),max(r,9)) with

~~~text
r in U = {0,1,2,3,4,5,6,7,8,10}.
~~~

In a singleton branch let F be the entire preparation before g_r.
It avoids9/11/12, and uses only U. The next maximum events are
(max(r,9),11), then(11,12). Gates preceding each of these events avoid
its currently live endpoints, so that event commutes left across them.
The branch consequently has the function-preserving necessary form

~~~text
B21 ; F ; K_r ; E,
K_r = g_r ; (max(r,9),11) ; (11,12).
~~~

F and E have arbitrary length and depth. We keep g_r after F, which
may touch its free operand r. Moving that first singleton across F
would be unjustified. The touch-budget argument is the complete event
cover; the312 checked next-gate controls are finite audits of it,
not a finite enumeration of F or E.

## 3. Six original histories exclude all ten singleton branches

The following independently reconstructed records already hold at B21.
Each original pair retains all2048 free Boolean assignments.

| Original HIGH mask | Original HIGH ports | Current HIGH pair | D |
|---:|---|---|---:|
|768|{8,9}|{9,10}|4|
|257|{0,8}|{9,11}|4|
|258|{1,8}|{9,12}|5|
|10|{1,3}|{5,12}|5|
|130|{1,7}|{6,12}|5|
|6|{1,2}|{7,12}|5|

The first three are the baseline. Throughout F their configurations
are unchanged. F avoids9/11/12. A HIGH mark at10 is stationary under
an F gate touching10 because every other F endpoint is smaller.
Their costs are at least4/4/5, and the first is at least5 if F touches10.
For each of the ten r values, after K_r the three histories give
distinct terminal classes

~~~text
{9,12}:D>=7, {10,12}:D>=7, {11,12}:D>=8.
~~~

For r=10 the first two histories exchange their destination classes;
the three-class mass is unchanged. Their total is at least
128+128+256=512. An F touch on10 raises this to at least640, impossible.
Thus a surviving F uses only0..8. All ten terminals and all90 one-gate
stationary10 controls are checked. Arbitrarily many touches only
increase the same bound.

The last three histories are shadows, initially at{5,12},{6,12},{7,12}
with D5. Under a standard F on0..8 the secondary HIGH mark moves only
upward, remains in5..8, and the mark at12 stays fixed. Let q_i,d_i be
their positions and costs after F. Applying Section1 to this selected
three-history family gives class-max mass at least3*2^5=96, regardless
of its mergers or the length of F.

If any q_i differs from r, the first two K_r gates avoid that secondary
mark. The final gate touches12 once, leaving{q_i,12}:D>=6. This is a
fourth class, distinct from the baseline's secondary ports9/10/11.
Its positive weight adds to the saturated512, violating the ceiling.

Otherwise all three q_i equal r. They form one selected class of
weight at least96; its integer maximum D is at least7, since2^6<96.
Here r must lie in5..8. All three K_r gates are marked touches, so
an original history reaches D>=7+3=10. A total44 sorter would then
prune to an eleven-input sorter of at most34 gates, contradicting
S(11)>=35. The40 terminal shadow cases and144 closed-map controls
verify the local routing premises for this exhaustive dichotomy.

Every singleton branch is excluded for arbitrary F and E. In the
direct branch(9,11) commutes across the initial preparation avoiding
its endpoints; the next merge(11,12) likewise commutes across subsequent
preparations. The total function and number of gates are preserved,
and the resulting literal prefix is B23. This applies the generic
maximum-only lemma9207. In particular the older changed
[E22=B21;(3,9) exclusion](../joint_slack_prefix_barrier/PROOF.md),
actual9154 bafkreibkufgutjw4ze7ypqhlf5touj4w4nh3bjyupal4gz6s4i2nedtz6q,
is now one of ten excluded singleton choices, with arbitrary F also
allowed. Its exclusion is not imported as a premise here.

## 4. Frozen outer ports and the exact construction target

At B23, every unary-LOW route is at0 and every unary-HIGH route at12.
The complete ordinary pair envelopes are

~~~text
LOW:  {0,1}:D7, {0,2}:D7, {0,3}:D6, {0,4}:D7.
HIGH: {5,12}:D6, {6,12}:D6, {7,12}:D6,
      {9,12}:D6, {10,12}:D6, {11,12}:D7.
~~~

Both ordinary masses and the respective anchors M0/M12 are448.
Any later touch on0 or12 would double its anchor to at least896>512.
Thus both ports are frozen in every total-size-at-most44 completion.
They already have their correct sorted Boolean values on all8192
original inputs; the two independent representations check this directly.

After normalizing to B23, all remaining comparators use physical1..11,
and at most44-23=21 are available. Their projection is a standard
eleven-wire word sorting I. Conversely, lift any standard word of at
most21 gates sorting all177 states by(a,b)->(a+1,b+1), and prepend B23.
The two fixed outer values and the sorted core then sort every one of
the8192 original Boolean inputs. The zero-one principle implies the
lifted network sorts every input. This proves both implications without
a depth restriction.

The compact-JSON core list, without a trailing newline, has SHA256
2c423b8dba76c1c8b779f505c8f42b7913fe18b83222476ac50db1525f573067.
Its counts by Hamming weight0..11 are

~~~text
1,6,13,21,26,29,29,22,17,8,4,1.
~~~

The certificate includes all179 full states and177 core states, plus
their original-input multiplicities, both summing to8192. The two
state counts need not agree when the already-correct outer ports are
projected away.

## Reproduction and trust boundaries

From the repository root, with Python3.11.2 and its standard library,
run sequentially:

~~~sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-1/changed_b21_core11/generate.py
python3 -B round-two/six-sorting-1/changed_b21_core11/verify.py
~~~

Expected checker status: B21_CORE11_SCALAR_CERTIFICATE_VERIFIED.
Repeat with python3 -O -B; certificate bytes and all finite output
fields agree. [checks.json](checks.json) records those observations.
The certificate is30679 bytes, SHA256
bdee9513ec155f2d2ba4c551d8cc1554bf0f446d38105e0af447b392d5775b31.

The producer uses the credited hash-pinned
[packed-column profiler](../../six-sorting-2/semantic-pruning/profile.py),
SHA256 dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719.
The standalone checker imports no producer, profiler, sibling checker,
solver or nonstandard package. It numerically replays distinct marked
ranks on all312 original pair domains and638976 complete free
assignments at B21/B23, reconstructing every D/R/mask/envelope field.
Numeric unary routes, local branch controls and scalar Boolean images
differ from the producer's masks and packed truth columns.

The52 unary tag routes,312 high next-gate controls,30 baseline terminal
histories,90 stationary10 scenarios,40 shadow alternatives and144
closure controls agree. Eleven damaged packet controls reject. The
known primary35-comparator eleven-input word and its reverse-dual each
pass2048 inputs. Removing identity gates of that reverse-dual on I
leaves a checked30-gate core word; its lift after B23 is a53-comparator
positive decoder control passing all8192 inputs. It tests the target
and lifting convention; it does not attain the desired21-gate budget.

Normal/optimized scalar checks took5.327/5.671 seconds, with20476/22736
KiB peak RSS; generation took about0.164 seconds. Every stage finished
under the unchanged55-second guard, one CPU job and threads1 in the
1CPU/2GiB scope. No solver, cutoff or incomplete enumeration is a proof
premise. The general pruning/anchor methods, maximum-only lemma9207
and S(11)>=35 are explicitly credited. Universal transport,
commutation and zero-one reasoning remain unformalized analytic
bridges; algorithmic independence is by this same researcher, not
an independent-person review. Large lower-bound corpora, raw heuristic
logs, keys, ledgers and private checkpoints are omitted.
