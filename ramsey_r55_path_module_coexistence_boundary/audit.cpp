#include <algorithm>
#include <array>
#include <cstdint>
#include <climits>
static_assert(CHAR_BIT==8, "eight-bit certificate bytes required");
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <vector>
using U=std::uint64_t;
int n; U full; std::vector<U> red,blue;
std::array<int,1024> pattern{};
U subset_visits=0, records=0; int max2=0,max3=0;
int pop(U x){return __builtin_popcountll(x);}
int bit(U x){return __builtin_ctzll(x);}
bool p5(int w){
 std::array<int,5>a{},d{};int pos=0;
 for(int i=0;i<5;++i)for(int j=i+1;j<5;++j,++pos)if((w>>pos)&1){a[i]|=1<<j;a[j]|=1<<i;++d[i];++d[j];}
 std::sort(d.begin(),d.end()); if(d!=std::array<int,5>{1,1,2,2,2})return false;
 int seen=1,prev=0;while(seen!=prev){prev=seen;for(int i=0;i<5;++i)if((seen>>i)&1)seen|=a[i];}return seen==31;
}
int word(const std::array<int,5>&v){int w=0,k=0;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j,++k)if((red[v[i]]>>v[j])&1)w|=1<<k;return w;}
std::vector<int> vertices(U m){std::vector<int>v;while(m){int x=bit(m);m&=m-1;v.push_back(x);}return v;}
void modules(U candidates,int size,U R,U B){
 if(size>=2){++subset_visits;int score=size+pop(R|B);max2=std::max(max2,score);if(size>=3)max3=std::max(max3,score);}
 while(candidates){int v=bit(candidates);candidates&=candidates-1;modules(candidates,size+1,R&red[v],B&blue[v]);}
}
U find_path(U mask,int wanted){
 auto v=vertices(mask);int len=static_cast<int>(v.size());
 for(int a=0;a<len-4;++a)for(int b=a+1;b<len-3;++b)for(int c=b+1;c<len-2;++c)for(int d=c+1;d<len-1;++d)for(int e=d+1;e<len;++e){
  std::array<int,5>q{v[a],v[b],v[c],v[d],v[e]};int p=pattern[word(q)];
  if(p && (!wanted || p==wanted))return (U{1}<<q[0])|(U{1}<<q[1])|(U{1}<<q[2])|(U{1}<<q[3])|(U{1}<<q[4]);
 }
 return 0;
}
void put(std::ostream&o,U m){std::array<unsigned char,8>bytes{};for(int i=0;i<8;++i)bytes[i]=static_cast<unsigned char>((m>>(8*i))&255);o.write(reinterpret_cast<const char*>(bytes.data()),8);++records;}
void cover(const std::vector<int>&pool,int wanted,int k,std::ostream&o){
 std::function<void(int,int,U)>walk=[&](int start,int left,U mask){
  if(!left){U witness=find_path(mask,wanted);if(!witness)throw std::runtime_error("Uncovered required subset: "+std::to_string(mask));put(o,witness);return;}
  for(int i=start;i<=static_cast<int>(pool.size())-left;++i)walk(i+1,left-1,mask|(U{1}<<pool[i]));
 };walk(0,k,0);
}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("usage: coexist_audit graph.edges cover.bin");
 std::ifstream in(argv[1]);int m,u,v;if(!(in>>n>>m)||n!=43||m<0)throw std::runtime_error("order43 input required");
 full=(U{1}<<n)-1;red.assign(n,0);blue.assign(n,0);
 for(int i=0;i<m;++i){if(!(in>>u>>v)||u<0||u>=v||v>=n||((red[u]>>v)&1))throw std::runtime_error("edge input");red[u]|=U{1}<<v;red[v]|=U{1}<<u;}
 if(in>>u)throw std::runtime_error("trailing input");
 for(int i=0;i<n;++i)blue[i]=full^red[i]^(U{1}<<i);
 for(int w=0;w<1024;++w)pattern[w]=p5(w)?1:(p5(w^1023)?2:0);
 std::array<int,43>parent{};for(int i=0;i<n;++i)parent[i]=i;
 std::function<int(int)>root=[&](int x){return parent[x]==x?x:parent[x]=root(parent[x]);};
 std::vector<std::array<int,6>>defects;std::array<U,3>counts{};
 for(int a=0;a<n-4;++a)for(int b=a+1;b<n-3;++b)for(int c=b+1;c<n-2;++c)for(int d=c+1;d<n-1;++d)for(int e=d+1;e<n;++e){
  std::array<int,5>q{a,b,c,d,e};int w=word(q);if(w==0||w==1023)defects.push_back({a,b,c,d,e,w==1023?1:2});
  int p=pattern[w];if(p){++counts[p];for(int x:q)parent[root(x)]=root(a);}
 }
 for(int r=0;r<n;++r){modules(red[r],0,full,full);modules(blue[r],0,full,full);}
 if(max2>=36||max3>=28)throw std::runtime_error("module resilience fails");
 std::ofstream out(argv[2],std::ios::binary);if(!out)throw std::runtime_error("output open");
 cover(vertices((U{1}<<21)-1),0,13,out);U first=records;
 cover(vertices(full^((U{1}<<21)-1)),0,14,out);U second=records-first;
 U global_records=records;
 std::vector<U>local_counts;
 for(int r=0;r<n;++r)for(int color=1;color<=2;++color){U before=records;cover(vertices(color==1?red[r]:blue[r]),color,18,out);local_counts.push_back(records-before);}
 out.close();if(!out)throw std::runtime_error("incomplete output");
 std::vector<int>component_sizes(n,0),components;for(int i=0;i<n;++i)++component_sizes[root(i)];for(int x:component_sizes)if(x)components.push_back(x);std::sort(components.begin(),components.end());
 std::cout<<"{\n  \"status\": \"PHYSICAL_NECESSARY_SYSTEM_SATISFIED\",\n  \"module_subset_visits\": "<<subset_visits<<",\n  \"maximum_induced_order_with_module_size_at_least_two\": "<<max2<<",\n  \"maximum_induced_order_with_module_size_at_least_three\": "<<max3<<",\n  \"red_paths\": "<<counts[1]<<",\n  \"blue_paths\": "<<counts[2]<<",\n  \"global_cover_records\": ["<<first<<", "<<second<<"],\n  \"neighborhood_cover_records\": "<<records-global_records<<",\n  \"total_records\": "<<records<<",\n  \"cover_bytes\": "<<8*records<<",\n  \"path_component_sizes\": [";
 for(std::size_t i=0;i<components.size();++i)std::cout<<(i?", ":"")<<components[i];
 std::cout<<"],\n  \"defects\": [";for(std::size_t i=0;i<defects.size();++i){if(i)std::cout<<", ";std::cout<<"[";for(int j=0;j<6;++j)std::cout<<(j?", ":"")<<defects[i][j];std::cout<<"]";}std::cout<<"],\n  \"neighborhood_records_by_root_and_color\": [";
 for(std::size_t i=0;i<local_counts.size();++i){std::cout<<(i?", ":"")<<local_counts[i];}
 std::cout<<"]\n}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}return 0;}
