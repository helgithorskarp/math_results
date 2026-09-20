# Inversion transfer for Schubert identity inflation

Write \(\iota_k(w)=w\otimes 1_k\) for identity-block inflation and
\(\Upsilon_w=\mathfrak S_w(1,1,\ldots)\).  Simple transpositions are
indexed from one.

## 1. Inversion preserves the principal specialization

Macdonald's weighted reduced-word identity is

\[
 \Upsilon_w=\frac{1}{\ell(w)!}
 \sum_{(a_1,\ldots,a_{\ell(w)})\in\operatorname{Red}(w)}
 a_1\cdots a_{\ell(w)}. \tag{1}
\]

Word reversal is a bijection

\[
 (a_1,\ldots,a_\ell)\longmapsto(a_\ell,\ldots,a_1)
\]

from \(\operatorname{Red}(w)\) to
\(\operatorname{Red}(w^{-1})\).  It preserves the product of the letters.
Consequently

\[
 \boxed{\Upsilon_{w^{-1}}=\Upsilon_w.} \tag{2}
\]

The permutation matrix of \(w^{-1}\) is \(P_w^{\mathsf T}\), so

\[
 P_{\iota_k(w^{-1})}=P_{w^{-1}}\otimes I_k
 =(P_w\otimes I_k)^{\mathsf T}
 =P_{\iota_k(w)^{-1}}.
\]

Thus

\[
 \boxed{\iota_k(w^{-1})=\iota_k(w)^{-1}} \tag{3}
\]

and a second application of (2) gives

\[
 \Upsilon_{\iota_k(w^{-1})}=\Upsilon_{\iota_k(w)}. \tag{4}
\]

Equations (2) and (4) prove the general symmetry

\[
 R_k(w^{-1})=R_k(w),\qquad
 R_k(w):=\frac{\Upsilon_{\iota_k(w)}}{\Upsilon_w^{k^2}}. \tag{5}
\]

In particular, every proved class for the identity-inflation inequality
automatically supplies its inverse class.

## 2. The Grassmannian input

For completeness, we include the all-\(k\) Grassmannian argument to make
the transfer self-contained.  Suppose \(u\) is Grassmannian with its only
descent at \(d\), and pad its partition to length \(d\):

\[
 \lambda=(\lambda_1\geq\cdots\geq\lambda_d\geq0).
\]

The Grassmannian Schubert-to-Schur identity and Weyl's dimension formula
give

\[
 \Upsilon_u=s_\lambda(1^d)
 =\prod_{1\leq i<j\leq d}
 \frac{\lambda_i-\lambda_j+j-i}{j-i}. \tag{6}
\]

The inflated permutation \(\iota_k(u)\) is Grassmannian with descent
\(kd\) and padded partition

\[
 \lambda^{[k]}=
 (\underbrace{k\lambda_1,\ldots,k\lambda_1}_{k},\ldots,
  \underbrace{k\lambda_d,\ldots,k\lambda_d}_{k}). \tag{7}
\]

Fix \(i<j\).  For residues \(r,s\in\{1,\ldots,k\}\), put

\[
 A=k(\lambda_i-\lambda_j+j-i),\qquad
 B=k(j-i),\qquad x=s-r.
\]

The associated factor in the Weyl product for (7) is
\((A+x)/(B+x)\).  Since \(A\geq B>|x|\), pairing \((r,s)\) with
\((s,r)\) gives

\[
 \frac{A+x}{B+x}\frac{A-x}{B-x}
 =\frac{A^2-x^2}{B^2-x^2}
 \geq \frac{A^2}{B^2}. \tag{8}
\]

Indeed, after cross multiplication the surplus is
\(x^2(A^2-B^2)\).  The \(r=s\) factors equal \(A/B\).  Multiplication over
all \(k^2\) residue pairs and then over all \(i<j\) proves

\[
 \Upsilon_{\iota_k(u)}\geq\Upsilon_u^{k^2}. \tag{9}
\]

For \(k>1\), equality in (9) holds exactly when all padded parts of
\(\lambda\) are equal: if some \(\lambda_i>\lambda_j\), then \(A>B\)
and a pair with \(x\ne0\) makes (8) strict.  The identity is the empty
partition case.

## 3. Transfer to inverse-Grassmannian permutations

Let \(w^{-1}=u\) be Grassmannian.  Combining (2), (4), and (9) gives,
for every \(k\geq1\),

\[
 \boxed{
 \Upsilon_{w\otimes1_k}
 =\Upsilon_{u\otimes1_k}
 \geq \Upsilon_u^{k^2}
 =\Upsilon_w^{k^2}.} \tag{10}
\]

For \(k>1\), the equality criterion is exactly the one in Section 2 for
the padded Grassmannian partition of \(w^{-1}\).

This is not merely a one-descent restatement.  Put

\[
 z_m=(m+1,1,m+2,2,\ldots,2m,m)\in S_{2m}.
\]

Then \(z_m\) has descents at all odd positions, while

\[
 z_m^{-1}=(2,4,\ldots,2m,1,3,\ldots,2m-1)
\]

is Grassmannian with descent \(m\) and padded shape
\((m,m-1,\ldots,1)\).  Hence (10) gives support-connected examples with
arbitrarily many ordinary descents; for \(m\geq2\) and \(k>1\), their
inequalities are strict.

For the support assertion, a simple generator \(s_r\) is absent from the
Coxeter support exactly when the permutation preserves the value set
\([r]\).  The first \(r<2m\) entries of \(z_m^{-1}\) contain a value larger
than \(r\): use \(2r\) if \(r\leq m\), and \(2m\) if \(r>m\).  Thus
\(z_m^{-1}\), and therefore \(z_m\), has full connected support.
