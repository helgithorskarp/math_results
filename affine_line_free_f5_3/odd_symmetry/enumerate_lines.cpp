// Independent representation: actual 25-bit plane subsets and 625 geometric
// transversals. No input catalogue, orbit-constraint file, or SAT solver.
#include <algorithm>
#include <array>
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using Row=std::array<int,5>;
int main(int argc,char**argv) {
    if(argc!=3)return 2;
    const int size=std::stoi(argv[1]), cm=std::stoi(argv[2]);
    if(size<64||size>72||cm<0||cm>=32)return 2;
    Row center{};int nc=0;
    for(int j=0;j<5;++j){center[static_cast<std::size_t>(j)]=(cm>>j)&1;nc+=center[static_cast<std::size_t>(j)];}
    if(nc==5||(size-nc)%3!=0)return 2;
    const int target=(size-nc)/3;
    std::array<bool,25> used{};used[0]=true;
    std::vector<std::array<int,3>> orbits;
    for(int p=1;p<25;++p)if(!used[static_cast<std::size_t>(p)]) {
        int q=p;std::array<int,3> orbit{};
        for(int j=0;j<3;++j) {
            orbit[static_cast<std::size_t>(j)]=q;used[static_cast<std::size_t>(q)]=true;
            const int y=q/5,z=q%5;q=5*((5-z)%5)+(y-z+5)%5;
        }
        if(q!=p)throw std::runtime_error("orbit");
        orbits.push_back(orbit);
    }
    if(orbits.size()!=8)throw std::runtime_error("orbit count");
    std::set<std::uint32_t> planar;
    for(int a=0;a<25;++a)for(int b=1;b<25;++b) {
        std::uint32_t line=0;
        for(int t=0;t<5;++t)line|=std::uint32_t(1)<<(5*((a/5+t*(b/5))%5)+(a%5+t*(b%5))%5);
        planar.insert(line);
    }
    if(planar.size()!=30)throw std::runtime_error("planar lines");
    std::vector<Row> transverse;
    for(int a=0;a<25;++a)for(int v=0;v<25;++v) {
        Row row{};
        for(int x=0;x<5;++x)row[static_cast<std::size_t>(x)]=5*((a/5+x*(v/5))%5)+(a%5+x*(v%5))%5;
        transverse.push_back(row);
    }
    std::array<std::array<std::uint32_t,256>,2> lifted{};
    std::array<int,256> weight{};
    std::array<std::vector<int>,2> menus;
    for(int c=0;c<2;++c)for(int m=0;m<256;++m) {
        weight[static_cast<std::size_t>(m)]=std::popcount(static_cast<unsigned>(m));
        std::uint32_t points=static_cast<std::uint32_t>(c);
        for(int j=0;j<8;++j)if(m>>j&1)for(int p:orbits[static_cast<std::size_t>(j)])points|=std::uint32_t(1)<<p;
        lifted[static_cast<std::size_t>(c)][static_cast<std::size_t>(m)]=points;
        bool valid=true;for(auto l:planar)if((points&l)==l){valid=false;break;}
        if(valid)menus[static_cast<std::size_t>(c)].push_back(m);
    }
    for(const auto& menu:menus)for(int m:menu)if(weight[static_cast<std::size_t>(m)]>5)throw std::runtime_error("cap");
    std::array<std::array<std::bitset<625>,256>,5> hit{};
    std::array<std::vector<int>,5> options;
    const int minimum=std::max(0,target-20);
    for(int x=0;x<5;++x)for(int m:menus[static_cast<std::size_t>(center[static_cast<std::size_t>(x)])]) {
        if(weight[static_cast<std::size_t>(m)]<minimum)continue;
        options[static_cast<std::size_t>(x)].push_back(m);
        const auto points=lifted[static_cast<std::size_t>(center[static_cast<std::size_t>(x)])][static_cast<std::size_t>(m)];
        for(int l=0;l<625;++l)if(points>>transverse[static_cast<std::size_t>(l)][static_cast<std::size_t>(x)]&1U)
            hit[static_cast<std::size_t>(x)][static_cast<std::size_t>(m)].set(static_cast<std::size_t>(l));
    }
    std::array<std::vector<int>,6> last;
    for(int m:options[4])last[static_cast<std::size_t>(weight[static_cast<std::size_t>(m)])].push_back(m);
    std::uint64_t triples=0,quads=0,solutions=0;
    Row first{};bool found=false;
    std::vector<Row> witnesses;
    for(int a:options[0])for(int b:options[1]) {
        const auto ab=hit[0][static_cast<std::size_t>(a)]&hit[1][static_cast<std::size_t>(b)];
        for(int c:options[2]) {
            const int w=weight[static_cast<std::size_t>(a)]+weight[static_cast<std::size_t>(b)]+weight[static_cast<std::size_t>(c)];
            if(w+10<target)continue;
            ++triples;
            const auto abc=ab&hit[2][static_cast<std::size_t>(c)];
            for(int d:options[3]) {
                const int needed=target-w-weight[static_cast<std::size_t>(d)];
                if(needed<minimum||needed>5)continue;
                ++quads;
                const auto abcd=abc&hit[3][static_cast<std::size_t>(d)];
                for(int e:last[static_cast<std::size_t>(needed)])
                    if((abcd&hit[4][static_cast<std::size_t>(e)]).none()) {
                        ++solutions;
                        witnesses.push_back(Row{a,b,c,d,e});
                        if(witnesses.size()>100000)throw std::runtime_error("witness output limit");
                        if(!found){first={a,b,c,d,e};found=true;}
                    }
            }
        }
    }
    std::cout<<"{\"size\":"<<size<<",\"center_mask\":"<<cm<<",\"orbit_total\":"<<target<<",\"triples\":"<<triples<<",\"quadruples\":"<<quads<<",\"solutions\":"<<solutions;
    if(found){std::cout<<",\"first_masks\":[";for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<first[static_cast<std::size_t>(i)];}std::cout<<']';}
    std::cout<<",\"solution_masks\":[";
    for(std::size_t i=0;i<witnesses.size();++i) {
        if(i)std::cout<<',';
        std::cout<<'[';
        for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<witnesses[i][static_cast<std::size_t>(j)];}
        std::cout<<']';
    }
    std::cout<<"]}\n";
}
