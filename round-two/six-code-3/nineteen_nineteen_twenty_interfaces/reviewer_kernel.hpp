// six-reviewer-5: independent include/exclude enumeration, no author code.
#include <algorithm>
#include <array>
#include <chrono>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <memory>
#include <numeric>
#include <openssl/evp.h>
#include <stdexcept>
#include <string>
#include <vector>

using Word = std::uint32_t;
struct Set {
    std::array<std::uint64_t,4> data{};
    bool operator[](std::size_t i) const {return (data[i/64]>>(i%64))&1U;}
    void set(std::size_t i) {data[i/64]|=std::uint64_t(1)<<(i%64);}
    void reset(std::size_t i) {data[i/64]&=~(std::uint64_t(1)<<(i%64));}
    bool any() const {return (data[0]|data[1]|data[2]|data[3])!=0;}
    bool none() const {return !any();}
    std::size_t count() const {std::size_t n=0;for(auto w:data)n+=static_cast<std::size_t>(__builtin_popcountll(w));return n;}
    int first() const {for(std::size_t i=0;i<4;++i)if(data[i])return static_cast<int>(64*i)+__builtin_ctzll(data[i]);throw std::runtime_error("empty first");}
    Set& operator&=(const Set& b) {for(std::size_t i=0;i<4;++i)data[i]&=b.data[i];return *this;}
    friend Set operator&(Set a,const Set& b) {return a&=b;}
    friend Set operator~(Set a) {for(auto& w:a.data)w=~w;return a;}
};
using List = std::vector<int>;
using Clock = std::chrono::steady_clock;
void require(bool p, const char* text) { if (!p) throw std::runtime_error(text); }
int size(Word w) { return __builtin_popcount(w); }
std::string array(const List& a) {
    std::string s="[";
    for (std::size_t i=0; i<a.size(); ++i) { if(i) s+=','; s+=std::to_string(a[i]); }
    return s+"]";
}
std::string arrays(const std::vector<List>& a) {
    std::string s="[";
    for (std::size_t i=0; i<a.size(); ++i) { if(i) s+=','; s+=array(a[i]); }
    return s+"]";
}
struct Digest {
    std::unique_ptr<EVP_MD_CTX, decltype(&EVP_MD_CTX_free)> ctx{EVP_MD_CTX_new(),EVP_MD_CTX_free};
    Digest() { require(bool(ctx),"hash allocation"); require(EVP_DigestInit_ex(ctx.get(),EVP_sha256(),nullptr)==1,"hash init"); }
    void add(const std::string& s) { require(EVP_DigestUpdate(ctx.get(),s.data(),s.size())==1,"hash update"); }
    std::string finish() {
        unsigned char out[EVP_MAX_MD_SIZE]; unsigned int n=0;
        require(EVP_DigestFinal_ex(ctx.get(),out,&n)==1 && n==32,"hash final");
        const char* hex="0123456789abcdef"; std::string s;
        for (unsigned int i=0; i<n; ++i) { s+=hex[out[i]>>4]; s+=hex[out[i]&15]; }
        return s;
    }
};

// All r-subsets, in the lexical point-tuple convention used only for comparison.
void subsets(int next, int left, Word selected, std::vector<Word>& out) {
    if (!left) { out.push_back(selected); return; }
    for(int v=next; v<=15-left; ++v) subsets(v+1,left-1,selected|(Word(1)<<v),out);
}
bool allowed(Word w, const std::vector<Word>& fixed) {
    return std::all_of(fixed.begin(),fixed.end(),[w](Word a){ return size(a&w)<=2; });
}
std::vector<Word> read_words(std::ifstream& input) {
    require(bool(input),"missing words input");
    std::vector<Word> words;std::string token;
    while(input>>token) {
        require(!token.empty()&&std::all_of(token.begin(),token.end(),[](unsigned char c){return std::isdigit(c)!=0;}),"bad word token");
        const auto value=std::stoull(token);require(value<(std::uint64_t(1)<<18),"word outside domain");
        words.push_back(static_cast<Word>(value));
    }
    require(input.eof()&&!input.bad(),"word input read failure");return words;
}
List indices(const Set& s, int n) {
    List a; for(int v=0; v<n; ++v) if(s[static_cast<std::size_t>(v)]) a.push_back(v); return a;
}

// Partition exact fixed-rank solutions by containing/not containing one vertex.
// A disjoint cover by conflict-cliques bounds an independent set's cardinality.
// Unlike either author engine this never enumerates maximal cliques and never
// branches over the reverse order of a colored compatibility-graph prefix.
struct Search {
    int n;
    std::vector<Set> conflicts;
    List order, inverse;
    std::uint64_t total_nodes=0, peak_query_nodes=0, calls=0;
    std::uint64_t query_nodes=0;
    Clock::time_point begun;
    explicit Search(const std::vector<Word>& words): n(static_cast<int>(words.size())),conflicts(words.size()) {
        require(n<=256,"too many vertices");
        for(int i=0;i<n;++i) for(int j=0;j<n;++j)
            if(i==j || size(words[static_cast<std::size_t>(i)]&words[static_cast<std::size_t>(j)])>2)
                conflicts[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
        order.resize(words.size()); std::iota(order.begin(),order.end(),0);
        std::stable_sort(order.begin(),order.end(),[this](int a,int b){return conflicts[static_cast<std::size_t>(a)].count()>conflicts[static_cast<std::size_t>(b)].count();});
        relabel();
    }
    // Generic constructor for exhaustive small-graph controls.
    Search(int count, std::vector<Set> bad):n(count),conflicts(std::move(bad)) {
        require(n>0 && n<=256 && static_cast<int>(conflicts.size())==n,"bad graph size");
        for(int i=0;i<n;++i) {
            conflicts[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(i));
            for(int j=0;j<n;++j) require(conflicts[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)]==conflicts[static_cast<std::size_t>(j)][static_cast<std::size_t>(i)],"asymmetric graph");
        }
        order.resize(static_cast<std::size_t>(n));std::iota(order.begin(),order.end(),0);
        std::stable_sort(order.begin(),order.end(),[this](int a,int b){return conflicts[static_cast<std::size_t>(a)].count()>conflicts[static_cast<std::size_t>(b)].count();});
        relabel();
    }
    void relabel() {
        inverse.resize(static_cast<std::size_t>(n));
        for(int i=0;i<n;++i)inverse[static_cast<std::size_t>(order[static_cast<std::size_t>(i)])]=i;
        std::vector<Set> mapped(static_cast<std::size_t>(n));
        for(int i=0;i<n;++i)for(int j=0;j<n;++j)
            if(conflicts[static_cast<std::size_t>(order[static_cast<std::size_t>(i)])][static_cast<std::size_t>(order[static_cast<std::size_t>(j)])])mapped[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
        conflicts=std::move(mapped);
    }
    int first(const Set& p) const {return p.first();}
    bool insufficient(Set uncovered, int need) const {
        int groups=0;
        while(uncovered.any()) {
            if(++groups>=need) return false;
            Set options=uncovered;
            while(options.any()) {
                const int v=first(options);
                uncovered.reset(static_cast<std::size_t>(v));
                options.reset(static_cast<std::size_t>(v));
                options &= conflicts[static_cast<std::size_t>(v)];
            }
        }
        return true;
    }
    void visit(Set available,int need,List& chosen,std::vector<List>& result) {
        ++query_nodes;
        require(query_nodes<=2000000,"INCOMPLETE node guard");
        if((query_nodes&255U)==0) require(Clock::now()-begun<std::chrono::seconds(20),"INCOMPLETE query time guard");
        if(!need) { List copy;for(int v:chosen)copy.push_back(order[static_cast<std::size_t>(v)]); std::sort(copy.begin(),copy.end()); result.push_back(std::move(copy)); return; }
        if(available.count()<static_cast<std::size_t>(need) || insufficient(available,need)) return;
        const int v=first(available);
        available.reset(static_cast<std::size_t>(v));
        chosen.push_back(v);
        visit(available&~conflicts[static_cast<std::size_t>(v)],need-1,chosen,result);
        chosen.pop_back();
        visit(available,need,chosen,result);
    }
    std::vector<List> run(const Set& available,int rank) {
        require(rank>0 && rank<=n,"bad requested rank");
        Set mapped;Set rest=available;
        while(rest.any()) {
            const int v=rest.first();require(v<n,"out-of-range available vertex");rest.reset(static_cast<std::size_t>(v));
            mapped.set(static_cast<std::size_t>(inverse[static_cast<std::size_t>(v)]));
        }
        query_nodes=0;begun=Clock::now();List chosen;std::vector<List> result;
        visit(mapped,rank,chosen,result);
        std::sort(result.begin(),result.end());
        require(std::adjacent_find(result.begin(),result.end())==result.end(),"duplicate solution");
        ++calls;total_nodes+=query_nodes;peak_query_nodes=std::max(peak_query_nodes,query_nodes);
        return result;
    }
};

// Increasing selection of disjoint three-subsets. Every four-tail set occurs once.
void tails(const std::vector<Word>& triples,int first_index,Word used,List& selected,
           std::vector<List>& covers) {
    if(selected.size()==4) { covers.push_back(selected);return; }
    for(int i=first_index;i<static_cast<int>(triples.size());++i) {
        if((used&triples[static_cast<std::size_t>(i)])!=0) continue;
        selected.push_back(i);tails(triples,i+1,used|triples[static_cast<std::size_t>(i)],selected,covers);selected.pop_back();
    }
}
Set compatible(const std::vector<Word>& words,Word fixed) {
    Set s;for(std::size_t i=0;i<words.size();++i) if(size(words[i]&fixed)<=2) s.set(i);return s;
}

