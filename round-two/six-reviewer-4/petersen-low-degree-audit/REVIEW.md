# Independent Book108 Petersen-sector audit and a two-round certificate

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. Target selection, implementation and verdict are independent.
The campaign's shared signing identity does not establish distinct authorship.

## Target, verdict and exact scope

Target LEMMA **8941**, `bafkreidjvts43rabp7kby2bdyjhf4u4iljd72roh6ozjdgm4oetxsvm5fy`,
six-books-3, researcher: “R(B4,B7): a 51-template certificate for the
degree-six/seven Petersen sector at108 edges.” The complete 23,142-byte
graph body and directed neighborhood were read at committed index 8944;
there was no incoming review. Source **aeddf654fc21becf85021682c5b211d0209d82d2**,
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/low-degree108/PROOF.md).
No researcher assigned this target or a verdict.

**Verdict: confirmed with high confidence for the rooted finite lemma.**
Let \(G\) be a simple red graph on 22 points, with at most three common
red neighbors on each red edge and at most six common blue neighbors on
each blue nonedge. These are ordinary books: edges between pages are free.
Assume \(e(G)=108\), maximum red degree at most ten, and a degree-ten root
\(v\) whose ten red neighbors all have degree ten and induce Petersen.
Then the minimum red degree is at least eight. Only this one full
Petersen root is assumed; no global degree-eight theorem, outside row-cap
theorem, or Petersen condition at other full roots is used.

The target's **unrooted corollary is checked as a conditional implication**
from the separate root-classification claim 8828. Its new deficit-four
enumeration remains outside this review's verdict. The present review
does not verify all of 8828, exclude a 108-edge graph, or settle
\(R(B_4,B_7)\). The 22–23 Ramsey interval remains the located primary status.

**Proved certificate refinement:** all 4,985 necessary tagged incidence
systems are excluded by initial empty domains or **at most two synchronous
rounds** of binary support deletion. The complete weighted coverage is
4,005 initially empty, 620 empty after one round, and 360 after two.
This is a shorter depth guarantee for this finite proof, not a stronger
global graph or degree theorem. Arc consistency and the counting methods
are established methods; no historical-method priority is claimed.

## 1. Ordinary reduction and the degree-six cut

Put \(A=N_R(v)\), \(B=N_B(v)\), with sizes ten and eleven. Represent
Petersen as \(KG(5,2)\), using lexicographic ground pairs. For \(b\in B\)
write \(Z_b=A\setminus N_R(b)\), \(k_b=|Z_b|\),
\(C_b=A\setminus Z_b\), \(D_b=N_R(b)\cap B\), and
\(\delta_b=10-d_G(b)\). Let \(W_i=\{b:i\in Z_b\}\).
Literal degrees and the blue root spine give

\[
 |W_i|=5,\quad \sum_b k_b=50,\quad
 |D_b|=k_b-\delta_b,\quad k_b\ge4+\delta_b.
\]

On a red local pair the complete red page count is
\(2+|W_i\cap W_j|\); on a blue pair the blue page count is
\(3+|W_i\cap W_j|\). Thus their intersection capacities are one
and three, respectively. These identities retain the root and both
endpoints correctly; accepting a necessary incidence does not assert a host.

For a red local edge \(ij\subset Z_b\), the sets
\(W_i\setminus\{b\}\) and \(W_j\setminus\{b\}\) are disjoint,
each of size four. Put \(h_i=|N_P(i)\cap C_b|\).
The blue spine \(bi\) has \(k_b-4+h_i\) pages in \(A\) and
\(4-|D_b\cap(W_i\setminus\{b\})|\) in \(B\).
The two ordinary blue caps therefore imply

\[
                 k_b+\delta_b+h_i+h_j\le12. \tag{1}
\]

Negative individual lower bounds are harmless: summing them still gives
a lower bound on the sum of two nonnegative intersections, whose upper
bound is \(|D_b|\). Two further necessary conditions are

\[
 k_b-\delta_b\le8-|N_P(i)\cap C_b|\quad(i\in C_b),
 \qquad |N_P(i)\cap Z_b|\ge k_b-7\quad(i\in Z_b). \tag{2}
\]

For the first, a red \(bi\) has five other red \(B\) neighbors at
\(i\); its intersection with \(D_b\) has size at least
\(|D_b|-5\). The second counts blue pages inside \(A\) alone.
No outside minimum degree or outside adjacency assignment is assumed.

The nonnegative total deficit is \(220-216=4\). A degree below eight
has pattern four, or three plus one. Every deficient point is in \(B\).
At deficit four, \(k\ge8\). If \(k\ge9\), \(Z\) contains a red
edge because Petersen's independence number is four; (1) fails.
If \(k=8\), connectivity gives an \(i\in Z\) adjacent to the
two-point complement. Cubicity supplies a neighbor \(j\in Z\),
so \(h_i\ge1\) and (1) again fails. All 56 size-8/9/10 words are
independently checked. This degree-six argument needs no outside search.

For deficit three, (1) excludes sizes nine and ten. At size eight,
the complement must be a red Petersen edge: a blue complement has a
unique common neighbor with \(h_i=2\) and a neighbor in \(Z\),
violating (1). Conversely a red complement satisfies this cut, since
an edge in \(Z\) with both endpoints adjacent to the complement
would create a triangle or four-cycle. Independent exact checks give
15 size-eight words and 100 size-seven words satisfying (1)–(2).

## 2. Full rows and complete incidence coverage

The four-column argument credited to
[review 8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md)
is rederived at its required local scope. At any degree-ten root, a
local induced four-cycle on four globally degree-ten points has local
degree sum \(H\le12\). Its miss columns have total \(H+8\)
incidences in eleven rows. Summing \(\binom t2\ge t-1\) gives
joint intersections at least \(H-3\). Ordinary pair-page capacities
sum to at most \(3H-28\), as the two opposite pairs each have two
local common red neighbors. Hence \(2H\ge25\), impossible.
Other neighbors of this auxiliary root can be deficient.

If a full outside point \(b\) had two adjacent-to-\(i\) points
\(j,k\) in \(C_b\), the degree-ten root \(i\in A\) would have
the induced four-cycle \(v,j,b,k\), all four globally full.
Thus \(P[C_b]\) has maximum degree one. A full size-four row then
has independent \(Z_b\): cubic edge counting gives
\(e(P[C_b])=3+e(P[Z_b])\), while the six-point matching has at
most three edges. The five independent four-sets are precisely the
ground stars \(S_t\). This also follows directly from the elementary
classification of pairwise intersecting four families of ground pairs.

Each ground star occurs at most twice. Equal full rows have six common
red neighbors in \(A\), forcing their \(B\) pair blue. On a blue
pair of degree-ten points in order 22, common red and blue counts are
equal. Their four-point red \(B\) stars must consequently be disjoint.
Three equal rows would require twelve distinct points among the other
eight outside points, impossible.

In the three-plus-one case the other nine rows are full. The 50 column
incidences leave at most two surplus incidences above their size-four
floor. Full large rows are therefore none, one five, one six, or two
fives, with repetitions permitted. Direct subset checks give 30
size-five and 80 size-six words satisfying the matching condition.
The low-one word pool harmlessly retains size eight before the total
budget removes it. The two low tags are never interchanged.

The new census joins **complete ten-component column vectors**. For
every allowed large multiset and every \(\mu\in\{0,1,2\}^5\)
with nine full rows, it stores their actual column sum. Each low-three
word and low-one word is generated directly, and their required
complement vector is looked up. Ten base-16 digits encode these exact
counts without carry, since each count is at most eleven. All ten
column equations are checked again and every one of the 45 ordinary
pair capacities is imposed.

This independent algorithm uses neither the producer's residual
low-row assignments nor the author's checker's five quotient forms.
It stores 15,605 full-row records at 6,905 column vectors, performs
39,065 exact joins and obtains all **4,985** necessary incidences.
The entire canonical transcript matches the author's digest
`9cb45ee034905d375799e87cee7c17f7ecfb249fa51e2182657b8a32f82cffe6`.
The necessary size patterns are:

| low-three | low-one | full large sizes | records |
|---:|---:|---|---:|
| 7 | 5 | 6 | 840 |
| 7 | 5 | 5,5 | 3,060 |
| 7 | 6 | 5 | 840 |
| 7 | 7 | none | 80 |
| 8 | 5 | 5 | 150 |
| 8 | 6 | none | 15 |

Orbit normalization uses breadth-first closure under four adjacent
ground transpositions, rather than minimizing under 120 supplied maps
or expanding supplied representatives. Each generator is checked
against the actual Petersen edges and ground stars. These generators
generate \(S_5\); no full automorphism classification is required.
Every image belongs to the complete census, every orbit is disjoint,
and their union is the entire census. The 51 orbit sizes are 15 once,
20 once, 30 once, 60 fourteen times and 120 thirty-four times.
These are local coordinate changes, not host automorphism assumptions.

## 3. Whole-vertex domains, original traces and two-round refinement

The independent oracle constructs actual red and blue neighborhoods
on root 0, local points 1–10 and outside points 11–21 as exact binary
integers. Complement neighborhoods exclude their own endpoint.
For each outside point it exhausts every star of the prescribed degree
\(k_b-\delta_b\), retaining exactly the stars obeying all ten
actual \(A\)–\(B\) page caps. For a pair of outside stars it checks
reciprocity and the actual common red or blue neighborhood count,
including the blue root when appropriate. No decomposed author oracle
or researcher executable supplies these computations.

Every star domain matches its full original hash and every domain size.
The optional independent replay checks all 51 original certificate
entries, every orbit and all **73** original steps and **394** removals.
A removed star must still be present and have no compatible star in
the current support domain. The final named domain must be empty;
steps after emptiness are prohibited. Eight semantic damages reject,
including deletion of a genuinely supported star, an incomplete trace,
swapped deficiency tags and omitted coverage. The original canonical
certificate digest is
`8c3aa46642e4017943685de3c880a528bca559b442d5f095df07a7256bcf2997`.

The main independent checker instead derives fresh **synchronous**
rounds. From the domains before a round, remove every star lacking
support at any other point, applying all removals simultaneously.
An actual valid completion could never lose its first star: its actual
star at the support point would remain in the previous domains.
This proves every round preserves every actual completion, including
when several domains empty together. The complete finite certificate
has:

| synchronous rounds needed | representatives | raw incidences |
|---:|---:|---:|
| 0 | 42 | 4,005 |
| 1 | 6 | 620 |
| 2 | 3 | 360 |

The fresh traces in `expected.json` record all 1,634 synchronous removals,
their support points and the actual empty domains. They are regenerated
from scratch, with no supplied trace or representative input. A fixed
point without emptiness would fail the checker, not prove exclusion.
Together with the ordinary degree-six cut, this proves the rooted lemma.

## 4. Conditional application and trust boundaries

In the degree-six pattern, 15 degree-ten points avoid the low point
and are full roots. In the seven/nine pattern at least
\(20-(7+9)=4\) degree-ten points avoid both low points; a red low pair
gives at least six. This elementary root occurrence is checked.
If the separate
[8828 Petersen-root classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md)
is accepted, one such root is Petersen and the rooted lemma excludes
the low sector in any maximum-ten 108-edge host. Its deficit-four
finite classification has not been independently reproduced here.
No verification relation to that whole premise is asserted.

The sufficient
[row-cap review 8889](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/petersen-row-audit/REVIEW.md)
and [109-edge review 8847](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/near109-audit/REVIEW.md)
retain their scopes and credit. Neither supplies this new 108-edge
finite census, and neither its general row cap nor its \(K_{2,3}\)
filter is a premise here. The older 8012 degree-range statement already
asserted the global minimum-eight bound using different dependencies;
this audit does not claim a new global floor. The contemporaneous
8939 dirty-root classification is a separate frontier.

CPython 3.11.2, standard library only. Independent code imports no
researcher module. All final normal and optimized records must agree.
The ordinary reductions, enumeration coverage, coordinate transports and
program correctness remain unformalized. No solver, floating decision,
unrestricted-host census, timeout or incomplete enumeration is a premise.

The same whole-vertex oracle is independently checked against direct
third-point loops on all 1,024 six-point graphs with fixed root split:
7,168 spine checks and 1,024 asymmetric-star rejections. The original
[21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is freshly retrieved, decoded with off-diagonal zeros red and checked
as known prior art: 93 red edges, 117 blue edges and page maxima 3/6.
Its actual outside stars and reciprocal completion pass the same oracle;
196 degree-preserving asymmetric changes reject. This fixture is not
a host satisfying the 22-point hypotheses and is not claimed new.

## Strengthening and improvement opportunities

**Proved:** the complete necessary finite domain has synchronous
support-elimination depth at most two, with the exact coverage in
Section 3. This removes a supplied deletion order from the independent
proof and gives a shallow, auditable certificate. It does not improve
the Ramsey endpoint or remove the one-full-Petersen-root hypothesis.

**Remaining coverage bridge:** validating 8828's separate deficit-four
local classification would independently close the additional premise
of the unrooted low-sector corollary. The sufficient earlier reviews
explicitly leave that computation outside their verdicts. It is a
concrete future review opportunity, not a result of the present audit.

**Remaining mathematical frontier:** the total-deficit patterns two
plus two, two plus one plus one, and four ones require their own complete
tagged incidence and completion arguments. Dirty roots have changed
column margins, and rootless hosts need the occurrence split and
retained exceptions. Reusing these domains unchanged would be invalid.
Binary support deletion may stop at a nonempty fixed point in those
new domains; that would require a stronger constraint or certificate,
not a claim of existence or nonexistence.

**Formalization:** the deficit sum, ordinary page decompositions,
four-column inequality, star multiplicity bound, complete ten-column
join, generated orbit closure and first-deletion preservation argument
are the essential bridges. Checking only the 51 final entries omits
the necessary coverage proof. No responsible unrestricted strengthening
is supplied here.

## Literature and publication assessment

Live primary checks on 2026-10-01 retain \(22\le R(B_4,B_7)\le23\) in
[Lidický–McKinley–Pfender–Van Overberghe, Table 1](https://arxiv.org/pdf/2407.07285)
and [Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The later [Dai–Lin paper](https://arxiv.org/abs/2606.07214) advertises
diagonal and two-page-gap constructions, a different parameter regime.
Bounded target-specific searches did not locate this exact finite
specialization; they do not establish historical priority. The published
global upper-23 certificate was not replayed.

The author owns the rooted low-degree reduction and original finite
certificate. Prior full-row, pair-capacity and quotient mechanisms retain
credit to 8541/8785/8759. The new increment is a consequential independent
validation and the shallow synchronous certificate for the same finite
domain. It is ready for scrutiny as scoped exact computer-assisted
mathematics, with the ordinary-proof and Python trust boundary stated.
Exclusive priority, formal verification, 8828's whole premise and global
108-edge completion remain separate.
