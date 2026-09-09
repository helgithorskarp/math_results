#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <filesystem>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

struct Bits {
    std::uint64_t lo=0,hi=0;
    Bits operator&(Bits b) const {return {lo&b.lo,hi&b.hi};}
    Bits without(Bits b) const {return {lo&~b.lo,hi&~b.hi};}
    void add(unsigned x) {if(x<64)lo|=std::uint64_t{1}<<x;else hi|=std::uint64_t{1}<<(x-64);}
    unsigned size() const {return std::popcount(lo)+std::popcount(hi);}
    bool has(unsigned x) const {return x<64 ? ((lo>>x)&1)!=0 : ((hi>>(x-64))&1)!=0;}
};
Bits tail(unsigned c) {
    if(c>=128)return {};
    if(c>=64)return {0,~std::uint64_t{0}<<(c-64)};
    return {~std::uint64_t{0}<<c,~std::uint64_t{0}};
}
using Graph=std::array<std::array<unsigned,7>,7>;
void require(bool b,const char* m){if(!b)throw std::runtime_error(m);}
Graph parse(const std::string& s) {
    require(s.size()==5 && s[0]=='F',"graph6 shape");
    for(char c:s)require(c>=63 && c<=126,"graph6 byte");
    require(((static_cast<unsigned>(s[4])-63)&7)==0,"graph6 padding");
    Graph a{};unsigned k=0;
    for(unsigned j=1;j<7;++j)for(unsigned i=0;i<j;++i,++k)
        a[i][j]=a[j][i]=((static_cast<unsigned>(s[1+k/6])-63)>>(5-k%6))&1;
    for(unsigned i=0;i<7;++i)for(unsigned j=i+1;j<7;++j)for(unsigned k2=j+1;k2<7;++k2)for(unsigned l=k2+1;l<7;++l){
        unsigned count=a[i][j]+a[i][k2]+a[i][l]+a[j][k2]+a[j][l]+a[k2][l];
        require(count!=0 && count!=6,"core Ramsey(4,4)");
    }
    return a;
}
std::uint32_t word(const Graph& a,const std::array<unsigned,7>& p,bool complement=false) {
    std::uint32_t w=0;unsigned k=0;
    for(unsigned i=0;i<7;++i)for(unsigned j=i+1;j<7;++j,++k)
        w|=(a[p[i]][p[j]]^static_cast<unsigned>(complement))<<k;
    return w;
}
std::array<std::uint64_t,2> count(const Graph& a,std::ostream* table=nullptr) {
    std::array<bool,128> ind{},tf{};
    std::vector<unsigned> edges,triangles,matching;unsigned used=0;
    for(unsigned u=0;u<7;++u)for(unsigned v=u+1;v<7;++v)if(a[u][v]){
        unsigned e=(1u<<u)|(1u<<v);edges.push_back(e);
        if((used&e)==0){matching.push_back(e);used|=e;}
        for(unsigned w=v+1;w<7;++w)if(a[u][w] && a[v][w])triangles.push_back(e|(1u<<w));
    }
    require(matching.size()>=2,"matching size");
    for(unsigned s=0;s<128;++s){
        ind[s]=std::all_of(edges.begin(),edges.end(),[s](unsigned x){return (s&x)!=x;});
        tf[s]=std::all_of(triangles.begin(),triangles.end(),[s](unsigned x){return (s&x)!=x;});
    }
    std::array<Bits,128> pair{},triple{},empty{};std::array<unsigned,128> types{};std::array<Bits,4> pure{};
    for(unsigned s=0;s<128;++s){
        types[s]=static_cast<unsigned>((s&matching[0])==matching[0])+2u*static_cast<unsigned>((s&matching[1])==matching[1]);
        pure[types[s]].add(s);
        for(unsigned d=0;d<128;++d){if(tf[s&d])pair[s].add(d);if(ind[s&d])triple[s].add(d);if((s&d)==0)empty[s].add(d);}
    }
    std::uint64_t plain=0,joint=0;
    std::vector<std::uint32_t> plain_prefix{0},joint_prefix{0};
    for(unsigned x=0;x<128;++x)for(unsigned y=x;y<128;++y){
        unsigned xy=x&y;
        Bits initial=pair[x]&pair[y]&triple[xy];
        for(unsigned z=y;z<128;++z){
            unsigned xz=x&z,yz=y&z,t=xy&z;
            if(!tf[xy] || !tf[xz] || !tf[yz] || !ind[t])continue;
            Bits d=initial&pair[z]&triple[xz]&triple[yz]&empty[t]&tail(z);
            unsigned high=24,tie=12;
            if(x==z){high=4;tie=1;}else if(x==y){high=12;tie=6;}else if(y==z){high=12;tie=4;}
            auto weighted=[=](Bits b)->std::uint64_t{return static_cast<std::uint64_t>((b&tail(z+1)).size())*high+static_cast<unsigned>(b.has(z))*tie;};
            plain+=weighted(d);
            unsigned tx=types[x],ty=types[y],tz=types[z];
            if((tx==1 || tx==2) && (ty==1 || ty==2) && (tz==1 || tz==2)){
                unsigned ones=(tx==1)+(ty==1)+(tz==1);
                if(ones==2)d=d.without(pure[2]);else if(ones==1)d=d.without(pure[1]);
            }
            joint+=weighted(d);
        }
        plain_prefix.push_back(static_cast<std::uint32_t>(plain));
        joint_prefix.push_back(static_cast<std::uint32_t>(joint));
    }
    require(joint<=plain && plain<=170859375,"count bounds");
    if(table){
        for(const auto* values:{&plain_prefix,&joint_prefix})for(std::uint32_t v:*values)
            for(unsigned b=0;b<4;++b)table->put(static_cast<char>((v>>(8*b))&255));
        require(static_cast<bool>(*table),"table write");
    }
    return {plain,joint};
}
int main(int argc,char** argv){try{
    require(argc>=3 && argc<=5,"usage: row_count catalogue.g6 output.tsv [limit] [tables.bin]");
    std::ifstream in(argv[1]);require(static_cast<bool>(in),"input open");std::string s;std::vector<Graph> graphs;
    while(std::getline(in,s)){graphs.push_back(parse(s));}
    require(graphs.size()==362,"catalogue count");
    unsigned limit=argc>=4 ? static_cast<unsigned>(std::stoul(argv[3])) : 362;require(limit>0 && limit<=362,"limit");
    std::map<std::uint32_t,unsigned> index;std::array<unsigned,7> id{0,1,2,3,4,5,6};
    for(unsigned i=0;i<graphs.size();++i)require(index.emplace(word(graphs[i],id),i).second,"literal duplicate");
    auto start=std::chrono::steady_clock::now();std::ofstream out(argv[2]);require(static_cast<bool>(out),"output open");
    std::ofstream table;
    if(argc==5){table.open(argv[4],std::ios::binary);require(static_cast<bool>(table),"table open");}
    for(unsigned i=0;i<limit;++i){
        auto c=count(graphs[i],argc==5?&table:nullptr);auto p=id;unsigned target=362,permutation=0;
        do {auto it=index.find(word(graphs[i],p,true));if(it!=index.end()){target=it->second;for(unsigned k=0;k<7;++k)permutation|=p[k]<<(3*k);break;}}while(std::next_permutation(p.begin(),p.end()));
        require(target<362,"complement destination");
        out<<i<<'\t'<<c[0]<<'\t'<<c[1]<<'\t'<<target<<'\t'<<permutation<<'\n';
    }
    require(static_cast<bool>(out),"output write");
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::cout<<"{\"method\":\"unordered_rows\",\"complete\":"<<(limit==362 ? "true":"false")<<",\"records\":"<<limit<<",\"seconds\":"<<seconds<<"}\n";
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
