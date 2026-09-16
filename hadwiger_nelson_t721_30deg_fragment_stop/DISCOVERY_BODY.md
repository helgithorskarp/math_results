Exact computer-assisted stopping result for one moved-fragment construction.
Start with the pinned 721-point T721 coordinate support.  Let M be the 238
labels appearing in the accepted positive terminal-deletion cover, and add the
first 16 outside labels under the exact order (-number of neighbours in M,
-native degree, label).  This defines a 254-point proper fragment F.  Rotate F
about native label 2, the origin, through 15 degrees and 45 degrees, and take
the collision-merged union.

Complete exact reconstruction over Q(sqrt(2),sqrt(3),sqrt(5)) gives 391
distinct physical points and 1,264 strict unit edges after checking all 76,245
unordered pairs.  The two formal 254-point copies have 117 collisions and 134
private--private cross edges.  The complete graph is connected, has no
articulation or bridge, and its 253-vertex four-core contains 94 private
vertices from each frame and 65 shared vertices.  Thus the interaction passes
the declared nonseparability and both-fragments-active gates.

Nevertheless the graph is exactly four-chromatic.  A literal 391-symbol
proper four-colour word has SHA-256
b773d0dab9bf129e18edc65b9cee028509e6a8e2b22f26461254ce96b460a22f.
For the lower bound, a recorded 26-vertex/50-edge induced subgraph uses private
vertices from both frames, five shared vertices and seven private cross edges.
A definition-level exhaustive checker finds no three-colouring after fixing
one triangle's palette and finds a three-colouring after every one-vertex
deletion.  No UNSAT solver result is trusted by the published verification.

The support is not a subgraph of the native 1,441-point spindle closed at
height 3707.  It is also outside the tested pointwise-Galois class: the
rational source point (-1,0) is fixed by every field automorphism but is moved
in both frames.  This result closes only this frozen 30-degree interaction. It
does not classify other fragments or placements and is not a record candidate.

Public exact verifier and compact evidence:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_t721_30deg_fragment_stop

Direct verifier:
https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_t721_30deg_fragment_stop/verify.py

Verified source commit: 9a34bc231a5f1e46919cdb7b815d72cd0c7dc212.

Reproduction from repository root:
python3 -B hadwiger_nelson_t721_weighted_cover/fetch_input.py /tmp/T721.vtx
python3 -B hadwiger_nelson_t721_30deg_fragment_stop/verify.py --input /tmp/T721.vtx --check-expected

CPython 3.11+ standard library suffices.  Normal and optimized verification
agree.  The external input has 40,529 bytes and SHA-256
a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6.
The complete coordinate and edge stream hashes are respectively
5870b3ef19889596592b6860b3d8b92effd8f1263523401c483683d29b8ea11b and
495b78d123023460b52d16786eef6ed2474a55780c5fb22903655818c1a4b235.
This is exact author-side evidence, not an independent review or formal proof.
