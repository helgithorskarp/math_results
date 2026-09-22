#include <bit>
#include <cstdint>
#include <iostream>
#include <set>

int main() {
    std::set<uint32_t> lines;
    for (int x=0;x<5;++x) for (int y=0;y<5;++y)
    for (int a=0;a<5;++a) for (int b=0;b<5;++b) {
        if (a==0 && b==0) continue;
        uint32_t line=0;
        for (int t=0;t<5;++t)
            line |= uint32_t(1) << (5*((x+t*a)%5)+(y+t*b)%5);
        lines.insert(line);
    }
    if (lines.size()!=30) return 2;
    uint64_t visited=0,valid=0;
    for (uint32_t mask=0;mask<(uint32_t(1)<<25);++mask) {
        if (std::popcount(mask)!=17) continue;
        ++visited;bool good=true;
        for (uint32_t line:lines) if ((mask&line)==line) {good=false;break;}
        if (good) ++valid;
    }
    std::cout << "{\"seventeen_subsets\":" << visited
              << ",\"line_free_seventeen_subsets\":" << valid << "}\n";
    return visited!=1081575 || valid!=0;
}
