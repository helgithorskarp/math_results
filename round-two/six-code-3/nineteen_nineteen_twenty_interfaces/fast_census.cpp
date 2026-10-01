// six-code-3, researcher: whole-case scheduling for mixed19/19/20.
// Include/exclude kernel credited to six-reviewer-5, source42daf31; see KERNEL_ORIGIN.json.
// Independent colored kernel is the unchanged published author implementation.
// Main-loop candidate masks have separately reconstructed literal coverage checks.
#define Search IncludeSearch
#include "reviewer_kernel.hpp"
#undef Search
#define Search ColorSearch
#define main unused_color_protocol_main
#include "../nineteen_twenty_twenty_interfaces/color_server.cpp"
#undef main
#undef Search

#ifndef FAST_ENGINE
#define FAST_ENGINE 0
#endif

struct RankSearch {
    IncludeSearch include;
    Graph graph;
    std::uint64_t total_nodes=0, peak_query_nodes=0, calls=0;
    explicit RankSearch(const std::vector<Word>& words):include(words),
        graph{static_cast<int>(words.size()), std::vector<Bits>(words.size())} {
        for(std::size_t i=0;i<words.size();++i)for(std::size_t j=0;j<words.size();++j)
            if(i!=j && size(words[i]&words[j])<=2)graph.adjacency[i].set(j);
    }
    RankSearch(int n,const std::vector<Set>& bad):include(n,bad),
        graph{n,std::vector<Bits>(static_cast<std::size_t>(n))} {
        for(int i=0;i<n;++i)for(int j=0;j<n;++j)
            if(i!=j && !bad[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)])
                graph.adjacency[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
    }
    std::vector<List> run(const Set& available,int rank) {
        require(rank>0&&rank<=graph.n,"invalid rank");
        std::vector<List> result;std::uint64_t nodes=0;
#if FAST_ENGINE == 0
        result=include.run(available,rank);nodes=include.query_nodes;
#elif FAST_ENGINE == 1
        Bits possible;
        for(int i=0;i<256;++i)if(available[static_cast<std::size_t>(i)]) {
            require(i<graph.n,"invalid available vertex");possible.set(static_cast<std::size_t>(i));
        }
        ColorSearch search{graph,rank,0,2000000,20000,Clock::now(),{}};
        List chosen;search.visit(chosen,possible,Bits());nodes=search.nodes;
        result.assign(search.solutions.begin(),search.solutions.end());
#else
#error Invalid FAST_ENGINE
#endif
        ++calls;total_nodes+=nodes;peak_query_nodes=std::max(peak_query_nodes,nodes);
        return result;
    }
};

std::string hash(const std::string& s) {Digest d;d.add(s);return d.finish();}
std::string masks(const std::vector<Word>& words) {
    List out;for(Word word:words)out.push_back(static_cast<int>(word));return array(out);
}
std::string adjacency(const std::vector<Word>& words) {
    std::vector<List> all;
    for(std::size_t i=0;i<words.size();++i) {
        List row;for(std::size_t j=0;j<words.size();++j)
            if(i!=j&&size(words[i]&words[j])<=2)row.push_back(static_cast<int>(j));
        all.push_back(row);
    }
    return arrays(all);
}
int y_leave(const List& words) {
    std::array<int,18> degree{};std::array<std::array<bool,18>,18> covered{};
    for(int word:words)if(word&(1<<15)) {
        for(int i=0;i<18;++i)if(i!=15&&(word&(1<<i))) {
            ++degree[static_cast<std::size_t>(i)];
            for(int j=i+1;j<18;++j)if(j!=15&&(word&(1<<j)))
                covered[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)]=true;
        }
    }
    int result=0;
    for(int i=0;i<18;++i)for(int j=i+1;j<18;++j)
        if(degree[static_cast<std::size_t>(i)]==5&&degree[static_cast<std::size_t>(j)]==5
           &&!covered[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)])++result;
    return result;
}

void controls_fast() {
    std::uint64_t checks=0;
    for(int encoding=0;encoding<1024;++encoding) {
        std::vector<Set> bad(5);int bit=0;
        for(int i=0;i<5;++i)for(int j=i+1;j<5;++j,++bit)if(encoding&(1<<bit)) {
            bad[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
            bad[static_cast<std::size_t>(j)].set(static_cast<std::size_t>(i));
        }
        RankSearch engine(5,bad);Set full;for(int i=0;i<5;++i)full.set(static_cast<std::size_t>(i));
        for(int rank=1;rank<=5;++rank) {
            std::vector<List> literal;
            for(int subset=1;subset<32;++subset)if(__builtin_popcount(static_cast<unsigned int>(subset))==rank) {
                List chosen;bool ok=true;
                for(int i=0;i<5;++i)if(subset&(1<<i)) {
                    chosen.push_back(i);
                    for(int j=i+1;j<5;++j)if((subset&(1<<j))&&bad[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)])ok=false;
                }
                if(ok)literal.push_back(chosen);
            }
            std::sort(literal.begin(),literal.end());require(engine.run(full,rank)==literal,"small graph mismatch");++checks;
        }
    }
    for(int n:{64,65,128,129,186,256}) {
        std::vector<Set> bad(static_cast<std::size_t>(n));
        for(int i=0;i<n;++i)for(int j=0;j<n;++j)if(i!=j)bad[static_cast<std::size_t>(i)].set(static_cast<std::size_t>(j));
        List selected={0,1,2,3,4,5,6,7,8,9,n-1};
        for(int i:selected)for(int j:selected)if(i!=j)bad[static_cast<std::size_t>(i)].reset(static_cast<std::size_t>(j));
        RankSearch engine(n,bad);Set full;for(int i=0;i<n;++i)full.set(static_cast<std::size_t>(i));
        require(engine.run(full,11)==std::vector<List>{selected},"bit boundary mismatch");++checks;
    }
    std::vector<Set> empty(12);RankSearch complete(12,empty);Set full;for(int i=0;i<12;++i)full.set(static_cast<std::size_t>(i));
    for(int rank:{10,11}) {
        std::vector<List> literal;
        for(int mask=0;mask<4096;++mask)if(__builtin_popcount(static_cast<unsigned int>(mask))==rank) {
            List selected;for(int i=0;i<12;++i)if(mask&(1<<i))selected.push_back(i);literal.push_back(selected);
        }
        std::sort(literal.begin(),literal.end());require(complete.run(full,rank)==literal,"private-rank control");++checks;
    }
    std::vector<Word> triples;subsets(0,3,0,triples);
    triples.erase(std::remove_if(triples.begin(),triples.end(),[](Word t){return t>=(Word(1)<<12);}),triples.end());
    std::vector<List> covers;List chosen;tails(triples,0,0,chosen,covers);
    require(triples.size()==220&&covers.size()==15400,"four-tail coverage control");
    require(std::adjacent_find(covers.begin(),covers.end())==covers.end(),"four-tail duplicate control");
    for(const auto& cover:covers) {
        Word used=0;for(int i:cover) {require(!(used&triples[static_cast<std::size_t>(i)]),"four-tail overlap control");used|=triples[static_cast<std::size_t>(i)];}
        require(size(used)==12,"four-tail union control");
    }
    std::cout<<"{\"status\":\"COMPLETE\",\"engine\":"<<FAST_ENGINE<<",\"literal_graph_checks\":"<<checks<<",\"twelve_point_four_tail_partitions\":15400}\n";
}

int main(int argc,char** argv) {
    try {
        if(argc==2&&std::string(argv[1])=="--controls") {controls_fast();return 0;}
        require(argc==4,"usage: fast_census CASE ORIENTATION FIXED_WORDS");
        const int case_id=std::stoi(argv[1]),orientation=std::stoi(argv[2]);
        require(case_id>=0&&case_id<46&&(orientation==0||orientation==1),"case/orientation domain");
        std::ifstream input(argv[3]);auto fixed=read_words(input);
        require(fixed.size()==19&&std::is_sorted(fixed.begin(),fixed.end())
                &&std::adjacent_find(fixed.begin(),fixed.end())==fixed.end(),"fixed input size/order");
        int xy=0,xz=0;
        for(std::size_t i=0;i<fixed.size();++i) {
            require(size(fixed[i])==5&&(fixed[i]&(Word(1)<<17))&&((fixed[i]&(Word(7)<<15))!=(Word(7)<<15)),"fixed word shape");
            xy+=(fixed[i]&(Word(1)<<15))!=0;xz+=(fixed[i]&(Word(1)<<16))!=0;
            for(std::size_t j=i+1;j<fixed.size();++j)require(size(fixed[i]&fixed[j])<=2,"fixed packing");
        }
        require(xy==5&&xz==5,"marked fixed pair degrees");
        const auto started=Clock::now();std::vector<Word> three,four,triples,ywords,zwords;
        subsets(0,3,0,three);subsets(0,4,0,four);
        for(Word tail:three)if(allowed(tail|(Word(3)<<15),fixed))triples.push_back(tail);
        for(Word tail:four) {
            if(allowed(tail|(Word(1)<<15),fixed))ywords.push_back(tail|(Word(1)<<15));
            if(allowed(tail|(Word(1)<<16),fixed))zwords.push_back(tail|(Word(1)<<16));
        }
        RankSearch ys(ywords),zs(zwords);std::vector<List> covers;List chosen;tails(triples,0,0,chosen,covers);
        std::vector<Set> ymask,zmask,cross;
        std::vector<List> yi,zi,cr;
        for(Word tail:triples) {
            Word word=tail|(Word(3)<<15);ymask.push_back(compatible(ywords,word));zmask.push_back(compatible(zwords,word));
            yi.push_back(indices(ymask.back(),ys.graph.n));zi.push_back(indices(zmask.back(),zs.graph.n));
        }
        for(Word word:zwords) {cross.push_back(compatible(ywords,word));cr.push_back(indices(cross.back(),ys.graph.n));}
        std::uint64_t z_count=0,y_count=0;std::vector<std::string> cores,intervals;
        Digest whole;std::unique_ptr<Digest> interval=std::make_unique<Digest>();
        std::size_t interval_start=0;std::uint64_t iz=0,iy=0;
        for(std::size_t ci=0;ci<covers.size();++ci) {
            require(Clock::now()-started<std::chrono::seconds(60),"INCOMPLETE whole-case guard");
            Set yd,zd;for(std::size_t i=0;i<ywords.size();++i)yd.set(i);for(std::size_t i=0;i<zwords.size();++i)zd.set(i);
            std::vector<Word> common=fixed;
            for(int t:covers[ci]) {
                yd&=ymask[static_cast<std::size_t>(t)];zd&=zmask[static_cast<std::size_t>(t)];
                common.push_back(triples[static_cast<std::size_t>(t)]|(Word(3)<<15));
            }
            const auto zsolutions=zs.run(zd,11);z_count+=zsolutions.size();iz+=zsolutions.size();
            std::vector<std::string> records;
            for(const List& z:zsolutions) {
                Set left=yd;for(int vertex:z)left&=cross[static_cast<std::size_t>(vertex)];
                const auto ysolutions=ys.run(left,10);y_count+=ysolutions.size();iy+=ysolutions.size();
                records.push_back("{\"y_candidates\":"+array(indices(left,ys.graph.n))+",\"y_ten\":"+arrays(ysolutions)+",\"z\":"+array(z)+"}");
                for(const List& y:ysolutions) {
                    List words;for(Word w:common)words.push_back(static_cast<int>(w));
                    for(int vertex:y)words.push_back(static_cast<int>(ywords[static_cast<std::size_t>(vertex)]));
                    for(int vertex:z)words.push_back(static_cast<int>(zwords[static_cast<std::size_t>(vertex)]));
                    std::sort(words.begin(),words.end());require(words.size()==44,"core word count");
                    const int m=y_leave(words);
                    cores.push_back("{\"blocks\":"+array(words)+",\"case\":"+std::to_string(case_id)+",\"core_sha256\":\""+hash(array(words)+"\n")+"\",\"cover\":"+std::to_string(ci)+",\"orientation\":"+std::to_string(orientation)+",\"y\":"+array(y)+",\"y_m\":"+std::to_string(m)+",\"z\":"+array(z)+"}");
                    require(cores.size()<=20000,"INCOMPLETE core-output guard");
                }
            }
            std::string record="{\"cover\":"+std::to_string(ci)+",\"y_cases\":[";
            for(std::size_t i=0;i<records.size();++i) {if(i)record+=',';record+=records[i];}
            record+="],\"z_candidates\":"+array(indices(zd,zs.graph.n))+",\"z_eleven\":"+arrays(zsolutions)+"}\n";
            whole.add(record);interval->add(record);
            if((ci+1)%5000==0||ci+1==covers.size()) {
                intervals.push_back("{\"start\":"+std::to_string(interval_start)+",\"finish\":"+std::to_string(ci+1)+",\"z_eleven\":"+std::to_string(iz)+",\"y_ten\":"+std::to_string(iy)+",\"carrier_sha256\":\""+interval->finish()+"\"}");
                interval_start=ci+1;iz=iy=0;interval=std::make_unique<Digest>();
            }
        }
        std::cout<<"{\"status\":\"COMPLETE\",\"engine\":"<<FAST_ENGINE<<",\"case\":"<<case_id<<",\"orientation\":"<<orientation<<",\"covers\":"<<covers.size()<<",\"z_eleven\":"<<z_count<<",\"y_ten\":"<<y_count<<",\"z_nodes\":"<<zs.total_nodes<<",\"y_nodes\":"<<ys.total_nodes<<",\"peak_query_nodes\":"<<std::max(ys.peak_query_nodes,zs.peak_query_nodes)<<",\"carrier_sha256\":\""<<whole.finish()<<"\",\"universes\":{\"triples\":"<<masks(triples)<<",\"y_words\":"<<masks(ywords)<<",\"z_words\":"<<masks(zwords)<<",\"covers_sha256\":\""<<hash(arrays(covers)+"\n")<<"\",\"y_adjacency_sha256\":\""<<hash(adjacency(ywords)+"\n")<<"\",\"z_adjacency_sha256\":\""<<hash(adjacency(zwords)+"\n")<<"\",\"tail_y_sha256\":\""<<hash(arrays(yi)+"\n")<<"\",\"tail_z_sha256\":\""<<hash(arrays(zi)+"\n")<<"\",\"z_to_y_sha256\":\""<<hash(arrays(cr)+"\n")<<"\"},\"intervals\":[";
        for(std::size_t i=0;i<intervals.size();++i) {if(i)std::cout<<',';std::cout<<intervals[i];}
        std::cout<<"],\"cores\":[";for(std::size_t i=0;i<cores.size();++i) {if(i)std::cout<<',';std::cout<<cores[i];}
        std::cout<<"],\"seconds\":"<<std::chrono::duration<double>(Clock::now()-started).count()<<"}\n";
        return 0;
    } catch(const std::exception& error) {std::cerr<<error.what()<<'\n';return 1;}
}
