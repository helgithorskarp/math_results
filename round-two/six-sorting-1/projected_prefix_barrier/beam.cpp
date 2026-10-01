// Heuristic beam construction using the exact necessary semantic filter.
// Beam truncation and Boolean-image deduplication are heuristic, not proofs.
#define SEMANTIC_PROFILE_LIBRARY
#include "filter_frontier.cpp"
#include <chrono>
#include <limits>
#include <tuple>

using Image=std::vector<unsigned>;
using FullBits=std::array<std::uint64_t,128>;
using FullState=std::array<FullBits,N>;
bool weight_input_counts=false;
struct Quality {
  unsigned bad=0,inversions=0,cardinality=0,failed_inputs=0;
  std::uint64_t pressure=0;
  auto key() const {return std::tuple{weight_input_counts?failed_inputs:bad,inversions,cardinality,pressure};}
  bool operator<(const Quality& o)const{return key()<o.key();}
};
struct Node {
  State profiles;
  Image image;
  FullState full;
  std::vector<Gate> suffix;
  Quality quality;
};

unsigned compare(unsigned x,Gate g) {
  auto [a,b]=g;
  return ((x>>a)&1U) && !((x>>b)&1U) ? x^((1U<<a)|(1U<<b)) : x;
}
bool sorted(unsigned x) {
  for(unsigned i=0;i<N-1;++i)if(((x>>i)&1U) && !((x>>(i+1))&1U))return false;
  return true;
}
Image next_image(const Image& xs,Gate g) {
  Image result;result.reserve(xs.size());
  for(auto x:xs)result.push_back(compare(x,g));
  std::sort(result.begin(),result.end());
  result.erase(std::unique(result.begin(),result.end()),result.end());
  return result;
}
void apply_full(FullState& s,Gate g) {
  auto a=static_cast<std::size_t>(g.first),b=static_cast<std::size_t>(g.second);
  for(unsigned w=0;w<128;++w) {
    auto x=s[a][w],y=s[b][w];s[a][w]=x&y;s[b][w]=x|y;
  }
}
Quality quality(const Image& xs,const State& profiles,const FullState& full) {
  Quality result;result.cardinality=static_cast<unsigned>(xs.size());
  for(auto x:xs) {
    result.bad+=!sorted(x);
    for(unsigned a=0;a<N;++a)for(unsigned b=a+1;b<N;++b)
      result.inversions+=((x>>a)&1U) && !((x>>b)&1U);
  }
  for(std::size_t f=0;f<profiles.size();++f)
    result.pressure+=masses(profiles[f]).second*(512/limits[f]);
  for(unsigned w=0;w<128;++w) {
    std::uint64_t bad=0;
    for(unsigned i=0;i<N-1;++i)bad|=full[i][w]&~full[i+1][w];
    result.failed_inputs+=static_cast<unsigned>(std::popcount(bad));
  }
  return result;
}
void save(const std::string& path,const std::vector<Gate>& prefix,const Node& best,
          const std::string& status,std::uint64_t nodes,unsigned width,double elapsed) {
  std::vector<Gate> gates=prefix;gates.insert(gates.end(),best.suffix.begin(),best.suffix.end());
  unsigned failures=0;
  for(unsigned x=0;x<(1U<<N);++x) {
    auto value=x;for(auto g:gates)value=compare(value,g);failures+=!sorted(value);
  }
  if(failures!=best.quality.failed_inputs)throw std::runtime_error("packed and scalar fitness disagree");
  std::ofstream out(path);
  if(!out)throw std::runtime_error("cannot write beam checkpoint");
  out<<"{\"status\":\""<<status<<"\",\"n\":13,\"target_size\":44,\"prefix_size\":"<<prefix.size()
     <<",\"size\":"<<gates.size()<<",\"beam_width\":"<<width<<",\"nodes\":"<<nodes
     <<",\"seconds\":"<<elapsed<<",\"score_policy\":\""<<(weight_input_counts?"all_original_inputs":"distinct_image_states")
     <<"\",\"failed_inputs\":"<<failures
     <<",\"unsorted_image_states\":"<<best.quality.bad<<",\"image_cardinality\":"<<best.image.size()
     <<",\"gates\":[";
  for(std::size_t i=0;i<gates.size();++i)out<<(i?",":"")<<'['<<gates[i].first<<','<<gates[i].second<<']';
  out<<"]}\n";out.close();if(!out)throw std::runtime_error("beam checkpoint write failed");
}

int main(int argc,char** argv) {
 try {
  if(argc!=5 && argc!=6)throw std::runtime_error("usage: beam PREFIX_TXT WIDTH MAX_NODES CHECKPOINT_JSON [WEIGHT_INPUT_COUNTS_0_OR_1]");
  auto prefix=read_network(argv[1]);const auto width=static_cast<unsigned>(std::stoul(argv[2]));
  const auto node_limit=std::stoull(argv[3]);const std::string output=argv[4];
  if(argc==6) {
    const std::string flag=argv[5];if(flag!="0" && flag!="1")throw std::runtime_error("bad fitness policy");
    weight_input_counts=flag=="1";
  }
  if(width==0 || width>128 || node_limit==0 || prefix.size()>=44)throw std::runtime_error("invalid beam bounds");
  State state=initial();for(auto g:prefix)apply(state,g);
  if(!passes(state))throw std::runtime_error("prefix already rejected");
  Image image;for(unsigned x=0;x<(1U<<N);++x)image.push_back(x);
  for(auto g:prefix)image=next_image(image,g);
  FullState full{};
  for(unsigned x=0;x<(1U<<N);++x)for(unsigned i=0;i<N;++i)
    if((x>>i)&1U)full[i][x/64]|=std::uint64_t{1}<<(x%64);
  for(auto g:prefix)apply_full(full,g);
  const auto q=quality(image,state,full);std::vector<Node> beam;
  beam.push_back({std::move(state),std::move(image),full,{},q});
  const auto started=std::chrono::steady_clock::now();std::uint64_t nodes=0,kept=0;
  const auto seconds=[&](){return std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();};
  for(unsigned level=0;prefix.size()+level<44;++level) {
    std::vector<Node> next;
    std::map<Image,std::size_t> seen;
    for(const auto& parent:beam) for(int a=0;a<N;++a)for(int b=a+1;b<N;++b) {
      if(nodes>=node_limit) {
        save(output,prefix,beam.front(),"INCOMPLETE_NODE_LIMIT",nodes,width,seconds());
        std::cout<<"INCOMPLETE_NODE_LIMIT nodes="<<nodes<<std::endl;return 0;
      }
      ++nodes;auto candidate_image=next_image(parent.image,{a,b});
      if(candidate_image==parent.image)continue;
      State child=parent.profiles;apply(child,{a,b});
      if(!passes(child))continue;
      ++kept;auto candidate_full=parent.full;apply_full(candidate_full,{a,b});
      auto score=quality(candidate_image,child,candidate_full);
      std::size_t position=next.size();auto duplicate=seen.find(candidate_image);
      if(duplicate!=seen.end()) {
        position=duplicate->second;
        if(!(score<next[position].quality))continue;
      } else if(next.size()>=width) {
        position=0;for(std::size_t i=1;i<next.size();++i)
          if(next[position].quality<next[i].quality)position=i;
        if(!(score<next[position].quality))continue;
      }
      auto suffix=parent.suffix;suffix.emplace_back(a,b);
      Node node{std::move(child),std::move(candidate_image),candidate_full,std::move(suffix),score};
      if(position==next.size())next.push_back(std::move(node));
      else {seen.erase(next[position].image);next[position]=std::move(node);}
      seen[next[position].image]=position;
    }
    if(next.empty()) {
      save(output,prefix,beam.front(),"INCOMPLETE_BEAM_EXHAUSTED",nodes,width,seconds());
      std::cout<<"INCOMPLETE_BEAM_EXHAUSTED at_size="<<(prefix.size()+level+1)<<" nodes="<<nodes<<std::endl;return 0;
    }
    std::sort(next.begin(),next.end(),[](const Node& a,const Node& b){return a.quality<b.quality;});
    beam=std::move(next);
    const auto& best=beam.front();
    std::cout<<"size="<<(prefix.size()+level+1)<<" nodes="<<nodes<<" filter_passing="<<kept
       <<" beam="<<beam.size()<<" best_unsorted_states="<<best.quality.bad<<" failed_inputs="<<best.quality.failed_inputs
       <<" inversions="<<best.quality.inversions
       <<" seconds="<<seconds()<<std::endl;
    save(output,prefix,best,"INCOMPLETE_HEURISTIC_BEAM",nodes,width,seconds());
    if(best.quality.bad==0) {
      save(output,prefix,best,"BOOLEAN_SORTER_FOUND",nodes,width,seconds());
      std::cout<<"BOOLEAN_SORTER_FOUND"<<std::endl;return 0;
    }
  }
  std::cout<<"INCOMPLETE_HEURISTIC_BEAM nodes="<<nodes<<" seconds="<<seconds()<<std::endl;
 }catch(const std::exception& e){std::cerr<<"ERROR "<<e.what()<<'\n';return 2;}
}
