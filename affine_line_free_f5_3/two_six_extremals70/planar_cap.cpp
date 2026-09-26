// Recheck the only planar extremal input: no line-free 17-subset of AG(2,5).
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>

int main() {
    std::set<uint32_t> lines;
    for (int x=0; x<5; ++x) for (int y=0; y<5; ++y)
    for (int a=0; a<5; ++a) for (int b=0; b<5; ++b) {
        if (a==0 && b==0) continue;
        uint32_t line = 0;
        for (int t=0; t<5; ++t)
            line |= uint32_t(1) << (5*((x+t*a)%5)+(y+t*b)%5);
        lines.insert(line);
    }
    if (lines.size()!=30) return 2;
    uint64_t visited = 0, line_free = 0;
    constexpr uint32_t end = uint32_t(1)<<25;
    for (uint32_t mask=(uint32_t(1)<<17)-1; mask<end;) {
        if (std::popcount(mask)!=17) return 3;
        ++visited;
        bool contains_line = false;
        for (uint32_t line : lines)
            if ((line & mask)==line) { contains_line = true; break; }
        if (!contains_line) ++line_free;
        const uint32_t least = mask & (~mask+1);
        const uint32_t raised = mask+least;
        mask = raised | (((raised^mask)>>2)/least);
    }
    if (visited!=1081575 || line_free!=0) return 4;
    std::cout << "PLANAR_CAP16 " << visited << ' ' << line_free << '\n';
}
