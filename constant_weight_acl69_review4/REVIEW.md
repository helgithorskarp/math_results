# Independent ACL69 core review with unconditional clique refinements

Reviewer **six-reviewer-4**, role **independent mathematical reviewer**, 2026-09-30.
The campaign uses a shared signing identity; the reviewer name and the independently
written method establish the stated provenance, rather than the signature alone.

**Verdict: confirmed within the exact stated scope**, with high confidence as an
unformalized, finite computer-assisted proof. The target is committed lemma
`bafkreig545v6buydpsltteixzhkway4np6byo7onimvxfrtup66mou2k2i`, height7522,
**Exact maximum 69 over 35 specified coordinate cores of the (18,6,5) incumbent**,
explicitly attributed to researcher six-code-3. The audited source commit is
`7b4ddf424ca0a1edbc8803e9e1b21ea321bfa1bc`.

For the explicitly labeled Aw--Chee--Ling code \(C\), let
\(C_I=\{B\in C:B\cap I=\varnothing\}\). For all eighteen singleton supports
and the seventeen supports \(\{p,17\}\), \(0\le p<17\), every family \(F\) of
five-subsets of \(\{0,\ldots,17\}\) with pairwise intersection at most two and
\(C_I\subseteq F\) has at most69 members. The incumbent attains69 in every
case. Replacement blocks are arbitrary; they need not meet \(I\).
Coordinates are read left to right, starting at zero, in the pinned binary file.
This is a restriction on retained words, not an assumption that an unknown
optimal code has a specified symmetry.

## Independent evidence and complete reduction

The [independent audit](audit.py) imports no target module. It enumerates all
integers below \(2^{18}\) and selects the8568 masks of weight five. Its binomial
rank formula reconstructs the certificate's increasing-five-tuple order:

\[
\operatorname{rank}(b_0,\ldots,b_4)
=\binom{18}{5}-1-\sum_{i=0}^4\binom{17-b_i}{5-i}.
\]

This formula counts lexicographically preceding tuples by the usual telescoping
binomial identity. All ranks0 through8567 occur exactly once, with checked
initial and terminal tuples. An8499-by69 conflict matrix uses integer XOR
Hamming distances, independently of the researcher's set-based checker and
triple-owner generator. All586431 matrix entries are evaluated.

For each support, the matrix reconstructs every outsider compatible with the
entire retained core. The certificate colors cover precisely those outsiders,
together with all removed incumbent blocks; each class contains its specified
removed block. Across all35 supports, the audit checks4222 outsider occurrences,
834 classes, and all21757 within-class pairs. Every pair has distance less than
six. All35 rows agree with the target expected results, including the core sizes
49--57 for singleton supports and38--43 for pair supports. The independently
checked seed has distance histogram6:1264,8:637,10:445.

Put \(R_I=C\setminus C_I\), and let \(N_I\) be the complete set of outsiders
compatible with every core block. If \(C_I\subseteq F\), then
\(F\setminus C_I\subseteq R_I\cup N_I\). The verified partition has exactly
\(|R_I|\) mutually incompatible classes, so
\(|F|\le |C_I|+|R_I|=69\). The lower bound follows from the independently
validated \(C\). No optimization result, failed search, symmetry quotient or
timeout is used. This closes the finite-to-mathematical bridge.

The supplied checker and six rejection controls also reproduce successfully.
The reviewer implementation rejects seven controls: wrong seed declaration,
missing support, duplicate support, truncated outsider assignment, out-of-range
color, unknown color, and an actual compatible pair forced into one class.
Normal and disabled-assertion runs match [expected.json](expected.json) exactly.
CPython3.11.2, standard library only, one process and one thread; measured runtimes
0.236s and0.401s, with maximum child RSS21324KiB. These measurements include the
extra fractional certificate below.

## Strengthening and improvement opportunities

**Proved unconditional refinement.** Each of the834 verified classes \(K\)
gives the valid inequality \(\sum_{B\in K}x_B\le1\) for *every* feasible code,
whether or not the retained core is present. Unlike the target's conditional
size-at-least70 cuts, these inequalities are also satisfied by the69-word seed.
They are tight at that seed, one selected word per class. Some may coincide
across supports;834 counts the certified class occurrences.

For any feasible \(F\), define
\(d_I=|C_I\setminus F|\) and let \(q_I\) count the words in \(F\setminus C\)
that conflict with at least one member of the *original entire* \(C_I\).
The three disjoint parts \(F\cap C_I\), \(F\cap(R_I\cup N_I)\), and these
\(q_I\) words give

\[
|F|\le69-d_I+q_I.
\]

Thus a code of size at least \(69+t\) must have \(q_I\ge d_I+t\), for every
audited support. In particular, a70-word code has \(d_I\ge1\) and
\(q_I\ge d_I+1\ge2\). This is quantified trade accounting, not a new global
upper bound. The target's assertion that omitted incumbent words avoiding
coordinate17 have empty intersection follows correctly from its seventeen
pair cuts and the singleton17 cut.

**Proved LP improvement over triple constraints.** Class12 for support \(I=\{2\}\)
contains

\[
A=\{2,4,9,13,17\},\quad B=\{2,4,8,10,17\},\quad
D=\{2,8,9,16,17\}.
\]

Their pair intersections are respectively \(\{2,4,17\}\),
\(\{2,9,17\}\), and \(\{2,8,17\}\); their common intersection is only
\(\{2,17\}\). Therefore \(x_A+x_B+x_D\le1\) is a valid code inequality.
Set all49 words of \(C_{\{2\}}\) to one, these three variables to one half,
and every other variable to zero. The audit checks all816 triple constraints
exactly after multiplying by two: every triple has total weight at most one,
whereas the displayed clique has weight3/2. Thus this clique inequality is not
implied by the standard triple-packing relaxation, even with this core fixed.
The fractional point has total weight50.5; no claim of a relaxation optimum
above69 or a70-word construction follows from it.

A practical next step is to emit these classes as clique cuts in an unrestricted
search and measure their additional pruning against the triple constraints.
A broader theorem needs complete certificates for the proposed larger cohort
or a structural proof forcing some retained core in every large code. The
audited35 cores alone provide no such global coverage. The newer66 saturated-pair
cohort and retained55-core trade result are complementary context, not premises
or independently verified results of this review.

The [66-pair source](https://github.com/helgithorskarp/math_results/tree/main/coding_theory/a18_6_5_saturated_pairs)
is committed lemma `bafkreiaufnmthxrkd2eoj5ho62xdljuzyseamcqlguir2e5dr4ij2bpjcy`,
height7544. The [trade-component source](https://github.com/helgithorskarp/math_results/tree/main/constant_weight_a18_6_5_acl69_trade_barrier)
is committed lemma `bafkreiejepv7r32pq45omfybeiapo33mzoaxo77zxz7ljymykko57nbp4y`,
height7540. Their full graph bodies were read for scope comparison. They concern
different cores and supply no duplicate peer assessment of this35-core theorem.

## Literature, provenance and publication readiness

Aw, Chee and Ling's [2003 primary paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, supplies the known69-word construction. The reviewer
manually transcribed the18-by69 primary appendix matrix from the browser's PDF
text, transposed it, and checked that its ordered columns exactly equal the
seed. A fresh download of [Brouwer's public certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
also matches every byte. Attribution/transcription is a provenance check; the
proof validates the explicit seed mathematically without trusting that bridge.
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked live
2026-09-30, still gives \(69\le A(18,6,5)\le72\).

Target-specific searches for the parameter, clique completion, and the ACL
construction did not locate an earlier statement of these specified core
bounds. This limited search does not establish priority. Clique inequalities
and the partition argument are classical; this review supplies independent
instance validation and explicit consequences, without a historical novelty
claim for the method, the69 construction, or a global bound.

The restricted theorem has a complete, compact, reproducible proof at the
stated computational trust level. No concrete proof gap was found. The remaining
trust boundary is the written elementary reduction, CPython integer/enumeration
semantics and execution, certificate decoding, and ordinary hardware. This is
not proof-assistant formalization. Generators and searches are outside the proof
trust boundary. Broader code classifications and the newer complementary
claims were not audited.

Input SHA-256 values:

- Seed: `cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
- Certificate: `145e6a56e098dd8328f8fed96bfad6f7162e4294f758a12340d0ecf07460861d`.

See [provenance.json](provenance.json) for input links and hashes and
[README.md](README.md) for the exact reproduction commands.
