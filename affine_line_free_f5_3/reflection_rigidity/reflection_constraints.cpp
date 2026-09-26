// Orbit-constraint enumeration with forbidden masks; different representation
// from reflection_direct.cpp's actual subsets and transversal bit vectors.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using Row=std::array<int,5>;
int main(int argc,char**argv) {
    if(argc!=6&&argc!=7)return 2;
    std::ifstream input(argv[1]);
    const int size=std::stoi(argv[2]),cm=std::stoi(argv[3]),first=std::stoi(argv[4]);
    const std::string perm=argv[5];
    if(!input||cm<0||cm>=31||perm.size()!=5)return 2;
    Row order{},center{},cap{},minimum{};std::set<int> used;
    int nc=0,total_cap=0;
    for(int j=0;j<5;++j) {
        const int x=perm[static_cast<std::size_t>(j)]-'0';
        if(x<0||x>4||!used.insert(x).second)return 2;
        order[static_cast<std::size_t>(j)]=x;
        center[static_cast<std::size_t>(j)]=(cm>>x)&1;
        nc+=center[static_cast<std::size_t>(j)];
        cap[static_cast<std::size_t>(j)]=center[static_cast<std::size_t>(j)]?6:8;
        total_cap+=cap[static_cast<std::size_t>(j)];
    }
    if((size-nc)%2)return 2;
    const int total=(size-nc)/2;
    std::array<int,4096> weight{};
    for(int m=0;m<4096;++m)weight[static_cast<std::size_t>(m)]=std::popcount(static_cast<unsigned>(m));
    std::array<std::vector<int>,2> menus;
    for(auto& menu:menus) {
        int n=0;input>>n;
        if(n<0||n>4096)return 2;
        for(int j=0;j<n;++j){int m=-1;input>>m;if(m<0||m>=4096)return 2;menu.push_back(m);}
    }
    int n=0;input>>n;if(n!=313)return 2;
    std::vector<Row> lines;
    for(int i=0;i<n;++i) {
        Row raw{},row{};for(int& x:raw){input>>x;if(x<0||x>12)return 2;}
        bool relevant=true;
        for(int j=0;j<5;++j){row[static_cast<std::size_t>(j)]=raw[static_cast<std::size_t>(order[static_cast<std::size_t>(j)])];if(row[static_cast<std::size_t>(j)]==12&&!center[static_cast<std::size_t>(j)])relevant=false;}
        if(relevant)lines.push_back(row);
    }
    if(!input)return 2;
    std::set<int> seconds;
    if(argc==7) {
        std::ifstream source(argv[6]);int m=0;
        if(!source)return 2;
        while(source>>m){if(m<0||m>=4096)return 2;seconds.insert(m);}
        if(!source.eof()||seconds.empty())return 2;
    }
    std::array<std::vector<int>,5> opts;
    for(int j=0;j<5;++j) {
        minimum[static_cast<std::size_t>(j)]=std::max(0,total-total_cap+cap[static_cast<std::size_t>(j)]);
        for(int m:menus[static_cast<std::size_t>(center[static_cast<std::size_t>(j)])]) {
            const int w=weight[static_cast<std::size_t>(m)];
            if(w<minimum[static_cast<std::size_t>(j)])continue;
            if(w>cap[static_cast<std::size_t>(j)])throw std::runtime_error("local cap failure");
            if(j==0&&first>=0&&m!=first)continue;
            if(j==1&&argc==7&&!seconds.contains(m))continue;
            opts[static_cast<std::size_t>(j)].push_back(m);
        }
    }
    std::array<std::array<int,4096>,9> completions{},last_first{};
    for(int w=0;w<=8;++w)for(int banned=0;banned<4096;++banned) {
        last_first[static_cast<std::size_t>(w)][static_cast<std::size_t>(banned)]=-1;
        for(int m:opts[4])if(weight[static_cast<std::size_t>(m)]==w&&(m&banned)==0) {
            ++completions[static_cast<std::size_t>(w)][static_cast<std::size_t>(banned)];
            if(last_first[static_cast<std::size_t>(w)][static_cast<std::size_t>(banned)]<0)last_first[static_cast<std::size_t>(w)][static_cast<std::size_t>(banned)]=m;
        }
    }
    std::uint64_t triples=0,quads=0,tuples=0,solutions=0;Row witness{};
    for(int a:opts[0])for(int b:opts[1])for(int c:opts[2]) {
        if(argc==7&&weight[static_cast<std::size_t>(c)]>weight[static_cast<std::size_t>(b)])continue;
        const int w=weight[static_cast<std::size_t>(a)]+weight[static_cast<std::size_t>(b)]+weight[static_cast<std::size_t>(c)];
        if(w+cap[3]+cap[4]<total)continue;
        ++triples;std::array<int,12> ban{};int base=0;
        for(auto row:lines) {
            if(row[0]!=12&&!(a>>row[0]&1))continue;
            if(row[1]!=12&&!(b>>row[1]&1))continue;
            if(row[2]!=12&&!(c>>row[2]&1))continue;
            if(row[3]==12)base|=1<<row[4];else ban[static_cast<std::size_t>(row[3])]|=1<<row[4];
        }
        for(int d:opts[3]) {
            if(argc==7&&weight[static_cast<std::size_t>(d)]>weight[static_cast<std::size_t>(b)])continue;
            const int need=total-w-weight[static_cast<std::size_t>(d)];
            if(need<minimum[4]||need>cap[4])continue;
            if(argc==7&&need>weight[static_cast<std::size_t>(b)])continue;
            ++quads;
            tuples+=static_cast<std::uint64_t>(completions[static_cast<std::size_t>(need)][0]);
            int banned=base,m=d;
            while(m) {
                const int i=std::countr_zero(static_cast<unsigned>(m));m&=m-1;
                banned|=ban[static_cast<std::size_t>(i)];
                if(std::popcount(static_cast<unsigned>(banned))>12-need)break;
            }
            if(banned&4096||std::popcount(static_cast<unsigned>(banned))>12-need)continue;
            const int count=completions[static_cast<std::size_t>(need)][static_cast<std::size_t>(banned)];
            if(count&&!solutions) {
                const Row raw{a,b,c,d,last_first[static_cast<std::size_t>(need)][static_cast<std::size_t>(banned)]};
                for(int j=0;j<5;++j)witness[static_cast<std::size_t>(order[static_cast<std::size_t>(j)])]=raw[static_cast<std::size_t>(j)];
            }
            solutions+=static_cast<std::uint64_t>(count);
        }
    }
    std::cout<<"{\"size\":"<<size<<",\"center_mask\":"<<cm<<",\"first_mask\":"<<first<<",\"triples\":"<<triples<<",\"quadruples\":"<<quads<<",\"tuples\":"<<tuples<<",\"solutions\":"<<solutions;
    if(solutions){std::cout<<",\"witness_masks\":[";for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<witness[static_cast<std::size_t>(i)];}std::cout<<']';}
    std::cout<<"}\n";
}
