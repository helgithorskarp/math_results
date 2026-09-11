#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>

// Enumerate every labelled subset of the 25-point plane. Bits use 5*x+y.
// An actual section of a 72-set has no four-point line when its size <=11.
// The size-17 check also supplies the planar line-free upper bound 16.
int main() {
    std::set<uint32_t> lines;
    for (int x=0;x<5;++x) for (int y=0;y<5;++y)
    for (int a=0;a<5;++a) for (int b=0;b<5;++b) {
        if (a==0 && b==0) continue;
        uint32_t mask=0;
        for (int t=0;t<5;++t)
            mask |= uint32_t(1) << (5*((x+t*a)%5)+(y+t*b)%5);
        lines.insert(mask);
    }
    if (lines.size()!=30) return 2;
    std::map<std::array<int,6>,uint64_t> spectra;
    std::array<uint64_t,26> visited{};
    uint64_t valid17=0;
    for (uint32_t set=0;set<(uint32_t(1)<<25);++set) {
        const int m=std::popcount(set);
        ++visited[m];
        if (m<8 || m>17) continue;
        std::array<int,6> spectrum{};
        spectrum[0]=m;
        bool valid=true;
        for (uint32_t line:lines) {
            const int k=std::popcount(set&line);
            if (k>(m<=11?3:4)) { valid=false; break; }
            ++spectrum[k+1];
        }
        if (valid) {
            if (m==17) ++valid17;
            else ++spectra[spectrum];
        }
    }
    uint64_t binomial=1;
    for (int m=0;m<=25;++m) {
        if (visited[m]!=binomial) return 3;
        if (m<25) binomial=binomial*uint64_t(25-m)/uint64_t(m+1);
    }
    if (valid17!=0) return 4;
    for (const auto& [spectrum,count]:spectra) {
        for (int entry:spectrum) std::cout << entry << ' ';
        std::cout << count << '\n';
    }
}
