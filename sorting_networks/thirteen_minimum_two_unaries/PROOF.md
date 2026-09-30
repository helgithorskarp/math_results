# R137 minimum kernels require two unary events

Author: **six-sorting-1, researcher**. This is a conditional computer-assisted structural theorem, not external-person review or proof-assistant formalization.

## Exact conditional theorem

Every standard 18-comparator sorter of the specified 137-state ten-wire
target R has at least two unary events in its minimum kernel. Thus its
minimum kernel has four or five gates. The global thirteen-input size
interval remains 44..45, and R remains 18..19. No arbitrary thirteen-wire
prefix, or unary-maximum Y20 class, is excluded by this theorem.

R is the common Boolean image after either literal P26=P21;Tj;(6,9);(9,10),
projected to wires0..9. Both prefixes fix the largest three values on10..12.
The exact input packet is the R137 field of the remotely verified source
[fixture.json](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_minimum_preparations/fixture.json).
The independently executed scalar19 control sorts every137 row and all
8192 original inputs for each P26. R18 would produce a44 full sorter;
R17 contradicts the established global lower bound44.

## Necessary conditions and their provenance

Use the standard zero-one principle, marked-input pruning, and ordinary
sorting sizes S9=25, S11=35, S12=39, S13>=44. The exact live primary sources
are [Harder](https://arxiv.org/abs/2012.04400v3),
[Codish et al.](https://arxiv.org/abs/1405.5754v3), and the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html).
These literature theorems and the written pruning/standardization bridge
are imports; their original large proof corpora were not rerun.

The committed earlier theorem7494 gives exactly two passages of the
single-zero input at wire1 in a Y20 completion. The two B gates avoid that
zero, and R18 is a Y20 subclass, so the same equality holds for R18.
That result is [minimum-once closure](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_once_closure),
graph `bafkreibd7xjljyxowbj3ly35iccehent53fkktliol35knttxsgblu56wu`.
It is not rerun here. The necessary leaf passage capacities at0,1,5 are
3,2,3. The independent checker rederives these from the original one-zero
inputs and S12=39. Stationary passages count.

The R single-one row512 is stationary on9. The original marked-input
capacities imply at most one suffix passage for that row, so at most one
gate uses9. Row256 must move from8 to9; consequently the unique9 gate is
(8,9). The independent checker derives the cap1 directly from all16384
original threshold inputs and verifies that both rows are present in R.

For two original minima, both P26 prefixes give the same strongest profile
F={(3,5),(6,5),(10,5),(17,4),(33,4),(34,5),(130,5),(257,4)}. A pair mask
marks the two zeros, and D counts deleted original prefix gates. Keep the
largest D in each fiber. The checker rederives this profile directly from
both sets of78 original zero pairs. Its weight is208.

At a comparator a fiber has at most two preimages. Every two-preimage
fiber deletes that comparator for both preimages, so its new weight is
2^(max(D1,D2)+1)>=2^D1+2^D2. A singleton never decreases weight. Thus
W(F)=sum2^D is monotone. At a sorted full44 output both minima occupy0/1,
and S11=35 implies final D<=9. Hence every prefix of a hypothetical R18
completion has W<=512. This statement needs no minimum-root timing bound.

## Complete one-unary class and finite coverage

Follow the three single-zero input rows separately, initially at0,1,5.
A kernel event touches at least one currently occupied zero port. It is
binary when it touches two distinct occupied ports, and unary when it
touches exactly one. A nongate avoids every currently occupied port.
There are exactly two binary merges before all three trajectories meet0.
No gate on the extracted global minimum can occur afterward: it would
be redundant on the reachable full13 image, giving a43 sorter after
removal. This uses S13>=44, not an imposed normalization.

With one unary there are exactly three kernel events. Applying all45
standard pairs to the three scalar one-zero rows, with capacities3/2/3
and passage1 exactly2, gives exactly59 kernel words. The independent
enumerator uses three complete Boolean rows, whereas discovery uses
positions and route counts. Their literal catalogues agree entry by entry.
Eight words contain a9 gate other than(8,9), and are impossible by the
sole9-gate condition. The other51 require closure computation.

For a selected word use state(phase,max_used,F). Phase is the number of
its three kernel events already used; max_used records whether(8,9)
has occurred. Admit the next selected kernel event, or any of the45
pairs avoiding the currently occupied minimum ports. Reject a9 gate
unless it is the first(8,9), and reject only profiles with W>512.
Accept at phase3. There is no limit on nongates, word length, root
position or depth. Repetitions and zero-cost cycles are included and
closed by state equality. This is a necessary relaxation, not a
classification of full R images: equal marker profiles may hide different
actual Boolean images. An empty complete closure suffices for exclusion.

The public scalar checker closes all51 finite state sets by scalar
two-zero transition tables, inverse fibers and DFS. It uses **no
preparation counter or three-preparation premise**. Therefore it proves
the quantified class even without the extra necessary conditions used
by the discovery BFS. All51 have no terminal. The compact certificate
JSON records each case's counts and canonical state hash, rather than
publishing a large state corpus.

The two q1=2 binary-only words are (0,1);(0,5) and (1,5);(0,1). Nongates
avoid their occupied binary endpoints, allowing both binary events to
commute to the front. Their resulting weights768 and704 are independently
recomputed and exceed512. The third binary word has q1=1 and is already
excluded by7494. Thus zero and one unary are both impossible. Two binary
merges charge at least five total leaf passages, while the three capacities
sum to eight. Each unary charges at least one, so at most three unaries
are possible: the surviving counts are exactly two or three.

## Certificate and independently checked coverage

The certificate has exactly59 literal words:51 complete empty closures and8
forbidden9 words. Both public algorithms reproduce the same51 state sets,
canonical hashes and all21793023 transition counts, totaling932386 states.
The largest individual closure has30454 states, below the existing50000
operational cap. BFS uses bitwise zero transport and direct maximum-D
aggregation. DFS independently evolves scalar two-zero rows and joins
inverse fibers. Their route catalogues use positions and complete scalar
one-zero rows respectively. The common driver handles only expected-output
comparison and local batching, not comparator mathematics. Matching output
supports the computation; the preceding completeness arguments remain
necessary proof boundaries.

Each public command has a45-second batch budget and stores only compact
completed-case progress under ignored scratch/. Resume as documented in
README. A timeout or incomplete batch is not exclusion. Final output must
say all_cases_complete with59 completed_cases. No full state corpus, CNF,
solver trace or external native dependency is needed.

The earlier preparation theorem, graph7520,
bafkreigyaqrbbipjtn2yuxzx4uyk2orchreoapypuqr3vvjdvqlvrpylai,
is source301e2c28b9db4c0bc1f41504a6d4cc334f60d3ba at
[thirteen_minimum_preparations](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_preparations).
Combining its three-preparation bound with this new two-unary result gives
a useful corollary: every R18 minimum extraction is at gate7 or later.
The independent closure here does not use that premise, a preparation
counter, or a root-time clause. The proof does not transfer two unaries
to the entire Y20 family; R is the binary-maximum subclass.

A constructive next class is K=(0,1);(3,5);(2,3);(0,2), with passage costs
2/2/3. Its two unaries may be separated by arbitrary nongates. A surviving
marker prefix would be only a partial construction: execute all137 rows,
retire only actually extracted extrema, project rank/union bounds by actual
prefix deletion costs, and search budget18-prefix_length. Any44 witness
must pass all8192 original inputs for both P26 prefixes.
