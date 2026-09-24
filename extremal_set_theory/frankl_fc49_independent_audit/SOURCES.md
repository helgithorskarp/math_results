# Sources and provenance

1. Mingchang Liu, *Frankl-complete configurations and Morris's asymptotic
   conjecture*, September 2026, V2,
   [Zenodo record](https://zenodo.org/records/22734469).
   Sections 6.1–6.6 contain the finite classification and lexicographic
   counterexample. The compact witness here changes the outside-coordinate
   construction of Section 6.1. No verification of the asymptotic part is claimed.
2. Liu's V1 computational source,
   [repository](https://github.com/michaeliu4/frankl-complete-four-sets),
   [release V1](https://github.com/michaeliu4/frankl-complete-four-sets/releases/tag/V1).
   Pinned and replayed commit: `17002022f9bb033fb6b40e7b5d1484e78ceb0ac2`.
   The complete tracked source is about 104 MB and is an external input.
   `lex_positive.tree` is copied byte-for-byte from `lexicographic/positive.tree`;
   the original MIT license is retained in `UPSTREAM_LICENSE`.
3. J. Pulaj and K. Wood, *Local Configurations in Union-Closed Families*,
   [arXiv:2301.01331v2](https://arxiv.org/abs/2301.01331v2).
   Conjecture 1 is the lexicographic claim refuted by the exhibited families.
   The published finite bounds motivate the original graph frontier.
4. [OR-Tools maximum-flow documentation](https://developers.google.com/optimization/flow/maxflow).
   OR-Tools 9.15.6755 is used only to generate candidate flows whose capacity,
   conservation, and value are checked separately with Python integers.
5. [DRAT-trim](https://github.com/marijnheule/drat-trim), pinned commit
   `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, is used for optional SAT proof
   extraction. The strict RUP checker is reused without changes from this
   repository's `combinatorial_topology/charney_davis_18_vertex_certificate/strict_rup.py`.
   The legacy `lrat-check.c` shipped with DRAT-trim is not a trust anchor here.

The graph source was the existing **Uniform Frankl-Complete Threshold FC(k,n)**
problem (`bafkreiasmhcmcvlmeqhqay7r7rmenhtk5ir7ktqrzqckgaxrsecw2vytk4`),
whose recorded 14–21 frontier led to the primary-literature check. The existing
lex conjecture is `bafkreifyuovkqprostxxx7i2bumahsh5pci2nhiiw32yyxju6xswuitlne`.
The external result was found during that check, rather than through another
researcher's active lane. Mathematical priority for FC(4,9)=16 and the
lexicographic refutation is not claimed by this reproduction.
