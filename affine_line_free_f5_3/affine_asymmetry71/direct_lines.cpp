// Independent check: enumerate complements by increasing integer mask;
// test every planar line for a hole, and every transverse line directly.
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
using U=std::uint32_t;
using Count=std::uint64_t;
struct Record {
    int n{}; U b{}; Count orbit{};
    std::array<std::vector<U>,25> requirements;
    std::array<Count,26> histogram{};
    Count survivors{}; int maximum{-1}; U example_c{},example_d{};
    Count digest{};
};
int point(int y,int z) { return 5*((y%5+5)%5)+(z%5+5)%5; }
// A bijective integer mixer is a diagnostic, not a mathematical certificate.
Count mixed(Count value) {
    value+=0x9e3779b97f4a7c15ULL;
    value=(value^(value>>30))*0xbf58476d1ce4e5b9ULL;
    value=(value^(value>>27))*0x94d049bb133111ebULL;
    return value^(value>>31);
}
int main(int argc,char** argv) {
    if(argc!=2) throw std::runtime_error("usage: direct c < catalogue.txt");
    const int csize=std::stoi(argv[1]);
    if(csize<12||csize>17) throw std::runtime_error("c must be 12..17");
    std::vector<U> lines;
    // Six directions, represented by a normal (0,1), (1,t).
    for(int direction=0;direction<6;++direction) for(int constant=0;constant<5;++constant) {
        U line=0;
        for(int y=0;y<5;++y)for(int z=0;z<5;++z)
            if((direction==0?z:(y+(direction-1)*z)%5)==constant)
                line|=1U<<point(y,z);
        if(std::popcount(line)!=5) throw std::runtime_error("planar line");
        lines.push_back(line);
    }
    std::vector<Record> records;
    int n; U b; Count orbit;
    while(std::cin>>n>>b>>orbit) {
        if(n<14||n>16||b>=(1U<<25)||std::popcount(b)!=n||orbit==0||12000%orbit!=0)
            throw std::runtime_error("invalid catalogue row");
        if(n<csize||n+csize<28) continue;
        Record r;r.n=n;r.b=b;r.orbit=orbit;
        for(int u=0;u<25;++u)for(int v=0;v<25;++v) {
            const int p1=point(u/5+v/5,u%5+v%5);
            const int p4=point(u/5+4*(v/5),u%5+4*(v%5));
            if((b>>p1&1U)&&(b>>p4&1U)) {
                const int p2=point(u/5+2*(v/5),u%5+2*(v%5));
                const int p3=point(u/5+3*(v/5),u%5+3*(v%5));
                // Duplicates from v and -v deliberately retained.
                r.requirements[u].push_back((1U<<p2)|(1U<<p3));
            }
        }
        records.push_back(r);
    }
    if(!std::cin.eof()||(records.empty()&&csize!=17)) throw std::runtime_error("bad/empty catalogue");
    constexpr U limit=1U<<25,full=limit-1;
    Count scanned=0,valid=0;
    for(U holes=0;holes<limit;++holes) {
        if(std::popcount(holes)!=25-csize) continue;
        ++scanned;
        bool blocking=true;
        for(U line:lines) if(!(holes&line)){blocking=false;break;}
        if(!blocking) continue;
        ++valid;
        const U c=full^holes;
        for(auto& r:records) {
            U d=0;
            for(int u=0;u<25;++u) {
                bool safe=true;
                for(U need:r.requirements[u]) if(!(holes&need)){safe=false;break;}
                if(safe)d|=1U<<u;
            }
            const int count=std::popcount(d);
            ++r.histogram[count];
            r.digest+=mixed((static_cast<Count>(c)<<25)|d);
            if(count>r.maximum||(count==r.maximum&&c<r.example_c)) {
                r.maximum=count;r.example_c=c;r.example_d=d;
            }
            if(2*(r.n+csize)+count>=71)++r.survivors;
        }
    }
    if(csize==17) {
        if(valid)throw std::runtime_error("unexpected line-free 17-set");
        std::cout<<"{\"csize\":17,\"subsets\":"<<scanned<<",\"line_free_c\":"<<valid<<"}\n";
    }
    for(const auto& r:records) {
        std::cout<<"{\"bsize\":"<<r.n<<",\"csize\":"<<csize<<",\"b\":"<<r.b
                 <<",\"b_orbit\":"<<r.orbit<<",\"subsets\":"<<scanned<<",\"line_free_c\":"<<valid
                 <<",\"max_allowed\":"<<r.maximum<<",\"relaxation_survivors71\":"<<r.survivors
                 <<",\"example_c\":"<<r.example_c<<",\"example_allowed\":"<<r.example_d
                 <<",\"digest\":"<<r.digest<<",\"histogram\":{";
        bool first=true;
        for(int j=0;j<=25;++j)if(r.histogram[j]) {
            if(!first)std::cout<<',';
            first=false;
            std::cout<<'\"'<<j<<"\":"<<r.histogram[j];
        }
        std::cout<<"}}\n";
    }
}
