// Audit normalized quotient orbits by all 12,000 affine maps of AG(2,5).
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
int main(int argc,char**argv) {
    if(argc!=3)throw std::runtime_error("raw representatives");
    std::ifstream raw(argv[1]),reps(argv[2]);std::string w;
    std::map<std::string,int> owner;
    while(raw>>w)if(w.size()!=25||!owner.emplace(w,-1).second)throw std::runtime_error("raw input");
    std::vector<std::string> representatives;while(reps>>w)representatives.push_back(w);
    std::uint64_t maps=0;std::vector<int> sizes;
    for(int k=0;k<static_cast<int>(representatives.size());++k) {
        std::set<std::string> images;
        for(int a=0;a<5;++a)for(int b=0;b<5;++b)for(int c=0;c<5;++c)for(int d=0;d<5;++d) {
            if((a*d-b*c+25)%5==0)continue;
            for(int tx=0;tx<5;++tx)for(int ty=0;ty<5;++ty) {
                ++maps;std::string image(25,'?');
                for(int x=0;x<5;++x)for(int y=0;y<5;++y)
                    image[5*((a*x+b*y+tx)%5)+(c*x+d*y+ty)%5]=representatives[k][5*x+y];
                auto it=owner.find(image);if(it==owner.end())continue;
                if(it->second!=-1&&it->second!=k)throw std::runtime_error("overlapping classes");
                it->second=k;images.insert(image);
            }
        }
        if(images.empty()||*images.begin()!=representatives[k])throw std::runtime_error("noncanonical representative");
        sizes.push_back(static_cast<int>(images.size()));
    }
    for(const auto& item:owner)if(item.second<0)throw std::runtime_error("uncovered quotient");
    std::cout<<"{\"maps\":"<<maps<<",\"covered\":"<<owner.size()<<",\"sizes\":[";
    for(std::size_t i=0;i<sizes.size();++i){if(i)std::cout<<',';std::cout<<sizes[i];}
    std::cout<<"]}\n";
}
