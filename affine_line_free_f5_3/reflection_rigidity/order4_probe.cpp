// For diag(2,T), B occurs at x=+-1 and T(B) at x=+-2.
// Find every possible x=0 point that does not complete a transverse line.
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using U=std::uint32_t;
int main() {
    std::set<U> line_set;
    for(int a=0;a<25;++a)for(int v=1;v<25;++v) {
        U line=0;
        for(int t=0;t<5;++t)line|=1U<<(5*((a/5+t*(v/5))%5)+(a%5+t*(v%5))%5);
        line_set.insert(line);
    }
    const std::vector<U> lines(line_set.begin(),line_set.end());
    if(lines.size()!=30)throw std::runtime_error("geometry");
    std::vector<int> dirs;
    for(int v=1;v<25;++v){const int nv=5*((5-v/5)%5)+(5-v%5)%5;if(v<nv)dirs.push_back(v);}
    std::array<std::array<U,12>,25> pairs{},twopairs{};
    for(int u=0;u<25;++u)for(int j=0;j<12;++j) {
        const int v=dirs[static_cast<std::size_t>(j)];
        for(int t:{1,4})pairs[static_cast<std::size_t>(u)][static_cast<std::size_t>(j)]|=1U<<(5*((u/5+t*(v/5))%5)+(u%5+t*(v%5))%5);
        for(int t:{2,3})twopairs[static_cast<std::size_t>(u)][static_cast<std::size_t>(j)]|=1U<<(5*((u/5+t*(v/5))%5)+(u%5+t*(v%5))%5);
    }
    constexpr U full=(1U<<25)-1U;
    for(int bsize=14;bsize<=16;++bsize) {
        std::uint64_t candidates=0,valid_b=0;
        std::array<int,3> maximum{-1,-1,-1};
        std::array<std::uint64_t,3> survivors{};
        std::array<U,3> witness_b{},witness_d{};
        std::array<std::array<std::uint64_t,26>,3> histogram{};
        U b=(1U<<bsize)-1U;
        while(b<(1U<<25)) {
            ++candidates;
            bool valid=true;for(U line:lines)if((b&line)==line){valid=false;break;}
            if(valid) {
                ++valid_b;
                for(int kind=0;kind<3;++kind) {
                    U tb=0;
                    for(int p=0;p<25;++p)if(b>>p&1U) {
                        const int y=kind==2?(5-p/5)%5:p/5;
                        const int z=kind==0?p%5:(5-p%5)%5;
                        tb|=1U<<(5*y+z);
                    }
                    U allowed=full&~(b&tb),scan=allowed;
                    while(scan) {
                        const int u=std::countr_zero(scan);scan&=scan-1;
                        for(int j=0;j<12;++j) {
                            const U p=pairs[static_cast<std::size_t>(u)][static_cast<std::size_t>(j)],q=twopairs[static_cast<std::size_t>(u)][static_cast<std::size_t>(j)];
                            if((b&p)==p&&(tb&q)==q){allowed&=~(1U<<u);break;}
                        }
                    }
                    const int count=std::popcount(allowed);
                    ++histogram[static_cast<std::size_t>(kind)][static_cast<std::size_t>(count)];
                    if(4*bsize+count>=71)++survivors[static_cast<std::size_t>(kind)];
                    if(count>maximum[static_cast<std::size_t>(kind)]){maximum[static_cast<std::size_t>(kind)]=count;witness_b[static_cast<std::size_t>(kind)]=b;witness_d[static_cast<std::size_t>(kind)]=allowed;}
                }
            }
            const U low=b&(~b+1U),next=b+low;
            b=next|(((b^next)>>2)/low);
        }
        for(int kind=0;kind<3;++kind) {
            std::cout<<"{\"bsize\":"<<bsize<<",\"kind\":"<<kind<<",\"subsets\":"<<candidates<<",\"line_free_b\":"<<valid_b<<",\"max_allowed\":"<<maximum[static_cast<std::size_t>(kind)]<<",\"relaxation_survivors71\":"<<survivors[static_cast<std::size_t>(kind)]<<",\"example_b\":"<<witness_b[static_cast<std::size_t>(kind)]<<",\"example_allowed\":"<<witness_d[static_cast<std::size_t>(kind)]<<",\"histogram\":{";
            bool first=true;
            for(int n=0;n<=25;++n)if(histogram[static_cast<std::size_t>(kind)][static_cast<std::size_t>(n)]) {
                if(!first)std::cout<<',';
                first=false;
                std::cout<<'\"'<<n<<"\":"<<histogram[static_cast<std::size_t>(kind)][static_cast<std::size_t>(n)];
            }
            std::cout<<"}}\n"<<std::flush;
        }
    }
}
