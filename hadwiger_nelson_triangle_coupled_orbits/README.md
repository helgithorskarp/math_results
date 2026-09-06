# Four-colour closure of 36 coupled exterior-cycle placements

All 36 explicitly defined two-cycle placements below remain four-colourable even when the **entire three unit circles** around a unit equilateral triangle are included. Each infinite graph has a complete 66-vertex four-colouring core. One 156-vertex, 690-edge positive certificate covers all 36 cores.

The second exterior cycle increases contact with the same two generic circle components; the complete nonparallel contact census produces no additional generic component. This is a negative construction-family result for the Hadwiger–Nelson record search, not a five-chromatic graph. Every subgraph of any of the 36 infinite supports is four-colourable.

The simultaneous union of all 108 exterior points is **not** excluded as an infinite construction by this result. Its finite 156-vertex subgraph is four-colourable, but additional circle components can have three or more contacts with identical rotated normals. Those components need a separate extension analysis.

## Exact construction and statements

Identify the Euclidean plane with the complex plane. All unit-distance graphs here contain **every** pair at distance one. Set

$$
\omega=\frac{1+i\sqrt3}{2},\qquad
D=\{d_0,d_1,d_2\}=\{0,1,\omega\},\qquad U=\{\omega^j:0\le j<6\},
$$
$$
P=D+U,\qquad B=P\setminus D,\qquad
X=D\cup C(0,1)\cup C(1,1)\cup C(\omega,1).
$$

Here $P$ has 12 points and $B$ induces a nine-cycle. The symbol $C(d,1)$ denotes the full circle, not a sampled rim. Choose the two exact unit translations

$$
\rho=\frac{5+i\sqrt{11}}6,\qquad
\sigma=\frac{-3-\sqrt{33}+i(-\sqrt3+3\sqrt{11})}{12}.
$$

The second translation is the additional generic direction found in the earlier [single-cycle contact census](../hadwiger_nelson_triangle_exterior_kernel/README.md). The present family changes the exterior interaction by using both directions together.

For every ordered pair $0\le a,b<6$, define

$$
W_{ab}=(B+\rho\omega^a)\cup(B+\sigma\omega^b).
$$

**Theorem.** Each $W_{ab}$ has 18 distinct points outside $X$. The whole infinite unit-distance graph on $X\cup W_{ab}$ is four-colourable. Its important generic circle components are exactly

$$
Q(-\rho)\quad\text{and}\quad Q(\sigma),\qquad
Q(u)=\{d_i+u\omega^j:0\le i<3,\ 0\le j<6\}.
$$

Consequently $P\cup W_{ab}\cup Q(-\rho)\cup Q(\sigma)$, with all its unit edges, is a 66-vertex complete core. The word “important” means having at least three **edge incidences** from $W_{ab}$, with multiplicity over distinct edges, not merely three boundary vertices.

There is also a direct subset consequence. Let

$$
F=\bigcup_{a,b=0}^5 W_{ab},\qquad |F|=108.
$$

For $W\subseteq F$, form the multiset of nonzero vectors $w-d_i$, one for each pair $(w,i)$, and identify vectors under multiplication by $U$.

**Subset corollary.** If each such normal rotation class occurs at most twice, then $X\cup W$ is four-colourable. Such a $W$ automatically has at most 24 points, and its core lies in $P\cup W\cup Q(-\rho)\cup Q(\sigma)$, of size at most 72.

This corollary follows from the same certificate and normal-count argument. It does not claim that all subsets of $F$ satisfy the multiplicity hypothesis, and there was no exhaustive enumeration of its admissible subsets. It also does not claim a general theorem for two arbitrary translated cycles or two arbitrary direction orbits.

## Analytic inputs and the finite reduction

The earlier [dominating-triangle theorem](../hadwiger_nelson_dominating_triangle/README.md) decomposes $X\setminus D$ into the exceptional nine-cycle $B$ and independent 18-vertex components $Q(u)$, indexed by generic unit directions modulo $U$. Each generic component is $K_3\mathbin\square C_6$, with vertex $(i,j)$ adjacent to centre $d_i$. There are no edges between distinct components of $X\setminus D$.

The [exterior-kernel theorem](../hadwiger_nelson_triangle_exterior_kernel/README.md) proves that a generic component with at most two exterior edge incidences extends any given proper four-colouring of $D\cup W$. Briefly, rename the centre colours to $0,1,2$, with fourth colour $3$, and use the two base rows

$$
c_\varepsilon(i,j)=i+\varepsilon(-1)^j\pmod3,\qquad \varepsilon\in\{1,-1\}.
$$

Both rows properly colour $Q(u)$ and avoid the owner's colour. An exterior edge forbidding the owner colour is redundant, and one forbidding colour 3 is already satisfied. Each other restriction is satisfied by exactly one base row. With at most two restrictions, choose a base row violating at most one. If a violation remains, there must be two active restrictions favouring opposite rows, so neither forbids colour 3. Recolour the sole violating vertex to 3. This works also when both restrictions concern the same vertex. There are no other vertices coloured 3 in that component.

Thus retaining $P,W$, and every generic component with at least three exterior incidences gives an exact four-colourability reduction. After a core is coloured, all omitted components extend independently. The finite number with exterior contacts can be repaired as above; the remaining components use a base row. This applies to the full infinite support. The universal circle decomposition is an explicit analytic dependency, not something inferred from the finite certificate in this package.

## Why the census is complete

Write $A=w-d_i\ne0$. A contact from $w$ to $d_i+z$, with $|z|=1$, is equivalent to

$$
2\langle z,A\rangle=|A|^2.
$$

When a component is parameterized by $u$, a contact to $d_i+u\omega^j$ gives this equation with normal $A\omega^{-j}$ and unknown $u$.

For each of the 36 placements the 54 source normals fall into exactly 36 rotation classes: 18 singleton and 18 double classes. If three component incidences had all their rotated normals identical, each source normal could account for at most one of those incidences, and the corresponding class would have multiplicity at least three. This is impossible. Therefore every important component has a pair of nonparallel contact normals, unless a parallel pair with distinct normals is compatible.

The latter exception cannot occur. If $A' = tA$ with both nonzero, simultaneous contact equations require $t=t^2$, hence $t=1$. Parallel compatible normals are exactly identical normals. This also handles negative multiples.

Collect the canonical normal representatives over all 36 placements. There are still only 36 representatives. Canonicalization uses the lexicographic order of exact coefficient vectors, which is only a labelling convention and need not agree with real numerical order. The union includes every source normal from $F$.

It suffices to examine all

$$
\binom{36+1}{2}\cdot6=3996
$$

representative-pair/relative-rotation cases. Equal representatives are included: two contacts from the same source may lie in one sixfold orbit. A simultaneous rotation of both equations only rotates the solution direction, and swapping the two equations loses no cases.

For nonparallel normals $A,A'$, the two linear equations have a unique solution over $K=\mathbb Q(\sqrt3,\sqrt{11})$ in each Cartesian coordinate. The producer solves those equations exactly. The independent checker instead uses the unit-circumradius criterion

$$
|A|^2|A'|^2|A-A'|^2=4\det(A,A')^2
$$

and then checks the certificate's unit direction against both original linear equations. The determinant is separately required to be nonzero. The complete outcome table is:

| Case | Number |
|---|---:|
| Identical normals | 36 |
| Parallel incompatible normals | 78 |
| Nonparallel with nonunit circumcentre | 3,742 |
| Nonparallel with unit circumcentre | 140 |
| Total | 3,996 |

All 140 unit witnesses lie in precisely the three orbits with canonical representatives

$$
-1,\quad -\rho,\quad \sigma.
$$

The first is the exceptional patch direction. Thus only $Q(-\rho)$ and $Q(\sigma)$ can be important for any $W_{ab}$, or for any $W\subseteq F$ satisfying the corollary's normal multiplicity condition. Actual edge enumeration confirms that both are important in all 36 placements.

This is **not** an enumeration of every circle intersection in $K$, nor an assumption that all contacts lie in $K$. Contacts in larger fields can occur. Under the stated multiplicity hypothesis their components have at most two exterior incidences, because any nonparallel pair would uniquely force a solution in $K$. The restoration argument covers them.

The subset bound follows because each point contributes three source normals, while at most two normals occupy each of 36 classes: $3|W|\le72$. No new subset enumeration is needed.

## One positive certificate for all cases

Construct the finite graph induced by

$$
M=P\cup F\cup Q(-\rho)\cup Q(\sigma).
$$

There are 156 distinct vertices and exactly 690 unit edges. Every coordinate has denominator 12 in the basis $1,\sqrt3,\sqrt{11},\sqrt{33}$, separately on each Cartesian axis. The checker reconstructs all points, checks all 12,090 unordered squared distances, and checks a single proper four-colouring with centre colours $0,1,2$.

Every required core is an induced subgraph of $M$, so restrict that colouring and extend the omitted generic components. The same reasoning proves the subset corollary. For completeness the checker also inspects all 36 restricted cores directly, totalling 7,260 edge checks.

| Quantity | Verified values |
|---|---|
| Exterior vertices per placement | 18 |
| Important generic components | 2 |
| Important-component incidence counts | (17,15) in 18 cases; (19,15) in 18 cases |
| Core vertices | 66 in all 36 cases |
| Core edges | 200 in 12 cases; 202 in 18 cases; 204 in 6 cases |
| Edges between the two exterior nine-cycles | 0 in 24 cases; 2 in 12 cases |
| Shared finite positive certificate | 156 vertices, 690 edges |

The 36 ordered orientation pairs are the exact finite domain. Each constituent exterior block is independently checked to be a connected nine-cycle. No assertion of 36 nonisomorphic graphs is made.

A positive four-colouring of $M$ does not alone colour $X\cup F$. The full $F$ has normal classes with multiplicities above two, so some extra generic components may be important without a nonparallel pair. The present claim deliberately retains the multiplicity hypothesis for the subset corollary. The larger full support has not been decided.

## Reproduction and evidence boundary

From the repository root, using Python 3.11.2 or a compatible Python 3 with only the standard library:

```sh
python3 -B hadwiger_nelson_triangle_coupled_orbits/build.py --out /tmp/hn-coupled-orbits
python3 -B hadwiger_nelson_triangle_coupled_orbits/verify.py --work /tmp/hn-coupled-orbits
```

The output directory must be new. [build.py](build.py) deterministically regenerates [certificate.json](certificate.json) and requires a byte-for-byte match with the publication. [verify.py](verify.py) independently reconstructs the fixed geometry, uses sparse squarefree-radical arithmetic, and applies the circumradius identity rather than the producer's field inversion. It imports neither the producer nor parent executable code. [expected.json](expected.json) contains the checked result; [validation.json](validation.json) records timings and provenance; [SHA256SUMS](SHA256SUMS) authenticates the public inputs.

The compact certificate is 19,427 bytes, with SHA-256

```text
8680dc794ddb0543fd89f93fa61e6119521ebba51c422a74c4eae0dcf7f5a23a
```

The positive row was discovered by deterministic Python backtracking in 176 recursive nodes. Its correctness is checked directly on all edges, so solver search correctness is not a proof dependency. There are no native solver calls, floating-point geometry, external coordinate inputs, omitted large traces, or unresolved negative certificates. The checker rejects five mutated certificates: a missing normal representative, a missing positive contact witness, a missing important component in a case row, a missing shared edge, and an improper colouring. Its normal and `python3 -O` reports agree byte for byte. The analytic circle decomposition and restoration theorem are imported from the linked public parent results; this pass supplies author-run independent computational validation, not external peer review or formal proof.

## Research context and stopping decision

The record target is a five-chromatic Euclidean unit-distance graph with at most 508 vertices. [Parts's primary paper](https://arxiv.org/abs/2010.12665) gives 509 vertices; the introduction of [Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4) still names 509 as the record. Both were checked live on 2026-09-06. No record improvement or priority claim is made here.

This pass closes the specified 36 placements and the stated admissible-subset family. It uses exact geometric contacts and full four-colouring, not a restricted residue-permutation test. It is separate from the teammate's [H632 fixed-library transport](../hadwiger_nelson_heule632_transport/README.md); that work, now [independently accepted](../hadwiger_nelson_heule632_transport_review1/README.md) as a frozen-library classification, supplies coordination context but no mathematical premise here. Its22 successful transported rows do not close the whole H632 support.

The natural next bounded question is whether the higher-multiplicity identical-normal components in the **fixed** 108-point simultaneous support extend the shared finite colouring, with full 11-state component colouring where necessary. That phase has not started. The current two-orbit contact census already shows why simply adding the second cycle in another one of these orientations does not open a new generic component. Further support or parameter changes require a subsequent construction phase.
