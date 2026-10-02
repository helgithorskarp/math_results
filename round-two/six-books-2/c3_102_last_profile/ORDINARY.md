# A summed row obstruction before host search

Actual author **six-books-2**, role **researcher**. The argument is ordinary
mathematics, with same-author exact corroboration. It is unformalized and
independent review is pending. No search result is a premise of this lemma.

Let G be a simple22-vertex red graph with red-edge common-neighbor cap3 and
off-diagonal blue-edge common-neighbor cap6. Let x have degree9, A=N_G(x),
and B be the twelve other vertices. Suppose A=L union U, where |L|=6,|U|=3,
every L vertex has global degree8 and H=G[A] degree3, every U vertex has
global degree10 and H degree2, and U is independent in H. Suppose the
twelve columns N_G(b) intersect A, b in B, have ranks3^3,4^9.
Then such a graph does not exist. **This local statement needs no host
automorphism.** Its explicit neighborhood/rank hypotheses are essential.

Put X_a=N_G(a) intersect B and Gamma_a=|X_a|=d(a)-1-d_H(a).
Thus Gamma_a=4 on L and7 on U. For an A pair the ordinary page conditions give

    |X_a intersect X_c| <= lambda_ac,
    lambda_ac = 2-c_H(a,c)                    on a red pair,
                d(a)+d(c)-15-c_H(a,c)        on a blue pair.

The red bound subtracts the known page x. The blue pages in A and B are
7-d_H(a)-d_H(c)+c_H(a,c) and12-Gamma_a-Gamma_c+|X_a intersect X_c|.
All page edges remain unrestricted: these are ordinary books.

For a in L sum the diagonal and all eight pair bounds. The full upper row is

    Gamma_a + sum_(c!=a) lambda_ac
      = D_A+8d(a)-121+d_H(a)(17-d(a))
        - sum_(c in N_H(a))(d(c)+d_H(c)),

where D_A=78. Its initial scalar is48. An H-neighbor in L contributes11
and an H-neighbor in U contributes12. If k_a=|N_H(a) intersect U|, its row
upper is therefore15-k_a. The diagonal Gamma_a is retained.
Since U is independent and its three degrees are2, sum_(a in L)k_a=6.
Consequently the summed full row upper on L is **90-6=84**.

On the other hand, if alpha_b is the rank of column b and n_b is its number
of L neighbors, the actual full Gram row sum on L is

    sum_(a in L)(Gamma_a+sum_(c!=a)|X_a intersect X_c|)
       = sum_(b in B) alpha_b*n_b.

There are24 L incidences in total. All but three columns have rank4, so

    sum_b alpha_b*n_b = 4*24 - sum_(alpha_b=3)n_b
                      >= 96-3*3 = **87**.

This contradicts84. A separate complete finite column-load DP corroborates
the lower87 even after forgetting every incidence relation except the
total load and column ranks; no numerical LP is used.

## Application to the complete P2 root reduction

P2 is the exact global degree multiset8^6,9^4,10^12 with an actual
automorphism of cycle type3^7 1. Its fixed point has degree9, and the seven
free orbit degrees are8,8,9,10,10,10,10. Counting at the root gives

    |E(G)|=102, k=102-D_A+h, D_x=171-2D_A,
    max_degree(H)<=3, h multiple3 and h<=12, minimum_degree(K)>=5.

Every root choice and whole marked column-load domain is reconstructed by
root_capacity.py and independently by capacity_audit.py. The full A-pair
capacity identity is

    C_H=17h-540+8D_A-sum_a d_H(a)*d(a)-sum_a binom(d_H(a),2).

The actual total intersection load is3 sum_j binom(alpha_j,2), so it cannot
exceed C_H. All h<12 and the8,8,9 root choice close by this capacity bound.
The only rank cases left by the full table are:

|A degrees|B degrees|alpha|capacity upper|actual pair load|
|---|---|---|---:|---:|
|8,8,10|9,10,10,10|3,4,4,4|63|63|
|8,8,10|9,10,10,10|4,3,4,4|63|63|
|8,9,10|8,10,10,10|3,3,5,5|78|78|
|8,9,10|8,10,10,10|3,4,4,5|78|75|
|8,10,10|8,9,10,10|3,4,5,5|93|87|

At A=8,8,10 and h12, the three orbit degrees of H sum to8 and each is
at most3, so they are a permutation of(3,3,2). The capacity is63 only when
the degree10 orbit has H degree2; the other two vectors give57. Thus the
two rank cases force H degrees3 on L and2 on U.

The three U points are a single C3 orbit. If there is an internal U edge,
all three U edges are red. Each U row then has Gamma=7. A pair has at least
7+7-12=2 common B neighbors, plus the known pages x and the third U point,
giving at least4 red pages against cap3. Hence U is independent. The two
cases have the physical column-rank multiset3^3,4^9, and the ordinary lemma
above applies to both, independently of their different outside degree marks.

The root domain initially caught a fifth rank case missing from the author's
four-case prediction. Both complete algorithms include3,3,5,5, and the
failed incomplete attempt is preserved privately. No zero or exclusion was
inferred from that failure. The two closed8,8,10 cases leave **three** exact
marked cases for fresh physical incidence/host analysis. Prior P1 completion
verdicts and peer review verdicts are not inputs to this reduction.
