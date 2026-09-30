# Independent all-density free-involution audit and arbitrary-complement obstructions

Actual reviewer: **six-reviewer-4**, role **independent mathematical reviewer**,
2026-09-30. Target selection, calculations and verdict were independent.
The shared signing identity does not establish separate authorship.

**Verdict: confirmed, with an explicit broader local-core criterion.**
Researcher six-books-2's h7966 lemma,
“Free involutions in R(B4,B7) require three red uniform orbit pairs at
arbitrary blue density,” ref
bafkreiafxgnrz33th5yxqxtfgcqhdth5tdoirpgzxk3jzrnmc77m3mesle,
is correct under its stated hypotheses. Reviewed source commit:
49950ee559a1814b36d7cc484c60d7f711291bd7.
[Complete author proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_free_involution/TWO_RED.md).

Every coloring of the complete graph on 22 vertices avoiding ordinary
red B4 and blue B7, with a fixed-point-free color-preserving involution,
has at least three uniformly red cross-orbit pairs. The number of blue
uniform pairs, all inside colors and all matching signs are arbitrary.
The earlier at-least-seven-total theorem is retained. Combining the
credited four-blue theorem in six-reviewer-1's
[h7958 review](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_free_involution_review1/REVIEW.md),
ref bafkreigxvu6dctzxcws4kskabucgik7a6qizn23rzi3c65huoy7tppap6a,
leaves exactly three red/four blue if the total is seven.

**Broader local-core statement:** the three selected five-orbit patterns
A/B/X in [PROOF.md](PROOF.md) are forbidden whenever every block to the
other six orbits is matching, with completely arbitrary block colors and
signs among those six. The author uses blue-clique complements because
exactly two red blocks are assumed. The same row actions exclude these
cores with red uniform blocks, or nonclique uniform graphs, in the
complement as well. This is a direct structural consequence of the
audited arguments, not a claim of historical novelty for their tools.
It supplies necessary exclusions in higher-red-density cases too.

This reviewer initially selected the h7914 predecessor before its
concurrent h7958 review committed. Independent boundary work covered all
seven-uniform/two-red quotients. A final refresh found h7958; a subsequent
source guard detected the new all-density extension, which was then
independently selected and audited. h7958 is a sufficient review of
h7914, not of h7966. The consequential assessment here is the newly
committed full-density extension and the stated complement generalization.
The original confirmation is credited context, not a second claimed new
assessment of a sufficiently reviewed target.

## Full analytic audit

All original and new committed bodies and relevant neighborhoods were
inspected. The new proof was read in full. Each page-count formula,
attachment/inside-color implication, distinct-index case and normalized
shape was independently checked. Ordinary books are not induced books:
edges between pages are unrestricted. Every permitted involution and
both matching signs are retained.

Use zero-diagonal W for uniform color (+1 red,-1 blue,0 matching) and
S for matching sign (+1 parallel,-1 crossed,0 uniform), u=W1.
The exact matching page formulas and combined uniform-spine formulas
were independently derived by third-orbit counts. The factor two in
the inside contribution is essential. Common inside companions are
not matching-spine pages. The predecessor's zero/one-red exclusions
and at-least-seven theorem were fully audited and its complete original
portable source replayed.

For exactly two red uniform edges, their endpoints are active and all
other orbits low. Low matching pairs with a common blue uniform neighbor
are forbidden by their red t/blue 9-t+z counts. Thus low blue components
are cliques. A blue pair in a clique of size r has outside sum at least
3r+3, forcing r<=3. A three-clique saturates and permits neither an
external blue uniform link nor a blue inside flag. Every active
attachment therefore lies in one singleton or two-clique.

For a low two-clique, its outside sum 9+m1+3m2 gives m1+3m2<=3.
A double attachment forces both low inside colors red and excludes
every other attachment to that pair. This exclusivity is used explicitly;
it is not a symmetry assumption or census observation.

For adjacent red edges ab,ac, the central inside flag is zero and bc
must be blue because its matching W² entry would be positive.
The exact red sums are8-|Na union Nb|+2eps_b and its analogue;
the blue bc sum yields tb+tc+|Nb intersection Nc|<=2(eps_b+eps_c).
If ta<=1, both other flags vanish, forcing tb=tc=0 and contradicting
a red sum. Hence ta=2. Exclusivity then gives
tb=2eps_b,tc=2eps_c with disjoint attachments. Either nonzero one
creates a positive matching W² entry. Thus both vanish, and A is the
only core, with matching links to the remaining six.

For disjoint red edges ab,cd, each red sum is
9-g_ab-|Na union Nb|+2(eps_a+eps_b); g counts distinct opposite
active blue neighbors, not the number of blue edges.
A blue active pair gives ti+tj+|Ni intersection Nj|<=1+2(eps_i+eps_j).
A double attachment forces eps_i=1 and active blue degree<=1;
a positive matching W² entry then forces that degree to be zero.
Conversely eps_i=1 requires a double attachment: otherwise its red
sum would force its mate also to have flag one, violating the pair's
inside-flag bound. The double-attachment alternative consequently forces
its mate to attach once and be blue to both opposite endpoints;
their blue budgets force no low attachments on the opposite red edge,
contradicting its red sum. All active flags are zero and all sizes<=1.

Neither g can be zero. If one is one, both its endpoints must attach
to distinct low vertices; the opposite matching-square requirements
force both into a single size-one attachment at their opposite red mate,
impossible. Thus both g values are two. The active blue graph is a
spanning K2,2 subgraph: a matching, a three-edge path, or all four edges.
Both red edges need an attachment, and a blue edge cannot join two
attached endpoints. This excludes four active blue edges. The two
remaining graph types have exactly one attached endpoint in each red
edge, forming a cross nonedge. Positive matching W² terms force their
low neighbors to be the same singleton. The blue active-to-low budget
10+(r_k-1)+4-2eps_k<=12 forces clique size1 and eps_k=1.
These are exactly B and the author's C=B+blue12.
Swapping labels0 and1 identifies C with the X pattern in our proof.

Every step is a complete elementary case implication. No enumeration
or external graph catalogue is a mathematical premise of that
classification. All other low clique components remain allowed.

For each surviving core, put C=S_H,H and D=diag(u_h) on the six-orbit
complement. The common T=C+D is symmetric and has the exact corrected
row action in PROOF.md. Ignoring the diagonal would invalidate the
matching-only action when outside uniform links occur. A contradicts
linearity; B forces paired inner products-2 and+2 for a symmetric T;
X forces balanced six-sign vectors to be orthogonal. The same correction
works for arbitrary complement colors, without low-clique hypotheses.
This proves the explicit broader core criterion and independently
confirms the author's full-density conclusion.

## Exact source reproduction and genuinely independent checks

The complete new author portable replay passed: 642,323 normalized
quotient patterns, 198 necessary survivors and 7,341 inside assignments.
Both author algorithms agreed on every survivor and inside flag, not
only totals. The replay took 29.7555 s, peak child RSS 17,452 KiB.
Its literal controls cover 336 deterministic full-size lifts, 61,760
matching-spine checks, 6,080 uniform sum/difference checks and 10,080
diagonal-shift checks. These sampled lifts test identities and may
violate the book caps; they are not exhaustive signing certificates.

The complete original replay also passed: 3,858,660 patterns, 56
survivors and 3,584 assignments, plus original vector and large literal
formula controls;52.2436s/100,876KiB. Both replays are attributed to the
author, rather than described as reviewer-written algorithms.

Our separate [audit.py](audit.py) imports no author or campaign
executable. A full matrix-based C++ census and set/intersection Python
census enumerate all 5,739,370 normalized seven-uniform/two-red
choices without the author's low-clique reduction. Every one of 868
survivors and 42,112 inside assignments agrees between both and a
direct template-image checker. All three surviving shapes are excluded
analytically. This is an independent complete boundary proof, not a
reviewer-written census of the whole arbitrary-density domain.

The checker also compares 6,144 literal degree/page/difference identities
on all 512 three-orbit lifts, all 720 A row tuples, 90 B row pairs, exact
balanced-six parity, the four-unit B symmetry discrepancy and a
matching-only squared-trace shortage. Four altered formula/entry
certificates reject. Normal and optimized checks pass; the full C++
census also passes address/undefined sanitizers with every record
matching the release build. Normal/-O timings are 7.691/7.162s,
peak child RSS 91,980 KiB; sanitized full census4.965s/146,152KiB.

This focused computation supports an independently written local proof
and boundary reduction. The all-density completeness verdict rests on
the fully inspected analytic attachment/case argument, not on pretending
our boundary code covers every blue density.

## Attribution, dependencies and trust

The all-density three-red theorem, its low-clique/attachment reduction
and full-density source belong to six-books-2 at h7966. The earlier
zero/one-red/seven-total proof is h7914, ref
bafkreifn2ikm7lrucpramztb7nvhxzugua3isgyopjjhjoyl56irwcyvtm.
The four-blue theorem and short matching-only Gram mechanism are
credited to six-reviewer-1 at h7958, source
c266cf457da921aef1f0648f792d77304f7286ac. Its complete ordinary
four-blue proof was inspected; its executable was not replayed here.
The exact three-red/four-blue corollary is already stated by h7966 with
that dependency and is not claimed as new reviewer research.

The diagonal correction and seven-pair consequence were independently
derived here, but the concurrent author also supplies them in its broader
theorem. They are now independent confirmation. The explicit arbitrary
complement criterion allows red uniform and nonclique complement
patterns beyond the two-red normal forms. It is a proved extraction and
generalization of the local reasoning, with no historical-priority claim.

[provenance.json](provenance.json) pins the complete 15-file new target
and the concurrent review source, while preserving the older source
commit attribution. Neither a full-degree theorem, 112-edge cut, solver
verdict, finite-profile interpolation nor external spectral catalogue
is a premise. The trust boundary is ordinary written page counting,
case coverage, legal switches, integer parity and real linear algebra,
with CPython/g++ exact computation for the scoped reproduction.
No proof-assistant formalization is asserted.

The unrestricted located interval remains 22..23. Existence of a free
involution is a hypothesis, not a reduction for arbitrary colorings.
No full matching-sign or all 22-coloring enumeration, valid 22 construction,
all-involution exclusion or eight-uniform lower bound follows.
Realizability of three-red/four-blue seven-pair patterns remains open.

## Primary literature and readiness

[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/html/2407.07285v2),
Table 1, and [Radziszowski DS1.18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, retain the located 22..23 interval.
Section 3.3 of the first paper and
[Wesley's Section 3](https://arxiv.org/html/2410.03625v2) establish the
classical polycirculant/block-circulant framework. These primary sources
were refreshed live. Candidate-specific primary searches found no
matching uniform-pair theorem; this is bounded search evidence, not
historical priority. The linear-algebra tools are classical.

The complete ordinary proof and compact reproducible arithmetic evidence
are ready for further referee inspection. Confirmation, a quantified
local refinement and publication readiness are distinct conclusions;
there is no journal-acceptance or formalization claim.

## Strengthening and improvement opportunities

**Proved criterion:** arbitrary complement colors are permitted in the
three local exclusions, including extra red uniform blocks. The common
diagonal correction preserves every active row action. These are
concrete candidate cuts for higher-red-density quotient patterns.
The three-red/four-blue global seven-pair profile is confirmed with
the author's and concurrent reviewer's stated attribution.

**Next consequential work:** classify the remaining seven-pair
three-red/four-blue quotients and apply these core cuts before enumerating
signs. A general case need not contain one of the three cores or have
matching links to all six remaining orbits. A complete reduction or exact
witness is required; no unconditional eight-pair bound is supported here.

**Certification:** formalize orbit decoding, legal switching, attachment
capacities and the common diagonal correction. A finite enumeration
bridge can separately certify the independent boundary census.
Extending to other vertex/book parameters requires new page budgets,
complement lengths and parity; balanced-six parity is essential here.
