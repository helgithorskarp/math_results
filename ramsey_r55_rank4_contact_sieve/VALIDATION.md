# Evidence and interpretation

The expected complete evidence SHA-256 is

    9bfd58873ef6811410c4488f86c4346fcec5ca13f4a5211664d9ceb53e383182

`reproduce.py` regenerates the evidence; the saved file is only an expected
output, never an exclusion verdict. All input and mathematical checks use
explicit exceptions, so disabling Python assertions does not disable them.

The evidence includes:

* all ten target marked-list counts checked by a separate algorithm;
  for rows it uses bounded set partitions and span-dimension subtraction,
  for columns individual-letter integer polynomials and actual-subspace
  subtraction, rather than the producer's grouped cell/Mobius computation;
* agreement of two complete subspace enumerations, with dimension counts
  1,15,35,15,1, and independent reproduction of the preceding exact capped
  denominator and complementary-rank-three overlap;
* all 98,304 binary matrices of sizes 4x4 and 5x3, with eight complete
  parameter configurations checking physical baseline counts, the first
  moment, the pair-intersection moment and the union bound;
* 72 full 43-vertex rejected graphs: 48 with one violating type, 12 with
  two, and 12 with three, each with a literal monochromatic five checked
  by the independent physical verifier;
* 72 factor-basis changes preserving every physical pair and violation
  multiplicity/contact count, plus dense graph decoding that independently
  recovers the number of violating row types;
* four retained endpoint cases (contact count 10 or 13, row population
  three or four), all 443 internal coordinates and all 460 cross contacts;
* 10,240 comparisons of the extractor's clique primitive against literal
  subsets of every five-vertex graph in both colors, and 152 rejected
  corruptions or inputs outside the declared certificate domain.

The small configurations test the finite counting machinery; they do not
apply the 43-vertex Ramsey contact theorem at smaller graph orders. The
72 large fixtures are deliberately non-Ramsey and are not candidates.
Neither set of controls enumerates the full 43-vertex family.

The published removal is a lower bound. If k types violate, the proof
uses k-binom(k,2)<=1_{k>0}. It also subtracts the full remaining
complementary-rank-three class, rather than asserting its exact overlap.
Graphs with three violating types appear in the physical controls,
illustrating why the moments alone should not be presented as an exact
union count. The prior affine class has no type occurring three times.

The source manifest and the four verbatim ancestor hashes are verified
locally. Reproduction uses Python integers and the standard library, with
no solver, graph catalog, private input, network download, stored proof
verdict or omitted generated certificate. Floating point is unnecessary
for every count and rational bound; percentages render the exact rational.

The local proof imports R(4,5)<=25 and uses elementary smaller Ramsey
bounds. Historical Ramsey computations are not replayed. Ordinary hardware
and unformalized mathematical reasoning remain trust boundaries. The
independent author algorithms are not an external review or a formal
proof-assistant verification. The remaining family is undecided and no
Ramsey-number bound changes.
