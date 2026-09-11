#include <bit>
#include <cstdint>
#include <iostream>
#include <set>

// Every labelled subset is visited. No isomorphism or solver assumptions.
int main() {
    std::set<uint32_t> lines;
    for (int x=0;x<5;++x) for (int y=0;y<5;++y)
    for (int dx=0;dx<5;++dx) for (int dy=0;dy<5;++dy) {
        if (dx==0 && dy==0) continue;
        uint32_t mask=0;
        for (int t=0;t<5;++t)
            mask |= uint32_t(1) << (5*((x+t*dx)%5)+(y+t*dy)%5);
        lines.insert(mask);
    }
    if (lines.size()!=30) return 2;
    uint64_t tried12=0,tried17=0,valid12=0,valid17=0;
    for (uint32_t s=0;s<(uint32_t(1)<<25);++s) {
        int n=std::popcount(s);
        if (n!=12 && n!=17) continue;
        if (n==12) ++tried12; else ++tried17;
        bool valid=true;
        for (auto l:lines) if (std::popcount(s&l)>(n==12?3:4)) {
            valid=false; break;
        }
        if (valid) { if (n==12) ++valid12; else ++valid17; }
    }
    std::cout << "{\"lines\":30,\"subsets12\":" << tried12
              << ",\"max3_valid12\":" << valid12
              << ",\"subsets17\":" << tried17
              << ",\"max4_valid17\":" << valid17 << "}\n";
    return valid12 || valid17 || tried12!=5200300 || tried17!=1081575;
}
