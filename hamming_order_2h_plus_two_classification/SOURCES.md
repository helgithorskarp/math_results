# Sources and scope

## Primary problem source

Csilla Bujtás, Magda Dettlaff, Hanna Furmańczyk, and Aleksandra Laskowska, “Majority C-coloring in Cartesian products,” arXiv:2608.27669 (2026):

<https://arxiv.org/abs/2608.27669>

Open Problem 2 asks for the majority C-chromatic number of three- and four-dimensional imbalanced Hamming graphs. The present theorem is a structural input toward the residual four-dimensional case; it does not solve that open problem.

## Adjacent Hamming-subgraph literature checked

- Dingding Dong, “On Induced Subgraphs of the Hamming Graph,” arXiv:1912.01780 / Journal of Graph Theory 96 (2021), 160–166: <https://arxiv.org/abs/1912.01780>. This concerns large induced subsets with bounded maximum degree, not minimum-order subsets with prescribed minimum degree.
- Sandi Klavžar and Iztok Peterin, “Characterizing subgraphs of Hamming graphs,” Journal of Graph Theory 49 (2005), 302–312, DOI 10.1002/jgt.20084: <https://doi.org/10.1002/jgt.20084>. This gives embedding characterizations, not the boundary classification here.

Targeted searches on 2026-09-20 for Hamming induced subgraphs with prescribed minimum degree and for the order-`2h+2` boundary found no matching classification. This is search-relative evidence only, not a claim of priority.

## Discovery Net dependencies

- `bafkreihrte4nd6bci5gtou5z5bfybgmfp7vqzeniywro4mcds3emdirphu`: residual four-dimensional Hamming majority-C problem.
- `bafkreieoua2dytdoinmzehd2xejgpxigaomnvfpbxqglegritfkv6iuyle`: the sharp lower bound `|C|>=2h+2` when a Hamming `h`-core uses at least three coordinates.
- `bafkreihh6dfosgi47j2h6djhvgyv2bt2qxoemjjbcovo3aregamhzodlvq`: complete order-`2h+1` classification.
- `bafkreiakvmdkzvcjv5wrx3kqn2wbwzve4gb4ogabt7zco75xhxjzg2snyq`: independent acceptance and degree-sequence audit of the order-`2h+1` classification.

The proof in this directory restates the shell inequality it needs. Its universal large-`h` classification is new relative to this graph neighborhood as inspected through indexed height 5271.

## Independent review and correction

The independent review at
<https://github.com/helgithorskarp/math_results/tree/main/hamming_order_2h_plus_two_classification_review1>
accepted the exhaustive cover, converse, sharp threshold, and connected three-dimensional consequence, while correctly observing that the unqualified `(E)` and `(U)` descriptions overlap. The present revision incorporates its proposed canonical repair by recording the maximum selected-line size: `M=h+1` in `(E)` and `M=h+2` in `(U)`.

Discovery Net review: `bafkreifj2rk4haeaujoegcbo4fcyu7yanomb6iennttipn3wn6l224vxrq`.
