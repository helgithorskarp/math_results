# A homogeneous A5 pencil needs a binomial event

Let E=Z[omega], where omega=(1+i sqrt(3))/2, and let T={0,1,omega}. The physical architecture is the fixed-scale set

    A5(z)=T+zT+z^2T+z^3T+z^4T.

An event row (a1,a2,a3,a4), with each coefficient zero or an Eisenstein unit, represents

    |a1 z+a2 z^2+a3 z^3+a4 z^4|=1.

The absent constant coefficient makes this a homogeneous event in the four formal coefficient positions. A binomial event has exactly two nonzero coefficients. The actual radix exponents here are precisely1,2,3,4. The theorem does not apply to arbitrary four exponents, four arbitrary complex input vectors, or an extra independent dilation.

Reduce E modulo 2 to F4=F2[t]/(t^2+t+1), with t the residue of omega. The five projective directions in any two-dimensional subspace of F4^4 form a full homogeneous F4 pencil. Each direction is lifted independently to an Eisenstein-unit event row; rows differing by a common unit give the same norm event.

## 1. Main result and physical scope

**Exact computer-assisted theorem.** Every simultaneously active full homogeneous F4 pencil of five nonmonomial unit events in A5 contains a binomial event.

Equivalently, the 54 homogeneous pencils without a binomial section, and all 110,592 unit-row lifts of them, have no physical concurrence. In fact their five norm equations have no common affine zero even when x,y are independently complexified in z=x+i sqrt(3)y.

The initially selected asymmetric h4195 pencil 2320 is

    ((0,1,1,1),0), ((1,0,1,2),0), ((1,1,0,3),0),
    ((1,2,3,0),0), ((1,3,2,1),0).

The notation is (normal,constant), using0,1,2=t,3=1+t in F4. Its six images under z -> omega^2 z and complex conjugation have residual indices 2320,4448,3768,2324,4452,3772. Its stabilizer is trivial. All54 pencils are treated explicitly, without a parameter quotient or a fundamental chamber.

There is a separate nonvacuous physical classification. For each pencil, order its five curve buckets by (bucket size, ascending curve-ID list), and take every pair across the first two buckets. The resulting864 distinct pairs define an explicit anchor envelope containing every possible full concurrence. Their complete intersections yield907 distinct irreducible rational component records;885 have real embeddings, representing2,988 distinct real parameters z. Every complete physical unit-distance graph on A5(z) at those parameters has chromatic number exactly 3.

| Physical points | Unit edges | Parameters |
|---:|---:|---:|
|243|297|2928|
|243|378|8|
|243|351|8|
|240|564|2|
|240|561|2|
|219|249|6|
|216|243|6|
|171|234|4|
|159|210|4|
|129|195|8|
|84|312|6|
|27|63|3|
|21|45|3|

There are44 collision parameters, including32 off the unit circle. The twelve unit-circle parameters are precisely the roots of z^12=1. The remaining 2,944 parameters have243 distinct points. At2,928 parameters exactly two norm events are active; the other60 have additional events, up to811. Thus the result includes substantial higher-incidence and collision cases. It is not restricted to exactly five active curves or to injective digit configurations.

The anchor envelope is larger than the set of possible full-pencil concurrences. It is not every pair of homogeneous events or the whole A5 parameter plane. The intrinsic54-pencil theorem and the explicit2,988-parameter physical classification have these separate scopes.

## 2. The 54 pencils form the entire intrinsic class

Represent a two-dimensional row space by a rank-two2x4 generator matrix. Its four columns are vectors in F4^2. If a column were zero, a nonzero row combination annihilating another column would have at most two nonzero coordinates. If two nonzero columns had the same projective direction, the combination annihilating that direction would again have support at most two. These cases are incompatible with a pencil having no monomial or binomial direction.

Conversely, four nonzero columns with distinct projective directions have precisely four row directions of support three and one of support four: each column kernel gives one zero coordinate, and no row direction can annihilate two columns. Hence every pencil in the target class has support profile3,3,3,3,4.

There are five directions in P1(F4). Choose four ordered, distinct directions and independently choose one of three nonzero scales for each column. This gives

    (5*4*3*2)*3^4 = 9,720

generator matrices. Each row space has |GL(2,4)|=(4^2-1)(4^2-4)=180 ordered bases, and every such basis retains the distinct-column property. Thus there are9,720/180=54 target pencils.

Two different exact enumerations check this entrywise. `interface.py` generates all 357 rank-two row spaces through their unique reduced row-echelon matrices and selects the 54 with minimum support at least three. The standard-library-only `classification.py` instead enumerates the 9,720 scaled projective-column matrices, finds exactly 180 copies of each row space, and checks the same54 literal pencils. These are different finite classification routes, not two aggregate count assertions.

A support-three direction has four unit-row lifts up to a common Eisenstein unit, and a support-four direction has eight. This follows from the two unit lifts, differing by sign, of each nonzero F4 entry after fixing one coefficient. The bucket reconstruction from the norm inventory verifies every actual lift. Each pencil therefore has4^4*8=2,048 lifts; all 54 have110,592 in total.

All54 intrinsic pencils occur in the h4195 residual. The optional residual input checks its pinned hash and all 54 index/signature records. The theorem itself does not need the residual's global accounting: the intrinsic enumeration proves completeness directly.

## 3. Exact algebraic concurrence gate

The h4105 norm inventory is regenerated and pinned by canonical SHA256
`85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.
Its2,797 primitive event curves include the radial circle event342; the other2,796 have individual nonmonomial row signatures. The selected54 homogeneous pencils have bucket sizes4,4,4,4,8.

Any common zero of all five selected event equations is a common zero of one of the 16 anchor pairs for that pencil. Across the 54 pencils there are864 distinct pairs. The exact solver decomposes every such affine intersection over Q. A component is encoded by an irreducible q(s) and exact rational polynomials x(s),y(s), reduced modulo q.

The two complete elimination routes are:

1. A lexicographic Groebner basis over Q, with y>x, followed by factoring the x-eliminant and solving linear algebraic fibers. Every exceptional rational vertical fiber is factored separately using the original equations.
2. The resultant Res_y(f,g), followed by exact polynomial gcds in (Q[x]/q)[y] above every irreducible resultant factor. Constant fiber gcds represent spurious resultant factors with no affine point. Rational vertical fibers are factored in y. Nonzero resultants are required.

Both routes stop on a whole vertical component or an unsupported nonlinear nonrational fiber. None occurs in these 864 pairs. Both account for leading-coefficient drops and all rational exceptional fibers. They produce identical complete canonical root tables, not merely matching root counts.

Completeness follows because every common affine zero makes the resultant vanish, and the fiber gcd describes all common zeros above each such x. The Groebner route supplies a different elimination check of the same exact data. No real-root filter is used for the complex concurrence decision.

Every component is substituted into all 2,797 norm-event polynomials. For every component of every selected anchor pair, at least one of its pencil's five sections has no vanishing event. Thus no choice of one event from each section can concur. The 1,852 component records counted with source-pair incidence are all checked; they are not1,852 distinct parameters.

Every physical z corresponds to real x,y and therefore lies in the complexified affine zero set if it is concurrent. Its emptiness proves the main theorem. Additional active curves do not change this implication.

## 4. Real components and actual graphs

The exact real roots of each irreducible q are counted over Q. There are885 components with real embeddings and 22 with none. Only the former are decoded as physical points.

The canonical representation uses x=s, or a rational x with y=s, with rational points normalized separately. It therefore separates the roots of each q. Distinct component records are disjoint: their irreducible coordinate factors differ, or their reduced other-coordinate polynomials differ modulo the same irreducible factor. Rational duplicates across source pairs are also merged canonically. This justifies counting2,988 distinct real parameters rather than root appearances or symmetry allowances.

An exact coordinate pair (a,b) means a+i sqrt(3)b, with a,b in Q[s]/q. Multiplication is

    (a,b)(c,d)=(ac-3bd,ad+bc).

The direct checker generates all 243 ternary digit words, forms the physical points in A5(z), merges exact coordinate equalities, and tests every pairwise squared norm against one. The squared norm is a^2+3b^2. No tolerance or event-edge ownership table is used for this graph check.

Because q is irreducible, a reduced nonzero polynomial cannot vanish at only one of its roots. Thus coordinate coincidences and all unit-distance predicates are valid at every real embedding of a component. The resulting physical graph, collision quotient, edge hash and point count are checked against the generated certificate. This construction is independent of the producer's event-owned edge union.

## 5. Positive colourings, including zero positional weights

For a digit word (t0,...,t4), where0,1,2 denote0,1,omega, the certificate gives weights w0=1 and w1,...,w4 in F3 and the colour

    sum_j wj tj  (mod 3).

Ten weight vectors suffice for the whole real catalogue. At a unit-circle parameter all radix steps are unit lengths, so the search requires every weight to be nonzero. Away from that circle, a zero positional weight can be valid: the corresponding single radix step need not be a unit edge. Every claimed colouring is checked against the actual graph; this heuristic distinction is not a substitute for verification.

The checker verifies that coincident labels get the same colour and that every directly computed unit edge is proper. This gives chi<=3. The distinct physical points0,1,omega always form a unit triangle and give chi>=3.

The eight129-point/195-edge parameters provide a useful boundary for the colour search. Their four irreducible component records each have two real embeddings. A control exhausts all 81 normalized positional weight choices on one such graph: exactly three work, and none has all five weights nonzero. The final certificate uses(1,0,1,2,2) or(1,0,1,1,2), depending on the component. These are ordinary positive three-colourings, not an UNSAT conclusion about all possible colourings. The failed all-nonzero search is explicitly narrower than a chromatic decision.

An exploratory SAT search first found the exceptional positive colourings. Expanding the positional weight domain produced the final solver-free witnesses. No SAT solver or UNSAT claim is required to generate or verify the published evidence.

`boundaries.py` additionally checks exactly that the twelve unit-circle parameters satisfy z^12=1. Their complete graphs have84 points at six parameters,27 at three and 21 at three. Together with the exact count this identifies the entire unit-circle part of the anchor envelope.

## 6. Validation, dependencies and limits

The main theorem is an exact computer-assisted result with written, unformalized reductions. SymPy 1.14.0, python-flint 0.8.0, the accepted norm inventory, and shared canonical field/physical arithmetic helpers from the earlier C0 package are explicit trust boundaries. Different elimination and graph-construction algorithms are author validation, not independent-author review of this result.

The complete54-pencil classification also has a standard-library-only independent column audit. Positive collision controls and six corruptions test real-root counts, collision colours, physical unit edges, active events, exceptional component coverage and invented concurrence. The full root table is generated locally and is not committed; source, compact expected output and hashes are published.

The selected residual export has canonical SHA256
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
The h4171 full-pencil framework explains the construction-search relevance. The earlier three-power and cubic-anchor theorems guided selection but are not mathematical premises here. The h4117/h4175/h4177 aggregate accounting remains conditional, unused and unchanged.

An optional triple-ideal audit was stopped after a poor runtime benchmark; its partial output is not a proof dependency. An early producer using only nonzero positional weights failed on the 129-point collision graph and was replaced by the verified larger weight domain. Both boundaries are retained in the research report rather than converted into exclusions.

This theorem constrains homogeneous full pencils in the fixed A5 architecture. Pencils containing a binomial event, nonhomogeneous pencils and more general plane constructions remain outside its scope. It does not close A5, give a five-chromatic realization, or improve Parts'509-vertex record.
