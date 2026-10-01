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

void controls() {
    std::uint64_t checks=0;
    for(int encoding=0;encoding<1024;++encoding) {
        std::vector<Set> bad(5);int bit=0;
        for(int i=0;i<5;++i) for(int j=i+1;j<5;++j,++bit) if(encoding&(1<<bit)) {bad[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));bad[static_cast<std::size_t>(j)].set(static_cast<std::size_t>(i));}
        Search s(5,bad);Set full;for(int i=0;i<5;++i) full.set(static_cast<std::size_t>(i));
        for(int rank=1;rank<=5;++rank) {
            std::vector<List> literal;
            for(int subset=1;subset<32;++subset) {
                if(__builtin_popcount(static_cast<unsigned int>(subset))!=rank) continue;
                bool ok=true;List chosen;
                for(int i=0;i<5;++i) if(subset&(1<<i)) {
                    chosen.push_back(i);
                    for(int j=i+1;j<5;++j) if((subset&(1<<j))&&bad[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)]) ok=false;
                }
                if(ok) literal.push_back(chosen);
            }
            std::sort(literal.begin(),literal.end());require(s.run(full,rank)==literal,"small graph control mismatch");++checks;
        }
    }
    for(int n:{64,65,128,129,186,256}) {
        std::vector<Set> bad(static_cast<std::size_t>(n));
        for(int i=0;i<n;++i) for(int j=0;j<n;++j) if(i!=j) bad[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
        List selected={0,1,2,3,4,5,6,7,8,9,n-1};
        for(int i:selected) for(int j:selected) if(i!=j) bad[static_cast<std::size_t>(i)].reset(static_cast<std::size_t>(j));
        Search s(n,bad);Set full;for(int i=0;i<n;++i) full.set(static_cast<std::size_t>(i));
        require(s.run(full,11)==std::vector<List>{selected},"bit boundary control mismatch");++checks;
    }
    std::vector<Word> triples;subsets(0,3,0,triples);
    triples.erase(std::remove_if(triples.begin(),triples.end(),[](Word t){return t>=(Word(1)<<12);}),triples.end());
    std::vector<List> covers;List chosen;tails(triples,0,0,chosen,covers);
    require(triples.size()==220&&covers.size()==15400,"four-tail partition control count");
    require(std::adjacent_find(covers.begin(),covers.end())==covers.end(),"four-tail duplicates");
    for(const auto& cover:covers) {
        Word used=0;
        for(int i:cover) {require(!(used&triples[static_cast<std::size_t>(i)]),"four-tail overlap");used|=triples[static_cast<std::size_t>(i)];}
        require(size(used)==12,"four-tail coverage");
    }
    std::cout<<"{\"status\":\"COMPLETE\",\"literal_graph_checks\":"<<checks<<",\"twelve_point_four_tail_partitions\":15400}\n";
}

int main(int argc,char** argv) {
    try {
        if(argc==2 && std::string(argv[1])=="--controls") {controls();return 0;}
        if(argc==4 && std::string(argv[1])=="--words") {
            const int rank=std::stoi(argv[2]);std::ifstream input(argv[3]);require(bool(input),"missing words input");
            std::vector<Word> words=read_words(input);
            require(!words.empty()&&words.size()<=256,"bad words count");
            auto sorted=words;std::sort(sorted.begin(),sorted.end());
            require(std::adjacent_find(sorted.begin(),sorted.end())==sorted.end(),"duplicate words");
            for(Word b:words)require(b<(Word(1)<<18)&&size(b)==5,"bad word");
            Search s(words);Set full;for(std::size_t i=0;i<words.size();++i)full.set(i);
            const auto result=s.run(full,rank);
            std::cout<<"{\"status\":\"COMPLETE\",\"solutions\":"<<arrays(result)<<",\"nodes\":"<<s.total_nodes<<"}\n";
            return 0;
        }
        require(argc==3,"usage: joint CASE INPUT or joint --controls");
        const int case_id=std::stoi(argv[1]);require(case_id>=0&&case_id<46,"bad case id");
        std::ifstream input(argv[2]);require(bool(input),"missing input");
        std::vector<Word> fixed=read_words(input);
        require(fixed.size()==19,"bad input count");
        require(std::is_sorted(fixed.begin(),fixed.end())&&std::adjacent_find(fixed.begin(),fixed.end())==fixed.end(),"bad input order/duplicate");
        for(std::size_t i=0;i<fixed.size();++i) {
            require(fixed[i]<(Word(1)<<18)&&size(fixed[i])==5&&(fixed[i]&(Word(1)<<17)),"bad input word");
            for(std::size_t j=i+1;j<fixed.size();++j) require(size(fixed[i]&fixed[j])<=2,"bad input packing");
        }
        const auto started=Clock::now();
        std::vector<Word> three,four;subsets(0,3,0,three);subsets(0,4,0,four);
        std::vector<Word> triples,ywords,zwords;
        for(Word t:three) if(allowed(t|(Word(1)<<15)|(Word(1)<<16),fixed)) triples.push_back(t);
        for(Word t:four) {
            if(allowed(t|(Word(1)<<15),fixed)) ywords.push_back(t|(Word(1)<<15));
            if(allowed(t|(Word(1)<<16),fixed)) zwords.push_back(t|(Word(1)<<16));
        }
        Search ys(ywords),zs(zwords);
        std::vector<List> covers;List selected;tails(triples,0,0,selected,covers);
        std::vector<Set> ymask,zmask;
        for(Word t:triples) {Word a=t|(Word(1)<<15)|(Word(1)<<16);ymask.push_back(compatible(ywords,a));zmask.push_back(compatible(zwords,a));}
        std::vector<Set> cross;
        for(Word a:ywords) cross.push_back(compatible(zwords,a));
        Digest transcript;std::uint64_t y_count=0,z_count=0;std::vector<std::string> cores;
        for(std::size_t ci=0;ci<covers.size();++ci) {
            require(Clock::now()-started<std::chrono::seconds(60),"INCOMPLETE whole-case guard");
            Set ydomain,zdomain;for(std::size_t j=0;j<ywords.size();++j) ydomain.set(j);for(std::size_t j=0;j<zwords.size();++j) zdomain.set(j);
            std::vector<Word> common=fixed;
            for(int t:covers[ci]) {
                ydomain &= ymask[static_cast<std::size_t>(t)];zdomain &= zmask[static_cast<std::size_t>(t)];
                common.push_back(triples[static_cast<std::size_t>(t)]|(Word(1)<<15)|(Word(1)<<16));
            }
            auto ysolutions=ys.run(ydomain,11);y_count+=ysolutions.size();
            std::string record="{\"cover\":"+std::to_string(ci)+",\"y_candidates\":"+array(indices(ydomain,ys.n))+",\"y_eleven\":"+arrays(ysolutions)+",\"z_cases\":[";
            bool first=true;
            for(const List& y:ysolutions) {
                Set left=zdomain;for(int v:y) left &= cross[static_cast<std::size_t>(v)];
                auto zsolutions=zs.run(left,11);z_count+=zsolutions.size();
                if(!first) record+=',';
                first=false;
                record+="{\"y\":"+array(y)+",\"z_candidates\":"+array(indices(left,zs.n))+",\"z_eleven\":"+arrays(zsolutions)+"}";
                for(const List& z:zsolutions) {
                    List words;for(Word a:common) words.push_back(static_cast<int>(a));
                    for(int v:y) words.push_back(static_cast<int>(ywords[static_cast<std::size_t>(v)]));
                    for(int v:z) words.push_back(static_cast<int>(zwords[static_cast<std::size_t>(v)]));
                    std::sort(words.begin(),words.end());Digest d;d.add(array(words)+"\n");
                    cores.push_back("{\"blocks\":"+array(words)+",\"case\":"+std::to_string(case_id)+",\"core_sha256\":\""+d.finish()+"\",\"cover\":"+std::to_string(ci)+",\"y\":"+array(y)+",\"z\":"+array(z)+"}");
                }
            }
            transcript.add(record+"]}\n");
        }
        std::cout<<"{\"case\":"<<case_id<<",\"status\":\"COMPLETE\",\"triples\":"<<triples.size()<<",\"covers\":"<<covers.size()<<",\"y_eleven\":"<<y_count<<",\"z_eleven\":"<<z_count<<",\"y_nodes\":"<<ys.total_nodes<<",\"z_nodes\":"<<zs.total_nodes<<",\"peak_query_nodes\":"<<std::max(ys.peak_query_nodes,zs.peak_query_nodes)<<",\"carrier_sha256\":\""<<transcript.finish()<<"\",\"cores\":[";
        for(std::size_t i=0;i<cores.size();++i) {if(i) std::cout<<',';std::cout<<cores[i];}
        std::cout<<"],\"seconds\":"<<std::chrono::duration<double>(Clock::now()-started).count()<<"}\n";
        return 0;
    } catch(const std::exception& e) { std::cerr<<e.what()<<'\n';return 1; }
}
