#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

struct Constraints { std::vector<uint64_t> positive, negative; };
using Matrix = std::vector<std::vector<unsigned char>>;
static constexpr uint64_t ALL41 = (1ULL << 41) - 1;

static Matrix decode_graph6(const std::string& s) {
    if (s.empty()) throw std::runtime_error("empty graph6 record");
    int n = static_cast<unsigned char>(s[0]) - 63;
    if (n != 41) throw std::runtime_error("certificate core order is not 41");
    std::vector<int> bits;
    for (size_t p=1;p<s.size();++p) {
        int x=static_cast<unsigned char>(s[p])-63;
        if(x<0||x>63) throw std::runtime_error("invalid graph6 byte");
        for(int b=5;b>=0;--b) bits.push_back((x>>b)&1);
    }
    if(static_cast<int>(bits.size())<820) throw std::runtime_error("truncated graph6");
    Matrix a(41,std::vector<unsigned char>(41));
    int at=0;
    for(int j=1;j<41;++j) for(int i=0;i<j;++i) a[i][j]=a[j][i]=bits[at++];
    return a;
}

static Constraints constraints_for(const Matrix&a) {
    Constraints c;
    for(int v0=0;v0<41;++v0) for(int v1=v0+1;v1<41;++v1)
    for(int v2=v1+1;v2<41;++v2) for(int v3=v2+1;v3<41;++v3) {
        int v[4]={v0,v1,v2,v3}; bool clique=true,independent=true;
        for(int i=0;i<4;++i) for(int j=i+1;j<4;++j) {
            clique &= a[v[i]][v[j]] != 0;
            independent &= a[v[i]][v[j]] == 0;
        }
        uint64_t m=(1ULL<<v0)|(1ULL<<v1)|(1ULL<<v2)|(1ULL<<v3);
        if(clique)c.negative.push_back(m);
        if(independent)c.positive.push_back(m);
    }
    return c;
}

static bool has_homogeneous_five(const Matrix&a,bool edge_value) {
    uint64_t neighbors[41]={0};
    for(int i=0;i<41;++i) for(int j=i+1;j<41;++j)
        if(static_cast<bool>(a[i][j])==edge_value) {
            neighbors[i]|=1ULL<<j;
            neighbors[j]|=1ULL<<i;
        }
    struct Search {
        const uint64_t* neighbors;
        bool run(uint64_t candidates,int depth) const {
            if(depth==5)return true;
            if(__builtin_popcountll(candidates)<5-depth)return false;
            while(candidates) {
                uint64_t bit=candidates&-candidates;
                int v=__builtin_ctzll(bit);
                candidates^=bit;
                if(run(candidates&neighbors[v],depth+1))return true;
            }
            return false;
        }
    } search{neighbors};
    return search.run(ALL41,0);
}

static bool valid_model(const Constraints&c,uint64_t ones) {
    for(uint64_t m:c.positive) if(!(ones&m)) return false;
    for(uint64_t m:c.negative) if((ones&m)==m) return false;
    return !(ones&~ALL41);
}

static bool propagate(const Constraints&c,uint64_t&assigned,uint64_t&ones) {
    bool changed=true;
    while(changed) {
        changed=false;
        for(uint64_t m:c.positive) {
            if(ones&m) continue;
            uint64_t rem=m&~assigned;
            if(!rem) return false;
            if(!(rem&(rem-1))) {
                assigned|=rem; ones|=rem; changed=true;
            }
        }
        for(uint64_t m:c.negative) {
            if((assigned&~ones)&m) continue;
            uint64_t rem=m&~assigned;
            if(!rem) return false;
            if(!(rem&(rem-1))) {
                assigned|=rem; ones&=~rem; changed=true;
            }
        }
    }
    return true;
}

static int branch_variable(const Constraints&c,uint64_t assigned,uint64_t ones) {
    int score[41]={0};
    for(uint64_t m:c.positive) if(!(ones&m)) {
        uint64_t rem=m&~assigned; int weight=1<<(4-__builtin_popcountll(rem));
        while(rem){int v=__builtin_ctzll(rem);score[v]+=weight;rem&=rem-1;}
    }
    for(uint64_t m:c.negative) if(!((assigned&~ones)&m)) {
        uint64_t rem=m&~assigned; int weight=1<<(4-__builtin_popcountll(rem));
        while(rem){int v=__builtin_ctzll(rem);score[v]+=weight;rem&=rem-1;}
    }
    int best=-1;
    for(int v=0;v<41;++v) if(!(assigned&(1ULL<<v))&&(best<0||score[v]>score[best]))best=v;
    return best;
}

static void enumerate_exact_impl(const Constraints&c,uint64_t assigned,uint64_t ones,
                                 std::vector<uint64_t>&models) {
    if(!propagate(c,assigned,ones))return;
    if(assigned==ALL41){models.push_back(ones);return;}
    int v=branch_variable(c,assigned,ones); uint64_t b=1ULL<<v;
    enumerate_exact_impl(c,assigned|b,ones,models);
    enumerate_exact_impl(c,assigned|b,ones|b,models);
}

static bool contains_triangle(const Matrix&a,uint64_t vertices,bool edge_value) {
    for(int i=0;i<41;++i) if(vertices&(1ULL<<i))
    for(int j=i+1;j<41;++j) if(vertices&(1ULL<<j))
    for(int k=j+1;k<41;++k) if(vertices&(1ULL<<k))
        if(static_cast<bool>(a[i][j])==edge_value &&
           static_cast<bool>(a[i][k])==edge_value &&
           static_cast<bool>(a[j][k])==edge_value) return true;
    return false;
}

static std::vector<std::vector<uint64_t>> read_certificate(const std::string&path,size_t expected) {
    std::ifstream in(path); if(!in)throw std::runtime_error("cannot open certificate");
    std::vector<std::vector<uint64_t>> all; std::string line;
    while(std::getline(in,line)) {
        std::istringstream iss(line); size_t index,n; char colon;
        if(!(iss>>index>>colon>>n)||colon!=':'||index!=all.size())throw std::runtime_error("bad certificate header");
        std::vector<uint64_t> row;
        for(size_t i=0;i<n;++i){std::string h;if(!(iss>>h))throw std::runtime_error("missing model");row.push_back(std::stoull(h,nullptr,16));}
        std::string extra;if(iss>>extra)throw std::runtime_error("extra certificate field");
        all.push_back(std::move(row));
    }
    if(all.size()!=expected)throw std::runtime_error("certificate length mismatch");
    return all;
}

int main(int argc,char**argv) try {
    if(argc!=3){std::cerr<<"usage: verify_extension_models CORES.g6 MODELS.txt\n";return 2;}
    std::ifstream gin(argv[1]);if(!gin)throw std::runtime_error("cannot open cores");
    std::vector<std::string> records;std::string line;while(std::getline(gin,line))if(!line.empty())records.push_back(line);
    auto certificate=read_certificate(argv[2],records.size());
    uint64_t total_models=0,total_pairs=0;
    for(size_t index=0;index<records.size();++index) {
        Matrix a=decode_graph6(records[index]);
        if(has_homogeneous_five(a,true)||has_homogeneous_five(a,false))
            throw std::runtime_error("core contains a homogeneous 5-set");
        Constraints c=constraints_for(a);
        auto listed=certificate[index];
        std::sort(listed.begin(),listed.end());
        if(std::adjacent_find(listed.begin(),listed.end())!=listed.end())throw std::runtime_error("duplicate listed model");
        for(uint64_t m:listed)if(!valid_model(c,m))throw std::runtime_error("listed model violates extension constraints");
        std::vector<uint64_t> exact;
        enumerate_exact_impl(c,0,0,exact);
        std::sort(exact.begin(),exact.end());
        if(exact!=listed)throw std::runtime_error("listed models are not exact");
        for(uint64_t x:listed)for(uint64_t y:listed) {
            ++total_pairs;
            if(!contains_triangle(a,x&y,true))throw std::runtime_error("valid extension with new-new edge present");
            if(!contains_triangle(a,ALL41&~(x|y),false))throw std::runtime_error("valid extension with new-new edge absent");
        }
        total_models+=listed.size();
        if(index%1000==999)std::cout<<"checked="<<(index+1)<<"\n";
    }
    std::cout<<"VERIFIED cores="<<records.size()<<" models="<<total_models<<" ordered_pairs="<<total_pairs<<"\n";
    return 0;
} catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<"\n";return 1;}
