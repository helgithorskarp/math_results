# Arbitrary-\(q\) resonance obstruction and the \(q=5\) classification

## 1. Setup

For

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf1_{\{\sum_i(|x_i|-1)_+\le R\}}\,dx,
\]

put

\[
M=\|v\|_\infty,\qquad
B=\frac{|b|-\|v\|_1}{M}>0,\qquad s=R-B.
\]

The global weighted formula cited in SOURCES.md places every candidate wall
for normalized active weights \(w_i\) among

\[
\omega_{u,J}=B(1/u-1)+\frac2u\sum_{w\in J}w,
\qquad u\notin J.                                      \tag{1}
\]

We study two-level weights

\[
1^p a^r,\qquad q=p+r,\qquad0<a<1.                     \tag{2}
\]

Write \(H_d(s;\omega)=(s-\omega)_+^d\) and
\(\lambda=(1-a)/a\).

## 2. Structural rows

A unit-supplier row is indexed by the numbers \(k,\ell\) of unit and
\(a\)-weights in its tail:

\[
0\le k<p,\qquad0\le\ell\le r.
\]

An \(a\)-supplier row is indexed by

\[
0\le i\le p,\qquad0\le j<r.
\]

Their walls and lowest hinge degrees are

\[
\begin{array}{c|c|c}
&\text{wall}&\text{lowest degree}\\ \hline
U_{k,\ell}&2(k+a\ell)&r+k\\
V_{i,j}&\lambda B+2i/a+2j&p+j.
\end{array}                                            \tag{3}
\]

The exact coefficients in those lowest degrees are

\[
U_{k,\ell}=
\frac{\binom pk\binom r\ell(-1)^{k+\ell}
(B+2k+2a\ell)^{p-k-1}}
{(p-k-1)!(r+k)!\,2^k a^r
(1-a)^{r-\ell}(1+a)^\ell},                            \tag{4}
\]

and

\[
V_{i,j}=
\frac{\binom pi\binom rj(-1)^{p+j}
a^{2p-r+j}(B+2i+2aj)^{r-j-1}}
{(r-j-1)!(p+j)!\,2^j
(1-a)^{p-i}(1+a)^i}.                                  \tag{5}
\]

**Derivation.** After the \(k+\ell\) tails in \(U\) are removed, the unit
pole has order \(p-k\). Its highest principal-part coefficient is
\([a(1-a)]^{-(r-\ell)}\). Every unit tail contributes the zero-moment
factor \(-1/2\), every \(a\)-tail contributes
\(-1/[a(1+a)]\), and the beta factors telescope. Including the
\(\binom pk\binom r\ell\) tail choices gives (4).

For \(V\), the pole has order \(r-j\), and its highest principal-part
coefficient is

\[
\frac{a^{2(p-i)-(r-j)}}{(a-1)^{p-i}}.
\]

A unit tail contributes \(-a^2/(1+a)\), an \(a\)-tail contributes
\(-1/2\), and the beta factors again telescope. This gives (5). In
particular, the displayed lowest coefficients are never zero before rows are
collected.

## 3. Arbitrary-\(q\) resonance theorem

Suppose \(U_{k,\ell}\) and \(V_{i,j}\) meet. Cancellation first requires
equal lowest degrees, hence equal residual pole multiplicity

\[
m=p-k=r-j.                                             \tag{6}
\]

Thus \(k=p-m\), \(j=r-m\). The common-wall equation gives

\[
B=\frac{2(ak+a^2\ell-i-aj)}{1-a},                     \tag{7}
\]

so \(B>0\) is equivalent to

\[
\ell a^2+(k-j)a-i>0.                                  \tag{8}
\]

Put

\[
X=k-i+a(\ell-j).
\]

At (7),

\[
B+2k+2a\ell=\frac{2X}{1-a},\qquad
B+2i+2aj=\frac{2aX}{1-a}.                             \tag{9}
\]

Since \(B>0\), \(X>0\). Substitution in (4)--(5) proves:

**Theorem 1 (closed lowest coefficient).** The aggregate coefficient of
\(H_{q-m}\) at a two-row cross-family resonance is

\[
\frac{2^{m-1}X^{m-1}}
{(m-1)!(q-m)!(1-a)^{m-1}}
\left[
\frac{(-1)^{p-m+\ell}\binom pm\binom r\ell}
{2^{p-m}a^r(1-a)^{r-\ell}(1+a)^\ell}
+
\frac{(-1)^{q-m}\binom pi\binom rm a^{2p-1}}
{2^{r-m}(1-a)^{p-i}(1+a)^i}
\right].                                               \tag{10}
\]

All factors outside the square brackets are positive. The two summands
inside have opposite signs only if

\[
\boxed{r-\ell\ \text{is odd}.}                        \tag{11}
\]

Therefore (6) and (11) are necessary for a generic missing wall. When
\(m=1\), each row has only the hinge \(H_{q-1}\), so equality of the two
magnitudes in (10) is also sufficient, provided no additional structural
row shares the wall.

Equation (10) is the reusable generalization of the dimension-four
residual-multiplicity lemma. The symbolic script checks it against exact
principal parts for all 42 positive resonance types in dimensions three,
four, and five; the proof above is valid for arbitrary \(p,r\).

## 4. Complete classification for \(q=5\)

For \(p+r=5\), conditions (6) and (8) leave 26 candidate types. The parity
condition (11) leaves only nine:

Indeed, the left side of (8) is convex, is nonpositive at \(a=0\), and
therefore is positive somewhere in \((0,1)\) exactly when its value at
\(a=1\) is positive. This makes the 26-type enumeration finite and exact.

| weights | \(m\) | \((\ell,i)\) | domain |
|---|---:|---:|---|
| \(1^4a\) | 1 | \((0,0),(0,1),(0,2)\) | \(a>0,\ a>1/3,\ a>2/3\) |
| \(1^3a^2\) | 2 | \((1,0),(1,1)\) | \(a>0,\ a^2+a-1>0\) |
| \(1^3a^2\) | 1 | \((1,0),(1,1)\) | \(a>0,\ a^2+a-1>0\) |
| \(1^2a^3\) | 2 | \((2,0)\) | \(a>1/2\) |
| \(1^2a^3\) | 1 | \((2,0)\) | \(a>1/2\) |

Here \(k=p-m\) and \(j=r-m\).

### Higher residual multiplicity

For the three \(m=2\) candidates, vanishing of the \(H_3\) and \(H_4\)
coefficients would require a common root of the following primitive
polynomials:

\[
\begin{array}{c|l|l|r}
(p,r;\ell,i)&F(a)&G(a)&|\operatorname{Res}(F,G)|\\ \hline
(3,2;1,0)&
a^8+a^7-3a^2+6a-3&
10a^{10}+4a^9-22a^8-16a^7-45a^4+90a^3-12a^2-66a+33&
908446872528\\
(3,2;1,1)&
a^7+a-1&
10a^9-2a^8-16a^7+15a^3-15a^2-11a+11&
55973\\
(2,3;2,0)&
a^8+2a^7+a^6+2a-2&
11a^{10}+18a^9-12a^8-34a^7-15a^6+32a^3-36a^2-16a+20&
1429061632.
\end{array}                                           \tag{12}
\]

All three resultants are nonzero. No \(m=2\) wall disappears.

### The six simple-pole orbits

For \(m=1\), (10) reduces to one equation. The six primitive equations,
resonance parameters, and walls are:

| weights | \((\ell,i)\) | polynomial \(P(a)\) | \(B\) | wall |
|---|---:|---|---|---|
| \(1^4a\) | \((0,0)\) | \(2a^8+a^3-3a^2+3a-1\) | \(6a/(1-a)\) | \(6\) |
| \(1^4a\) | \((0,1)\) | \(8a^8-a^3+a^2+a-1\) | \(2(3a-1)/(1-a)\) | \(6\) |
| \(1^4a\) | \((0,2)\) | \(12a^8+a^3+a^2-a-1\) | \(2(3a-2)/(1-a)\) | \(6\) |
| \(1^3a^2\) | \((1,0)\) | \(2a^8+2a^7-3a^2+6a-3\) | \(2a(a+1)/(1-a)\) | \(2(a+2)\) |
| \(1^3a^2\) | \((1,1)\) | \(2a^7+a-1\) | \(2(a^2+a-1)/(1-a)\) | \(2(a+2)\) |
| \(1^2a^3\) | \((2,0)\) | \(a^8+2a^7+a^6+4a-4\) | \(2a(2a-1)/(1-a)\) | \(2(2a+1)\) |

Each polynomial is irreducible over \(\mathbb Q\) and has exactly one root
in \((0,1)\). In table order, those roots are

\[
\begin{split}
&0.630979443162890038\ldots,\quad
0.636690912035195880\ldots,\quad
0.716658280303551875\ldots,\\
&0.697890411717118109\ldots,\quad
0.745071972941756557\ldots,\quad
0.795592019016402274\ldots.
\end{split}                                            \tag{13}
\]

Rational intervals of width \(10^{-12}\), certified by Sturm sequences, are
respectively

\[
\begin{array}{c}
(630979443162,630979443163)/10^{12},\\
(636690912035,636690912036)/10^{12},\\
(716658280303,716658280304)/10^{12},\\
(697890411717,697890411718)/10^{12},\\
(745071972941,745071972942)/10^{12},\\
(795592019016,795592019017)/10^{12}.
\end{array}                                            \tag{14}
\]

Each interval lies inside its required domain in the first table.

## 5. Nongeneric subset sums and the diagonal

Internal same-family wall collisions occur only at \(a=1/2\) or \(a=1/3\).
There are ten colliding row pairs:

- two constant pairs on \(1^3a^2\) at \(a=1/2\);
- one constant pair on \(1^2a^3\) at \(a=1/3\), and two constant plus two
  moving pairs there at \(a=1/2\);
- one moving pair on \(1a^4\) at \(a=1/3\), and two moving pairs there at
  \(a=1/2\).

Within each pair the lowest hinge degrees differ, so the pair alone cannot
vanish. Exact collection at every possible positive cross-family resonance
gives 25 cases; every resulting positive wall retains a nonzero coefficient.
Both scripts enumerate these cases from the structural indices rather than
assuming the list.

At the diagonal \(1^5\), the positive rows are

\[
\begin{array}{c|rrrrr}
\omega&H_0&H_1&H_2&H_3&H_4\\ \hline
2&0&-5(B+2)^3/12&-55(B+2)^2/16&-355(B+2)/48&-585/128\\
4&0&0&5(B+4)^2/8&5(B+4)/2&415/192\\
6&0&0&0&-5(B+6)/24&-65/192\\
8&0&0&0&0&5/384.
\end{array}                                           \tag{15}
\]

None disappears.

**Theorem 2 (classification).** Up to coordinate permutation and common
scaling, the six roots and parameters above are all missing positive
candidate walls for five active weights taking at most two distinct values.
There are no missing positive walls on \(1a^4\) or \(1^5\).

## 6. Verification boundary

derive.py works over \(\mathbb Q(a,B)\) in SymPy 1.13.3. It rebuilds all five
hinge tables, verifies (10) in 42 lower-dimensional and dimension-five
types, performs the candidate and internal-collision exhaustions, computes
the three resultants, and certifies the six roots.

verify.py uses only Python integers and fractions.Fraction. It independently
reconstructs repeated principal parts, checks (10) at 673 exact rational
instances, computes the resultants by fraction-free Bareiss elimination,
proves the root counts by rational Sturm sequences, and repeats all 25
special resonance audits. The interpretation of the previously proved
global chamber expansion is an external dependency; finite rational checks
do not alone prove the rational-function identities.
