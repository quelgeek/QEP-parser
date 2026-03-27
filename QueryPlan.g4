/* proof-of-concept ANTLR 4 grammar to parse "Lisp format" Ingres QEPs  */
/* roy.hann@rationalcommerce.com */
/* pretty rough-and-ready but good enough to prove that Lisp format QEPs can be parsed */
/* still contains some deadwood from tried-and-failed ideas; I'll clean it up some day... */

grammar QueryPlan;
import QEPLexer;

qep
	:	QEP_LABEL '|' '{' plan '}' ';';

plan_nr
	:	NUMBER;

subplan_nr
	:	NUMBER;

enumeration
	:	(NO TIMEOUT)	#NOTIMEOUT
	|	(TIMED OUT) 	#TIMEDOUT
	|	GREEDY			#GREEDYENUM;

construct
	:	(UNION VIEW name) |
		(UNION SUBQUERY) |
		(MAIN QUERY) |
		(SIMPLE AGGREGATE AGGREGATE EXPRESSION PRODUCING 
				function_name '(' ('*'|argument_name) ')') ;

function_name
	:	NAME;

argument_name
	:	NAME;

plan
	:	join			
	|	proj_rest		
	|	exchange_node	
	|	sort
	|	orig_node;

join
	:	(outer_join JOIN)?
		join_technique JOIN
		('(' key_column_list ')')?
		result_structure 
		result_size
		disk_cost cpu_cost
		'{' plan '}' '{' plan '}';

result_size
	:	PAGES page_count TUPS row_count;

outer_join
	:	LEFT | RIGHT | FULL ;

join_technique
	:	FSM | PSM | HASH | KLOOKUP | TIDLOOKUP | SQEXEC ;

key_column_list
	:	( key_column_name (',' key_column_name)* );

key_column_name
	:	(function_attribute | intermediate_attribute)? name;

function_attribute
	:	FUNCATT;

intermediate_attribute
	:	TEMPATT;

result_structure	
	:	HEAP|((SORTED|SORT|SORTU) ON? '(' (not_used_flag | key_column_list) ')');

page_count
	:	NUMBER;

row_count
	:	NUMBER;

disk_cost
	:	DUNITS;

cpu_cost
	:	CUNITS;

proj_rest
    :	PROJ_REST
		result_structure
		result_size
		disk_cost cpu_cost 
		'{' orig_node '}';

sort
	:	SORT (UNIQUE)?
		result_size
		disk_cost cpu_cost 
		'{' plan '}';

exchange_node
    :	EXCHANGE
		result_structure
		PAGES page_count TUPS row_count
		REDUCTION reduction_count
		THREADS thread_count
		disk_cost cpu_cost 
		'{' proj_rest '}';

reduction_count
	:	NUMBER;

thread_count
	:	NUMBER;

orig_node
	:	table_name  
		(INDEX_OF '(' base_table_name ')' )?
		('('correlation_name')' )?
		source_structure ('(' (not_used_flag | key_column_list) ')')?
		PAGES page_count TUPS row_count
		(PARTITIONS partition_count)?;

base_table_name
	:	table_name;

partition_count
	:	NUMBER;

not_used_flag
	:	NOT_USED;

source_structure	
	:	HEAP|CHEAP|B_TREE|CB_TREE|ISAM|CISAM|HASH|CHASH|HASHED; 

index_name
	:	name INDEX_OF '(' key_column_list ')';

table_name
	:	name;

correlation_name
	:	name;

name
	:	NAME			#SNAME				
	|	DELIMITED_NAME	#DNAME	
	|	keyword_as_name	#KNAME;

keyword_as_name
	:	CHECK_ONLY | CUNITS  | DUNITS  | EXCHANGE | FUNCATT  | 
		FSM   | FULL  | GREEDY  | HASH  | HASHED  | 
		HEAP  | INDEX_OF | ISAM  | JOIN  | KLOOKUP  | 
		LEFT  | MAIN  | NO   | NOT_USED | OF   | 
		ON   | OUT   | PAGES  | PARTITIONS | PLAN  | 
		PSM   | QUERY  | REDUCTION | RIGHT  | SORT  | 
		SORTED  | SORTU  | SQEXEC  | SUBQUERY | TEMPATT  | 
		TIDLOOKUP | TIMEOUT  | TIMED  | THREADS  | TUPS  | 
		UNION  | UNIQUE  | VIEW ;

/* DON'T DELETE THE LINE BELOW */
/* ex: set tabstop=4 shiftwidth=4 autoindent number ignorecase : */
