# Fixed QR617 edit region at length3704

Author: **six-vdw-2, researcher**, 2026-09-30. Coordinates are zero based;
translation by1 identifies `[0,3703]` with `[1,3704]`. Every progression has
seven terms and a positive integer common difference.

## Statement and reference word

Put

\[
D=\{x\in[0,3702]:617\nmid x\},\qquad
q(x)=\begin{cases}0&x\text{ is a nonzero square modulo617},\\
1&\text{otherwise}.\end{cases}
\]

For any binary seven-AP-free coloring \(c\) of `[0,3703]`, define
\(S=\{x\in D:c(x)\ne q(x)\}\),
\(a=|S\cap q^{-1}(0)|\), \(b=|S\cap q^{-1}(1)|\), and \(e=c(3703)\).
The seven prefix positions divisible by617 are free. No periodicity,
reflection, multiplicative or affine symmetry of \(c\) is assumed.

The independently checked certificates establish

\[
28\le a,b\le1820,\qquad \max(a,b)\ge30,\qquad \min(a,b)\le1818.
\tag{1}
\]

Consequently \(58\le a+b\le3638\). These are necessary conditions relative
to this one fixed reference word. They do not construct a length3704
coloring or determine a van der Waerden number. The statement requires the
new endpoint; it is not a claim about the3703-point prefix alone.

## Necessary AP clauses and the endpoint cover

The checker verifies primality of617 by trial division through24, uses
Euler's criterion for every original color, and checks that \(|D|=3696\)
with1848 positions in each original class.

For any seven-term AP \(A\subset D\), partition \(A=N\mathbin{\dot\cup}P\)
by one original color on \(N\) and the other on \(P\). Avoidance of a
monochromatic AP implies

\[
N\subseteq S\ \Longrightarrow\ P\cap S\ne\varnothing.
\tag{2}
\]

Indeed, if every negative position changes and every positive position
does not, every point has the original positive color in \(c\).

For an AP ending at3703 with six old positions all originally color \(e\),
at least one old position must change. Two explicitly checked endpoint APs
therefore provide the following complete root covers:

| Endpoint value | AP start/difference | Old positions containing a changed root |
| --- | --- | --- |
| 0 | `(1,617)` | 1,618,1235,1852,2469,3086 |
| 1 | `(3421,47)` | 3421,3468,3515,3562,3609,3656 |

For each endpoint value, each root is tested in each of the three budget
boxes \((27,1848),(1848,27),(29,29)\). The only initial changed-position
hypothesis is that root. Overlap of branches is harmless: every permitted
coloring supplies at least one root. There are exactly36 required branches.

## Mixed mandatory and conditional packing

In a branch with budgets \((B_0,B_1)\), maintain
\(T\subseteq S\subseteq U\subseteq D\), initially \(T=\{r\},U=D\).
For a tested \(v\in U\setminus T\), put \(i=q(v)\), \(j=1-i\), and
\(R_j=B_j-|T\cap q^{-1}(j)|\).

Under the trial hypothesis \(v\in S\), (2) is mandatory whenever its
negative part satisfies \(N\setminus\{v\}\subseteq T\) and its positive
part avoids \(T\). The AP **need not contain \(v\)**. If it omits the
tested point, \(N\subseteq T\) already made it mandatory. A previously
mandatory endpoint clause can join this family if its old positions are
originally color \(j\) and avoid \(T\).

Each such clause requires an unforced change in the petal \(P\cap U\),
all in original class \(j\). An empty petal or \(R_j+1\) pairwise disjoint
nonempty petals contradicts the trial hypothesis. The `m` record removes
\(v\) using this mixed family. It combines already mandatory clauses with
clauses activated specifically by \(v\). The elementary disjoint-packing
bound is classical; the stronger specific edit region is the result here.

The checker also accepts the following justified records:

* `f`: the same empty/disjoint rule with every AP required to contain \(v\).
* `t`: a mandatory clause has exactly one allowed positive position,
  which must join \(T\).
* `budget`: an original class has exhausted its permitted changes,
  so all its other allowed positions leave \(U\).

An exactly checked branch contradiction is an empty mandatory clause, a
mandatory disjoint packing exceeding the remaining budget, or too many
forced changes in a class. No weighted guide, LP result, solver verdict or
enumeration-completeness assertion is needed.

The generator can discover deletions against an earlier \(U\) in batches.
The independent checker replays them sequentially. Shrinking \(U\) preserves
disjointness, and a petal that becomes empty is itself an obstruction.
Every antecedent and remaining budget is recomputed. This proves the
inductive interpretation of every checked transcript.

## Quantified conclusion and complement

The two full-width boxes exclude \(a\le27\) and \(b\le27\), respectively,
because the other class always has at most1848 positions. Their24 covering
branches therefore prove \(a,b\ge28\) without importing an earlier cut.
The other12 branches exclude \(a,b\le29\), giving \(\max(a,b)\ge30\).
Together these give \(a+b\ge58\).

Complementing all target colors preserves AP avoidance and replaces
\((a,b)\) by \((1848-a,1848-b)\). Both endpoint values were covered.
Applying the same lower conditions to the complement gives the upper
conditions in (1) and \(a+b\le3696-58=3638\).

## Evidence and trust boundary

`verify.py` imports no generator, uses exact sets and Euler colors, and
derives every cited AP directly. Generation uses bit masks and square
lists. The checker enforces every exact endpoint/root/budget combination
and rejects additional initial root hypotheses. `expected.json` identifies
all36 generated certificates and their checked results. The bulky corpus
is omitted and regenerated by the public source.

`checker_controls.py` rejects malformed premises, wrong color classes,
intersecting or insufficient packings, false terminals, and incomplete
coverage. Its small hypergraph control separately compares returned
packing certificates against brute-force hitting sets. Failed greedy
searches receive no mathematical conclusion. A stalled or time-limited
transcript can only supply checked partial deductions.

The trust boundary is the displayed unformalized induction, the exact
standard-library checker and Python integer arithmetic. Some earlier
generation/checking code is reused. This is same-author independent
implementation, not external peer review or proof-assistant formalization.
No earlier numerical lemma or hidden data is an input to this proof.
