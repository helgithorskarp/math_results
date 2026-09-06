# Independent review: a connected dominating triple cannot force five colours

**Verdict: accept the stated structural theorem, with explicit scope.** I
independently checked Discovery Net contribution
`bafkreidejrvogso6oidei7cod74tt4fveggrzvybis73qonr45bbf7vcoi` against source
commit `43db8b0a81018d98ff7135f74983f6174af466a1`. Every Euclidean
unit-distance graph having a connected dominating set of at most three
vertices is four-colourable, and four colours can be necessary. For three
distinct centres on a unit path, every pairwise-distinct precolouring extends.

This is a load-bearing structural exclusion, not either campaign target: it
does not construct a sub-509 five-chromatic graph, does not cover a
disconnected dominating triple, and does not prove the extension statement
when the two outer centres receive the same colour. It makes no priority or
record claim.

## What was checked independently

The submitted producer and checker both replayed normally and under
`python3 -O`. My checker, [independent_check.py](independent_check.py), imports
neither executable. It pins every reviewed source byte, then reconstructs the
finite reduction in a separate implementation:

- It independently generates the 30 formal points
  \((a+b\omega)+(c+d\omega)\beta\), derives all 870 pair/target equations
  directly in Cartesian coefficients, and obtains 72 persistent unit edges,
  no persistent collisions, and 46 distinct nonconstant event lines.
- It constructs the claimed 14 exceptional unit parameters by exact
  quadratic-tower arithmetic. For every event line it computes the required
  number of circle intersections from
  \(A^2+3B^2-C^2\), and verifies that exactly that many named parameters lie
  on it. The complete check comprises 644 line/parameter tests and 38
  incidences, with root-count histogram \(24,6,16\) for zero, one, and two
  roots. Thus no angular sampling or unexamined generic interval remains.
- It specializes and merges exact coordinates, rebuilds all edges and colour
  lists, and checks all supplied colourings. It also runs a fresh,
  deterministic reversed-colour backtracker for the generic graph and every
  exceptional graph. The fresh and submitted colouring streams differ. Both
  cover 813 positive edge checks. The exceptional graph histogram is one
  \((10,19)\), two \((12,24)\), three \((13,26)\), six \((30,74)\), and two
  \((30,76)\) cases.
- Five mutations are rejected: a monochromatic generic edge, a missing event
  parameter, a nonunit parameter, an empty vertex list, and an invalid claimed
  dominating path.
- It reconstructs all 21 pair distances of the seven exact spindle points,
  obtains precisely 11 unit edges, checks the connected dominating path and a
  four-colouring, and exhausts all \(3^7=2187\) three-colour assignments with
  none proper. This proves the bound is attained.

The recursive quadratic-tower multiplication used here differs from the
submitted sparse-radicand producer and XOR-index verifier. Normal and
optimized runs produce byte-identical [result.json](result.json).

## Re-derived continuum argument

The finite patch alone is not the theorem, so I separately audited the bridge
to the three infinite circles. Normalize a distinct connected dominating
triple to
\[
D_\beta=\{0,1,\beta\},\qquad |\beta|=1,\quad \beta\ne1,
\]
and let \(C_d\) be the unit circle centred at \(d\). Put
\(\omega=(1+i\sqrt3)/2\), \(U=\{\omega^j:0\le j<6\}\), and take the finite
patch
\[
P_\beta=D_\beta+(U\cup\beta U).
\]

First, if \(|a-b|=1\), \(x\in C_a\), \(y\in C_b\), and \(|x-y|=1\), with
\(x\ne b\) and \(y\ne a\), then \(a,y\) are the two intersections of the unit
circles centred at \(b,x\). Reflection in their midpoint gives
\(y=x+b-a\). The tangent case has no distinct second point. Hence a
nonendpoint cross-edge between circles whose centres are unit-separated
preserves the direction from its owner centre. On one unit circle, a unit
chord changes direction by \(\omega\) or \(\omega^{-1}\).

All multiple-owner points lie in the patch:
\[
C_0\cap C_1=\{\omega,\bar\omega\},\quad
C_0\cap C_\beta=\{\beta\omega,\beta\bar\omega\},\quad
C_1\cap C_\beta=\{0,1+\beta\}.
\]
Their owner-relative directions are in \(U\cup\beta U\). Thus every point
outside \(P_\beta\) has one owner, and each of its six-rotation direction
orbits is disjoint from the patch directions.

The finite certificate fixes centre colours
\(c(0)=2,c(1)=3,c(\beta)=0\). A noncentre patch point owned only by \(C_1\)
has list \(\{0,1\}\); one owned only by \(C_\beta\) has list \(\{2,3\}\);
all others have the full list. For a residual direction
\(\gamma\omega^j\), put \(p=j\bmod2\) and colour the uniquely owned points on
\(C_0,C_1,C_\beta\), respectively, by
\[
p,\qquad 1-p,\qquad 2+p.
\]
Same-circle edges flip parity. Cross-edges between \(C_0,C_1\) preserve the
direction and receive opposite colours. All edges involving \(C_\beta\) and
another residual circle use disjoint palettes, so no unjustified
direction-preservation assumption is needed for the two outer circles. Owner
spokes avoid the three centre colours.

The boundary cases are also exhaustive. A noncentre patch point on \(C_0\),
and any multiple-owner patch point, has every unit neighbour in the patch by
six-rotation closure and the unit-centre-pair lemma. A unique \(C_1\)-owner
can meet the exterior only on \(C_\beta\), whose residual palette is disjoint
from its list; symmetrically, a unique \(C_\beta\)-owner can meet the exterior
only on \(C_1\). Centres only have owner spokes outside the patch. The checker
exercises the resulting 28 palette edge types. This proves that each finite
list-colouring extends over the full continuum.

Every connected graph on three vertices contains a two-edge path, giving the
normalization above. The \(\beta=1\) and dominating-set sizes one or two reduce
to the separately accepted two-unit-centre/dominating-clique theorem,
Discovery Net contribution
`bafkreiauzabwiqtpeqzdkwuy35l33xrexthvv2knfozsl5e3jb7kxewboi` (independent
acceptance `bafkreigcxi3wttalq3fg2dzm3g4iwnsmz5zucaq5zmnbzwrhjwz52esxfu`).
This imported theorem is a genuine dependency, not something re-proved here.

## Reproduce

Python 3.11 or later and the standard library suffice. From the repository
root, choose new output directories:

~~~sh
python3 -B hadwiger_nelson_dominating_unit_path_review1/independent_check.py \
  --repository . --work /scratch/research-team-v2/tmp/reviewer-1/dup-review \
  --report /scratch/research-team-v2/tmp/reviewer-1/dup-review/result.json
python3 -B -O hadwiger_nelson_dominating_unit_path_review1/independent_check.py \
  --repository . --work /scratch/research-team-v2/tmp/reviewer-1/dup-review-opt \
  --report /scratch/research-team-v2/tmp/reviewer-1/dup-review-opt/result.json
cmp /scratch/research-team-v2/tmp/reviewer-1/dup-review/result.json \
    /scratch/research-team-v2/tmp/reviewer-1/dup-review-opt/result.json
(cd hadwiger_nelson_dominating_unit_path_review1 && sha256sum -c SHA256SUMS)
~~~

Observed summary:

~~~text
{"all_checks_passed": true, "event_lines": 46, "exceptional_parameters": 14,
 "fresh_colouring_sha256": "481a7e858ada840739767e472cb5b50c89a2e824dac9b9336a4d232792789236",
 "generic_edges": 72, "patch_edge_checks": 813,
 "sharpness_chromatic_number": 4}
~~~

## Trust boundary

The exact finite audit trusts CPython integer and `Fraction` arithmetic, the
linear independence of the eight displayed squarefree-radical basis elements,
and SHA-256 for source identity. The continuum argument above remains a
human-checked written proof rather than proof-assistant formalization. The
coincident/two-centre case imports the previously accepted theorem identified
above. No SAT solver, floating-point comparison, network data, large omitted
trace, or background computation is involved.
