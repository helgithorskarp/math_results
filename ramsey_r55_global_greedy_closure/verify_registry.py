"""Verify all complete-task records and disjoint covering-code intervals."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def verify():
 registry=json.loads((HERE/'TASKS.json').read_text());counts=json.loads((HERE/'GLOBAL_COUNTS.json').read_text());audit=json.loads((HERE/'INTERFACE_AUDIT.json').read_text());stats={tuple(r['branch']):r for r in audit['formula_stats']};offset=0
 if registry['task_count']!=39 or len(registry['tasks'])!=39 or registry['code_is_physical_graph_bijection'] is not False or not registry['all_tasks_undecided']:raise ValueError('Task scope')
 for task,row in zip(registry['tasks'],counts['branches']):
  b=row['branch'];r,s,t=b;label=f'r{r}-s{s}-t{t}';stat=stats[tuple(b)]
  expected={'task_id':'gc1-'+label,'parent_task_id':label,'branch':b,'variables':847,'clauses':stat['clauses'],'extra_clauses':stat['extra_clauses'],'extra_statistics':stat['extra_statistics'],'carrier_mode':row['carrier_mode'],'tail_carrier_count':row['tail_carrier_count'],'catalog_order':row['residual_vertices'] if row['carrier_mode']=='catalog_embedding' else None,'whole_graph_cover_count':row['whole_graph_cover_count'],'global_start':offset,'global_stop':offset+row['whole_graph_cover_count'],'red_four_free_union_size':43-4*r if r<7 else None,'red_triangle_free_union_size':15-3*s if s<4 else None,'decision':'UNDECIDED'}
  if task!=expected:raise ValueError('Task/physical family mismatch')
  offset=expected['global_stop']
 if offset!=registry['whole_graph_representation_count'] or offset!=counts['whole_graph_representation_count']:raise ValueError('Whole cover interval')
 ranked=sorted(registry['tasks'],key=lambda x:x['whole_graph_cover_count'])
 if registry['least_carrier_task']!=ranked[0]['task_id'] or ranked[0]['whole_graph_cover_count']==ranked[1]['whole_graph_cover_count']:raise ValueError('Least carrier task')
 return {'status':'VERIFIED_COMPLETE39_TASK_REGISTRY','tasks':39,'whole_graph_representation_count':offset,'least_carrier_task':ranked[0]['task_id'],'all_tasks_undecided':True}

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
