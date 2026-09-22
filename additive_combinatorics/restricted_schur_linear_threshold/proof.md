# A uniform linear threshold for restricted Schur numbers

For integers $k\geq\ell\geq2$, let $S_2(k;\ell)$ be the least $N$
such that every two-coloring of $[N]=\{1,\ldots,N\}$ has a
monochromatic solution of

$$
x_1+\cdots+x_k=y
$$

with **exactly $\ell$ distinct summand values**. Repetitions among the
summands are allowed; positivity makes $y$ distinct from every summand.
Let $S_2^{\geq}(k;\ell)$ use at least $\ell$ distinct summand values.
Both use the least-forcing-integer convention.

**Theorem.** For every $\ell\geq3$ and $k\geq2\ell+1$,

$$
S_2(k;\ell)=S_2^{\geq}(k;\ell)
=F:=k^2+\left(\frac{(\ell+1)(\ell-2)}2+2\right)k+\ell(\ell-2).
\tag{1}
$$

This is an ordinary combinatorial proof, supplemented by exact arithmetic
checks. The computation is not a premise of the infinite theorem.

Gaiser [1, Theorem 1.1] proves this formula for each fixed $\ell$ and all
sufficiently large $k$, and asks for the optimal threshold in Open Question
6.4. We prove the uniform bound $K(\ell)\leq2\ell+1$, including a linearly
growing distinctness parameter. We do not determine the optimal threshold. In particular, if $k$ and $\ell$
grow with $\ell/k\to\alpha\in(0,1/2)$, then
$S_2(k;\ell)/k^3\to\alpha^2/2$.
The lower construction and the basic color-forcing strategy are from [1].
The new argument uses all small opposite-color values and a compression
estimate to keep every forced value in $[F]$.

## 1. The lower bound

Write

$$
T=k+\frac{(\ell+1)(\ell-2)}2,
\qquad F=k(T+2)+\ell(\ell-2).
$$

Use red on $[1,T]\cup[(k+1)T+1,F-1]$ and blue on
$[T+1,(k+1)T]$. This is Gaiser's construction.

A sum of $k$ small red integers with at least $\ell$ distinct values
is at least

$$
1+\cdots+\ell+(k-\ell)=T+1
$$

and at most $kT$, so it is blue. If a red summand lies in the upper red
interval, the sum is at least

$$
(k+1)T+1+(1+\cdots+(\ell-1))+(k-\ell)=F.
$$

A sum of $k$ blue integers with at least $\ell$ distinct values is at
least

$$
(T+1)+\cdots+(T+\ell)+(k-\ell)(T+1)=(k+1)T+1,
$$

outside blue. These estimates also cover more than $\ell$ distinct
values. Thus both thresholds in (1) are at least $F$.

## 2. Majority prefix and the two generic forced values

Suppose a coloring of $[F]$ avoids an exactly-$\ell$-distinct
monochromatic solution. In $[2\ell-1]$, call the majority color red.
Let $R=\{r_1<\cdots<r_\ell\}$ be its first $\ell$ red values and let

$$
B=\{b_1<\cdots<b_m\}
$$

contain **all** the blue values in that prefix. Put $U=\sum R$.
The cases $R=[\ell]$ and $R=\{1,3,\ldots,2\ell-1\}$ are treated
in Section 5. Otherwise $1\leq m\leq\ell-1$, $v:=b_1\leq\ell$,
and $R$ contains an adjacent pair. Let $a,a+1$ be its first adjacent
pair. Set

$$
q=\ell-m,\qquad u=k-\ell,\qquad S=U+ua.
$$

For $0\leq t<q$, use every element of $R$ once, then $u-t$ more
copies of $a$ and $t$ more copies of $a+1$. This forces $S+t$ blue.
Here $u\geq\ell+1\geq q-1$. Also

$$
S\geq U\geq\ell(\ell+1)/2>2\ell-1,
$$

so these generated values are distinct from $B$.

Using all $m$ elements of $B$, all $q$ generated values, and $u$
extra copies of $v$ forces

$$
V=\sum B+qS+\frac{q(q-1)}2+uv
$$

red. Replacing one extra copy of $v$ with another $S$ forces

$$
W=V+S-v=\sum B+(q+1)S+\frac{q(q-1)}2+(u-1)v
\tag{2}
$$

red. Both sums have $k$ terms and exactly $\ell$ distinct values.
We have $S+q-1<V<W$. Section 3 proves $W\leq F$, so all these
forcing steps are within the coloring's domain.

## 3. Compression estimate: all forced values fit

Define the canonical comparison quantities

$$
a_*=2m+1,\quad
U_*=\frac{\ell(\ell+1)}2+\ell m-\frac{m(m+1)}2,
$$

$$
W_*=(q+1)(U_*+ua_*)+m(m+1)+\frac{q(q-1)}2+2(u-1).
\tag{3}
$$

These are a numerical comparison; the canonical prefix need not itself
belong to the generic case.

**Compression lemma.** If $u\geq\ell$, then $W\leq W_*$.

*Proof.* Before $a$, red values have no adjacent pair, so $a\leq2m+1$.
Put $d=2m+1-a\geq0$. For every $i\leq m$,

$$
2i-d\leq b_i\leq 2\ell-m+i-1=\ell+q+i-1.
\tag{4}
$$

For the lower inequality, if $b_i<a$, the interval $(b_i,a]$ has no
adjacent red pair and has at most $m-i$ blue values. Hence its length is
at most $2(m-i)+1$. If $b_i\geq a$, the same lower bound is immediate.
The upper inequality follows from the $m-i$ later blue values in the
prefix.

Counting the blue values preceding the first $\ell$ red values gives
the exact identity

$$
U=\frac{\ell(\ell+1)}2+
\sum_{i=1}^m(\ell+i-b_i)_+.
\tag{5}
$$

For fixed $i$, the function $g_i(b)=(q+1)(\ell+i-b)_++b$ is convex.
At the endpoints in (4) its values satisfy

$$
g_i(2i-d)=g_i(2i)+qd,
$$

$$
g_i(2i)-g_i(\ell+q+i-1)=q(\ell-i-1)+1>0.
$$

Consequently

$$
(q+1)U+\sum B\leq(q+1)U_*+m(m+1)+qmd.
$$

Substitution into (2) yields

$$
W\leq W_*-D d+(u-1)(v-2),\qquad
D=(q+1)u-qm>0.
\tag{6}
$$

If $a\geq2$, then $v\leq2$, since otherwise 1 and 2 would be the
first adjacent red pair. Equation (6) proves the assertion. If $a=1$,
then $d=2m$ and $v\leq\ell$. Moreover

$$
\begin{aligned}
2mD-u(\ell-2)
&=u((2m-1)q+m+2)-2qm^2\\
&\geq m^2+(2m-1)q^2+2m+2q>0,
\end{aligned}
$$

where $u\geq\ell=m+q$ was used. Thus the negative term in (6)
dominates the possible positive term, proving the lemma. $\square$

It remains to bound $W_*$. Write $k=2\ell+1+h$, $h\geq0$, and
use $\ell=m+q$. Direct expansion gives

$$
2(F-W_*)=P+Q+h((m-q)^2+3m+5q)+2h^2,
\tag{7}
$$

where

$$
P=2m^3-2mq^2+q^3,\qquad
Q=m^2+4mq+4q^2-5m-q+2.
$$

Both are positive for $m,q\geq1$. Indeed, with $x=m-1,y=q-1$,

$$
Q=x^2+4xy+4y^2+x+11y+5.
$$

If $m=q+r$, $r\geq0$, then

$$
P=q^3+4q^2r+6qr^2+2r^3>0.
$$

If $q=m+r$, $r\geq0$, then

$$
P=m(m-r)^2+m^2r+r^3>0.
$$

Therefore $W\leq W_*<F$.

## 4. Closing the generic case

Except for the two triples $\{1,3,4\}$ and $\{1,4,5\}$ when
$\ell=3$, there exists

$$
r\in R\setminus\{a,a+1\},\qquad 0<r-v\leq\ell+1\leq u.
\tag{8}
$$

Here is the full selection argument. If $v\geq3$, then $a=1$, and
the first red value after $v$ belongs to $R$, avoids the pair $1,2$,
and differs from $v$ by at most $m$. If $v=1$, take the first red
value outside the pair: it is at most the third red value, hence is at most
$m+3$. If $v=2$, then 1 is red; take the first red value greater than
2 outside the pair. It is at most the fourth red value, hence is at most
$m+4$. For $\ell\geq4$ it exists. For $\ell=3$, failure to
exist means the first triple is $\{1,a,a+1\}$, with $a=3$ or $a=4$,
exactly the stated exceptions. These bounds give (8).

Put $t=r-v$. Use each element of $R\setminus\{r\}$ once, another
$u-t$ copies of $a$, another $t$ copies of $a+1$, and $V$ once.
There are $k$ red summands and exactly $\ell$ distinct values;
$V>\max R$, and neither adjacent-pair value was removed. Their sum is

$$
U-r+ua+t+V=S-v+V=W,
$$

which is red. This contradiction closes the generic case.

## 5. The special prefixes

In this section, a monochromatic sum forces its result to the other color
under the avoidance assumption. If a result already has its summands'
color, the contradiction occurs earlier and the argument is finished.

### 5.1. The first $\ell$ integers are red

The consecutive values $T+1,\ldots,T+2\ell-1$ are blue. To see this
with only $u\geq2$ extra summands, express each
$j\in[0,2\ell-2]$ as $e+f$, $0\leq e,f\leq\ell-1$. Use
every value in $[\ell]$ once, $u-2$ additional 1's, and the two
additional values $1+e,1+f$. Their sum is $T+1+j$.

The $\ell$ blue values $T+1,\ldots,T+\ell$, with $u$ extra
copies of $T+1$, force $A=(k+1)T+1$ red. There is also a blue sum
equal to $F$. For $\ell=3$, use shifts 1,4,4 and $k-3$ copies of
shift 2, all added to $T$. For $\ell\geq4$, use shifts

$$
1,4,4,7,9,\ldots,2\ell-1
$$

and $k-\ell$ copies of shift 2. The displayed list has $\ell$
entries and sum $\ell^2$; the complete sum is
$kT+2k+\ell(\ell-2)=F$, with exactly $\ell$ distinct values.
Thus $F$ is red. But the red values $1,\ldots,\ell-1,A$, with
$u$ extra 1's, sum to $F$, a contradiction. All values are at most
$F$: in particular $F-A=k+\ell(\ell-3)/2>0$.

### 5.2. The alternating prefix

Here all odd values through $2\ell-1$ are red and all even values
through $2\ell-2$ are blue. Define successively

$$
A=k+\ell^2-\ell,\quad C=3k+2\ell^2-4\ell,
$$
$$
D=4k+3\ell^2-7\ell+1,\quad E=6k+4\ell^2-10\ell+1.
$$

The following sums force the indicated colors:

* All $\ell$ small odd values, and $u$ more 1's, sum to $A$: blue.
* All $\ell-1$ small even values, $A$, and $u$ more 2's, sum to $C$: red.
* The odd values through $2\ell-3$, $C$, and $u$ more 1's, sum to $D$: blue.
* The small even values, $D$, and $u$ more 2's, sum to $E$: red.

Finally take two copies of each of $3,5,\ldots,2\ell-1$, one $C$,
and $k-2\ell+1$ further 3's. This is a red sum of $k$ terms with
exactly $\ell$ distinct values, equal to $E$, a contradiction.
The largest value is $E$. At $k=2\ell+1$,

$$
F-E=\ell^3+\tfrac12\ell^2+\tfrac32\ell-5>0;
$$

this gap increases with $k$ in the stated range.

### 5.3. The red triple $\{1,4,5\}$

Now $\ell=3$, $k\geq7$, and 2,3 are blue. The red sum with
$k-2$ copies of 1, one 4, and one 5 forces $k+7$ blue. Then
$k-2$ copies of 2, one 3, and one $k+7$ force $3k+6$ red.

Choose the unique $c\in\{1,2,3\}$ with $c\equiv2k\pmod3$, and set

$$
b=(2k+6-4c)/3,\qquad a=(k-6+c)/3.
$$

For $k\geq7$, these are positive integers satisfying
$a+b+c=k$ and $a+4b+5c=3k+6$. Thus the red result is also a red
sum with exactly three distinct values, a contradiction. All values lie
below $F=k^2+4k+3$.

### 5.4. The red triple $\{1,3,4\}$

Here 2 is blue. Red sums force $k+5,k+7,k+9,k+10$ blue, respectively
using multiplicities on $(1,3,4)$

$$
(k-2,1,1),\ (k-3,2,1),\ (k-4,3,1),\ (k-4,2,2).
$$

Blue sums with $k-2$ copies of 2 and pairs $(k+5,k+7)$ and
$(k+9,k+10)$ force $4k+8,4k+15$ red. Red sums

$$
(k-2)\cdot1+3+(4k+8)=5k+9,
$$
$$
3+(k-2)\cdot4+(4k+15)=8k+10
$$

force both results blue. Finally

$$
(k-2)\cdot2+(k+5)+(5k+9)=8k+10
$$

is a blue sum, a contradiction. Every sum has $k$ terms and three
distinct values; $k\geq7$ makes all multiplicities positive. The largest
value is $8k+10\leq F$, since $k^2-4k-7>0$ for $k\geq7$.

The cases exhaust all majority prefixes and prove the upper bound. Since
an exactly-$\ell$-distinct solution is also an at-least-$\ell$-distinct
one, the lower construction completes both equalities in (1).

## 6. Status and scope

The theorem gives an explicit uniform linear threshold. It does not give
the smallest $K(\ell)$, settle the diagonal weak Schur problem $k=\ell$,
or settle the three-color question in [1]. The proof is not formalized in
a proof assistant and has not received independent researcher review.
The accompanying checker validates individual forcing certificates directly
from the definition and checks the polynomial identities; its finite
enumeration is validation, not an extrapolation premise.

The graph-first source was the campaign's exact $WS_8(2)=365$ finding,
artifact `bafkreia3aflad3gd3luzplok4y54x47l7jljqgmren7c427xl42xjgfnxy`.
Its source trail led to [1]. That finite theorem is not used in this proof.
Live primary-source and graph searches on 2026-09-22 found no overlapping
uniform linear threshold result. This is a search-relative novelty statement,
not a priority claim.

[1] Collier Gaiser, *Restricted generalized Schur numbers*,
arXiv:2608.08789v1, 2026-08-09.
[Primary text](https://arxiv.org/html/2608.08789v1),
[version record](https://arxiv.org/abs/2608.08789).
