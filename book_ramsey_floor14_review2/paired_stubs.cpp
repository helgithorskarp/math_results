// six-reviewer-2: literal pairing of nine indistinguishable unit edges.
// No author executable or producer is imported. SHA is provenance only.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <openssl/evp.h>
using Mat=std::array<std::array<int,10>,10>;
using Vec=std::array<int,10>;
using Edge=std::array<int,3>;
struct Hash{
 EVP_MD_CTX* p;
 Hash():p(EVP_MD_CTX_new()){if(!p||EVP_DigestInit_ex(p,EVP_sha256(),nullptr)!=1)throw std::runtime_error("hash init");}
 void add(const std::string&s){if(EVP_DigestUpdate(p,s.data(),s.size())!=1)throw std::runtime_error("hash update");}
 std::string finish(){unsigned char out[32];unsigned int n=0;if(EVP_DigestFinal_ex(p,out,&n)!=1||n!=32)throw std::runtime_error("hash final");std::ostringstream s;s<<std::hex;for(unsigned char x:out){s.width(2);s.fill('0');s<<static_cast<int>(x);}return s.str();}
 ~Hash(){EVP_MD_CTX_free(p);}
};
void need(bool b,const char*m){if(!b)throw std::runtime_error(m);}
std::string list(const std::vector<int>&x){std::ostringstream s;s<<'[';for(size_t i=0;i<x.size();++i){if(i)s<<',';s<<x[i];}s<<']';return s.str();}
std::string edge_list(const std::vector<Edge>&x){std::ostringstream s;s<<'[';for(size_t i=0;i<x.size();++i){if(i)s<<',';s<<'['<<x[i][0]<<','<<x[i][1]<<','<<x[i][2]<<']';}s<<']';return s.str();}
std::string matrix(const Mat&r){std::ostringstream s;s<<'[';for(int i=0;i<10;++i){if(i)s<<',';s<<'[';for(int j=0;j<10;++j){if(j)s<<',';s<<r[i][j];}s<<']';}s<<']';return s.str();}
struct Pairing{
 Mat base,used{};Vec rem;
 std::vector<std::vector<Edge>> states;
 uint64_t nodes=0,limit;std::chrono::steady_clock::time_point start;
 Pairing(Mat b,Vec d,uint64_t cap):base(b),rem(d),limit(cap),start(std::chrono::steady_clock::now()){}
 void tick(){++nodes;need(nodes<=limit,"INCOMPLETE pairing node guard");if(nodes%1024==0)need(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<=10,"INCOMPLETE pairing time guard");}
 void choose(){
  tick();int u=-1;
  // Highest remaining degree, then greatest point, differs from producer order.
  for(int i=0;i<10;++i)if(rem[i]>0&&(u<0||rem[i]>=rem[u]))u=i;
  if(u<0){std::vector<Edge> e;for(int i=0;i<10;++i)for(int j=i+1;j<10;++j)if(used[i][j])e.push_back({i,j,used[i][j]});states.push_back(e);return;}
  fill(u,0);
 }
 void fill(int u,int lower){
  tick();if(!rem[u]){choose();return;}
  int capacity=0;
  for(int v=lower;v<10;++v)if(v!=u)capacity+=std::min(rem[v],base[u][v]-used[u][v]);
  if(capacity<rem[u])return;
  for(int v=lower;v<10;++v)if(v!=u&&rem[v]>0&&used[u][v]<base[u][v]){
   --rem[u];--rem[v];++used[u][v];++used[v][u];
   fill(u,v);
   --used[u][v];--used[v][u];++rem[u];++rem[v];
  }
 }
};
int main(int argc,char**argv){try{
 if(argc==2 && std::string(argv[1])=="--pairing"){
  int count;uint64_t limit;need(bool(std::cin>>count>>limit)&&count>=0&&count<=1024&&limit<=200000,"invalid control header");
  for(int k=0;k<count;++k){Mat base{};Vec d{};for(auto&r:base)for(auto&x:r)need(bool(std::cin>>x)&&x>=0&&x<=5,"invalid control capacity");for(auto&x:d)need(bool(std::cin>>x)&&x>=0&&x<=5,"invalid control degree");for(int i=0;i<10;++i){need(base[i][i]==0,"control loop capacity");for(int j=0;j<10;++j)need(base[i][j]==base[j][i],"asymmetric control");}Pairing p(base,d,limit);p.choose();std::sort(p.states.begin(),p.states.end());need(std::adjacent_find(p.states.begin(),p.states.end())==p.states.end(),"duplicate control pairing");need(std::chrono::duration<double>(std::chrono::steady_clock::now()-p.start).count()<=10,"INCOMPLETE control final guard");std::cout<<"[";for(size_t i=0;i<p.states.size();++i){if(i)std::cout<<",";std::cout<<edge_list(p.states[i]);}std::cout<<"]\n";}
  std::string junk;need(!(std::cin>>junk),"trailing control input");return 0;
 }
 need(argc==1,"invalid command option");
 int count;uint64_t limit;need(bool(std::cin>>count>>limit)&&count>=0&&count<=10000&&limit<=200000,"invalid header");
 Hash whole;uint64_t total=0,nodes=0;int last=-1;Hash profile_hash;uint64_t profile_count=0;
 auto emit=[&](){if(last>=0)std::cout<<"P "<<last<<' '<<profile_count<<' '<<profile_hash.finish()<<'\n';};
 for(int c=0;c<count;++c){
  int index;std::vector<int>a(5),b(5);Mat base{};Vec d{};int nv;
  need(bool(std::cin>>index),"truncated profile");need(index>=0&&index<56&&index>=last,"invalid profile index");
  if(index!=last){emit();if(last>=0)need(EVP_DigestInit_ex(profile_hash.p,EVP_sha256(),nullptr)==1,"hash reset");profile_count=0;last=index;}
  for(auto&x:a){need(bool(std::cin>>x),"truncated row");}
  for(auto&x:b)need(bool(std::cin>>x),"truncated row");
  for(const auto&v:{a,b})need(std::is_sorted(v.begin(),v.end())&&std::adjacent_find(v.begin(),v.end())==v.end()&&v.front()>=0&&v.back()<10,"invalid selected row");
  need(a<=b,"unordered selected rows");
  for(auto&r:base)for(auto&x:r)need(bool(std::cin>>x)&&x>=0&&x<=5,"invalid matrix entry");
  for(auto&x:d)need(bool(std::cin>>x)&&x>=0&&x<=5,"invalid degree");
  for(int i=0;i<10;++i){need(std::accumulate(base[i].begin(),base[i].end(),0)-4*base[i][i]==d[i],"degree bridge failed");for(int j=0;j<10;++j)need(base[i][j]==base[j][i],"asymmetric base");}
  need(std::accumulate(d.begin(),d.end(),0)==18,"not nine unit edges");
  need(bool(std::cin>>nv)&&nv>=0&&nv<=880,"invalid witness count");std::vector<Vec> q(nv);for(auto&v:q)for(auto&x:v)need(bool(std::cin>>x)&&x>=-820&&x<=820,"invalid witness coordinate");
  Pairing p(base,d,limit);p.choose();
  need(std::chrono::duration<double>(std::chrono::steady_clock::now()-p.start).count()<=10,"INCOMPLETE final pairing time guard");
  std::sort(p.states.begin(),p.states.end());need(std::adjacent_find(p.states.begin(),p.states.end())==p.states.end(),"duplicate multiset edge pairing");
  int preferred=-1;int64_t largest_negative=INT64_MIN;
  for(const auto&e:p.states){Mat r=base;Vec deg{};for(const auto&t:e){int i=t[0],j=t[1],w=t[2];need(w>0&&w<=base[i][j],"invalid edge capacity");r[i][j]-=w;r[j][i]-=w;deg[i]+=w;deg[j]+=w;}
   need(deg==d,"pairing did not satisfy degrees");for(int i=0;i<10;++i)need(std::accumulate(r[i].begin(),r[i].end(),0)==4*r[i][i],"residual row sum failed");
   auto form=[&](int k){int64_t x=0;for(int i=0;i<10;++i)for(int j=0;j<10;++j)x+=int64_t(q[k][i])*r[i][j]*q[k][j];return x;};
   int found=-1;int64_t value=0;if(preferred>=0&&(value=form(preferred))<0)found=preferred;
   if(found<0)for(int k=0;k<nv;++k)if((value=form(k))<0){found=k;break;}
   need(found>=0,"residual lacks negative certificate; NO exclusion verdict");preferred=found;largest_negative=std::max(largest_negative,value);
   std::string data="["+std::to_string(index)+","+list(a)+","+list(b)+","+edge_list(e)+","+matrix(r)+"]\n";whole.add(data);profile_hash.add(data);
  }
  total+=p.states.size();profile_count+=p.states.size();nodes+=p.nodes;
  std::cout<<"C "<<c<<' '<<index<<' '<<p.states.size()<<' '<<p.nodes<<' '<<largest_negative<<'\n';
 }
 emit();std::string junk;need(!(std::cin>>junk),"trailing input");std::cout<<"COMPLETE "<<total<<' '<<nodes<<' '<<whole.finish()<<'\n';return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
