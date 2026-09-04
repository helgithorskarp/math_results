#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using Matrix=std::vector<std::vector<unsigned char>>;
struct Data {std::vector<uint64_t> pos4,neg4,pos3,neg3,pos2,neg2;};

static Matrix decode(const std::string&s) {
    if(s.empty())throw std::runtime_error("empty graph6");
    int n=static_cast<unsigned char>(s[0])-63;
    if(n<1||n>62)throw std::runtime_error("unsupported graph6 order");
    std::vector<int>b;
    for(size_t p=1;p<s.size();++p){int x=static_cast<unsigned char>(s[p])-63;if(x<0||x>63)throw std::runtime_error("bad graph6 byte");for(int k=5;k>=0;--k)b.push_back((x>>k)&1);}
    if(static_cast<int>(b.size())<n*(n-1)/2)throw std::runtime_error("truncated graph6");
    Matrix a(n,std::vector<unsigned char>(n));int at=0;
    for(int j=1;j<n;++j)for(int i=0;i<j;++i)a[i][j]=a[j][i]=b[at++];
    return a;
}

static Data make_data(const Matrix&a) {
    const int n=a.size();Data d;
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){uint64_t m=(1ULL<<i)|(1ULL<<j);if(a[i][j])d.pos2.push_back(m);else d.neg2.push_back(m);}
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)for(int k=j+1;k<n;++k){
        uint64_t m=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);
        if(a[i][j]&&a[i][k]&&a[j][k])d.pos3.push_back(m);
        if(!a[i][j]&&!a[i][k]&&!a[j][k])d.neg3.push_back(m);
    }
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)for(int k=j+1;k<n;++k)for(int l=k+1;l<n;++l){
        int v[4]={i,j,k,l};bool all1=true,all0=true;
        for(int p=0;p<4;++p)for(int q=p+1;q<4;++q){all1&=a[v[p]][v[q]]!=0;all0&=a[v[p]][v[q]]==0;}
        uint64_t m=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l);
        if(all1)d.neg4.push_back(m); // clause says not all incidence bits are one
        if(all0)d.pos4.push_back(m); // clause says at least one incidence bit is one
    }
    return d;
}

static bool propagate(const Data&d,uint64_t all,uint64_t&assigned,uint64_t&ones) {
    bool change=true;
    while(change){change=false;
        for(uint64_t m:d.pos4){if(ones&m)continue;uint64_t r=m&~assigned;if(!r)return false;if(!(r&(r-1))){assigned|=r;ones|=r;change=true;}}
        for(uint64_t m:d.neg4){if((assigned&~ones)&m)continue;uint64_t r=m&~assigned;if(!r)return false;if(!(r&(r-1))){assigned|=r;ones&=~r;change=true;}}
    }
    assigned&=all;ones&=all;return true;
}

static int branch_var(const Data&d,int n,uint64_t assigned,uint64_t ones) {
    int score[62]={0};
    for(uint64_t m:d.pos4)if(!(ones&m)){uint64_t r=m&~assigned;int w=1<<(4-__builtin_popcountll(r));while(r){int v=__builtin_ctzll(r);score[v]+=w;r&=r-1;}}
    for(uint64_t m:d.neg4)if(!((assigned&~ones)&m)){uint64_t r=m&~assigned;int w=1<<(4-__builtin_popcountll(r));while(r){int v=__builtin_ctzll(r);score[v]+=w;r&=r-1;}}
    int best=-1;for(int v=0;v<n;++v)if(!(assigned&(1ULL<<v))&&(best<0||score[v]>score[best]))best=v;return best;
}

static void enumerate(const Data&d,int n,uint64_t all,uint64_t assigned,uint64_t ones,std::vector<uint64_t>&out) {
    if(!propagate(d,all,assigned,ones))return;
    if(assigned==all){out.push_back(ones);return;}
    int v=branch_var(d,n,assigned,ones);uint64_t bit=1ULL<<v;
    enumerate(d,n,all,assigned|bit,ones,out);
    enumerate(d,n,all,assigned|bit,ones|bit,out);
}

static bool contains(uint64_t vertices,const std::vector<uint64_t>&patterns) {
    for(uint64_t p:patterns) if((vertices&p)==p) return true;
    return false;
}

static uint64_t first_contained(uint64_t vertices,const std::vector<uint64_t>&patterns) {
    for(uint64_t p:patterns) if((vertices&p)==p) return p;
    return 0;
}

static bool has_homogeneous_five(const Matrix&a,bool value) {
    int n=a.size();uint64_t nb[62]={0};
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)if(static_cast<bool>(a[i][j])==value){nb[i]|=1ULL<<j;nb[j]|=1ULL<<i;}
    struct R{const uint64_t*n;bool go(uint64_t c,int d)const{if(d==5)return true;if(__builtin_popcountll(c)<5-d)return false;while(c){uint64_t b=c&-c;int v=__builtin_ctzll(b);c^=b;if(go(c&n[v],d+1))return true;}return false;}}r{nb};
    return r.go((1ULL<<n)-1,0);
}

static bool verify_full(const Matrix&core,const std::vector<uint64_t>&m,int edge_bits,Matrix&out) {
    int old=core.size();out.assign(old+3,std::vector<unsigned char>(old+3));
    for(int i=0;i<old;++i)for(int j=i+1;j<old;++j)out[i][j]=out[j][i]=core[i][j];
    for(int q=0;q<3;++q)for(int i=0;i<old;++i)out[i][old+q]=out[old+q][i]=(m[q]>>i)&1;
    int u[3]={0,0,1},v[3]={1,2,2};for(int e=0;e<3;++e)out[old+u[e]][old+v[e]]=out[old+v[e]][old+u[e]]=(edge_bits>>e)&1;
    return !has_homogeneous_five(out,true)&&!has_homogeneous_five(out,false);
}

static std::string graph6(const Matrix&a) {
    int n=a.size();std::string s(1,char(n+63));int x=0,used=0;
    for(int j=1;j<n;++j)for(int i=0;i<j;++i){x=(x<<1)|a[i][j];if(++used==6){s.push_back(char(x+63));x=used=0;}}
    if(used){x<<=6-used;s.push_back(char(x+63));}return s;
}

int main(int argc,char**argv)try{
    if(argc!=4){std::cerr<<"usage: search_three_extension CORES.g6 START COUNT\n";return 2;}
    size_t start=std::stoull(argv[2]),count=std::stoull(argv[3]);
    std::ifstream in(argv[1]);if(!in)throw std::runtime_error("cannot open cores");std::vector<std::string>records;std::string line;while(std::getline(in,line))if(!line.empty())records.push_back(line);
    if(start>records.size()||count>records.size()-start)throw std::runtime_error("range outside file");
    uint64_t total_models=0,total_triples=0,total_patterns=0;std::map<size_t,size_t>distribution;
    for(size_t index=start;index<start+count;++index){
        Matrix a=decode(records[index]);int n=a.size();if(n!=40)throw std::runtime_error("core order is not 40");
        if(has_homogeneous_five(a,true)||has_homogeneous_five(a,false))throw std::runtime_error("core is not Ramsey(5,5)");
        Data d=make_data(a);uint64_t all=(1ULL<<n)-1;std::vector<uint64_t>models;enumerate(d,n,all,0,0,models);
        std::sort(models.begin(),models.end());if(std::adjacent_find(models.begin(),models.end())!=models.end())throw std::runtime_error("duplicate model");
        ++distribution[models.size()];total_models+=models.size();size_t m=models.size();std::vector<unsigned char>allow(m*m);
        for(size_t i=0;i<m;++i)for(size_t j=0;j<m;++j){
            if(!contains(all&~(models[i]|models[j]),d.neg3))allow[i*m+j]|=1;
            if(!contains(models[i]&models[j],d.pos3))allow[i*m+j]|=2;
        }
        for(size_t i=0;i<m;++i)for(size_t j=0;j<m;++j)for(size_t k=0;k<m;++k){
            ++total_triples;unsigned char a01=allow[i*m+j],a02=allow[i*m+k],a12=allow[j*m+k];if(!a01||!a02||!a12)continue;
            for(int bits=0;bits<8;++bits){if(!(a01&(1<<((bits>>0)&1)))||!(a02&(1<<((bits>>1)&1)))||!(a12&(1<<((bits>>2)&1))))continue;++total_patterns;
                if(bits==7) {
                    uint64_t obstruction=first_contained(models[i]&models[j]&models[k],d.pos2);
                    if(obstruction) {
                        std::cerr<<"FINAL_OBSTRUCTION core="<<index<<" models="<<std::hex
                                 <<models[i]<<','<<models[j]<<','<<models[k]<<std::dec
                                 <<" edge_bits=7 color=K5 old_pair_mask="<<std::hex
                                 <<obstruction<<std::dec<<"\n";
                        continue;
                    }
                }
                if(bits==0) {
                    uint64_t obstruction=first_contained(all&~(models[i]|models[j]|models[k]),d.neg2);
                    if(obstruction) {
                        std::cerr<<"FINAL_OBSTRUCTION core="<<index<<" models="<<std::hex
                                 <<models[i]<<','<<models[j]<<','<<models[k]<<std::dec
                                 <<" edge_bits=0 color=I5 old_pair_mask="<<std::hex
                                 <<obstruction<<std::dec<<"\n";
                        continue;
                    }
                }
                Matrix witness;std::vector<uint64_t>ms{models[i],models[j],models[k]};if(!verify_full(a,ms,bits,witness))throw std::runtime_error("survivor failed full verification");
                std::cout<<"SAT core="<<index<<" models="<<std::hex<<models[i]<<','<<models[j]<<','<<models[k]<<std::dec<<" edge_bits="<<bits<<"\n"<<graph6(witness)<<"\n";return 10;
            }
        }
        if((index-start+1)%5000==0)std::cerr<<"checked="<<(index-start+1)<<'/'<<count<<" start="<<start<<"\n";
    }
    std::cout<<"UNSAT start="<<start<<" count="<<count<<" models="<<total_models<<" ordered_triples="<<total_triples<<" compatible_patterns_tested="<<total_patterns<<" distribution=";
    bool first=true;for(auto [m,c]:distribution){if(!first)std::cout<<',';first=false;std::cout<<m<<':'<<c;}std::cout<<"\n";return 20;
}catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<"\n";return 1;}
