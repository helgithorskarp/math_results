// Independent exhaustive core and marked-component graph enumeration.
// Base orders6,7 are literal edge-word sweeps. Order8 extends every surviving7
// by all128 edge words and uses full forbidden-subgraph tests. Marked graphs
// use star MULTISETS, full graph tests, then all distinct tail permutations.
#include <algorithm>
#include <array>
#include <cstdint>
#include <exception>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Graph=std::array<std::uint32_t,11>;
using Word=std::uint64_t;
static std::uint32_t full(unsigned n){return (std::uint32_t{1}<<n)-1U;}
static void require(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
static Graph decode(unsigned n,Word code){
    Graph a{};unsigned pos=0;
    for(unsigned u=0;u<n;++u)for(unsigned v=u+1;v<n;++v,++pos)
        if((code>>pos)&Word{1}){a[u]|=std::uint32_t{1}<<v;a[v]|=std::uint32_t{1}<<u;}
    require((code>>pos)==0,"code padding");return a;
}
static Word encode(const Graph& a,unsigned n){
    Word code=0;unsigned pos=0;
    for(unsigned u=0;u<n;++u)for(unsigned v=u+1;v<n;++v,++pos)
        if((a[u]>>v)&1U)code|=Word{1}<<pos;
    return code;
}
static bool independent(const Graph& a,std::uint32_t m){
    auto remaining=m;
    while(remaining){const auto v=static_cast<unsigned>(__builtin_ctz(remaining));remaining&=remaining-1U;if(a[v]&m)return false;}
    return true;
}
static bool has_independent(const Graph& a,std::uint32_t m,int k){
    if(k==0)return true;
    while(__builtin_popcount(m)>=k){
        const auto v=static_cast<unsigned>(__builtin_ctz(m));m&=m-1U;
        if(has_independent(a,m&~a[v],k-1))return true;
    }
    return false;
}
static bool good(const Graph& a,unsigned n,int alpha){
    for(unsigned u=0;u<n;++u)for(unsigned v=u+1;v<n;++v)
        if(((a[u]>>v)&1U)&&(a[u]&a[v]))return false;
    return !has_independent(a,full(n),alpha+1);
}
static void cores(){
    std::vector<Graph> sevens;
    for(unsigned n=6;n<=7;++n){
        const auto bits=n*(n-1U)/2U;
        for(Word code=0;code<(Word{1}<<bits);++code){
            const auto a=decode(n,code);if(!good(a,n,3))continue;
            std::cout<<"C "<<n<<' '<<code<<'\n';
            if(n==7)sevens.push_back(a);
        }
    }
    std::vector<Word> eights;
    for(const auto& a:sevens)for(std::uint32_t m=0;m<128U;++m){
        auto b=a;b[7]=m;
        for(unsigned v=0;v<7;++v)if((m>>v)&1U)b[v]|=128U;
        if(good(b,8,3))eights.push_back(encode(b,8));
    }
    std::sort(eights.begin(),eights.end());
    require(std::adjacent_find(eights.begin(),eights.end())==eights.end(),"duplicate order8 graph");
    for(auto code:eights)std::cout<<"C 8 "<<code<<'\n';
}
static Graph augment(const Graph& a,unsigned h,const std::vector<std::uint32_t>& tuple){
    auto b=a;
    for(std::size_t i=0;i<tuple.size();++i){
        const auto w=h+static_cast<unsigned>(i);b[w]=tuple[i];
        for(unsigned v=0;v<h;++v)if((tuple[i]>>v)&1U)b[v]|=std::uint32_t{1}<<w;
    }
    return b;
}
static void marked(){
    unsigned n=0,h=0;Word code=0;
    while(std::cin>>n>>h>>code){
        require((n==10&&(h==6||h==7||h==8))||(n==11&&(h==7||h==8)),"unsupported job");
        const auto a=decode(h,code);require(good(a,h,3),"invalid core");
        std::vector<std::uint32_t> stars;
        for(std::uint32_t m=0;m<=full(h);++m)if(independent(a,m))stars.push_back(m);
        std::vector<Word> words;std::vector<std::uint32_t> tuple;
        std::function<void(std::size_t)> visit=[&](std::size_t start){
            if(tuple.size()==static_cast<std::size_t>(n-h)){
                if(!good(augment(a,h,tuple),n,4))return;
                auto order=tuple;
                do{words.push_back(encode(augment(a,h,order),n));}while(std::next_permutation(order.begin(),order.end()));
                return;
            }
            for(std::size_t j=start;j<stars.size();++j){tuple.push_back(stars[j]);visit(j);tuple.pop_back();}
        };
        visit(0);std::sort(words.begin(),words.end());
        require(std::adjacent_find(words.begin(),words.end())==words.end(),"duplicate marked graph");
        for(auto word:words)std::cout<<"M "<<n<<' '<<h<<' '<<code<<' '<<word<<'\n';
    }
    require(std::cin.eof(),"malformed marked jobs");
}
int main(int argc,char** argv){
    try{
        require(argc==2,"use: independent cores|marked");const std::string mode(argv[1]);
        if(mode=="cores")cores();else if(mode=="marked")marked();else throw std::runtime_error("unknown mode");
        require(static_cast<bool>(std::cout),"output failure");return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
