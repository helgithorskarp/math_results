#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Matrix=std::vector<std::vector<unsigned char>>;

static Matrix decode(const std::string&s){
    if(s.empty()) throw std::runtime_error("empty graph6");
    int n=static_cast<unsigned char>(s[0])-63;
    if(n!=42) throw std::runtime_error("order is not 42");
    std::vector<int>b;for(size_t p=1;p<s.size();++p){int x=static_cast<unsigned char>(s[p])-63;if(x<0||x>63)throw std::runtime_error("bad graph6 byte");for(int k=5;k>=0;--k)b.push_back((x>>k)&1);}
    if(b.size()<861) throw std::runtime_error("truncated graph6");
    Matrix a(n,std::vector<unsigned char>(n));int at=0;
    for(int j=1;j<n;++j) for(int i=0;i<j;++i) a[i][j]=a[j][i]=b[at++];
    return a;
}

static std::string record_at(const std::string&path,int wanted){std::ifstream in(path);std::string line;for(int i=0;std::getline(in,line);++i)if(i==wanted)return line;throw std::runtime_error("record out of range");}

static int edge_index(int u,int v){if(u>v)std::swap(u,v);return v*(v-1)/2+u;}
static int flip_var(int u,int v){return 43+edge_index(u,v);}
static int counter_var(int edge,int level){return 904+3*edge+(level-1);}
static int literal_actual_zero(const Matrix&a,int u,int v){int f=flip_var(u,v);return a[u][v]?f:-f;}
static int literal_actual_one(const Matrix&a,int u,int v){return -literal_actual_zero(a,u,v);}

static bool homogeneous_five(const Matrix&a,bool value){
    for(int a0=0;a0<42;++a0) for(int a1=a0+1;a1<42;++a1)
    for(int a2=a1+1;a2<42;++a2) for(int a3=a2+1;a3<42;++a3)
    for(int a4=a3+1;a4<42;++a4){
        int v[5]={a0,a1,a2,a3,a4};bool good=true;
        for(int i=0;i<5;++i) for(int j=i+1;j<5;++j)
            good&=static_cast<bool>(a[v[i]][v[j]])==value;
        if(good)return true;
    }
    return false;
}

int main(int argc,char**argv)try{
    if(argc!=4){std::cerr<<"usage: gen_edge_radius2 CATALOG.g6 INDEX OUTPUT.cnf\n";return 2;}int index=std::stoi(argv[2]);Matrix a=decode(record_at(argv[1],index));
    if(homogeneous_five(a,true)||homogeneous_five(a,false))throw std::runtime_error("catalog record is not Ramsey(5,5)");
    std::vector<std::vector<int>>clauses;long old_k=0,old_i=0,new_k=0,new_i=0,card=0;
    for(int e=0;e<861;++e){int f=43+e,s1=counter_var(e,1);clauses.push_back({-f,s1});++card;if(e){for(int j=1;j<=3;++j){clauses.push_back({-counter_var(e-1,j),counter_var(e,j)});++card;}for(int j=2;j<=3;++j){clauses.push_back({-f,-counter_var(e-1,j-1),counter_var(e,j)});++card;}}}
    clauses.push_back({-counter_var(860,3)});++card;
    for(int v0=0;v0<42;++v0)for(int v1=v0+1;v1<42;++v1)for(int v2=v1+1;v2<42;++v2)for(int v3=v2+1;v3<42;++v3)for(int v4=v3+1;v4<42;++v4){
        int v[5]={v0,v1,v2,v3,v4},ones=0;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)ones+=a[v[i]][v[j]];
        if(10-ones<=2){std::vector<int>c;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)c.push_back(literal_actual_zero(a,v[i],v[j]));clauses.push_back(std::move(c));++old_k;}
        if(ones<=2){std::vector<int>c;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)c.push_back(literal_actual_one(a,v[i],v[j]));clauses.push_back(std::move(c));++old_i;}
    }
    for(int v0=0;v0<42;++v0)for(int v1=v0+1;v1<42;++v1)for(int v2=v1+1;v2<42;++v2)for(int v3=v2+1;v3<42;++v3){
        int v[4]={v0,v1,v2,v3},ones=0;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)ones+=a[v[i]][v[j]];
        if(6-ones<=2){std::vector<int>c;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)c.push_back(literal_actual_zero(a,v[i],v[j]));for(int i=0;i<4;++i)c.push_back(-(v[i]+1));clauses.push_back(std::move(c));++new_k;}
        if(ones<=2){std::vector<int>c;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)c.push_back(literal_actual_one(a,v[i],v[j]));for(int i=0;i<4;++i)c.push_back(v[i]+1);clauses.push_back(std::move(c));++new_i;}
    }
    std::ofstream out(argv[3]);if(!out)throw std::runtime_error("cannot open output");out<<"p cnf 3486 "<<clauses.size()<<'\n';for(const auto&c:clauses){for(int x:c)out<<x<<' ';out<<"0\n";}
    std::cout<<"index="<<index<<" variables=3486 clauses="<<clauses.size()<<" cardinality="<<card<<" old_k="<<old_k<<" old_i="<<old_i<<" new_k="<<new_k<<" new_i="<<new_i<<"\n";
    return 0;
}catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<'\n';return 1;}
