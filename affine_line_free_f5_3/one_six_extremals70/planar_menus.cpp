// Exhaust all relevant planar subsets, using all30 affine lines.
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
using U=std::uint32_t;
int main(int argc,char**argv) {
    if(argc!=2)throw std::runtime_error("output directory required");
    std::set<U> lines;
    for(int x=0;x<5;++x)for(int y=0;y<5;++y)
    for(int a=0;a<5;++a)for(int b=0;b<5;++b)if(a||b) {
        U line=0;
        for(int t=0;t<5;++t)line|=1U<<(5*((x+t*a)%5)+(y+t*b)%5);
        lines.insert(line);
    }
    if(lines.size()!=30)throw std::runtime_error("planar geometry");
    for(int n:std::array<int,3>{6,16,17}) {
        std::ofstream out(std::string(argv[1])+"/planar"+std::to_string(n)+".txt");
        if(!out)throw std::runtime_error("menu output");
        std::uint64_t total=0,accepted=0;
        const int cap=n==6?3:4;
        for(U mask=(1U<<n)-1;mask<(1U<<25);) {
            ++total;bool good=true;
            for(U line:lines)if(std::popcount(mask&line)>cap){good=false;break;}
            if(good){++accepted;out<<mask<<'\n';}
            const U low=mask&(~mask+1U),next=mask+low;
            mask=next|(((mask^next)>>2)/low);
        }
        std::cout<<"{\"size\":"<<n<<",\"line_cap\":"<<cap
                 <<",\"visited\":"<<total<<",\"accepted\":"<<accepted<<"}\n";
    }
}
