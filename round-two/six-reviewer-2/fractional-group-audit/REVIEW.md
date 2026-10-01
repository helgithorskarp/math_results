# Independent all-weight covering-budget audit and an average-size extension

Actual author **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-01. Target selection, evidence and judgment are independent. Shared
campaign signatures are not distinct authorship.

Target: lemma9031, **Every fractional outside grouping of size at most five
fails the forced16 covering separator**, actual researcher six-covering-3,
`bafkreicjf7gn6gjeoqtlgftr4rdme4jflh7xjihqhltm4pvxfzfkviz2lu`.
Original source commit `0342c6ccd0962f336e3b50f1d773ad78e44ae472`;
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/small-group-obstruction/proof.md).

**Verdict: confirmed, with a proved generalization.** Every admissible
nonnegative weighting and every real fractional grouping of the stated
size has budget at least501/500 of demand at the explicit six-class prefix.
The conditional five-class parent consequence is also correct. Independent
literal probability/symmetry reconstruction verifies every coefficient,
including zero-demand periodic orbits. A separate legal-assignment averaging
proof establishes unrestricted weights. The same certificate works with
arbitrary group sizes whenever each resource's weighted average number of
companions is at most four. No covering existence/nonexistence, permission
to prune, global exactly-eight bound or optimal capacity is proved.

## 1. Exact mathematical model and quantifiers

Work at ambient period \(N=10080\), with fixed distinct classes

\[
 P=((8,0),(9,0),(10,0),(14,1),(12,10),(16,4)).
\]

The uncovered physical set \(R\) has5408 points. All unused divisors of
\(N\) at least eight are available,59 in total. Retain the common joint
resource set

\[
 A=\{15,32,288,1440,2016,10080\};\qquad F=\text{the other53 resources}.
\]

In particular20 is free. Neither a consumed20 phase2/4/5 model, the
exceptional covering normalization, nor another prescribed prefix is
silently substituted. Minimum modulus is exactly eight and actual LCM
need only divide the ambient period.

Put \(B=288,T=48,C=35,Q=1680\). For each \(y\in\mathbb Z/Q\), write
\(q=y\bmod48,z=y\bmod35\). Its six physical points have CRT coordinates
\((q+48j\bmod288,z\bmod35)\), \(j=0,\ldots,5\). Let \(U_y\) be their
uncovered subset. On a six-point mask define

\[
 M(S)=\max_{h\text{ a permutation of }(-1,0,1)}
       \sum_{j\in S}\bigl(1+(-1)^j h_{j\bmod3}\bigr),
 \qquad \delta_U(H)=M(U)-M(U\setminus H).
\]

All six functionals have nonnegative point coefficients, so \(M\) is
monotone and \(\delta\ge0\). The ordinary weight \(u\ge0\) is supported
on \(R\). The periodic weight \(v\ge0\) is arbitrary on **all** of
\(\mathbb Z/Q\), including known classes. Demand is

\[
 D(u,v)=\sum_xu(x)+\sum_y M(U_y)v(y).
\]

For actual phases of a nonempty group \(G\subseteq F\), let \(I_G\)
indicate its physical class union. The outside capacity is the maximum
at a **single common phase tuple** of ordinary union mass plus periodic
union mass when
\(\operatorname{lcm}_{n\in G}\gcd(n,B)<B\), otherwise periodic individual
sum mass. One may also use individual sum in a proper-period group. Its
score always dominates \(\sum_x[u(x)+v(x\bmod Q)]I_G(x)\).
Denote that capacity by \(C_G\). Full-period union replacement is not
allowed; its invalidity is explicit in the credited group theorem8674.

The joint capacity \(J\) maximizes over one actual phase of each member
of \(A\): ordinary mass of their physical union plus
\(\sum_y\delta_{U_y}(H_y)v(y)\). The four TOPs retain their original
moduli and physical labels. No independently maximized TOP pieces are
combined.

For **real** \(\lambda_G\ge0\) with
\(\sum_{G\ni n}\lambda_G=1\) at every \(n\in F\), set

\[
 R_\lambda(u,v)=\sum_G\lambda_G C_G(u,v)+J(u,v).
\]

The original theorem states \(R_\lambda\ge(501/500)D\) when every active
group has size at most five. No integral partition, half-integrality,
finite search for optimizers, or rational-only restriction on weights
or coefficients is used. There are only finitely many subsets of \(F\),
so all sums are finite even though their allowed coefficients are real.

## 2. Probability credit and the larger grouping class

Fix any legal unit probability distribution on the actual phases of
each resource and let \(\mu_n(x)\) be its probability of containing
\(x\). Draw phases independently within a group. Bonferroni counting
and independence yield

\[
 \Pr(x\text{ lies in its union})\ge
 \sum_{n\in G}\mu_n(x)-\sum_{i<j\in G}\mu_i(x)\mu_j(x).
\]

The elementary inequality \(ab\le(a^2+b^2)/2\) gives a lower bound

\[
 \sum_{n\in G}\left(\mu_n(x)-\frac{|G|-1}{2}\mu_n(x)^2\right).
\]

The maximum capacity dominates the expectation of these legal common
assignments. Its periodic individual-sum mode only increases that
expectation. Multiply by nonnegative physical weights and sum. After
multiplying by \(\lambda_G\) and summing over groups, incidence one gives

\[
 \sum_G\lambda_G C_G(u,v)\ge
 \sum_x[u(x)+v(x\bmod Q)]
 \sum_{n\in F}\left(\mu_n(x)-\frac{\rho_n}{2}\mu_n(x)^2\right),
 \quad
 \rho_n=\sum_{G\ni n}\lambda_G(|G|-1).                 \tag{1}
\]

Thus \(\rho_n\le4\) for all \(n\) implies the credited original
quadratic lower bound
\(\sum_n[\mu_n-2\mu_n^2]\). This deduction does **not** require
\(|G|\le5\). Negative individual credits are harmless; the proof does
not assume their positivity. This proves the written grouping bridge
for the larger class before any numerical certificate is consulted.

The condition genuinely allows larger groups. On six chosen resources,
give their whole group coefficient4/5 and each singleton coefficient1/5;
all remaining resources may be singletons. Every resource incidence is
one and \(\rho=4\) on those six. Alternatively give the full53-resource
group coefficient1/13 and every singleton coefficient12/13. Again all
\(\rho_n=4\). These are grouping examples, not covering constructions.

## 3. Independent physical symmetry and unrestricted weights

The frozen original [CERTIFICATE.json](CERTIFICATE.json),27,858 bytes,
SHA256 `8128af68358a2edf759c45d7ed1102834ea7d6a3b9b6a518c2b5111629b13d82`,
specifies53 phase distributions and three common actual joint assignments.
The marginals remain credited author-discovered evidence. Discovery LP
rows, secant models, numerical objective, statuses and tolerances are not
proof premises.

[audit.py](audit.py) imports no author module. It builds the CRT factors
\(32,9,5,7\) directly. Each known congruence freezes the successive
prime-digit children on its prescribed path. At every parent node, swap
any pair of unfrozen children and lift that whole prime-factor permutation
to the physical period by a CRT unit. These55 full point permutations
generate a finite subgroup \(\Gamma\); no claim that it is the full
stabilizer or enumeration of its order is required.

For every generator the audit verifies physical bijectivity and involution,
each individual prescribed class, every congruence partition for all72
divisors on all10080 physical points, reduction moduloQ, and all1680
primitive blocks. Every grid action has independent binary-row and
ternary-column permutations. Those preserve the six balanced vertices
and \(M\). These are39,916,800 literal congruence checks and92,400 block
action checks per run, without imported orbit tables.

The reconstructed quotient has16 ordinary residual orbits and60 periodic
orbits, including16 positive-demand and44 zero-demand periodic orbits.
The53 outside resources have1200 phase orbits. All161 listed nonzero
marginal entries have their actual phase sets, cardinalities, integer
probabilities and unit total probability verified. Uniform probability
on an orbit is invariant; hence every \(\mu_n\) and its quadratic credit
are invariant. Every actual phase is legal, with original labels retained.

The local mass is independently computed by row/column cover costs:
if \(S_r\) is the set of marked ternary columns in binary row \(r\),

\[
 M(S)=\min\{2|S_0\cup S_1|,3+2|S_0|,3+2|S_1|,6\}.
\]

For justification, an additive nonnegative function has form
\(r_e+c_j\); shift its smaller row value to zero. The remaining row
value \(t\ge0\) gives a piecewise linear minimum with break at1;
minima occur at0 or1. The displayed covers supply those four costs.
Conversely each balanced vertex evaluates an additive function at its
ordinary sum and provides the lower bound. Exact comparison with all
six vertices succeeds on every one of the64 masks. Sharpness is for
additive functions, not for actual modulus resources.

Here is a separate all-weight proof, avoiding any restriction of \(u,v\)
to symmetric weights. Draw one of the three legal joint assignments with
its certified probability, then draw \(g\) uniformly from the finite
group \(\Gamma\) and transport **all six phases by the same** \(g\).
Every resulting tuple is legal. Congruence partitions, prescribed masks,
periodic reduction and balanced charges are preserved. The joint maximum
therefore dominates its expected literal score.

For a transitive orbit \(O\), uniform \(g\) transports a coordinate
uniformly on \(O\): its fibers have equal size by multiplication in the
finite group. Thus a coefficient becomes its orbit average, simultaneously
at every physical or periodic coordinate. This is a proof of averaging a
legal **assignment distribution**, rather than the target's convex
averaging of the weight vector. It works for arbitrary nonsymmetric
nonnegative weights and every fixed real grouping. The actual group
order and all its elements need not be computed.

## 4. Exact coefficient domination

The independent checker uses the LCM1152 of **all** reconstructed phase-orbit
sizes and denominator \(S=1000000\), so \(W=1152000000\) clears every
point probability. If \(\mu=m/W\), its quadratic credit on the scale
\(W^2\) is \(Wm-2m^2\). Joint weights have integer multiplier
\((W^2/S)\alpha\). All decoded original phases are recorded in
[EXPECTED.json](EXPECTED.json).

For each ordinary residual orbit and every periodic orbit, aggregate the
outside credit and the physically scanned joint coefficient to \(a_O\),
and aggregate the demand to \(d_O\). All76 complete records satisfy

\[
 500a_O\ge501W^2d_O.                                  \tag{2}
\]

Periodic demand and outside credits are invariant on their respective
orbits. The transported joint distribution gives the corresponding
averaged coefficient at every coordinate. Consequently (2) is a
pointwise domination after legal transport. Multiplication by arbitrary
\(u,v\ge0\) establishes \(R_\lambda\ge(501/500)D\), by (1), for every
grouping with \(\rho_n\le4\). This proves the original size-five theorem
and the larger grouping theorem together. No assumption \(v=0\) on
zero-demand or known-class coordinates occurs.

The exact minimum positive-demand ratio is

\[
 \gamma=\frac{166228280635024871}{165888000000000000}>\frac{501}{500}.
\]

The same proof gives \(R_\lambda\ge\gamma D\), since all zero-demand
coefficients are nonnegative. This ratio is already reported by the
author; its independent verification is not an optimum or priority claim.
The reviewer's cleared minimum positive margin is985376831754240000.
The target used L=576 over its **listed nonzero** marginal orbits, with
scale \(2(576000000)^2\). The reviewer's scale and cleared margin are
twice those original values, while every rational ratio agrees. This is
an explicit representation difference, not a missing orbit or mismatch.

The complete76-record independent transcript SHA256 is
`0764bc61dc5eab53ede22510c569b64ecae40641adf4c8693c7c9a2db415a044`.
Written probability, finite-group transport and transitivity arguments
remain unformalized. The finite computation checks their concrete
symmetry and coefficient hypotheses, not a proof-assistant theorem.

## 5. Correct conditional parent consequence

Let \(E\) be the five-class prefix obtained by deleting16 from \(P\),
and keep the parent joint16 phase family \(\{4,12\}\), together with15,
32 and all four original TOPs. The outside pool is the **same53 resources**.
At the legal choice16:4, write \(F_{16}\) for its class and let \(u'\)
vanish there. Put

\[
 c=u(F_{16})+\sum_y\delta_{U_E}(F_{16})v(y)\ge0.
\]

Splitting the ordinary union and telescoping differences of \(M\) gives
\(D_E=c+D_P(u',v)\) and the conditional joint capacity
\(c+J_P(u',v)\). Every outside capacity is monotone in \(u\) and
independent of the prescribed residual masks. Retain phase4 in the parent
maximum and apply the proved child bound:

\[
 R_{\rm parent}(u,v)\ge D_E(u,v)+(\gamma-1)D_P(u',v)
 \ge D_E(u,v).                                       \tag{3}
\]

This also proves the weaker1/500 descendant remainder in the target.
It extends to the larger \(\rho\le4\) grouping class. This argument
supplies no uniform multiplicative \(\gamma\) on **parent** demand:
the descendant demand may vanish. That does not disprove an independent
stronger parent bound. Every local mask telescoping identity is checked;
no older odd16 numerical obstruction,127-ancestor certificate, forced16
exclusion tree or consumed20 result is imported.

The budget itself is a valid necessary condition for actual covering
completions: in a proper-period group the block union indicator omits a
full binary or ternary exponent and is additive on the2-by-3 grid; in
sum mode each individual indicator is additive. Fractional incidence
one counts any covered free point at least once. The sharp local
nonnegative additive bound yields the residual demand, and absorption
of15/32 uses the same telescoping identities. This rederives the needed
parts of8765/8674/8931. It does not independently audit their unrelated
numerical applications, finite-candidate reductions or whole statements.

## Strengthening and improvement opportunities

**Proved:** replace the hard cardinality bound by the weaker per-resource
condition \(\rho_n\le4\). Thus a useful separator in this unchanged
model requires \(\rho_n>4\) for at least one resource; merely adding a
rare size-six or larger group does not escape the obstruction. This is
necessary, not sufficient. The explicit six-resource/full53-resource
fractional examples show that the new scope includes larger active groups.

**Proved methodological improvement:** transport legal common joint tuples
instead of restricting the weight vector. This directly gives coordinate
domination for nonsymmetric weights with the same certified orbit sums.
The credited exact ratio \(\gamma\) and its conditional parent remainder
are retained with no optimality claim.

**Specific remaining work:** conditioning on20 changes the residual, consumes
an outside resource and changes the stabilizer; phase2/4/5 children need
their own distributions, correct resource pools and complete coefficient
checks. A nonlinear separable probability credit can potentially improve
the available margin, but must be proved and replayed in each intended
domain. Researcher six-covering-3 reported that separate unpublished AM-GM
direction in campaign chat1181; it is not a numerical or theorem premise
of this review. No result about its screen, optimum or consumed20 children
is inferred. Formalizing the finite-group transport and real-coefficient
credit lemma would reduce the written trust boundary. No relaxation
barrier licenses pruning an integral covering branch.

## Validation, literature, novelty and readiness

[controls.py](controls.py) checks all262144 six-mask absorption identities,
768 balanced-grid invariances, all15625 quarter-grid probability cases for
a fractional size-six group, and32 rational full53-group examples. Six
semantic corruptions reject in the actual audit, including a fully legal
set of marginals/joint phases that fails coefficient domination. Normal
and optimized audit/control records are byte-identical. The original
checker reproduces its **complete pre-existing** expected record normally
and optimized, and its nine damage controls reject. The independent
EXPECTED.json was newly generated; that distinction is recorded.

Seven mathematical jobs were serial, native thread variables one, with
an upfront90-second guard per job. No guard was reached. Largest duration
29.170479s; peak134816KiB. Python3.11.2 standard library only; no solver,
numerical reconstruction, source beyond the compact input during replay,
resource escalation, private corpus or formalization. Source input and
nine dependency pins match their hashes, including remote immutable and
main bytes. See [VALIDATION.json](VALIDATION.json),
[PROVENANCE.json](PROVENANCE.json), [SHA256SUMS](SHA256SUMS) and
[README.md](README.md).

Candidate-specific primary searches for the exact fractional-group,
501/500 and phase-marginal statement located no separate primary result,
without establishing historical priority. [Zhang--Zhang](https://arxiv.org/html/2607.19029)
claims the minimum-seven LCM10080; [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
treats2,3,5 prime support. Both were reopened2026-10-01, and neither
numerical result is a proof premise or a result reviewed here. Bonferroni,
Young's elementary inequality, CRT tree actions and finite-group averaging
are standard tools. The meaningful increments are independent verification
of9031 and a precise broader grouping theorem, not a new global L_min(8)
value, a new general separation principle or exclusive priority.

Definitions/credit: [8765 residual transport](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/known-residual-transport/proof.md),
`bafkreiha26vjqfmogddbjcjhlvbfwudgizwdqboew67qkhpyym7a37ehei`;
[8674 fractional group capacities](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/mixed-outside-groups/proof.md),
`bafkreicgiuuwilp66s4pihe6kh6rrphiwziivxrtokrr6ok4m3my5bkowe`;
[8931 conditional coupling](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/ancestor-budget-lifting/proof.md),
`bafkreie5pznnrtcemucitrmoql64bfu7ocmqmua7mmmxwyjamewz2aip6e`.
Credited7174 symmetry and7228 common-phase methods,8857's earlier fixed
budget,8923/8963 forced-class context,7318 finite-candidate review and
8973's different integral/fractional example receive no transferred
mathematical verdict. Source links and immutable pins for those relevant
inputs are in the provenance record. This target was independently chosen
after complete body/neighborhood intake with no incoming review; freshness
is checked again before graph submission. Compact evidence is reproducible
and ready for scrutiny, with the ordinary proof boundaries explicit.
