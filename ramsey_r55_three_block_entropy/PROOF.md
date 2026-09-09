# A three-block projection bound removes at least 74.4525% of the remaining carrier

This is a computer-assisted upper bound for a **complete, globally covering family of labelled 43-vertex colorings**. It refines h4059's exact bare carrier. The new family's cardinality is not counted exactly: a rigorously rounded entropy bound proves that at least 74.45253502733943318485884821636544217895...% of the old carrier is excluded. No complete task is decided and no good43 graph is produced.

## One declared family and gate

Use precisely the complete h4059 bare carrier, including its q7, q8, q9, and q10 classes. Its 18 classes contain 2,189,178 task IDs. The ordinary non-root block matrices have the original h3887/h3835 pair domains. The q8/q9 augmentation restriction is exactly h4035's; h4059's joint block/core contacts apply exactly as previously defined. The root-block multiset ordering keeps ties. No h4029 degree bound or optional composite upper envelope is multiplied into the present count.

For every three distinct **non-root** four-clique blocks, forbid every monochromatic five-set with three vertices in one of the blocks and one in each of the other two. This is the entire new restriction. Root-bearing triples, 2+2+1 splits, and larger block tuples are outside this milestone.

Every forbidden set is an actual physical monochromatic K5. Hence any good43 represented in h4059 remains represented in the new family. The global coverage theorem is inherited, and the new restriction is a literal Ramsey consequence inside each old task. The gate in `GATE.json`, declared before the count, requires a rigorously certified new global upper bound at most three quarters of the h4059 bare count, independent complete local counts, and literal physical checking. All requirements are met.

## Ordinary matrix coordinates

A physical cross-matrix has bit 4i+j equal to the red edge between row vertex i and column vertex j. For two red four-cliques the R(5,5) domain consists exactly of the matrices with no all-one row or column, no two rows having three common ones, and no two columns having three common ones. These are the four possible red K5 splits across the two blocks. A blue K5 is impossible because two vertices from either block have a red internal edge. There are 37,823 such matrices.

For a red block and blue block, only the red 4+1 and blue 1+4 splits are possible. Thus no column is all one and no row is all zero. This gives 35,714 matrices. The blue/blue domain is the color complement of red/red. Reversing block order transposes the domain. All these identities are checked against every state of the pinned original palette bitmaps; this includes the red/blue versus blue/red orientation.

For a fixed task, the ordinary non-root matrices are mutually independent uniform coordinates under its uniform bare-carrier measure. The fixed core, ordered root matrices, and block/core contact choices do not constrain these coordinates. The selected augmentation clauses and h4059 contact conditions involve only block/core edges. Consequently a bound on the ordinary-matrix fraction multiplies the exact h4059 count for that task. This factorization holds separately for every admissible fixed core/root/contact choice.

This statement does not justify applying the same multiplier after fixing arbitrary non-root matrix entries, imposing degrees, or conditioning on a solver's surviving assignments.

## Complete centred-triple count

Normalize the centre block to red by complementing all colors if necessary. Let A and B be the matrices from its four vertices to the other two blocks, and C the matrix between those blocks, in that order. Each outside column of A or B has at most three red neighbours in the centre: four would already violate its pair domain.

Assign a column type 0 if it has at most two red neighbours, and type i+1 if its three red neighbours omit centre row i. There are five possibilities per column. For two outside vertices, a centre-red 3+1+1 K5 occurs exactly when their nonzero types agree and their joining C-edge is red. Thus the allowed C matrices have zeros in the forced mask

    F(t,u) = { (j,k) : t_j = u_k != 0 }.

Let h_R(t), h_B(t) count the A-matrices of type pattern t when its outside block is red or blue. These histograms have respectively 209 and 621 nonzero entries. For a C-domain D, let Z_D(M) count its matrices whose set of red positions is contained in M. A 16-bit subset sum computes this table exactly. The centred event count is

    sum_(t,u) h_left(t) h_right(u) Z_D(complement F(t,u)).

There are three cases, up to color complementation and interchange of the two outside blocks:

| Centre relative to its triple | Allowed | Total |
| --- | ---: | ---: |
| All three blocks have the same color | 50,076,756,774,655 | 54,108,801,960,767 |
| Centre belongs to the majority color | 42,206,573,324,092 | 48,242,850,554,108 |
| Centre belongs to the minority color | 38,488,830,004,364 | 48,242,850,554,108 |

Call the three ratios p_S, p_M, p_N. These are exact counts of complete three-matrix assignments. The three denominators sum to 150,594,503,068,983 indexed assignments. No symmetry quotient, orbit representative, graph seed, or random sample is used. The five column types summarize the required physical triples, while every labelled matrix retains its full multiplicity.

### Independent decomposition

The Python producer conditions on the type patterns of A and B, then counts C via subset sums of **physical edge masks**.

The independent C++ checker first enumerates all 196,608 pair assignments for the three color cases by testing all literal five-subsets of the eight physical vertices. It then conditions on a type pattern of A and on each individual physical C matrix. A column of B may use type 0 or any centre triple not joined by a red C-edge to an A-column of the same type. A separate subset sum over **permissions for B-column types** counts the admissible B matrices.

These conditionings agree on all 830 histogram entries, all 1,039 per-A-pattern completion profiles, and all three totals. The independent computation visits 38,857,316 conditioned cases. The original pair-domain bitmaps agree on all 111,360 states in the three counted domains; transpose and color-complement identities are audited over all four ordered color cases. Nine corrupt numerical/cover certificates are rejected.

## Projection inequality, proved directly

Let the finite independent coordinate domains be D_e, one for each unordered pair of non-root blocks. Each centred event E_t depends on the three coordinates of its block triangle. Let A be the set of assignments passing every event. If A is empty the desired bound is immediate. Otherwise choose Y uniformly from A.

Order the coordinates. The chain rule gives

    H(Y_S) = sum_(e in S) H(Y_e | Y_(earlier coordinates in S))
           >= sum_(e in S) H(Y_e | Y_(all earlier coordinates)).

The inequality is the elementary fact that conditioning cannot increase entropy. If every coordinate occurs in exactly k of the subsets S_t, summing gives

    k H(Y) <= sum_t H(Y_(S_t)) <= sum_t log |E_t|.

Here H(Y)=log |A|, and each projection is supported in its local allowed event set E_t. Also each domain size occurs exactly k times in the product of the local product-space sizes. Subtracting the corresponding logarithms and exponentiating proves

    |A| / product_e |D_e| <= product_t Pr(E_t)^(1/k).

This standard entropy projection inequality is not claimed new. The exact local probabilities and their quantified use on the complete current Ramsey carrier are the new computation.

## Apply to every class

For class (q,r), put m=q-1, a=r-1, b=q-r. Among the non-root block triples let

    U = binom(a,3) + binom(b,3),
    V = binom(m,3) - U.

There are three same-color centred events for each uniform triple. Each mixed triple has two majority-centre events and one minority-centre event. Every ordinary matrix coordinate occurs in exactly

    k = 3(m-2) = 3(q-3)

events: choose its third block, then its centre in three ways. Therefore the retained ordinary-matrix fraction is at most

    beta(q,r) = [p_S^(3U) p_M^(2V) p_N^V]^(1/k).

`global_bound.py` rounds each beta **upward** to the least multiple of 10^-18 satisfying the integer power inequality. No floating-point inference is used. `verify.py` independently lists every centred event in all 18 classes, counts every coordinate occurrence, identifies the color case, checks the power inequalities by exact fractions, and checks the weighted sum against the h4059 class counts. This covers 2,952 abstract centred events and 8,856 coordinate incidences across the 18 class schemas; each schema applies to all its core records.

The exact rational certificate in `EXPECTED.json` yields:

- Removed fraction of the entire h4059 bare carrier: **at least 0.7445253502733943318485884821636544217895...**.
- Removed fraction in every single task carrier: **at least 0.321044393298405427**.
- Affected task IDs: **all 2,189,178**, with **zero new task verdicts**.

The global percentage is a lower bound on removal, not an exact count of the refined family. Positive upper bounds do not establish feasibility of individual tasks. Correlations between different centred events are accounted for by the projection inequality; their probabilities are not multiplied as if the events were independent.

## Physical witness interface and controls

`physical.py` takes a complete graph in the existing 903-edge red-bit representation and scans only the declared non-root three-block patterns. It returns a physical five-set and its block split if one exists. The independent checker verifies all ten edge colors, all five vertex labels, and occupancy 3+1+1. A pass is only a pass of this filter; all other Ramsey and maximality requirements remain.

A complete 900-case primitive truth table checks both centre colors, both possible closing-edge colors, and every pair of proper column masks by literal five-set evaluation.

Physical tests use only the three public h4059 q9 fixtures. Their ordinary non-root matrices are replaced by a fixed matrix with two red and two blue entries in every row and column. Such a matrix lies in every applicable pair palette and has no centre-color triple column. All other physical coordinates remain byte-for-byte unchanged, so h4059 membership is preserved. An independent full five-subset scan verifies the absence of all 10,752 declared patterns in each of the three resulting control graphs.

For each control, every non-root centre, every pair of other non-root blocks, and every centre triple are tested with all four choices of outside vertices that require only one added centre-color neighbour per affected star. The closing edge is given the centre color. This gives **8,064 indexed mutation tests** (6,048 red and 2,016 blue), not a claim of 8,064 distinct graphs. Every affected pair palette is rechecked by literal eight-vertex five-set enumeration. Every mutation yields a correct physical witness. There are 24,276 complete pair-palette checks, and six corrupt physical inputs/witnesses are rejected.

These are controlled interface tests, not candidate-search results. Every mutation has an explicitly verified red K5 on five of the eight first non-root vertices. The positive controls also have a red K5 using one such vertex in each of five blocks; their defects use a split outside the present filter. No test fixture is a good43.

## Trust, ownership, and stopping boundary

The global cover and exact parent counts are imported from h4059, h3887, and their earlier dependencies, including the large R(4,4) catalogue completeness assumptions. The original pair palettes are pinned separately. This pass downloads no graph data and does not recompute h4059, h4045, or any earlier carrier census.

The independent h4067 review accepts the h4059 parent conditional on its imported cover, packing bridge, and catalogue completeness. Its warning about dependent marginal bounds is addressed here by the explicit separation of ordinary non-root matrix coordinates from all parent contact coordinates; no degree, maximality, or color-orientation multiplier is introduced. The review is context and validation of the parent, not an independent review of this new theorem.

The finite counts rely on Python/C++ integer and bit semantics, SHA256, compiler/interpreter execution, and the supplied source. Strict release and address/undefined-sanitized C++ runs agree; Python checks run normally and with assertions disabled. The entropy argument is mathematical, not proof-assistant formalized. No solver answer or heuristic search is trusted, and no historical priority is claimed.

The numerical fraction is not a conditional bound on team-r55-1's 161 q10 children. No child input or physical child prefix is inspected. The h3987 ledger stays 99 certified closures/161 UNKNOWN under its existing ownership. The later h4063 color-orientation queue retains 67 active children and redirects 94; those redirects are not UNSAT. The present baseline is explicitly the un-oriented h4059 bare carrier, not the orientation-conditioned queue. No multiplier is applied to that queue. Separately, h4001 stays 518 q7-r5 exclusions/122 UNKNOWN, leaving 2,188,660 whole task IDs undecided. The present restriction was already implicit in the full Ramsey CNF; no solver acceleration is claimed.

This completes the single predeclared milestone. It does not begin a root-triple, 2+2+1, larger-tuple, degree, matching, or alternate-cover extension.
