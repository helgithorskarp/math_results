// Complete labelled planar census and AGL(2,5) orbit representatives.
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
    std::set<U> line_set;
    for(int a=0;a<25;++a) for(int v=1;v<25;++v) {
        U line=0;
        for(int t=0;t<5;++t)
            line|=1U<<(5*((a/5+t*(v/5))%5)+(a%5+t*(v%5))%5);
        line_set.insert(line);
    }
    if(line_set.size()!=30) throw std::runtime_error("line geometry");
    const std::vector<U> lines(line_set.begin(),line_set.end());
    std::vector<std::array<int,25>> maps;
    for(int a=0;a<5;++a) for(int b=0;b<5;++b)
    for(int c=0;c<5;++c) for(int d=0;d<5;++d) {
        if((a*d-b*c+25)%5==0) continue;
        for(int e=0;e<5;++e) for(int f=0;f<5;++f) {
            std::array<int,25> map{};
            for(int p=0;p<25;++p)
                map[p]=5*((a*(p/5)+b*(p%5)+e)%5)+(c*(p/5)+d*(p%5)+f)%5;
            maps.push_back(map);
        }
    }
    if(maps.size()!=12000) throw std::runtime_error("affine group");
    std::vector<bool> seen(1U<<25,false);
    for(int n=14;n<=17;++n) {
        std::uint64_t scanned=0,valid=0,covered=0,orbits=0;
        U mask=(1U<<n)-1U;
        while(mask<(1U<<25)) {
            ++scanned;
            bool good=true;
            for(U line:lines) if((mask&line)==line){good=false;break;}
            if(good) {
                if(n==17) throw std::runtime_error("unexpected line-free 17-set");
                ++valid;
                if(!seen[mask]) {
                    std::vector<int> points;
                    for(U scan=mask;scan;scan&=scan-1) points.push_back(std::countr_zero(scan));
                    std::vector<U> orbit;
                    for(const auto& map:maps) {
                        U image=0;
                        for(int p:points) image|=1U<<map[p];
                        orbit.push_back(image);
                    }
                    std::sort(orbit.begin(),orbit.end());
                    orbit.erase(std::unique(orbit.begin(),orbit.end()),orbit.end());
                    if(orbit.front()!=mask||12000%orbit.size()!=0)
                        throw std::runtime_error("bad orbit normalization");
                    for(U image:orbit) {
                        if(seen[image]||std::popcount(image)!=n)
                            throw std::runtime_error("overlapping orbit");
                        for(U line:lines) if((image&line)==line)
                            throw std::runtime_error("bad orbit image");
                        seen[image]=true;
                    }
                    covered+=orbit.size(); ++orbits;
                    std::cout<<n<<' '<<mask<<' '<<orbit.size()<<'\n';
                }
            }
            const U low=mask&(~mask+1U),next=mask+low;
            mask=next|(((mask^next)>>2)/low);
        }
        if(covered!=valid) throw std::runtime_error("incomplete orbit coverage");
        std::cerr<<"{\"size\":"<<n<<",\"subsets\":"<<scanned
                 <<",\"line_free\":"<<valid<<",\"orbits\":"<<orbits
                 <<",\"covered\":"<<covered<<"}\n";
    }
}
