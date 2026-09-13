// Definition-level contact census for the weighted support.
//
// Input vectors are the distinct source differences in the basis
// 1,sqrt(33),alpha,beta (alpha^2=-3, beta^2=-11), with denominator 12.
// For every ordered pair (d,r), split
//
//   (1-u)d+ur = P + sqrt(13) Q,
//   P=(3d+5r)/8, Q=alpha(r-d)/8.
//
// The vector has norm one iff N(P)+13N(Q)=1 and
// P*conj(Q)+Q*conj(P)=0. This differs from the target C++ reduction.

#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using I = std::int64_t;
using W = __int128_t;
using V = std::array<I, 4>;
using X = std::array<W, 4>;

static V conjugate(const V &z) {
    return {z[0], z[1], -z[2], -z[3]};
}

static X multiply(const V &x, const V &y) {
    const auto [a,b,c,d] = x;
    const auto [A,B,C,D] = y;
    return {
        W(a)*A + W(33)*b*B - W(3)*c*C - W(11)*d*D,
        W(a)*B + W(b)*A - W(c)*D - W(d)*C,
        W(a)*C + W(c)*A + W(11)*(W(b)*D + W(d)*B),
        W(a)*D + W(d)*A + W(3)*(W(b)*C + W(c)*B)
    };
}

static X norm(const V &z) {
    return multiply(z, conjugate(z));
}

int main() {
    std::size_t n = 0;
    if (!(std::cin >> n) || n == 0 || n > 20000) return 2;
    std::vector<V> values(n);
    for (auto &z : values) {
        for (auto &coefficient : z) {
            if (!(std::cin >> coefficient) || coefficient < -1000000 || coefficient > 1000000) return 3;
        }
    }
    std::string trailing;
    if (std::cin >> trailing) return 4;
    if (std::set<V>(values.begin(), values.end()).size() != n) return 5;

    constexpr W scale_squared = W(96) * 96;
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            V p{};
            V delta{};
            for (int k = 0; k < 4; ++k) {
                p[k] = 3 * values[i][k] + 5 * values[j][k];
                delta[k] = values[j][k] - values[i][k];
            }
            // alpha*(a+b sqrt33+c alpha+d beta)=(-3c,-d,a,3b).
            const V q = {-3 * delta[2], -delta[3], delta[0], 3 * delta[1]};
            const X np = norm(p);
            const X nq = norm(q);
            bool base_ok = np[0] + W(13)*nq[0] == scale_squared;
            for (int k = 1; k < 4; ++k) base_ok = base_ok && np[k] + W(13)*nq[k] == 0;
            if (!base_ok) continue;

            const X pq = multiply(p, conjugate(q));
            const X qp = multiply(q, conjugate(p));
            bool cross_ok = true;
            for (int k = 0; k < 4; ++k) cross_ok = cross_ok && pq[k] + qp[k] == 0;
            if (cross_ok) std::cout << i << ' ' << j << '\n';
        }
    }
    return std::cout ? 0 : 6;
}
