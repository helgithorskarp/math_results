// Independent planar census by Gray-code toggles; test all 25 geometric slopes.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using U=std::uint32_t;
int main() {
    std::set<std::array<int,5>> all_lines;
    for(int a=0;a<25;++a)for(int v=1;v<25;++v) {
        std::array<int,5> line{};
        for(int t=0;t<5;++t)line[static_cast<std::size_t>(t)]=5*((a/5+t*(v/5))%5)+(a%5+t*(v%5))%5;
        std::sort(line.begin(),line.end());all_lines.insert(line);
    }
    if(all_lines.size()!=30)throw std::runtime_error("line count");
    std::array<std::vector<int>,25> through;
    int j=0;for(auto line:all_lines){for(int p:line)through[static_cast<std::size_t>(p)].push_back(j);++j;}
    for(auto v:through)if(v.size()!=6)throw std::runtime_error("pencil");
    std::array<std::array<std::array<int,4>,25>,25> trans{};
    for(int u=0;u<25;++u)for(int v=0;v<25;++v)for(int t=1;t<=4;++t)
        trans[static_cast<std::size_t>(u)][static_cast<std::size_t>(v)][static_cast<std::size_t>(t-1)]=5*((u/5+t*(v/5))%5)+(u%5+t*(v%5))%5;
    std::array<int,30> counts{};
    std::array<bool,25> selected{};
    std::array<std::array<std::array<std::uint64_t,26>,3>,3> hist{};
    std::array<std::uint64_t,3> tested{},valid{};
    int size=0,bad=0,planar_max=0;U previous=0;
    for(U i=1;i<(1U<<25);++i) {
        const U gray=i^(i>>1),change=gray^previous;previous=gray;
        const int p=std::countr_zero(change),delta=(gray>>p&1U)?1:-1;
        selected[static_cast<std::size_t>(p)]=delta==1;size+=delta;
        for(int line:through[static_cast<std::size_t>(p)]) {
            int& c=counts[static_cast<std::size_t>(line)];
            if(c==5)--bad;
            c+=delta;
            if(c==5)++bad;
        }
        if(!bad)planar_max=std::max(planar_max,size);
        if(size<14||size>16)continue;
        ++tested[static_cast<std::size_t>(size-14)];
        if(bad)continue;
        ++valid[static_cast<std::size_t>(size-14)];
        for(int kind=0;kind<3;++kind) {
            std::array<bool,25> image{};
            for(int q=0;q<25;++q) {
                const int y=kind==2?(5-q/5)%5:q/5,z=kind==0?q%5:(5-q%5)%5;
                image[static_cast<std::size_t>(5*y+z)]=selected[static_cast<std::size_t>(q)];
            }
            int allowed=0;
            for(int u=0;u<25;++u) {
                bool possible=true;
                for(int v=0;v<25;++v) {
                    const auto row=trans[static_cast<std::size_t>(u)][static_cast<std::size_t>(v)];
                    if(selected[static_cast<std::size_t>(row[0])]&&image[static_cast<std::size_t>(row[1])]&&image[static_cast<std::size_t>(row[2])]&&selected[static_cast<std::size_t>(row[3])]){possible=false;break;}
                }
                if(possible)++allowed;
            }
            ++hist[static_cast<std::size_t>(size-14)][static_cast<std::size_t>(kind)][static_cast<std::size_t>(allowed)];
        }
    }
    if(planar_max!=16)throw std::runtime_error("planar maximum");
    for(int s=0;s<3;++s)for(int kind=0;kind<3;++kind) {
        const auto& h=hist[static_cast<std::size_t>(s)][static_cast<std::size_t>(kind)];
        int maximum=0;std::uint64_t survivors=0;
        for(int n=0;n<=25;++n)if(h[static_cast<std::size_t>(n)]){maximum=n;if(4*(s+14)+n>=71)survivors+=h[static_cast<std::size_t>(n)];}
        std::cout<<"{\"bsize\":"<<s+14<<",\"kind\":"<<kind<<",\"subsets\":"<<tested[static_cast<std::size_t>(s)]<<",\"line_free_b\":"<<valid[static_cast<std::size_t>(s)]<<",\"max_allowed\":"<<maximum<<",\"relaxation_survivors71\":"<<survivors<<",\"histogram\":{";
        bool first=true;
        for(int n=0;n<=25;++n)if(h[static_cast<std::size_t>(n)]) {
            if(!first)std::cout<<',';
            first=false;
            std::cout<<'\"'<<n<<"\":"<<h[static_cast<std::size_t>(n)];
        }
        std::cout<<"}}\n";
    }
}
