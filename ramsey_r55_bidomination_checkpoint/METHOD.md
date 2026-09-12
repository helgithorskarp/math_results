# Pass 38: domination as a new structural feasibility test

This pass follows the renewed structural-feasibility mandate. It does not extend the parked core-exchange, monotone-chain, packing, rank, separator, or edge-window programs. Its success criterion is a genuine exclusion, not a reduced workload.

## Complete finite target

Let a good graph have no clique and no independent set of size five. The tested statement is:

> Every good graph of order 43 has a dominating set of at most three vertices in at least one of its two colors.

Equivalently, the complete class of good43 graphs with domination number four in both colors is empty. The class is defined without automorphism, catalog member, packing size, prescribed degree sequence, or chosen local profile. A proof would exclude that entire intrinsic class. It would not by itself settle R(5,5), and there is no demonstrated short route from that proposed theorem to the remaining graphs.

The broader preliminary hope of forcing a dominating triple in each color lacks even order-42 support: the 328 supplied McKay graphs and their complements contain 328 colorings without a dominating triple. They are controls, not a complete order-42 census. Their incomplete catalog cannot be used to decide good43.

## Elementary equivalence and full encoding

A set T dominates G exactly when every vertex outside T has a neighbor in T. Thus T fails to dominate G exactly when there is a vertex outside T adjacent to all of T in the complement. Any dominating set of size at most three extends to a dominating triple when n>=3. Consequently gamma(G)>=4 if and only if every triple has a common neighbor in the complement. Applying the statement to both colors gives the encoding below. Also gamma(G)<=alpha(G)<=4 in a good graph, since every maximal independent set is dominating.

The common-neighbor property itself guarantees a red K4. Any clique of size less than four can be enlarged: include its vertices in any triple, then take a common red neighbor of that triple. Starting with a vertex and repeating gives a red K4. Thus relabeling a red K4 onto vertices 0,1,2,3 is valid. No symmetry of the graph is assumed. This is the only label restriction. The new complete-class bridge uses no catalog or numerical Ramsey result, including R(4,5)=25.

There are binomial(n,2) physical edge variables, ordered lexicographically on unordered pairs; positive means red. For every five-set S include both the disjunction of its ten edge variables and the disjunction of their negatives. For each triple T, color c, and vertex w outside T, introduce y(c,T,w). Add y -> c(uw) for each u in T and add the disjunction of all y(c,T,w) over w. No reverse definition is needed: a witness can be set true precisely for an actual common neighbor.

A graph in the tested class, relabeled at a red K4, satisfies the clauses by setting witness variables to true for actual common neighbors. Conversely, any model gives a literal good graph and a common neighbor in each color for every triple. Thus the SAT problem is exactly the entire class, modulo the harmless choice of the first red K4.

For n=43 this gives 903 physical variables, 988183 total variables, 4911724 clauses, and a 137301312-byte DIMACS file. Its SHA256 is 80d71dc1901166572cfe2864be91e48f026afc16e0eaedf83e92db3f07a9cb27.

## Structural consequences explored

In either color of a graph in the tested class, every triangle extends to a K4, every edge extends to a K4, and every vertex belongs to a K4. For an edge uv, the common-neighbor graph S is triangle-free (otherwise uv and a triangle form a K5), has independence number at most four, and is a total dominating set of the entire graph: for any x distinct from u,v, use a common neighbor of the triple u,v,x. For x=u or v, use any vertex of S. In particular S has no isolated vertices. Both the clique and independence complexes are pure of dimension three.

These are necessary consequences, not a new feasibility theorem. They leave the incidences between different edge links unresolved. No proof was found that they force regularity, a bounded list of graphs, or an order bound below 43. Regularity, full three-existential closure, and completeness of the known order-42 catalog are not assumed.

## Controls and trust model

The primary approach is combinatorial (domination and simultaneous link constraints). Symbolic certificates are the auxiliary closure/validation method. The concrete tools are Python research code, a proof-producing SAT solver, and a bounded compute run.

The explicit quadratic-residue graphs on 29 and 37 vertices are positive controls only. The program relabels a red K4 first and extends their physical assignments to the witness variables. Every generated clause is evaluated: 814848 clauses at order29 and 2472420 at order37. Negative controls separately detect 410 forbidden five-sets in the order-41 quadratic-residue graph and 1250 domination failures in C5[C5] of order25. Closed-neighborhood union checks agree with generated clause failures. This verifies nonvacuity and exercises the full generator; it is not an independent review of the mathematical bridge or a completeness result about any symmetric family.

The separate supplied order-42 catalog diagnostic evaluates every dominating triple in both colors of each record. No bounded census is extrapolated to good43.

A SAT answer would require direct validation of the 43-vertex graph. An UNSAT answer would require an independently checked complete proof trace. An interrupted/UNKNOWN trace proves no exclusion. No parent carrier task is retired by merely constructing this formula.

## Literature and overlap

The pass-start committed graph snapshot was height4363, with 2207 contributions and 10837 relations. The direct R(5,5) neighborhood and exact relevant source/review bodies were inspected. The module resilience theorem already covers the initially considered module/twin direction; it is not reused as a new result. No domination-class closure was located in the inspected neighborhood or repository.

Primary background: Angeltveit and McKay, R(5,5)<=46, arXiv:2409.15709 and Journal of Graph Theory DOI10.1002/jgt.70029; Angeltveit and McKay, R(5,5)<=48, arXiv:1703.08768, for the completed R(4,5) extremal catalog; McKay's Ramsey data page https://users.cecs.anu.edu.au/~bdm/data/ramsey.html for the explicitly incomplete order-42 collection.

The newer Angeltveit preprint arXiv:2602.11459, R(K5,K5-e)=30, was inspected as a possible new external input. Its direct consequence that every thirty-set of a good43 contains an induced K5-e in each color supplies a hereditary necessary condition, not a new closure. It was not inserted into the proof attempt. Its introductory statement R(4,5)=24 is a typographical error and is not a premise here.

## Gate

The first milestone is met only by a proved exclusion of this complete class or another genuinely new unrestricted feasibility theorem. A formula, a timeout, the control census, the elementary equivalence, or the link observations do not meet it. At the boundary record the actual solver result and gate verdict. There is no automatic enlargement of the compute limit, no queue handoff, and no permission to count any original task as closed without a proof.

## Actual boundary outcome

CaDiCaL returned UNKNOWN after900.474138seconds, exit0. The unfinished binary DRAT trace has191874073bytes and SHA2564a294511853a5800e8740c5364c2ca6bac23b0295143e146bca56ec538b4de1a. There is no checked refutation and no SAT graph. The complete class is unresolved; the first gate is not met. No original task or physical family is reported closed. The graph remained unchanged at height4363. No graph submission or pending-transaction resubmission is made.
