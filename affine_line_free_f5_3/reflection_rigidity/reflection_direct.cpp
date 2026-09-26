// Exact line-reflection layer search: actual 25-point subsets and geometric lines.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using Bits=std::array<std::uint64_t,10>;
using Row=std::array<int,5>;
int main(int argc,char**argv) {
    if(argc<4||argc>7)return 2;
    const int size=std::stoi(argv[1]),cm=std::stoi(argv[2]),first=std::stoi(argv[3]);
    if(size<1||size>80||cm<0||cm>=31)return 2;
    const int nc=std::popcount(static_cast<unsigned>(cm));
    if((size-nc)%2)return 2;
    const int target=(size-nc)/2;
    std::vector<std::array<int,2>> pairs;
    for(int p=1;p<25;++p){const int q=5*((5-p/5)%5)+(5-p%5)%5;if(p<q)pairs.push_back({p,q});}
    if(pairs.size()!=12)throw std::runtime_error("pairs");
    std::set<std::uint32_t> lines;
    for(int a=0;a<25;++a)for(int v=1;v<25;++v) {
        std::uint32_t line=0;
        for(int t=0;t<5;++t)line|=1U<<(5*((a/5+t*(v/5))%5)+(a%5+t*(v%5))%5);
        lines.insert(line);
    }
    if(lines.size()!=30)throw std::runtime_error("lines");
    std::array<std::vector<int>,2> menus;
    std::array<std::array<std::uint32_t,4096>,2> lifted{};
    std::array<int,4096> weight{};
    for(int m=0;m<4096;++m) {
        weight[static_cast<std::size_t>(m)]=std::popcount(static_cast<unsigned>(m));
        std::uint32_t subset=0;
        for(int i=0;i<12;++i)if(m>>i&1)for(int p:pairs[static_cast<std::size_t>(i)])subset|=1U<<p;
        for(int c=0;c<2;++c) {
            const auto s=subset|static_cast<std::uint32_t>(c);
            lifted[static_cast<std::size_t>(c)][static_cast<std::size_t>(m)]=s;
            bool ok=true;for(auto l:lines)if((s&l)==l){ok=false;break;}
            if(ok)menus[static_cast<std::size_t>(c)].push_back(m);
        }
    }
    Row order{0,1,2,3,4};
    // Put the smaller centered menus first; tie break by original x coordinate.
    std::stable_sort(order.begin(),order.end(),[cm](int x,int y){return (cm>>x&1)>(cm>>y&1);});
    if(argc>=5) {
        const std::string requested=argv[4];
        if(requested.size()!=5)return 2;
        std::set<int> used;
        for(int j=0;j<5;++j){const int x=requested[static_cast<std::size_t>(j)]-'0';if(x<0||x>4||!used.insert(x).second)return 2;order[static_cast<std::size_t>(j)]=x;}
    }
    const bool second_restricted=argc>=6&&std::string(argv[5])!="-";
    std::set<int> seconds,common;
    if(second_restricted) {
        std::ifstream source(argv[5]);int m=0;
        if(!source)return 2;
        while(source>>m){if(m<0||m>=4096)return 2;seconds.insert(m);}
        if(!source.eof()||seconds.empty())return 2;
    }
    if(argc==7) {
        std::ifstream source(argv[6]);int m=0;
        if(!source)return 2;
        while(source>>m){if(m<0||m>=4096)return 2;common.insert(m);}
        if(!source.eof()||common.empty())return 2;
    }
    Row cap{},minimum{};int total_cap=0;
    for(int j=0;j<5;++j){cap[static_cast<std::size_t>(j)]=(cm>>order[static_cast<std::size_t>(j)]&1)?6:8;total_cap+=cap[static_cast<std::size_t>(j)];}
    std::array<std::vector<int>,5> opts;
    for(int j=0;j<5;++j) {
        minimum[static_cast<std::size_t>(j)]=std::max(0,target-total_cap+cap[static_cast<std::size_t>(j)]);
        for(int m:menus[static_cast<std::size_t>(cm>>order[static_cast<std::size_t>(j)]&1)]) {
            if(weight[static_cast<std::size_t>(m)]<minimum[static_cast<std::size_t>(j)])continue;
            if(j==0&&first>=0&&m!=first)continue;
            if(j==1&&second_restricted&&!seconds.contains(m))continue;
            if(argc==7&&!common.contains(m))continue;
            opts[static_cast<std::size_t>(j)].push_back(m);
        }
    }
    std::vector<std::array<Bits,4096>> hit(5);
    for(int j=0;j<5;++j)for(int m:opts[static_cast<std::size_t>(j)]) {
        const int x=order[static_cast<std::size_t>(j)];
        const auto s=lifted[static_cast<std::size_t>(cm>>x&1)][static_cast<std::size_t>(m)];
        int l=0;
        for(int a=0;a<25;++a)for(int v=0;v<25;++v,++l) {
            const int p=5*((a/5+x*(v/5))%5)+(a%5+x*(v%5))%5;
            if(s>>p&1U)hit[static_cast<std::size_t>(j)][static_cast<std::size_t>(m)][static_cast<std::size_t>(l/64)]|=1ULL<<(l%64);
        }
    }
    std::array<std::vector<int>,9> last;
    for(int e:opts[4])last[static_cast<std::size_t>(weight[static_cast<std::size_t>(e)])].push_back(e);
    std::uint64_t triples=0,quads=0,tuples=0,solutions=0;
    Row witness{};
    for(int a:opts[0])for(int b:opts[1]) {
        Bits ab{};for(int i=0;i<10;++i)ab[static_cast<std::size_t>(i)]=hit[0][static_cast<std::size_t>(a)][static_cast<std::size_t>(i)]&hit[1][static_cast<std::size_t>(b)][static_cast<std::size_t>(i)];
        for(int c:opts[2]) {
            if(second_restricted&&weight[static_cast<std::size_t>(c)]>weight[static_cast<std::size_t>(b)])continue;
            const int w=weight[static_cast<std::size_t>(a)]+weight[static_cast<std::size_t>(b)]+weight[static_cast<std::size_t>(c)];
            if(w+cap[3]+cap[4]<target)continue;
            ++triples;Bits abc{};
            for(int i=0;i<10;++i)abc[static_cast<std::size_t>(i)]=ab[static_cast<std::size_t>(i)]&hit[2][static_cast<std::size_t>(c)][static_cast<std::size_t>(i)];
            for(int d:opts[3]) {
                if(second_restricted&&weight[static_cast<std::size_t>(d)]>weight[static_cast<std::size_t>(b)])continue;
                const int need=target-w-weight[static_cast<std::size_t>(d)];
                if(need<minimum[4]||need>cap[4])continue;
                if(second_restricted&&need>weight[static_cast<std::size_t>(b)])continue;
                ++quads;Bits abcd{};
                for(int i=0;i<10;++i)abcd[static_cast<std::size_t>(i)]=abc[static_cast<std::size_t>(i)]&hit[3][static_cast<std::size_t>(d)][static_cast<std::size_t>(i)];
                for(int e:last[static_cast<std::size_t>(need)]) {
                    ++tuples;bool valid=true;
                    for(int i=0;i<10;++i)if(abcd[static_cast<std::size_t>(i)]&hit[4][static_cast<std::size_t>(e)][static_cast<std::size_t>(i)]){valid=false;break;}
                    if(valid) {
                        ++solutions;
                        if(solutions==1){const Row raw{a,b,c,d,e};for(int j=0;j<5;++j)witness[static_cast<std::size_t>(order[static_cast<std::size_t>(j)])]=raw[static_cast<std::size_t>(j)];}
                    }
                }
            }
        }
    }
    std::cout<<"{\"size\":"<<size<<",\"center_mask\":"<<cm<<",\"first_mask\":"<<first<<",\"triples\":"<<triples<<",\"quadruples\":"<<quads<<",\"tuples\":"<<tuples<<",\"solutions\":"<<solutions;
    if(solutions){std::cout<<",\"witness_masks\":[";for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<witness[static_cast<std::size_t>(i)];}std::cout<<']';}
    std::cout<<"}\n";
}
