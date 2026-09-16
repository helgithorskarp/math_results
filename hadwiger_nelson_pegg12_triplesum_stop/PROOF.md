# Proof outline

1. `model.py` constructs the twelve displayed Pegg/Shibuya points in the
   exact biquadratic field `Q(sqrt(3),sqrt(11))`.  All-pairs comparison gives
   21 unit edges.  Exhaustive colouring gives no proper three-colouring and a
   proper four-colouring.
2. The 364 weakly increasing triples `(i,j,k)` are evaluated as
   `p_i+p_j+p_k`.  Equality in the exact coefficient representation merges
   them into 175 points.  All `C(175,2)` pairs are tested exactly, producing
   813 unit edges.
3. The 78 translated fibres `p_i+p_j+P` account for 729 distinct inherited
   unit edges.  The reconstructed complete graph has 84 further unit edges.
4. Canonical restricted-renaming enumeration produces exactly 756 proper
   source four-colourings.  For each word, a deterministic exhaustive DSATUR
   search pins the twelve vertices of the fibre `p_0+p_0+P` and decides
   extension to all 175 vertices.  Exactly 340 return exhaustive failure and
   416 return checked extensions; their ordered stream has the committed
   SHA-256 digest.
5. The literal first extension in `certificate.json` is checked on every one
   of the 813 edges and checked to restrict to its source word.  Hence the
   complete physical graph is four-colourable.  It contains the source fibre,
   which is not three-colourable, so its chromatic number is exactly four.

No solver binary, random choice, numerical equality, or undeclared edge list
is a trust input.  The standard-library verifier regenerates every object from
the formulas.
