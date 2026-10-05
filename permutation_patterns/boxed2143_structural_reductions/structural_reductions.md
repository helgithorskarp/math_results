# Structural reductions for the agreed boxed2143 growth question

Author: Theo, literature-researcher-4. Target remains decision410. Status: written elementary arguments with finite controls; a different researcher's independent check is pending. These do not settle the growth question. Skew sums, unique skew factorization, and the supermultiplicative limit argument are standard mechanisms; no priority claim is made.

## 1. Skew components isolate the unresolved entropy

For p in S_m and q in S_n define p skew-sum q by first listing p with every value increased by n and then listing q. Every point in the first block lies above every point in the second block.

**Lemma 1.** Every boxed2143 occurrence in a skew sum lies wholly inside one block; its occurrence set is the disjoint union of the two blocks' occurrence sets, with the second block's positions translated by m. Consequently the skew sum avoids boxed2143 exactly when both blocks do.

**Proof.** If selected points occur on both sides of the skew boundary, the first r selected values, for some r=1,2,3, must be the largest r of the four values. The prefixes of2143 have rank sets {2}, {2,1}, and {2,1,4}, respectively; none is the set of the largest r ranks. Thus even a classical2143 occurrence cannot cross that boundary. A selected quadruple wholly inside one block has the same value order and the same interior points in its bounding rectangle as in the original block, since the other block is horizontally outside that rectangle. This proves both assertions. The argument applies across every boundary in a skew sum of any number of blocks.

A skew cut after k entries of a permutation of size n is a prefix whose values are exactly the largest k values. Such cuts are intrinsic and all may be taken simultaneously, producing the unique finest factorization into nonempty skew-indecomposable permutations. Each factor's values form an interval, and standardization subtracts a constant. If a factor had a further skew cut, it would also be a cut of the whole permutation, contrary to taking all cuts. Conversely any skew factorization can cut only at these intrinsic boundaries. Thus the finest factors are unique.

Let b_n count skew-indecomposable boxed2143 avoiders of size n>=1, and set a_0=1. Lemma1 and unique factorization imply

    a_n = sum_{k=1}^n b_k a_{n-k},
    A(z) = 1/(1-B(z))

as formal power series, with A(z)=sum_{n>=0} a_n z^n and B(z)=sum_{n>=1} b_n z^n. This is a coefficient identity, not an analytic convergence assertion.

**Lemma 2.** The agreed bounded-exponential question for a_n is equivalent to bounded-exponential growth of b_n.

**Proof.** If a_n<=C^n then b_n<=a_n<=C^n. Conversely suppose b_n<=D^n for all n>=1, increasing D to at least1 if necessary. For a fixed composition n=k_1+...+k_r, the number of factor choices is product b_{k_i}<=D^n. There are2^{n-1} compositions of n, so a_n<=2^{n-1}D^n<=(2D)^n. Every object is counted once by the unique factorization. This proves the equivalence without changing the agreed target.

In particular, a family made only from a fixed finite set of skew blocks has at most exponential growth. It cannot settle the negative answer by varying only the sequence of those blocks. Any lower-bound lane using skew sums must supply increasingly complex indecomposable blocks or some other source of unbounded entropy.

**Lemma 3.** The extended limit of a_n^{1/n} exists and equals sup_{m>=1} a_m^{1/m}, possibly infinity.

**Proof.** Fixed-size skew summation is injective, hence a_{m+n}>=a_m a_n. Also a_n>=1. For fixed m write n=qm+r,0<=r<m; repeated skew summation gives a_n>=a_m^q a_r>=a_m^q. Therefore liminf log(a_n)/n>=log(a_m)/m. Taking the supremum over m and using the defining upper bound log(a_n)/n<=sup_m log(a_m)/m gives equality of liminf and limsup when the supremum is finite. If it is infinite, the fixed-m lower bound exceeds any prescribed finite rate after choosing m and then taking n sufficiently large. Exponentiating gives the stated extended limit. This standard supermultiplicative argument strengthens the limsup formulation but supplies no unbounded rate by itself.

## 2. Increasing-block inflation cannot repair arbitrary input

Given p in S_m and positive integer sizes s_1,...,s_m indexed by position, replace p_i by an increasing block of size s_i. Blocks occupy consecutive position intervals and consecutive value intervals, ordered in value as the entries of p. Call the resulting permutation I_s(p).

**Lemma 4.** Boxed2143 occurrences of p and I_s(p) are in bijection. If an original occurrence occupies blocks (i_1,i_2,i_3,i_4), its unique lift selects the last entry of blocks i_1 and i_2 and the first entry of blocks i_3 and i_4. Consequently occurrence counts are preserved for every positive size vector, and I_s(p) avoids boxed2143 if and only if p does.

**Proof.** A classical2143 occurrence in I_s(p) uses at most one entry from any increasing block. Two entries from the same block must be adjacent in the selected subsequence, because other blocks are horizontally disjoint. The only adjacent ascent of2143 is between its second and third selected entries, the minimum and maximum. If those belonged to one block, the first and fourth selected values would have to lie strictly between them, impossible for entries in different, disjoint value blocks. Three or more entries in one block would contain an increasing three-term subsequence, which2143 does not have.

Thus an inflated occurrence projects to four distinct blocks in2143 order. If an unselected original point lay inside their bounding rectangle, its entire block would lie strictly between the selected blocks in position and strictly between the second and third selected value blocks. It would supply an extra point in the inflated rectangle. Hence every boxed inflated occurrence projects to a boxed original occurrence.

For a fixed projected occurrence, the first selected block must contribute its last entry: any later entry in that block would lie horizontally inside the selected rectangle and vertically between the minimum block and maximum block. The fourth block must contribute its first entry for the analogous reason with earlier entries. In the second block, which supplies the minimum, any entry after the selection would be vertically inside the rectangle, so it too must contribute its last entry. In the third block, which supplies the maximum, an earlier entry would be inside, so it must contribute its first entry.

These forced choices are also sufficient. The remaining points of the first/fourth selected blocks lie horizontally outside the rectangle; remaining points of the minimum/maximum selected blocks lie vertically outside. Every other block between the first/fourth blocks lies vertically outside, because the projected occurrence is boxed. There are no extra interior points. Projection and this forced lift are mutually inverse, proving the claim.

The all-sizes-equal2 case is the published occurrence-preserving doubling [Kitaev–Qiu–Xu, Proposition7.6](https://arxiv.org/html/2609.13764v1). The proof above checks the arbitrary-positive-size version directly. A targeted search for boxed2143 increasing inflation found the doubling source and general mesh-pattern literature but no matching exact all-sizes statement; this does not establish novelty. The result's role is a uniform obstruction to one potential completion method: changing increasing block lengths alone cannot turn a general input permutation into an avoider. It does not refute flexible interleaving/completion constructions that place points between different blocks in rank or position.

## Reproducible controls and limits

`structural_checks.py` exhausts labelled permutations through a stated finite length to compare component occurrence sets and the counting recurrence. It also checks the forced occurrence lift for all permutations through base length5 and all positive size vectors with entries1 or2. One unequal-size fixture uses sizes(1,2,3,4). These controls can falsify the written reductions; they are not the universal proofs. The reduction argument, Python interpreter and code remain the trust base pending a different researcher's check.

Every lemma is partial infrastructure or negative evidence. A bound on b_n or an unbounded-rate family of indecomposable avoiders is still missing. Target410 is not solved, no completion request is justified, and no public source or graph contribution has been submitted for this packet.
