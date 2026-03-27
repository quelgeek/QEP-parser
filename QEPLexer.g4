/* proof-of-concept ANTLR 4 lexer to parse "Lisp format" Ingres QEPs  */
/* roy.hann@rationalcommerce.com */
/* pretty rough-and-ready but good enough to prove that Lisp format QEPs can be parsed */

lexer grammar QEPLexer;

QEP_LABEL	:	'QUERY PLAN' ~[|]+;

AGGREGATE	:	[Aa][Gg][Gg][Rr][Ee][Gg][Aa][Tt][Ee];
B_TREE		:	[Bb]'-'[Tt][Rr][Ee][Ee];
CB_TREE		:	[Cc][Bb]'-'[Tt][Rr][Ee][Ee];
CHASH		:	[Cc][Hh][Aa][Ss][Hh];
CHEAP		:	[Cc][Hh][Ee][Aa][Pp];
CISAM		:	[Cc][Ii][Ss][Aa][Mm];
CHECK_ONLY	:	[Cc][Oo];
CUNITS		:	'C'[0-9]+;
DUNITS		:	'D'[0-9]+;
EXCHANGE	:	[Ee][Xx][Cc][Hh][Aa][Nn][Gg][Ee];
EXPRESSION	:	[Ee][Xx][Pp][Rr][Ee][Ss][Ss][Ii][Oo][Nn];
FUNCATT		:	'FA'[0-9]+;
FSM			:	[Ff][Ss][Mm];
FULL		:	[Ff][Uu][Ll][Ll];
GREEDY		:	[Gg][Rr][Ee][Ee][Dd][Yy];
HASH		:	[Hh][Aa][Ss][Hh];
HASHED		:	[Hh][Aa][Ss][Hh][Ee][Dd];
HEAP		:	[Hh][Ee][Aa][Pp];
INDEX_OF	:	[Ii];
ISAM		:	[Ii][Ss][Aa][Mm];
JOIN		:	[Jj][Oo][Ii][Nn];
KLOOKUP		:	[Kk];
LEFT		:	[Ll][Ee][Ff][Tt];
MAIN		:	[Mm][Aa][Ii][Nn];
NO			:	[Nn][Oo];
NOT_USED	:	'NU';	/* upper-case only */
OF			:	[Oo][Ff];
ON			:	[Oo][Nn];
OUT			:	[Oo][Uu][Tt];
PAGES		:	[Pp][Aa][Gg][Ee][Ss];
PARTITIONS	:	[Pp][Aa][Rr][Tt][Ii][Tt][Ii][Oo][Nn][Ss];
PLAN		:	[Pp][Ll][Aa][Nn];
PROJ_REST	:	[Pp][Rr][Oo][Jj]'-'[Rr][Ee][Ss][Tt];
PSM			:	[Pp][Ss][Mm];
QUERY		:	[Qq][Uu][Ee][Rr][Yy];
REDUCTION	:	[Rr][Ee][Dd][Uu][Cc][Tt][Ii][Oo][Nn];
RIGHT		:	[Rr][Ii][Gg][Hh][Tt];
SIMPLE		:	[Ss][Ii][Mm][Pp][Ll][Ee];
SORT		:	[Ss][Oo][Rr][Tt];
SORTED		:	[Ss][Oo][Rr][Tt][Ee][Dd];
SORTU		:	[Ss][Oo][Rr][Tt][Uu];
SQEXEC		:	[Ss][Ee];
SUBQUERY	:	[Ss][Uu][Bb][Qq][Uu][Ee][Rr][Yy];
TEMPATT		:	[Tt][0-9]+[Aa][0-9]+;
TIDLOOKUP	:	[Tt];
TIMEOUT		:	[Tt][Ii][Mm][Ee][Oo][Uu][Tt];
TIMED		:	[Tt][Ii][Mm][Ee][Dd];
THREADS		:	[Tt][Hh][Rr][Ee][Aa][Dd][Ss];
TUPS		:	[Tt][Uu][Pp][Ss];
UNION		:	[Uu][Nn][Ii][Oo][Nn];
UNIQUE		:	[Uu][Nn][Ii][Qq][Uu][Ee];
VIEW		:	[Vv][Ii][Ee][Ww];

PRODUCING	:	'->';

NUMBER		:	[0-9]+;

NAME
			:	(LETTER|'_')(LETTER|'0'..'9'|'_'|'#'|'$')*;	

fragment
LETTER
			:	[A-Z]|[a-z];

DELIMITED_NAME
			:	'"' ( '""' | ~('"') )* '"';

WS			:	(' '|'\r'|'\n'|'\t')+ -> skip;

/* DON'T DELETE THE LINE BELOW */
/* ex: set tabstop=4 shiftwidth=4 autoindent number ignorecase : */
