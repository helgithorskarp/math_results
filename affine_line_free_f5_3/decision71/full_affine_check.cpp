// Independent exhaustive AGL(2,5) orbit check on the complete typed catalogue.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "profiles.hpp"

struct Map {
    std::array<unsigned char,25> image{};
    std::array<unsigned char,5> zero_row{},zero_column{};
};

int main(int argc,char**argv){
    if(argc!=3)return 2;
    std::ifstream catalogue(argv[1]),representatives(argv[2]);
    if(!catalogue || !representatives)return 3;
    std::vector<std::pair<int,std::string>> entries;
    std::unordered_map<std::string,int> index;
    int type;std::string word;
    while(catalogue>>type>>word){
        if(type<0 || type>=20 || word.size()!=25)return 4;
        int total=0;for(char c:word){if(c<'0' || c>'4')return 5;total+=c-'0';}
        if(total!=71 || index.count(word))return 6;
        index[word]=static_cast<int>(entries.size());entries.emplace_back(type,word);
    }
    std::vector<Map> maps;
    std::set<std::array<unsigned char,25>> permutations;
    for(int a=0;a<5;++a)for(int b=0;b<5;++b)for(int c=0;c<5;++c)for(int d=0;d<5;++d){
        if((a*d-b*c+25)%5==0)continue;
        for(int u=0;u<5;++u)for(int v=0;v<5;++v){
            Map map;int r=0,s=0;
            for(int x=0;x<5;++x)for(int y=0;y<5;++y){
                const int p=5*x+y,X=(a*x+b*y+u)%5,Y=(c*x+d*y+v)%5;
                map.image[p]=static_cast<unsigned char>(5*X+Y);
                if(X==0)map.zero_row[r++]=static_cast<unsigned char>(p);
                if(Y==0)map.zero_column[s++]=static_cast<unsigned char>(p);
            }
            if(r!=5 || s!=5 || !permutations.insert(map.image).second)return 7;
            maps.push_back(map);
        }
    }
    if(maps.size()!=12000)return 8;
    std::vector<bool> seen(entries.size(),false);
    int orbit_count=0,covered=0,multiplicity;
    while(representatives>>type>>word>>multiplicity){
        std::array<int,25> w{};for(int i=0;i<25;++i)w[i]=word.at(static_cast<size_t>(i))-'0';
        std::unordered_set<int> images;
        for(const auto&map:maps){
            int first=0;for(auto p:map.zero_row)first+=w[p];
            if(first>9)continue;
            int second=0;for(auto p:map.zero_column)second+=w[p];
            if(second>10 || (second==10 && first!=7))continue;
            std::string image(25,' ');std::array<int,5> rows{},cols{};
            for(int i=0;i<25;++i){
                const int j=map.image[i];image[static_cast<size_t>(j)]=word[static_cast<size_t>(i)];rows[j/5]+=w[i];cols[j%5]+=w[i];
            }
            const auto ri=std::find(PROFILES.begin(),PROFILES.end(),rows),ci=std::find(PROFILES.begin(),PROFILES.end(),cols);
            if(ri==PROFILES.end() || ci==PROFILES.end())continue;
            const std::array<int,2> pair{static_cast<int>(ri-PROFILES.begin()),static_cast<int>(ci-PROFILES.begin())};
            const auto pi=std::find(PAIRS.begin(),PAIRS.end(),pair);
            if(pi==PAIRS.end())continue;
            const int image_type=static_cast<int>(pi-PAIRS.begin());
            const auto found=index.find(image);
            if(found==index.end() || entries[found->second].first!=image_type)return 9;
            if(std::make_pair(image_type,image)<std::make_pair(type,word))return 10;
            images.insert(found->second);
        }
        if(static_cast<int>(images.size())!=multiplicity)return 11;
        for(int i:images){if(seen[i])return 12;seen[i]=true;++covered;}
        ++orbit_count;
    }
    if(covered!=static_cast<int>(entries.size()) || covered!=309611 || orbit_count!=109676)return 13;
    std::cout<<"{\"status\":\"FULL_AFFINE_PARTITION_VERIFIED\",\"maps_per_representative\":12000,\"representatives\":"<<orbit_count<<",\"typed_matrices\":"<<covered<<"}\n";
}
