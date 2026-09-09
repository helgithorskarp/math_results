// Independent checker for the q12 alternating-switch census.
// Uses the identity T(S)=sum_{v in S} e(S cap N(v))/3, unlike the primary
// enumerator's smallest-vertex triangle counter.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

constexpr int N=43,M=903;
using Adj=std::array<uint64_t,N>;
struct Row{int toggles=0;uint64_t switches=0,descending=0,neutral=0,min_count=0;int minimum=0;};

std::vector<std::vector<int>> load_rows(const std::string& path){
  std::ifstream f(path);if(!f)throw std::runtime_error("input open");
  std::string s((std::istreambuf_iterator<char>(f)),{});
  size_t k=s.find("\"complete_additional_objective_12_rotation_representatives\"");
  if(k==std::string::npos)throw std::runtime_error("input key");
  size_t p=s.find('[',k);int level=0;std::vector<std::vector<int>> rows;std::vector<int> row;
  while(p<s.size()){
    char ch=s[p++];
    if(ch=='['){++level;if(level==2)row.clear();continue;}
    if(ch==']'){if(level==2)rows.push_back(row);if(--level==0)break;continue;}
    if(level==2&&ch>='0'&&ch<='9'){int value=ch-'0';while(p<s.size()&&s[p]>='0'&&s[p]<='9')value=10*value+s[p++]-'0';row.push_back(value);}
  }
  if(rows.size()!=238)throw std::runtime_error("input row count");
  return rows;
}

std::vector<Row> load_claim(const std::string& path){
  std::ifstream f(path);if(!f)throw std::runtime_error("claim open");std::string line;std::getline(f,line);
  if(line!="index\ttoggles\tswitches\tdescending\tneutral\tminimum_q\tminimum_multiplicity\tbest_edges")throw std::runtime_error("claim header");
  std::vector<Row> rows;int expected=0;
  while(std::getline(f,line)){std::replace(line.begin(),line.end(),'\t',' ');std::istringstream in(line);int index;Row r;if(!(in>>index>>r.toggles>>r.switches>>r.descending>>r.neutral>>r.minimum>>r.min_count))throw std::runtime_error("claim row");if(index!=expected++)throw std::runtime_error("claim order");rows.push_back(r);}
  if(rows.size()!=238)throw std::runtime_error("claim row count");
  return rows;
}

int induced_edges(uint64_t s,const Adj& a){int n=0;while(s){int v=std::countr_zero(s);s&=s-1;n+=std::popcount(a[v]&s);}return n;}
int triangles(uint64_t s,const Adj& a){int total=0;uint64_t t=s;while(t){int v=std::countr_zero(t);t&=t-1;total+=induced_edges(s&a[v],a);}if(total%3)throw std::runtime_error("triangle divisibility");return total/3;}
int delta(Adj& red,int u,int v){constexpr uint64_t ALL=(UINT64_C(1)<<N)-1;bool c=(red[u]>>v)&1;uint64_t r=red[u]&red[v];Adj blue{};for(int x=0;x<N;++x)blue[x]=ALL&~(red[x]|(UINT64_C(1)<<x));uint64_t b=blue[u]&blue[v];int ans=c?-triangles(r,red)+triangles(b,blue):triangles(r,red)-triangles(b,blue);red[u]^=UINT64_C(1)<<v;red[v]^=UINT64_C(1)<<u;return ans;}
int direct(const Adj& a){int total=0;for(int i=0;i<N;++i)for(int j=i+1;j<N;++j)for(int k=j+1;k<N;++k)for(int l=k+1;l<N;++l)for(int m=l+1;m<N;++m){int v[5]{i,j,k,l,m},r=0;for(int x=0;x<5;++x)for(int y=x+1;y<5;++y)r+=(a[v[x]]>>v[y])&1;total+=(r==0||r==10);}return total;}

int main(int argc,char**argv)try{
  if(argc!=3){std::cerr<<"usage: verify INPUT.json CLAIM.tsv\n";return 2;}
  auto inputs=load_rows(argv[1]);auto claims=load_claim(argv[2]);
  std::array<std::array<int,N>,N> id{};std::array<std::pair<int,int>,M> ends{};int ne=0;
  for(int u=0;u<N;++u)for(int v=u+1;v<N;++v){id[u][v]=id[v][u]=ne;ends[ne++]={u,v};}
  const std::array<int,11>L{1,2,7,10,12,13,14,16,18,20,21};std::array<uint8_t,M>base{};
  for(int e=0;e<M;++e){auto[u,v]=ends[e];int d=std::min(v-u,N-v+u);base[e]=std::find(L.begin(),L.end(),d)!=L.end();}
  uint64_t all=0,down=0,flat=0;std::map<int,int> histogram;
  for(int z=0;z<238;++z){auto color=base;for(int e:inputs[z]){if(e<0||e>=M)throw std::runtime_error("edge id");color[e]^=1;}Adj original{};for(int e=0;e<M;++e)if(color[e]){auto[u,v]=ends[e];original[u]|=UINT64_C(1)<<v;original[v]|=UINT64_C(1)<<u;}if(direct(original)!=12)throw std::runtime_error("source q");
    uint64_t count=0,lower=0,equal=0,min_count=0;int minimum=100000;
    for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)for(int c=b+1;c<N;++c)for(int d=c+1;d<N;++d){
      int match[3][2]{{id[a][b],id[c][d]},{id[a][c],id[b][d]},{id[a][d],id[b][c]}};
      for(int i=0;i<3;++i)for(int j=i+1;j<3;++j){bool x=color[match[i][0]],y=color[match[j][0]];if(color[match[i][1]]!=x||color[match[j][1]]!=y||x==y)continue;++count;Adj work=original;int q=12;int move[4]{match[i][0],match[i][1],match[j][0],match[j][1]};for(int e:move){auto[u,v]=ends[e];q+=delta(work,u,v);}if(q<minimum){minimum=q;min_count=1;}else if(q==minimum)++min_count;lower+=(q<12);equal+=(q==12);}
    }
    Row const&r=claims[z];if(r.toggles!=(int)inputs[z].size()||r.switches!=count||r.descending!=lower||r.neutral!=equal||r.minimum!=minimum||r.min_count!=min_count)throw std::runtime_error("claim mismatch at row "+std::to_string(z));
    all+=count;down+=lower;flat+=equal;++histogram[minimum];
  }
  if(all!=12056241||down||flat||histogram!=std::map<int,int>{{17,10},{18,5},{19,27},{20,84},{21,58},{22,54}})throw std::runtime_error("aggregate mismatch");
  std::cout<<"PASS independent alternating-switch census seeds=238 switches="<<all<<" descending="<<down<<" neutral="<<flat<<"\n";
  std::cout<<"minimum_neighbor_histogram=17:10,18:5,19:27,20:84,21:58,22:54\n";
  return 0;
}catch(std::exception const&e){std::cerr<<e.what()<<'\n';return 2;}
