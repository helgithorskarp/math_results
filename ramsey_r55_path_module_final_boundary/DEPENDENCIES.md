# Sources, accepted inputs, and trust boundaries

## Campaign inputs

At the start of pass 43 the committed index was unchanged at height 4363,
with 2207 contributions and 10837 relations. Exact contribution bodies and
their relation neighbourhoods were retrieved again. The required results
and independent acceptances are:

| Result | Contribution | Acceptance |
|---|---|---|
| Module resilience at induced orders 36 and 28 | h3579, `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku` | h3583, `bafkreigpgiwq63wwv445jjf4r75pn7ajlajtivdzshhof25jr6wu3kj6eu` |
| Every 26-set contains P5 or complement-P5 | h3931, `bafkreif2yr3qvnkolxmmzy44ntigchjluornje6majm63gjsmj2z3c2wd4` | h3935, `bafkreidbusopqwbjovyrozgmhaxqje7di5ortnr5lb4bz2imnjtks2ib4m` |
| Every colour-neighbourhood 18-set contains a P5 of that colour | h4015, `bafkreie24uooup5ktzr2yzojueosytukexykqxnr4yjmrjcpy6xzd7y5fy` | h4019, `bafkreialkzex2jcgh436iycexftu4qh5yinulxbauune53ipb77phm5mli` |

Their source directories are [module resilience](../ramsey_r55_module_resilience),
[the hereditary core bound](../ramsey_r55_path_complement_core_exclusion),
and [neighbourhood path forcing](../ramsey_r55_one_sided_induced_path).
Source commits are respectively `823d258fe6dfa33a695e148bbed08b1709fbe3c9`,
`e7d5932b57e804bf1f2dcb00f89360af0f76fa2e`, and
`687178a20b787b5b53fba3ba90380b8e94063bee`.

The neighbourhood theorem remains conditional on the imported
computer-assisted critical-graph classification, Theorem 7 of Cameron,
Goedgebeur, Huang and Shi,
[k-Critical Graphs in P5-Free Graphs](https://arxiv.org/html/2005.03441),
arXiv:2005.03441, published in Theoretical Computer Science 864 (2021),
80–91. Neither the original campaign contribution nor its acceptance
replayed classification completeness. This final pass does not remove
that boundary. The older global inputs also retain classical small
Ramsey bounds, Fouquet's theorem, and SPGT as stated in their sources.

These accepted results motivate the failed order-43 approach. The
auxiliary probability proposition does not rely on them: its proof
starts directly from independent fair physical edges. In particular it
does not extend the imported critical-graph classification to other
clique numbers.

## Primary literature and prior-art limits

The first-moment Ramsey argument is classical:
Paul Erdős, [Some remarks on the theory of graphs](https://users.renyi.hu/~p_erdos/1947-09.pdf),
Bulletin of the American Mathematical Society 53 (1947), 292–294,
Theorem I. The original page was inspected, including its counting
argument. Its Ramsey lower bound is prior art and is not improved here.

The core-decomposition investigation consulted Chudnovsky, Esperet,
Lemoine, Maceli, Maffray and Penev,
[Graphs with no induced five-vertex path or antipath](https://iuuk.mff.cuni.cz/~ipenev/P5P5b-revised.pdf),
author manuscript dated November 30, 2015; Journal of Graph Theory 84
(2017), 221–232. Its substitution and split-unification description
concerns graphs globally avoiding the two patterns. It provides no
unrestricted join for a path-free induced core with an arbitrary
complement, nor a theorem that path-hypergraph components are modules.
No such extension is imported or claimed.

The binomial concentration, special Turán bound, and full-module union
argument needed in the auxiliary proposition are proved in PROOF.md.
They are elementary uses of standard probabilistic and extremal methods.
No novelty or separate paper-scale publication claim is made for their
combination or the deliberately loose constants.

## Provenance and validation scope

The prior complete control remains at source commit
`168f17bd7143c9d8750563ed639ec543b7a644bb` in
[the first-pass directory](../ramsey_r55_path_module_coexistence_boundary).
Its graph, 5,682,520-byte path certificate, separate module algorithms,
hashes and archive are preserved. Nothing from that computation is rerun
or used to infer actual Ramsey avoidance.

The latest full principal report read at intake is
`20260913T033427.227520Z.md`; its R2 supplement is
`20260913T034148.811875Z.md`. The orchestrator frontier was also read.
The new full report `20260913T055237.818000Z.md` was read at the publication
boundary; it preserves the final pass and requires reassignment on a miss.
The accepted assignment and final gate are unchanged. Source-published
but uncommitted/unreviewed R2, R3 or R4 results are not accepted premises.

The new controls use exact Python integers and fractions. Their role is
to check the probability constants and finite path definitions, not to
certify a literal graph or replace the all-parameter proof. The written
probabilistic argument, ordinary mathematical inference, Python runtime,
hashing, OS and hardware remain trust boundaries. There is no external
peer review, proof-assistant formalization, solver certificate, numerical
approximation in a decision, catalogue input or generated large graph.

No Discovery Net contribution is submitted for this failed trial. All
pending identifiers remain untouched and are not resubmitted. Earlier
order-44, good43 structural, critical-graph, Property B and order-54
programs remain parked. No other researcher's queue or preserved
computation was operated, and the historical workspace was not changed.
