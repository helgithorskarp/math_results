# Uniform scalars with unequal light counts

Actual author **six-downset-1 / researcher**, 2026-10-04. Ordinary
algebraic lemma, **UNFORMALIZED and independently UNREVIEWED**. This
document proves inequalities of rational functions. PROOF.md separately
identifies them with the entire original Gram, physical frame and
weighted dual. Source and graph records are separate delivery facts.

The scalar recipes descend from own four-mark source
9e7ada1cd3b0b966815e1711c9212e94dad2881f (LEMMA10316/0); its certificate
and review status are not transported. The sealed private equal-light
ordinary proof is a credited predecessor, not published prior art.

## Algebraic domain and definitions

Let r be an integer at least3 and let h,k1,...,k_(r-1),q be REAL with

    h>=3, 2<=k_g<h, q>=8, F=h+sum_light k_g>=9.

Set k0=h, L=sum_light k_g, ell=3F+1, s=q+3h and define

    c0=[q ell+9sum_light k_g(h-k_g)+3h-6F-1]/ell^2,
    R_g=[ell+1-q-3(h-k_g)]/ell,
    mu_g=(s-3)/3-c0-9R_g^2/[2s(k_g-1)],
    alpha_g=2s-27(2k_g-3)R_g^2/[s(k_g-1)],
    beta_g=2s/3-3(k_g+3)R_g^2/[s(k_g-1)],
    S=sum_groups k_g mu_g, S_L=sum_light k_g mu_g,
    nu_g=mu_g+k_g mu_g^2/[S(k_g-1)],
    kappa=1/(h mu_0)+1/S_L
          +4sum_light k_g mu_g^2/(S_L^2 beta_g).

**Lemma.** All denominators are positive, and throughout this region

    0<c0<s/27+1/4,             |R_g|/s<1/17,
    mu_g-s/5>1123/9180>0,      mu_g<s/3,
    s<alpha_g<=2s,             s/2<beta_g<=2s/3,
    Fs/5<S<Fs/3,              Ls/5<S_L<Ls/3,
    0<nu_g<37s/81<s/2,        0<kappa<25/68.

Moreover sum_light k_g mu_g^2/S_L^2<5/(3L)<=5/12.
The theorem's integer domain r>=3, n>=max(4,r), h>k_g>=2,
F>=9 embeds here with q=2^(n-1). No original r5 matrix is needed.

## Proof

We have L>=4, ell>=28 and s>=17. Since each k_g(h-k_g)>0,
the numerator of c0 is greater than or equal to

    8ell+3h-6F-1=18F+3h+7>0.

For its upper bound discard the negative 3h-6F-1 and use ell>3F.
Cauchy's inequality gives sum_light k_g^2>=L^2/(r-1). The exact square

    (r-1)(h+L)^2-4r[hL-L^2/(r-1)]
      =[(r-1)h-(r+1)L]^2/(r-1)

therefore implies

    sum_light k_g(h-k_g)/F^2 <= (r-1)/(4r)<1/4,
    c0<q/(3F)+sum_light k_g(h-k_g)/F^2<s/27+1/4.

For fixed counts, R_g/s=(A_g-q)/[ell(q+3h)], where
A_g=ell+1-3(h-k_g)=3(L+k_g)+2. Its q derivative is
-(A_g+3h)/[ell(q+3h)^2]<0. At q=8, every R_g is strictly between
0 and1: for a light group A_g>=20, and R_g<R_0=(ell-7)/ell<1.
The heavy case has the same positive upper bound. Thus the positive
maximum ratio is below1/(8+3h)<=1/17. Its negative limiting ratio is
-1/ell, with magnitude at most1/28<1/17. This proves the strict
absolute bound for EVERY real q>=8.

For k>=2, the c0 and R bounds give

    mu_g>s(8/27-9/578)-5/4,
    mu_g-s/5>s(13/135-9/578)-5/4
             >=17(13/135-9/578)-5/4=1123/9180>0.

The coefficient of s is positive. The upper mu bound follows from
c0>0 and its defining formula. Since

    0<(2k-3)/(k-1)<2, 0<(k+3)/(k-1)<=5,

we obtain alpha>(2-54/289)s>s and beta>(2/3-15/289)s>s/2.
Their upper bounds follow by subtracting nonnegative squares.
Summing the mu bounds proves the stated S and S_L inequalities.
Consequently, using k/(k-1)<=2 and F>=9,

    0<nu_g<(s/3)[1+5k_g/(3F(k_g-1))]
           <=(s/3)(1+10/27)=37s/81<s/2.

For the weighted repair energy, mu_g/beta_g<2/3, so

    kappa<5/(hs)+11/(3S_L)
          <5/(hs)+55/(3Ls)
          <=5/51+55/204=25/68.

Finally mu_g^2<(s/3)mu_g yields

    sum_light k_g mu_g^2/S_L^2<s/(3S_L)<5/(3L)<=5/12.

These are ordinary inequalities on the declared real domain. Finite
original controls validate the identification of the functions; they
are not an enumeration proof of this lemma.
