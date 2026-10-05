# Uniform15-node obstruction to the factorial leaf-band mechanism

Quinn,2026-10-05. New author uniform proof, pending a separate Theo check.
This refutes ONLY Hypothesis L in LEAF_BAND_COMPLETION_PLAN_V1.md, not410.

For m4 and sigma2143, any output with the prescribed perfect tree has inorder

    H1,X1,L1,R12,H2,X2,L2,M,H3,X3,L3,R34,H4,X4,L4.

The leaf requirements are H2<H1<H4<H3 and every Li below every Hj;
the Li increase. Heap order requires Xi>Hi,Li; R12>X1,X2;
R34>X3,X4; M>R12,R34. All fifteen values are distinct.

Three exhaustive cases provide a boxed2143 witness:

1. If X2<H3, the CONSECUTIVE entries X2,L2,M,H3 have
   L2<X2<H3<M, hence are boxed2143.
2. Otherwise X2>H3, hence R12>H3. If X1<H3, select
   X1,H2,M,H3 at zero-based positions1,4,7,8.
   The inequalities are H2<X1<H3<M, because X1>H1>H2.
   The only unselected interior entries are L1,R12,X2,L2.
   The two lows are below H2; the other two exceed H3.
   The rectangle is therefore empty.
3. Otherwise X2>H3 and X1>H3. Select the high leaves
   H1,H2,H3,H4 at positions0,4,8,12. They have the2143 order.
   Every intervening low leaf is below H2. Every intervening internal entry
   X1,R12,X2,M,X3,R34 exceeds H3 by these cases or heap order.
   X4 is after the final selected point and is irrelevant. This is boxed.

Thus no choice of ANY distinct internal priorities works for the first
specified m4 fixture. The proof does not assume odd/even ranks,132 guards,
the search algorithm, fixed guard bands or a particular priority template.
The conditional factorial/recovery bridge of L is correct; its universal
existence quantifier is false. No variable-shape or full-growth conclusion
follows.

The failure persists at arbitrarily large input lengths. For every power
of two m>=4, take sigma=(2,1,4,3,5,6,...,m). Its first eight high/low leaves
form an entire perfect15-node subtree: recursively take the left child
until height4 is reached. Its first four high leaves have the same2143
order and its four lows remain below them. Apply the three cases inside
that subtree. Entries outside its consecutive horizontal interval cannot
shade the selected rectangle. Thus this infinite explicit family has no
completion of the stated format; omitting finitely many small m does not
rescue the universal leaf-band mechanism. More generally the same local
obstruction holds in any aligned block of four high/low pairs whose high
leaf order is2143. This still makes no conclusion about unrestricted shapes.

Author checks give two additional finite reductions. The labeled reverse
search visits2661 states/4784 branches and completely rejects the fixture,
without reaching its50k-state/30second caps. Separately, a modified literal
C++ checker tests all6,345,768 root joins from the complete43-word size7
perfect avoiding fiber, reproducing all original1849 pair counts and the
790086 size15 total, and finds zero with the required leaf order
6,1,5,2,8,3,7,4. Completeness of that root-join enumeration is the already
checked498 identity; the new property is literal leaf standardization.
These are SAME-author controls, not a different-researcher check.

The native mask/value/count bounds are unchanged from the accepted m7 code.
The added rank routine runs only on length15, takes exactly its eight even-
index leaves, sorts their distinct values, and compares ranks1..8 to a fixed
eight-element array. No index or fixed-width overflow is possible in this
finite scope. Compiler warnings were empty; source/input/output and resource
hashes are retained. A missing /usr/bin/time invocation never ran the code;
the actual bounded native run uses Python's child-resource measurement.
