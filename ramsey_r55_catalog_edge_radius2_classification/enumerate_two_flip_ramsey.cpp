#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
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
static std::string graph6(const Matrix&a){std::string s(1,char(a.size()+63));int x=0,n=0;for(int j=1;j<(int)a.size();++j)for(int i=0;i<j;++i){x=(x<<1)|a[i][j];if(++n==6){s.push_back(char(x+63));x=n=0;}}if(n){x<<=6-n;s.push_back(char(x+63));}return s;}
static int edge_index(int u,int v){if(u>v)std::swap(u,v);return v*(v-1)/2+u;}

int main(int argc,char**argv)try{
    if(argc!=4){std::cerr<<"usage: enumerate_two_flip_ramsey CATALOG.g6 START COUNT\n";return 2;}size_t start=std::stoull(argv[2]),count=std::stoull(argv[3]);
    std::ifstream in(argv[1]);std::vector<std::string>records;std::string line;while(std::getline(in,line))if(!line.empty())records.push_back(line);if(start>records.size()||count>records.size()-start)throw std::runtime_error("bad range");
    std::vector<std::pair<int,int>>edges;for(int v=1;v<42;++v)for(int u=0;u<v;++u)edges.emplace_back(u,v);uint64_t total=0,total_single=0;
    for(size_t index=start;index<start+count;++index){Matrix a=decode(records[index]);std::vector<unsigned char>invalid(861*861);std::vector<unsigned char>single_bad(861);long near1=0,near2=0;
        for(int v0=0;v0<42;++v0)for(int v1=v0+1;v1<42;++v1)for(int v2=v1+1;v2<42;++v2)for(int v3=v2+1;v3<42;++v3)for(int v4=v3+1;v4<42;++v4){
            int v[5]={v0,v1,v2,v3,v4};std::vector<int>present,absent;
            for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)(a[v[i]][v[j]]?present:absent).push_back(edge_index(v[i],v[j]));
            auto mark=[&](const std::vector<int>&required,const std::vector<int>&opposite){
                if(required.size()==1){++near1;int r=required[0];single_bad[r]=1;std::vector<unsigned char>blocked(861);for(int e:opposite)blocked[e]=1;blocked[r]=1;for(int e=0;e<861;++e)if(!blocked[e]){int x=std::min(r,e),y=std::max(r,e);invalid[x*861+y]=1;}}
                else if(required.size()==2){++near2;int x=std::min(required[0],required[1]),y=std::max(required[0],required[1]);invalid[x*861+y]=1;}
            };
            if(absent.size()<=2)mark(absent,present);
            if(present.size()<=2)mark(present,absent);
        }
        long valid=0;
        for(int e=0;e<861;++e)if(!single_bad[e]){
            Matrix b=a;auto [u,v]=edges[e];b[u][v]=b[v][u]=!b[u][v];
            std::cout<<1<<'\t'<<index<<'\t'<<u<<','<<v<<"\t-\t"<<graph6(b)<<'\n';
            ++total_single;
        }
        for(int e1=0;e1<861;++e1)for(int e2=e1+1;e2<861;++e2)if(!invalid[e1*861+e2]){
            Matrix b=a;auto [u1,v1]=edges[e1];auto [u2,v2]=edges[e2];b[u1][v1]=b[v1][u1]=!b[u1][v1];b[u2][v2]=b[v2][u2]=!b[u2][v2];
            std::cout<<2<<'\t'<<index<<'\t'<<u1<<','<<v1<<'\t'<<u2<<','<<v2<<'\t'<<graph6(b)<<'\n';++valid;++total;
        }
        long good_single=std::count(single_bad.begin(),single_bad.end(),0);
        std::cerr<<"parent="<<index<<" valid_two_flips="<<valid<<" valid_single_flips="<<good_single<<" near1="<<near1<<" near2="<<near2<<"\n";
    }
    std::cerr<<"SUMMARY start="<<start<<" count="<<count<<" valid_single_flips="<<total_single<<" valid_two_flips="<<total<<"\n";return 0;
}catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<'\n';return 1;}
