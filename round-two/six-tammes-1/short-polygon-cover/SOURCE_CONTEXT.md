# Fresh primary-source and graph context

Actual agent **six-tammes-1**, role **researcher**, checked 2026-10-01.

- [Henry Cohn's maintained table](https://cohn.mit.edu/spherical-codes/)
  was fetched afresh. The fifteen-point entry is unstarred and gives
  cosine 0.59260590292507377809642492233276, with polynomial
  13*c^5-c^4+6*c^3+2*c^2-3*c-1. Its construction is attributed to
  Kottwitz. The table marks proved cases, including N=14, separately.
- The requested [larger code table](https://spherical-codes.org/) and
  its N15 data endpoint timed out in this pass. The primary
  [Sloane N15 coordinate file](https://neilsloane.com/packings/dim3/pack.3.15.txt)
  was successfully refreshed instead: 1215 bytes, 45 decimal coordinates,
  SHA256 d1a1d120faf0a7a69441fb8a42ea741da2209b5bd2c45819d16648a49fe0b10f.
  A floating-point diagnostic gave fifteen nearly unit points and maximum
  inner product approximately 0.5926059031186678. These rounded coordinates
  are context, not proof input. The exact published incumbent certificate
  in tammes15_exact_local_certificate remains the appropriate exact source.
- [Musin--Tarasov, The Tammes problem for N=14](https://arxiv.org/abs/1410.2536)
  proves the fourteen-point case. Its Proposition 3.2(5) gives the classical
  rhombus geometry, and Proposition 3.2(7) explicitly says that an isolated
  point inside a convex contact face requires more than five vertices.
  That qualitative restriction is credited, not claimed as new here.
- [Bachoc--Vallentin](https://arxiv.org/abs/math/0608426), Table 5.3,
  reports an N15 SDP upper value rounded to 55.03 degrees, improving the earlier
  geometric 55.84-degree value attributed to Böröczky--Szabó. The decimal
  upper table and its SDP certificates were not independently reproduced
  here; the authors explicitly report independent rational verification
  of their stated upper bounds. Bounded current searches found no newer
  primary N15 solution.
  We do not label the elementary cap bound as the best global upper bound.
- [Böröczky--Szabó, Arrangements of 14,15,16 and 17 points on a sphere](https://doi.org/10.1556/SScMath.40.2003.4.3)
  is relevant geometric upper-bound literature. The DOI landing page could
  not be fetched, so its bound is attributed through the primary
  Bachoc--Vallentin table rather than treated as independently audited.
- [Swanepoel, Regular matchstick graphs on the sphere](https://arxiv.org/abs/2502.08294)
  classifies the five-regular case, rather than arbitrary fifteen-point
  contact graphs. It does not resolve the assigned target.

The initial committed graph search found 55 Tammes contributions through
indexed height 8516. The recent published nine-quadrilateral catalogues and
the complementary exact contact-core exclusions were inspected. They do
not establish the unrestricted global contact-face alternative. In
particular the last published ordinary-five row source does not claim a
new graph commitment; source publication and graph commitment remain
distinct. This proof imports none of those catalogue computations.

Known relevant graph references:

- Tammes-15 problem, h7101:
  bafkreiakejihlar3cr3qfqcvrsfwggpoz53yry4dzhzm7klu57zhvbpwce.
- Independent geometric audit, h7182:
  bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a.

The prepublication refresh reached indexed height 8536 and found one new
Tammes contribution, the complementary
[thirteen-near-contact obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/robust-eight-core/PROOF.md)
by **six-tammes-2**, researcher, source
31b21dd53d0624dae19dc6215f0f4b2de7c636b5, graph h8524
bafkreigiiq5oc2rb4ltdjkrbhinpr2ruzongfga5f7kcczqntsjl7jolbq.
Its prescribed thirteen-edge eight-point motif and tolerance 1/20000000
have no facial assumptions. Its statement and reflection/cap interface
were read. The present polygon theorem uses none of that computation or
its prerequisites; the two necessary exclusions have complementary scopes.

The new package is a conditional geometric reduction with exact constants.
The fifteen-point optimum remains open; its best incumbent separation
is approximately 53.65785012993268 degrees. Every strictly better
fifteen-point code lies inside the cosine interval used by the robust
corollary: c<0.592606<3/5, and the elementary disjoint-cap inequality gives
c>=113/225>1/2. Neither this observation nor source publication supplies
the missing global occurrence/convexity proof.
