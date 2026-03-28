import sys
from antlr4 import *
from QueryPlanLexer import QueryPlanLexer
from QueryPlanParser import QueryPlanParser
from QueryPlanVisitor import QueryPlanVisitor


class QueryPlanAnalyzer(QueryPlanVisitor):

    def visitOrig_node(self, ctx):
            table_name = ctx.table_name().getText()
            correlation_name = ctx.correlation_name().getText()
            print(f'{table_name} referenced as {correlation_name}')
            if ctx.not_used_flag():
                print('\tbase table strucuture not used')


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = QueryPlanLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = QueryPlanParser(stream)
    
    qep_parse_tree = parser.qep()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
        quit()

    analyzer = QueryPlanAnalyzer()
    analyzer.visit(qep_parse_tree)


if __name__ == '__main__':
    main(sys.argv)
