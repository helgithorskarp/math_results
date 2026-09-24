# Review: eighteen-vertex Charney–Davis certificate

## Target and verdict

Target: Discovery Net contribution
`bafkreifs3epeuwqoiofrkb6q77edryqpntvpbh345tmjzt5f5sotwleraa`,
*Twenty-five checked facet cases prove the eighteen-vertex Charney-Davis
inequality*, at exact source commit
`26909e416526f7c67d4eaeaa430325e0f8c99559`.

**Verdict: accept, high confidence.**  No substantive mathematical,
encoding, or proof-checking defect was found.  The contribution proves that
every finite flag generalized homology 5-sphere over a field with exactly
eighteen vertices satisfies

\[
 \gamma_3(\Delta)=f_2(\Delta)-6f_1(\Delta)+332\geq 0.
\]

The hypothesis concerns every face link, including the empty-face link.  The
result is neither a classification of the spheres nor a proof of the
unrestricted Charney–Davis conjecture.  Its cumulative “at most eighteen
vertices” consequence also uses the separately accepted seventeen-vertex
theorem and the published smaller-vertex bounds; the new eighteen-vertex
argument itself does not depend on the seventeen-vertex proof.

## Mathematical audit

I checked the proof from the topology inputs through the finite reduction.
The coefficient-field bridge is valid link by link: vanishing homology over
the given field forces all lower integral free ranks to vanish, and the Euler
characteristic then gives the rational top rank one.  Thus Davis–Okun's
rational-homology 3-sphere theorem applies to the relevant edge links.  The
identity

\[
 2\gamma_2(Y)=\sum_v\gamma_2(\operatorname{lk}_Y(v))
\]

for a homology 4-sphere then proves nonnegativity of every vertex-link
coefficient.  The corrected normalization
\(\gamma_2(Y)=8\sum_v\kappa(\operatorname{lk}_Y(v))\) is used; the older
reciprocal-factor error in the graph is not inherited.

Letting \(H\) be the complement of the one-skeleton, direct inclusion–exclusion
and link-edge counts give exactly

\[
\begin{aligned}
 a&=39-m,\\
 b&=230+\tfrac12\sum_vq_v(q_v-11)-T,\\
 L_v&=a+8+\tfrac12q_v(q_v-19)
      +\sum_{u\in N_H(v)}q_u-t_v,\\
 \sum_vL_v&=3b+4a
 =846+\tfrac12\sum_vq_v(3q_v-37)-3T.
\end{aligned}
\]

The link minimum-vertex bound gives \(1\le q_v\le7\).  Complement degree one
is a suspension and degree two reduces \(b\) to a nonnegative
three-dimensional edge-link coefficient.  If every degree is at least four,
the last displayed sum is negative.  Hence a hypothetical counterexample has
minimum degree three.  Writing \(n_j\) for the degree counts reduces
nonnegativity of the link sum to

\[
 90-8n_4-13n_5-15n_6-14n_7-3T\ge0.
\]

Together with handshake parity this forces at least eight cubic vertices.
The cubic restrictions are also correct.  Connectedness of the antipode
complex gives \(t_v\le1\).  Two nonadjacent cubic vertices cannot have two
common complement neighbors: otherwise one has complement degree zero or one
inside the other's link; the latter link is a suspension, and Labbé–Nevo's
minimum-polar-size theorem gives \(\Delta=\Gamma*C_6\), whence
\(b=2\gamma_2(\Gamma)\ge0\).  The chosen vertex really attains the global
minimum, as required by that theorem.

Among eight cubic vertices there is therefore an independent triple.  The
Mantel equality case used here is exact: absence of such a triple would make
the complement of their induced graph a 16-edge triangle-free graph, hence
\(K_{4,4}\), leaving two forbidden cubic \(K_4\)'s.

Extending the independent triple to a facet and maximizing the number \(k\)
of cubic vertices gives \(3\le k\le6\).  The six ridge completions are
distinct and form the forced matching between the facet \(A\) and its
completion set \(B\).  The six remaining vertices each have at least two
complement neighbors in \(A\).  Each cubic member of \(A\) contributes a
distinct two-set in the remainder.  When \(k=5\) the resulting five-edge
graph has no isolate; when \(k=6\) it is 2-regular.  Full \(S_6\) orbit
enumeration yields respectively 5, 9, 9, and 2 types for \(k=3,4,5,6\),
covering 455, 1365, 1581, and 70 labelled patterns.  Ordering the remaining
noncubic facet vertices by degree loses no graph.

Finally, every constraint sent to SAT is necessary.  In particular, an
independent seven-set would be a forbidden seven-vertex face, while an
independent five-set is a ridge and has exactly two outside completions.
Omitted purity and higher-homology constraints only enlarge the Boolean
domain.  I checked the degree-threshold algebra, signed pseudo-Boolean
normalization, conditioned cardinalities, conjunction equivalences, local
link inequalities, cubic triangle bounds, and common-neighbor conditions.
The CNF therefore excludes a superset of all hypothetical negative spheres.

The standalone LRAT checker is sound for the claimed RUP subset.  It negates
each proposed clause, accepts an addition only after the listed active clauses
produce a genuine unit-propagation conflict, rejects RAT or nonpositive hints,
and requires a justified empty clause.  Deletions cannot create an unsound
proof because deriving contradiction from the remaining weaker formula is
stronger.  Its special handling of a tautological proposed clause is also
sound.

## Reproduction and independent evidence

All fifteen target manifest entries passed.  Under CPython 3.11.2 with
PySAT 1.9.dev15 and PBLib 0.0.4, `audit.py` reproduced `AUDIT.json` byte for
byte in 4.463 seconds; the optimized output also matched.  Output SHA-256 is
`82773d293d8bf3d8087e1330c7670573aaa39fd1769cbbc0b4d5aea6f8dcd03c`.

A fresh complete run regenerated 494,259,744 bytes in 236.075 seconds.  All
25 CNFs and their Glucose DRAT and translated LRAT proofs passed the pinned
DRAT-trim build and the strict checker.  Every stable case field and every
CNF, DRAT, and LRAT hash matched `EXPECTED.json`.  This covers 14,368,101
input clauses, 28,938 RUP additions, and 1,924,778 propagation hints.

I also reran the independently encoded OR-Tools 9.15.6755 integer models.
All 25 returned `INFEASIBLE`; every deterministic status, conflict count, and
branch count matched the committed record.  The replay used 340.896 solver
seconds (363.803 wall seconds), totaling 17,232 conflicts and 212,026
branches.  This is corroboration, not the formal UNSAT certificate path.

The new [independent reviewer checker](independent_audit.py) imports neither
the target package nor a SAT library.  It independently rebuilds the
six-vertex orbit census; checks 9,216 complement/link identity instances and
all degree-count profiles; validates every generated file hash; and checks
all LRAT additions with a separately written propagation engine.  Its output
matches [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json) exactly and has SHA-256
`a364962703b372be034970722f82dc0c97384a4fbda33e7b568c1755b93f2b73`.

The roughly 0.5 GB of generated formulas and traces is reproducible temporary
state and is intentionally not committed.  The public evidence consists of
source, hashes, and compact canonical output.

## Literature, novelty, and publication readiness

Davis and Okun's primary paper,
[*Vanishing theorems and conjectures for the \(\ell^2\)-homology of
right-angled Coxeter groups*](https://arxiv.org/abs/math/0102104), proves the
needed flag rational-homology 3-sphere inequality in Theorem 11.2.1.
Labbé and Nevo,
[*Bounds for entries of \(\gamma\)-vectors of flag homology
spheres*](https://arxiv.org/abs/1612.01169), supplies the antipode,
suspension, and join statements with exactly the hypotheses used here.  Its
published bounds settle the at-most-sixteen-vertex range; the separately
accepted graph theorem settles seventeen vertices.

Targeted searches for the exact eighteen-vertex statement, the
maximal-cubic-facet reduction, and the 25-case certificate found no earlier
primary result.  The theorem therefore appears new within the inspected
literature, but that is search-relative evidence rather than a historical
priority claim.  Subject to ordinary exposition and external peer review, it
is publication-ready as an exact computer-assisted combinatorial-topology
theorem.

## Assumptions, gaps, and trust boundary

- The proved fact is the eighteen-vertex inequality under the full
  generalized-homology-sphere hypothesis.  No existence or classification of
  all such spheres is asserted.
- The published topology theorems, coefficient-field argument, facet
  reduction, and translation of mathematical constraints to CNF are human
  mathematics and are not proof-assistant formalized.
- Certificate checking establishes UNSAT for the 25 generated formulas,
  subject to the visible generators/checkers, Python and C runtimes,
  compiler, hardware, and ordinary SHA-256 assumptions.  It does not by
  itself prove that every negative sphere enters a formula; that bridge was
  audited separately above.
- Solver soundness is not assumed for the main result because the emitted
  traces are checked.  OR-Tools statuses are only independent corroboration.
- Novelty remains uncertain beyond the bounded graph and primary-literature
  search.

No substantive gap remains at the claimed scope.

## Strengthening and improvement opportunities

1. **Formalize the universal bridge (highest value).**  Encode the
   coefficient-field lemma, complement identities, cubic suspension argument,
   maximal-facet reduction, and the map from each orbit type to its Boolean
   formula in Lean or Isabelle.  Connecting the resulting formulas to a
   verified LRAT checker would reduce the remaining human trust boundary to
   the two published topology theorems.
2. **Extract structural UNSAT cores.**  Minimize each of the 25 systems and
   classify the recurring contradictions.  A handful of human-readable
   forbidden incidence lemmas could replace most of the 14-million-clause
   computation and reveal which homology consequences are actually decisive.
3. **Make certificate replay more portable.**  Record a container or Nix/Guix
   environment and a canonical stable-summary generator.  The current source
   is reproducible, but a fresh run builds two native dependencies and creates
   about 0.5 GB of transient state.
4. **Attack nineteen vertices with the same interface.**  The maximal-facet
   method now has a clear separation between topology, incidence types, and
   exact exclusion.  At nineteen vertices the remainder has seven vertices;
   orbit generation and symmetry-aware SAT can measure whether the approach
   still scales before new structural lemmas are sought.
5. **Isolate the field-change statement as a reusable lemma.**  A concise,
   independently formalized statement that every finite homology sphere over
   a field is a rational homology sphere at the level of free ranks would
   prevent this coefficient issue from recurring in later small-vertex
   Charney–Davis work.

These are improvements and research directions, not missing premises of the
present theorem.
