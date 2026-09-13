// Independent all-pairs polynomial audit. Input: sorted distinct E coefficient
// vectors with common denominator 12. Output: all oriented unit directions.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <vector>
using I = std::int64_t;
using V = std::array<I,4>;
int main() {
    std::size_t n;
    if (!(std::cin >> n) || n > 20000) return 2;
    std::vector<V> v(n);
    for (auto &p:v) for (auto &x:p)
        if (!(std::cin >> x) || x < -1000000 || x > 1000000) return 3;
    std::string extra;
    if (std::cin >> extra) return 4;
    if (std::set<V>(v.begin(),v.end()).size() != n) return 5;
    std::vector<I> n0(n),n1(n);
    for (std::size_t i=0;i<n;++i) {
        auto [a,b,c,d]=v[i];
        n0[i]=a*a+33*b*b+3*c*c+11*d*d;
        n1[i]=2*(a*b+c*d);
    }
    for (std::size_t i=0;i<n;++i) {
        auto [a,b,c,d]=v[i];
        for (std::size_t j=0;j<n;++j) {
            auto [A,B,C,D]=v[j];
            if (a*C-c*A+11*(b*D-d*B) != 0) continue;
            if (a*D-d*A+3*(b*C-c*B) != 0) continue;
            I h0=a*A+33*b*B+3*c*C+11*d*D;
            I h1=a*B+b*A+c*D+d*C;
            if (3*n0[i]+4*n0[j]-3*h0 != 576) continue;
            if (3*n1[i]+4*n1[j]-3*h1 != 0) continue;
            std::cout << i << ' ' << j << '\n';
        }
    }
    return std::cout ? 0 : 6;
}
