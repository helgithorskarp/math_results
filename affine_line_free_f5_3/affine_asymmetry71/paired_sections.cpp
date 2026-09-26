// Exhaustive search for 71 points fixed by (x,y,z)->(-x,y,z).
// stdin: complete planar affine representatives: size, mask, orbit_size.
// argv[1]: size c of the x=+-2 section (12 through 16).
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using U=std::uint32_t;
using Count=std::uint64_t;
using Signature=std::array<std::uint16_t,25>;
struct Record {
    int n{}; U mask{}; Count orbit{}; Signature signature{};
    std::array<std::vector<U>,25> geometric_requirements;
    std::array<Count,26> histogram{};
    Count survivors{}; int maximum{-1}; U example_c{},example_d{};
    Count digest{};
};
Count mixed(Count value) {
    value+=0x9e3779b97f4a7c15ULL;
    value=(value^(value>>30))*0xbf58476d1ce4e5b9ULL;
    value=(value^(value>>27))*0x94d049bb133111ebULL;
    return value^(value>>31);
}
std::vector<U> lines;
int point(int y,int z) { return 5*(y%5)+z%5; }
int main(int argc,char** argv) {
    if(argc!=2) throw std::runtime_error("usage: search c < catalogue.txt");
    const int csize=std::stoi(argv[1]);
    if(csize<12||csize>16) throw std::runtime_error("c must be 12..16");
    std::set<U> line_set;
    for(int a=0;a<25;++a)for(int v=1;v<25;++v) {
        U line=0;
        for(int t=0;t<5;++t)
            line|=1U<<(5*((a/5+t*(v/5))%5)+(a%5+t*(v%5))%5);
        line_set.insert(line);
    }
    lines.assign(line_set.begin(),line_set.end());
    if(lines.size()!=30) throw std::runtime_error("line geometry");
    std::vector<int> dirs;
    for(int v=1;v<25;++v) {
        const int neg=5*((5-v/5)%5)+(5-v%5)%5;
        if(v<neg) dirs.push_back(v);
    }
    if(dirs.size()!=12) throw std::runtime_error("pair geometry");
    std::array<std::array<U,12>,25> pairs{},double_pairs{};
    for(int u=0;u<25;++u)for(int j=0;j<12;++j) {
        const int v=dirs[static_cast<std::size_t>(j)];
        for(int t:{1,4}) pairs[u][j]|=1U<<(5*((u/5+t*(v/5))%5)+(u%5+t*(v%5))%5);
        for(int t:{2,3}) double_pairs[u][j]|=1U<<(5*((u/5+t*(v/5))%5)+(u%5+t*(v%5))%5);
    }
    std::vector<Record> records;
    int n; U mask; Count orbit;
    while(std::cin>>n>>mask>>orbit) {
        if(n<14||n>16||mask>=(1U<<25)||std::popcount(mask)!=n||orbit==0||12000%orbit!=0)
            throw std::runtime_error("invalid catalogue row");
        if(n<csize||n+csize<28) continue;
        Record r; r.n=n;r.mask=mask;r.orbit=orbit;
        for(int u=0;u<25;++u)for(int j=0;j<12;++j)
            if((mask&pairs[u][j])==pairs[u][j]) r.signature[u]|=static_cast<std::uint16_t>(1U<<j);
        // A second, definition-level construction keeps all 25 geometric
        // slopes, including zero and both signs, independently of signatures.
        for(int u=0;u<25;++u)for(int v=0;v<25;++v) {
            const int p1=point(u/5+v/5,u%5+v%5);
            const int p4=point(u/5+4*(v/5),u%5+4*(v%5));
            if((mask>>p1&1U)&&(mask>>p4&1U)) {
                const int p2=point(u/5+2*(v/5),u%5+2*(v%5));
                const int p3=point(u/5+3*(v/5),u%5+3*(v%5));
                r.geometric_requirements[u].push_back((1U<<p2)|(1U<<p3));
            }
        }
        records.push_back(r);
    }
    if(!std::cin.eof()||records.empty()) throw std::runtime_error("bad/empty catalogue");
    constexpr U limit=1U<<25,full=limit-1;
    Count scanned=0,valid=0;
    U c=(1U<<csize)-1U;
    while(c<limit) {
        ++scanned;
        bool good=true;
        for(U line:lines)if((c&line)==line){good=false;break;}
        if(good) {
            ++valid;
            Signature cs{};
            for(int u=0;u<25;++u)for(int j=0;j<12;++j)
                if((c&double_pairs[u][j])==double_pairs[u][j])cs[u]|=static_cast<std::uint16_t>(1U<<j);
            for(auto& r:records) {
                U allowed=0;
                const U zeros=full&~(c&r.mask);
                for(int u=0;u<25;++u)
                    if((zeros>>u&1U)&&!(cs[u]&r.signature[u]))allowed|=1U<<u;
                U direct=0;
                for(int u=0;u<25;++u) {
                    bool safe=true;
                    for(U need:r.geometric_requirements[u])
                        if((c&need)==need){safe=false;break;}
                    if(safe)direct|=1U<<u;
                }
                if(allowed!=direct) throw std::runtime_error("entrywise geometry mismatch");
                const int count=std::popcount(allowed);
                ++r.histogram[count];
                r.digest+=mixed((static_cast<Count>(c)<<25)|allowed);
                if(count>r.maximum){r.maximum=count;r.example_c=c;r.example_d=allowed;}
                const int asize=71-2*(csize+r.n);
                if(count>=asize) ++r.survivors;
            }
        }
        const U low=c&(~c+1U),next=c+low;
        c=next|(((c^next)>>2)/low);
    }
    for(const auto& r:records) {
        std::cout<<"{\"bsize\":"<<r.n<<",\"csize\":"<<csize<<",\"b\":"<<r.mask
                 <<",\"b_orbit\":"<<r.orbit<<",\"subsets\":"<<scanned<<",\"line_free_c\":"<<valid
                 <<",\"max_allowed\":"<<r.maximum<<",\"relaxation_survivors71\":"<<r.survivors
                 <<",\"example_c\":"<<r.example_c<<",\"example_allowed\":"<<r.example_d
                 <<",\"digest\":"<<r.digest<<",\"histogram\":{";
        bool first=true;
        for(int j=0;j<=25;++j)if(r.histogram[j]){
            if(!first)std::cout<<',';
            first=false;
            std::cout<<'\"'<<j<<"\":"<<r.histogram[j];
        }
        std::cout<<"}}\n";
    }
}
