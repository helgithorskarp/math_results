// Complete enumeration of order-three invariant line-free layer choices.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <stdexcept>
using Row=std::array<int,5>;
int main(int argc,char**argv) {
    if(argc!=4)return 2;
    std::ifstream input(argv[1]);const int size=std::stoi(argv[2]);
    const int center_mask=std::stoi(argv[3]);
    if(!input||size<64||size>72||center_mask<0||center_mask>=32)return 2;
    Row center{};int nc=0;
    for(int j=0;j<5;++j){center[static_cast<std::size_t>(j)]=(center_mask>>j)&1;nc+=center[static_cast<std::size_t>(j)];}
    if(nc==5||(size-nc)%3!=0)return 2;
    const int total=(size-nc)/3, minimum=std::max(0,total-20);
    std::array<std::vector<int>,2> all;
    std::array<int,256> weight{};
    for(int m=0;m<256;++m)weight[static_cast<std::size_t>(m)]=std::popcount(static_cast<unsigned>(m));
    for(auto& menu:all) {
        int n;input>>n;
        for(int i=0;i<n;++i){int m;input>>m;if(m<0||m>=256||weight[static_cast<std::size_t>(m)]>5)return 2;menu.push_back(m);}
    }
    int nlines;input>>nlines;
    std::vector<Row> lines;
    for(int i=0;i<nlines;++i) {
        Row row{};bool relevant=true;
        for(int j=0;j<5;++j){input>>row[static_cast<std::size_t>(j)];if(row[static_cast<std::size_t>(j)]<0||row[static_cast<std::size_t>(j)]>8)return 2;if(row[static_cast<std::size_t>(j)]==8&&!center[static_cast<std::size_t>(j)])relevant=false;}
        if(relevant)lines.push_back(row);
    }
    if(!input)return 2;
    std::array<std::vector<int>,5> menu;
    for(int j=0;j<5;++j)for(int m:all[static_cast<std::size_t>(center[static_cast<std::size_t>(j)])])
        if(weight[static_cast<std::size_t>(m)]>=minimum)menu[static_cast<std::size_t>(j)].push_back(m);
    std::array<std::array<std::vector<int>,256>,6> last{};
    for(int k=0;k<=5;++k)for(int banned=0;banned<256;++banned)
        for(int m:menu[4])if(weight[static_cast<std::size_t>(m)]==k && (m&banned)==0)
            last[static_cast<std::size_t>(k)][static_cast<std::size_t>(banned)].push_back(m);
    std::uint64_t triples=0,quads=0,solutions=0;
    Row witness{};bool found=false;
    std::vector<Row> witnesses;
    for(int a:menu[0])for(int b:menu[1])for(int c:menu[2]) {
        const int abc=weight[static_cast<std::size_t>(a)]+weight[static_cast<std::size_t>(b)]+weight[static_cast<std::size_t>(c)];
        if(abc+10<total)continue;
        ++triples;
        std::array<int,8> ban{};int base=0;
        for(const auto& line:lines) {
            if(line[0]!=8&&!(a>>line[0]&1))continue;
            if(line[1]!=8&&!(b>>line[1]&1))continue;
            if(line[2]!=8&&!(c>>line[2]&1))continue;
            const int bit=1<<line[4];
            if(line[3]==8)base|=bit;else ban[static_cast<std::size_t>(line[3])]|=bit;
        }
        for(int d:menu[3]) {
            const int needed=total-abc-weight[static_cast<std::size_t>(d)];
            if(needed<minimum||needed>5)continue;
            ++quads;
            int banned=base;
            for(int i=0;i<8;++i)if(d>>i&1)banned|=ban[static_cast<std::size_t>(i)];
            if(banned&256)continue;
            const auto& completions=last[static_cast<std::size_t>(needed)][static_cast<std::size_t>(banned)];
            solutions+=completions.size();
            for(int e:completions)witnesses.push_back(Row{a,b,c,d,e});
            if(witnesses.size()>100000)throw std::runtime_error("witness output limit");
            if(!completions.empty()&&!found){witness={a,b,c,d,completions[0]};found=true;}
        }
    }
    std::cout<<"{\"size\":"<<size<<",\"center_mask\":"<<center_mask<<",\"orbit_total\":"<<total<<",\"triples\":"<<triples<<",\"quadruples\":"<<quads<<",\"solutions\":"<<solutions;
    if(found){std::cout<<",\"first_masks\":[";for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<witness[static_cast<std::size_t>(i)];}std::cout<<']';}
    std::cout<<",\"solution_masks\":[";
    for(std::size_t i=0;i<witnesses.size();++i) {
        if(i)std::cout<<',';
        std::cout<<'[';
        for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<witnesses[i][static_cast<std::size_t>(j)];}
        std::cout<<']';
    }
    std::cout<<"]}\n";
}
