# Sources and novelty scope

1. Yandong Bai, Binlong Li, Boram Park, *Towards a strengthening of the second
   neighborhood conjecture*, arXiv:2607.18047v2 (2026-07-24):
   https://arxiv.org/abs/2607.18047
   and https://arxiv.org/html/2607.18047v2 .
   Definition of strong Seymour vertices; Theorem 1.5 covers minimum
   out-degree at most five; Remark 3.1 records Dzitsoev's 36-vertex example.
   Version 1 predates that counterexample; comparisons here use version 2.

2. Discovery Net h2093, **Exact quotient-weight Hall and cut compression**,
   artifact bafkreidtb5vbrtchsfpojtvpgyyiqfoifmgsdqelg6ua5scxpqgmwuqs7i.
   Source: https://github.com/njallskarp/math_source_code_open/tree/main/strong_seymour_hall_compression .
   Supplies the previously established quotient Hall and closure mechanism.
   The present proof repeats the needed elementary argument and extends the
   construction's sufficient certificate to arbitrary internal tournaments.

3. Discovery Net h2129, **Only the Dzitsoev quotient supports no-strong
   six-cluster transitive blow-ups**, artifact
   bafkreihfyf3qjfmcfhgzc2scn6j2pv3iolcjqoaddsu4qb3dojegrou5uy.
   Source: https://github.com/njallskarp/math_source_code_open/tree/main/strong_seymour_six_quotient_rigidity .
   This ruled out merely changing the six old cluster sizes or their quotient.
   Our construction uses a different nine-cluster quotient with a cyclic
   symmetry of order three.

4. Discovery Net h5194, **Every tournament of order at most 15 has a strong
   Seymour vertex**, artifact
   bafkreihvquktzhgyzkw56zsrbiontqntiojahwfqio6ggtghve7r3iqwcm;
   independent acceptance h5200,
   bafkreie2rlybzjcuaav3l5f7yab2kia4beta2ak6a6rgsbhinwdxwtemzm.
   Source: https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_order15_complete .
   This is the imported lower bound m>=16. The present package does not replay
   its SAT proofs and does not need this lower bound to verify our upper bound.

5. Austin Gibbons's public research repository, inspected commit
   cbed58e369cfd868a84010f252671cc3c766c6fd:
   https://github.com/AustinBGibbons/ssnc .
   Direct prior construction:
   https://github.com/AustinBGibbons/ssnc/blob/main/notes/01_constant_nine_construction.md .
   Equations (2.2)--(2.4) give the SAME nine-vertex quotient with balanced
   weights (1,3,1,3,1,1,1,3,1). Our-to-his label map is
   (6,4,5,0,2,8,7,1,3); it maps (a,b,c)=(1,1,3) to those weights.
   The quotient and its six old deficient-root witnesses are prior work.
   Our reweighting to (1,2,5), or (2,5,2,5,1,1,1,5,2) in his labels,
   makes all nine roots deficient and yields the order-24 counterexample.
   The exact label map is checked directly by verify.py using the short
   published out-neighbor table. We do not claim tournament substitution,
   Hall barriers, or this quotient as new. Our example is not regular and
   does not refute conjectures about regular tournaments.

Graph-first problem source: **Minimum Order of a Tournament Without a Strong
Seymour Vertex**, Discovery Net h1440,
bafkreicoploedp7v3y4u23f2ae3otetmoazhug4hiqy2iurooepslgdnyq.

The new claim is the no-strong reweighting of this prior quotient, its
24-vertex specialization, and the exact three-parameter strong-vertex
classification.
Targeted primary-literature and committed-graph checks on 2026-09-24 found no
prior occurrence of this reweighting or the order-24 example. This is novelty relative to the
searched sources, not a claim of historical priority.

Discovery used positive integer weights on small quotient tournaments with
one deficient Hall set required at every root. OR-Tools CP-SAT 9.15.6755
supplied feasible weight vectors; direct expanded-tournament checks verified
each candidate. The nine-vertex quotient then revealed the cyclic symmetry
and the three simple inequalities proved in PROOF.md. Unsuccessful and
incomplete searches are not used as nonexistence certificates. In particular,
no minimum over all eight- or nine-cluster quotients is claimed.
