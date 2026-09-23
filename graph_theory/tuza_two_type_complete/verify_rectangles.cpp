// Exact finite closure of the two-neighborhood split-graph Tuza inequality.
// C++20; all arithmetic is signed 64-bit, with bounds in PROOF.md.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
using Z = std::int64_t;

Z pairs(Z k) { return k * (k - 1) / 2; }
Z triples(Z k) { return k * (k - 1) * (k - 2) / 6; }
Z colors(Z s) { return s < 2 ? 1 : (s % 2 ? s : s - 1); }
Z clique_packing(Z k) {
    if (k < 3) return 0;
    const Z r = k % 6;
    const Z leave = (r == 1 || r == 3) ? 0 : r == 5 ? 4 : k / 2 + (r == 4);
    return (pairs(k) - leave) / 3;
}
Z ceiling(Z a, Z b) { return a >= 0 ? (a + b - 1) / b : a / b; }

struct Shape {
    Z a, b, c, d, k, s, t, u, q, p;
    Shape(Z aa, Z bb, Z cc, Z dd)
        : a(aa), b(bb), c(cc), d(dd), k(a+b+c+d), s(a+c), t(b+c),
          u(a+b+c), q(pairs(k)), p(clique_packing(k)) {}

    Z cover(Z m, Z n) const {
        Z answer = q + m*s + n*t;
        for (Z sign : {Z(1), Z(-1)}) {
            std::array<std::pair<Z,Z>,4> weights{{
                {m+sign*n,c}, {m,a}, {sign*n,b}, {0,d}}};
            std::sort(weights.begin(), weights.end(), std::greater<>());
            Z before = 0, prefix = 0;
            const Z constant = sign == 1 ? m*s+n*t : m*s;
            for (auto [weight, count] : weights) {
                // Integer minimizer of l^2-(k+weight)l on this interval.
                // If k+weight < 0, truncation and floor both clamp to 0.
                const Z l = std::clamp((k+weight)/2, before, before+count);
                answer = std::min(answer,
                    q-l*(k-l)+constant-prefix-(l-before)*weight);
                before += count;
                prefix += weight*count;
            }
        }
        return answer;
    }

    Z centered(Z m, Z n) const {
        const Z cs = colors(s), ct = colors(t), cu = colors(u);
        Z h = ceiling(m*pairs(s)*ct+n*pairs(t)*cs-m*n*pairs(c), cs*ct);
        Z mm = m, nn = n;
        if (mm+nn > cu) {
            if (s >= t) nn = cu-mm;
            else mm = cu-nn;
        }
        return std::max(h, ceiling(mm*pairs(s)+nn*pairs(t), cu));
    }

    Z lower(Z m, Z n) const {
        const Z h = centered(m,n), e = q-h;
        return std::max({p, h, h+ceiling(p*e*(4*e-k*k), 3*k*triples(k))});
    }
};

struct Counts {
    Z cells=0, rectangles=0, nodes=0, failures=0, shapes=0;
    void add(const Counts& c) {
        cells+=c.cells; rectangles+=c.rectangles; nodes+=c.nodes;
        failures+=c.failures; shapes+=c.shapes;
    }
};

void check(const Shape& g, Z ml, Z mh, Z nl, Z nh, Counts& count) {
    ++count.nodes;
    // The graph parameters nu and tau are monotone in m,n. No monotonicity
    // assumption about our numerical formulas is needed for this pruning.
    if (2*g.lower(ml,nl) >= g.cover(mh,nh)) {
        count.cells += (mh-ml+1)*(nh-nl+1);
        ++count.rectangles;
        return;
    }
    if (ml == mh && nl == nh) {
        ++count.cells; ++count.failures;
        std::cout << "FAIL " << g.a << ' ' << g.b << ' ' << g.c << ' ' << g.d
                  << ' ' << ml << ' ' << nl << ' ' << g.lower(ml,nl)
                  << ' ' << g.cover(ml,nl) << '\n';
        return;
    }
    if ((mh-ml)*g.s >= (nh-nl)*g.t && ml < mh) {
        const Z mid = (ml+mh)/2;
        check(g,ml,mid,nl,nh,count);
        check(g,mid+1,mh,nl,nh,count);
    } else {
        const Z mid = (nl+nh)/2;
        check(g,ml,mh,nl,mid,count);
        check(g,ml,mh,mid+1,nh,count);
    }
}

void print_row(const std::string& label, const Counts& c) {
    std::cout << label << ' ' << c.shapes << ' ' << c.cells << ' '
              << c.rectangles << ' ' << c.nodes << ' ' << c.failures << std::endl;
}

Z parse(const char* arg) {
    const std::string s(arg);
    std::size_t used=0;
    const Z value=std::stoll(s,&used);
    if (used != s.size()) throw std::runtime_error("invalid integer");
    return value;
}

int main(int argc, char** argv) {
    try {
        const bool dump = argc == 3 && std::string(argv[1]) == "--dump";
        if (argc > 3 || (argc == 3 && !dump)) throw std::runtime_error("usage");
        const Z last = dump ? parse(argv[2]) : argc == 2 ? parse(argv[1]) : 112;
        if (last < 3 || last > (dump ? 12 : 112)) throw std::runtime_error("range");
        Counts total;
        for (Z k=3; k<=last; ++k) {
            Counts row;
            for (Z a=0; a<=k; ++a)
                for (Z b=0; b<=a && a+b<=k; ++b)
                    for (Z c=0; c<=k-a-b; ++c) {
                        const Shape g(a,b,c,k-a-b-c);
                        ++row.shapes;
                        const Z mm=std::max(Z(0),g.s-1), nn=std::max(Z(0),g.t-1);
                        if (dump) {
                            for (Z m=0; m<=mm; ++m) for (Z n=0; n<=nn; ++n)
                                std::cout << a << ' ' << b << ' ' << c << ' ' << g.d
                                          << ' ' << m << ' ' << n << ' '
                                          << g.lower(m,n) << ' ' << g.cover(m,n)
                                          << ' ' << g.centered(m,n) << '\n';
                        } else check(g,0,mm,0,nn,row);
                    }
            if (!dump) { total.add(row); print_row("ROW "+std::to_string(k),row); }
        }
        if (!dump) print_row("TOTAL",total);
        return total.failures ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << " (expected [3..112] or --dump [3..12])\n";
        return 2;
    }
}
