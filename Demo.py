import sys 
from antlr4 import *
from QueryPlanLexer import QueryPlanLexer
from QueryPlanParser import QueryPlanParser
from QueryPlanVisitor import QueryPlanVisitor


class QEP():

    def __init__(self,label):
        self.label = label
        self.orig_nodes = []
        self.projrest_nodes = []
        self.join_nodes = []
        self.sort_nodes = []
        self.exchange_nodes = []
        self.edges = []


    def as_dot(self):
        dot = [
            'digraph QEP',
            '{',
            '\tgraph',
            '\t[',
            '\t\tranksep=.25;',
            '\t\trankdir="RL"',
            '\t\tlabelloc="t"',
            '\t\tlabeljust="l"',
            '\t\tfontname="Courier"',
            '\t\tfontsize=10',
            '\t\tordering="in"',
            f'\t\tlabel="{self.label}"',
            '\t];',
            '',
            '\tedge [arrowsize=.5 dir="back"];',
            '',
            '\tnode [shape=rectangle,fontname="Courier",fontsize=8,height=.45];'
            '\n'
            ]
            
        for node in self.orig_nodes:
            dot += node.as_dot()

        for node in self.projrest_nodes:
            dot += node.as_dot()

        for node in self.join_nodes:
            dot += node.as_dot()

        for node in self.exchange_nodes:
            dot += node.as_dot()

        for node in self.sort_nodes:
            dot += node.as_dot()

        for edge in self.edges:
            dot += edge.as_dot()

        dot += '}'

        return dot


    def __str__(self):
        '''return Graphviz DOT script for the QEP'''
        dot = self.as_dot()
        return '\n'.join(dot)


class QEPNode():

    discriminator = 0
    nodeNamePrefix = 'XX'

    def __init__(self):
        nodeName = f'{self.nodeNamePrefix}{QEPNode.discriminator}'
        QEPNode.discriminator += 1
        self.nodeName = nodeName


    def as_dot(self):
        raise NotImplementedError


class OrigNode(QEPNode):

    nodeNamePrefix = 'ON'


    def __init__(self):
        super().__init__()
        self.table_name = None
        self.correlation_name = None
        self.page_count = None
        self.row_count = None    
        self.index = ''
        self.source_structure = None
        self.physical_key = ''
        self.T_join_inner_source = False


    def as_dot(self):
        '''return Graphviz DOT representation of the orig node'''

        if self.correlation_name:
            correlation = f'referenced as {self.correlation_name}'
        else:
            correlation = ''
        if self.T_join_inner_source:
            self.physical_key = f'(not used; accessed by TID)'
        if self.page_count == '1':
            pages = '1 page'
        else:
            pages = f'{self.page_count} pages'
        if self.row_count == '1':
            rows = '1 row'
        else:
            rows = f'{self.row_count} rows'

        dot = [
            f'\t"{self.nodeName}"',
            '\t[',
            '\t\tshape=cylinder, label=',
            '\t\t<',
            '\t\t\t<TABLE BORDER="0" CELLSPACING="0">',
            '\t\t\t\t<TR><TD>&nbsp;</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'<B>{self.index}{self.table_name}</B></TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'{correlation}</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'{self.source_structure} {self.physical_key}</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'Approximate size: {pages}, {rows}</TD></TR>',
            '\t\t\t</TABLE>',
            '\t\t>',
            '\t];'
            '\n'
        ]

        return dot


class ProjRestNode(QEPNode):
    '''return Graphviz DOT representation of the proj-rest node'''

    nodeNamePrefix = 'PR'


    def __init__(self):
        super().__init__()
        self.page_count = None
        self.row_count = None    


    def as_dot(self):
        '''return Graphviz DOT representation of the proj-rest node'''

        if self.page_count == '1':
            pages = '1 page'
        else:
            pages = f'{self.page_count} pages'
        if self.row_count == '1':
            rows = '1 row'
        else:
            rows = f'{self.row_count} rows'

        dot = [
            f'\t"{self.nodeName}"',
	        '\t[',
		    '\t\tstyle=filled,fillcolor="WHITESMOKE",label=',
		    '\t\t<',
            '\t\t\t<TABLE BORDER="0" CELLSPACING="0">',
			'\t\t\t\t<TR><TD ALIGN="CENTER">'
                '<B>PROJECT &amp; RESTRICT</B>'
                '</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'{self.result_structure}</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted result size:   </TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {pages} pages</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {rows} rows</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted cost:</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.dios} DIOs</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.cpu} CPU</TD></TR>',
		    '\t\t\t</TABLE>',
		    '\t\t>',
	        '\t];'
            '\n'
        ]

        return dot


class JoinNode(QEPNode):
    '''return Graphviz DOT representation of the join node'''

    nodeNamePrefix = 'JN'


    def __init__(self):
        super().__init__()
        self.outer_join = ''
        self.join_technique = None
        self.key_column_list = []
        self.result_key_components = []
        self.result_structure = 'Heap'
        self.page_count = None
        self.row_count = None    
        self.disk_cost = None
        self.cpu_cost = None


    def as_dot(self):
        '''return Graphviz DOT representation of the join node'''

        fill_colors = {
            "T": "WHITESMOKE",
            "Hash": "HONEYDEW",
            "FSM": "HONEYDEW",
            "PSM": "MINTCREAM",
            "K": "IVORY",
            "SE": "MISTYROSE" }

        fillcolor = fill_colors[self.join_technique]
        disk_cost = self.disk_cost[1:]
        cpu_cost = self.cpu_cost[1:]
        result_structure = (
            self.result_structure + '(' +
            ','.join(self.result_key_components) +
            ')' )

        dot = [
            f'\t"{self.nodeName}"',
            '\t[',
            f'\t\tstyle=filled,fillcolor="{fillcolor}",label=',
		    '\t\t<',
            '\t\t\t<TABLE BORDER="0" CELLSPACING="0">',
			f'\t\t\t\t<TR><TD ALIGN="CENTER"><B>{self.outer_join} '
                f'{self.join_technique} join</B></TD></TR>',
            f'\t\t\t\t<TR><TD ALIGN="LEFT">Key({self.key_column_list})</TD></TR>',
            f'\t\t\t\t<TR><TD ALIGN="LEFT">{result_structure}</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted result size:   </TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.page_count} pages</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.row_count} rows</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted cost:</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {disk_cost} DIOs</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {cpu_cost} CPU</TD></TR>',
		    '\t\t\t</TABLE>',
		    '\t\t>',
	        '\t];'
            '\n'
        ]        

        return dot


class ExchangeNode(QEPNode):

    nodeNamePrefix = 'EN'

    def __init__(self):
        super().__init__()
        self.result_structure = ''
        self.page_count = 0
        self.row_count = 0
        self.reduction = 0
        self.thread_count = 0
        self.disk_cost = ''
        self.cpu_cost = ''


    def as_dot(self):
        '''return Graphviz DOT representation of the exchange node'''

        dot = [
            f'\t"{self.nodeName}"',
            '\t[',
            f'\t\tlabel=',
		    '\t\t<',
            '\t\t\t<TABLE BORDER="0" CELLSPACING="0">',
			f'\t\t\t\t<TR><TD ALIGN="CENTER"><B>EXCHANGE</B></TD></TR>',
			f'\t\t\t\t<TR><TD ALIGN="LEFT">{self.result_structure}</TD></TR>',
			f'\t\t\t\t<TR><TD ALIGN="LEFT">{self.reduction} reduction</TD></TR>',
			f'\t\t\t\t<TR><TD ALIGN="LEFT">{self.thread_count} threads</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted result size:   </TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.page_count} pages</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.row_count} rows</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted cost:</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.disk_cost} DIOs</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.cpu_cost} CPU</TD></TR>',
		    '\t\t\t</TABLE>',
		    '\t\t>',
	        '\t];'
            '\n'
        ]        

        return dot


class SortNode(QEPNode):

    nodeNamePrefix = 'ST'

    def __init__(self):
        super().__init__()
        self.unique = False
        self.page_count = 0
        self.row_count = 0
        self.disk_cost = ''
        self.cpu_cost = ''


    def as_dot(self):
        '''return Graphviz DOT representation of the sort node'''

        sort = 'Sort Unique' if self.unique else 'Sort'

        dot = [
            f'\t"{self.nodeName}"',
            '\t[',
            f'\t\tstyle=filled,fillcolor="WHITESMOKE",label=',
		    '\t\t<',
            '\t\t\t<TABLE BORDER="0" CELLSPACING="0">',
			f'\t\t\t\t<TR><TD ALIGN="CENTER"><B>{sort}</B></TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted result size:   </TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.page_count} pages</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.row_count} rows</TD></TR>',
			'\t\t\t\t<TR><TD ALIGN="LEFT">Predicted cost:</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.disk_cost} DIOs</TD></TR>',
            '\t\t\t\t<TR><TD ALIGN="LEFT">'
                f'   {self.cpu_cost} CPU</TD></TR>',
		    '\t\t\t</TABLE>',
		    '\t\t>',
	        '\t];'
            '\n'
        ]        

        return dot


class QEPEdge():

    def __init__(self, sink, source):
        self.sink = sink
        self.source = source

    def as_dot(self):
        dot = [f'\t"{self.sink.nodeName}" -> "{self.source.nodeName}";']
        return dot


class QueryPlanVisualizer(QueryPlanVisitor):

    def visitQep(self, ctx):
        '''generate a Dot script to draw the QEP'''


        qep_label = ctx.QEP_LABEL().getText().rstrip()
        self.qep = QEP(qep_label)

        self.visit(ctx.plan())
        
        dot_script = self.qep.as_dot()
        return dot_script


    def visitJoin(self, ctx):

        outer_source = self.visit(ctx.plan(0))
        inner_source = self.visit(ctx.plan(1))

        node = JoinNode()
        try:
            node.outer_join = ctx.outer_join().getText()
        except AttributeError:
            pass
        node.join_technique = ctx.join_technique().getText()
        if ctx.key_column_list():
            # node.key_column_list = self.visit(ctx.key_column_list())
            node.key_column_list = ctx.key_column_list().getText()

        if not ctx.result_structure():
            pass
        elif ctx.result_structure().nonheap():
            nonheap = ctx.result_structure().nonheap().getText()
            if ctx.result_structure().not_used_flag():
                node.result_key_components.append('NU')
            else:
                # pull out each of the key components because we want to
                # highlight any function attributes (FAn) in red
                result_key = ctx.result_structure().result_key()
                key_components = [result_key.result_key_component(i)
                    for i in range(result_key.getChildCount())
                    if result_key.result_key_component(i)]
                for key_component in key_components:
                    if key_component.function_attribute():
                        FAname = key_component.function_attribute().getText()
                        name = key_component.name().getText()
                        key_name = ( 
                            '<font color="RED">'
                            f'{FAname} {name}'
                            '</font>' )
                    elif key_component.intermediate_attribute():
                        IAname = key_component.intermediate_attribute().getText()
                        name = key_component.name().getText()
                        key_name = f'{IAname} {name}'
                    else:
                        key_name = key_component.name().getText()
                    node.result_key_components.append(key_name)
        else:
            node.result_structure = ctx.result_structure().getText()

#        try:
#            # node.result_structure = ctx.result_structure().getText() # <- FIX ME
#            
#            node.result_structure = ctx.result_structure().getText() # <- FIX ME
#            breakpoint()
#            rs = ctx.result_structure()
#            rk = rs.result_key()
#            components = [rk.result_key_component(i)
#                for i in range(rk.getChildCount())]
#            for component in components:
#                prefix = ''
#                if component.function_attribute():
#                    FAname = component.function_attribue().getText()
#                    prefix = '<font color="RED">' + FAname + ' ' + '</font>'
#                component_name = prefix + component.name().getText()
#        except AttributeError:
#            pass


        node.page_count = ctx.result_size().page_count().getText()
        node.row_count = ctx.result_size().row_count().getText()
        node.disk_cost = ctx.disk_cost().getText()
        node.cpu_cost = ctx.cpu_cost().getText()

        edge = QEPEdge(sink=node,source=outer_source)
        self.qep.edges.append(edge)
        edge = QEPEdge(sink=node,source=inner_source)
        self.qep.edges.append(edge)

        self.qep.join_nodes.append(node)

        return node


    def visitResult_size(self, ctx):
        '''emit predicted result set size'''

        page_count = ctx.page_count().getText()
        fragment = f'Predicted result size: {page_count} '
        if page_count == '1':
            fragment += 'page, '
        else:
            fragment += 'pages, '

        row_count = ctx.row_count().getText()
        fragment += row_count
        if row_count == '1':
            fragment += ' row'
        else:
            fragment += ' rows'

        #self.fragments.append(fragment)



    def visitKey_column_list(self, ctx):
        '''emit key column name list'''

        msg = 'entered visitKey_column_list ' + ctx.getText()
        column_names = [child.name().getText()
            for child in ctx.children
            if child is QueryPlanParser.Key_column_nameContext]
        key_column_list = ', '.join(column_names)
        return key_column_list

    
    def visitResult_structure(self, ctx):
        '''gather attributes of result structure'''

        result_structure = ctx.getText()


    def visitProj_rest(self, ctx):
        '''gather attributes of project-restrict operation'''


        try:
            result_structure = ctx.result_structure().getText() # <-- FIX ME
        except AttributeError:
            result_structure = 'Heap'
        page_count = ctx.result_size().page_count().getText()
        row_count = ctx.result_size().row_count().getText()
        dios = int(ctx.disk_cost().getText()[1:])
        cpu = int(ctx.cpu_cost().getText()[1:])

        node = ProjRestNode()
        node.result_structure = result_structure
        node.page_count = page_count
        node.row_count = row_count
        node.dios = dios
        node.cpu = cpu
        
        orig_node = self.visit(ctx.orig_node())
        edge = QEPEdge(sink=node,source=orig_node)

        self.qep.projrest_nodes.append(node)
        self.qep.edges.append(edge)


        return node


    def visitSort(self, ctx):
        '''gather attributes of sort node'''


        page_count = ctx.page_count().getText()
        row_count = ctx.row_count().getText()
        disk_cost = int(ctx.disk_cost().getText()[1:])
        cpu_cost = int(ctx.cpu_cost().getText()[1:])
        try: 
            if ctx.UNIQUE():
                unique = True
        except AttributeError:
            unique = False

        node = SortNode()
        node.unique = unique
        node.page_count = page_count
        node.row_count = row_count
        node.disk_cost = disk_cost
        node.cpu_cost = cpu_cost

        source = self.visit(ctx.plan())
        edge = QEPEdge(sink=node,source=source)

        self.qep.sort_nodes.append(node)
        self.qep.edges.append(edge)


        return node


    def visitExchange_node(self,ctx):
        '''gather attributes of exchange node'''

        try:
            result_structure = ctx.result_structure().getText() # <-- FIX ME
        except AttributeError:
            result_structure = 'Heap'
        page_count = ctx.page_count().getText()
        row_count = ctx.row_count().getText()
        disk_cost = int(ctx.disk_cost().getText()[1:])
        cpu_cost = int(ctx.cpu_cost().getText()[1:])
        reduction = ctx.reduction().getText()
        thread_count = ctx.thread_count().getText()

        node = ExchangeNode()
        node.result_structure = result_structure
        node.page_count = page_count
        node.row_count = row_count
        node.disk_cost = disk_cost
        node.cpu_cost = cpu_cost
        node.reduction = reduction
        node.thread_count = thread_count
        
        source = self.visit(ctx.plan())
        edge = QEPEdge(sink=node,source=source)

        self.qep.exchange_nodes.append(node)
        self.qep.edges.append(edge)
        
        return node


    def visitOrig_node(self, ctx):

        def is_T_join_input(ctx):
            '''return True if orig-node is inner source for T-join, else False'''
            
            try:
                grandparent = ctx.parentCtx.parentCtx
                join_technique = grandparent.join_technique().getText()
            except AttributeError:
                join_technique = None
            T_join_input = True if join_technique == 'T' else False

            return T_join_input



        table_name = ctx.table_name().getText()
        index = 'SECONDARY INDEX ' if ctx.INDEX_OF() else ''
        try:
            correlation_name = ctx.correlation_name().getText()
        except AttributeError:
            correlation_name = ''
        T_join_inner_source = is_T_join_input(ctx)
        source_structure = ctx.source_structure().getText()
        page_count = ctx.page_count().getText()
        row_count = ctx.row_count().getText()

        node = OrigNode()
        node.table_name = table_name
        node.index = index
        node.correlation_name = correlation_name
        node.T_join_inner_source = T_join_inner_source
        node.source_structure = source_structure
        node.page_count = page_count
        node.row_count = row_count

        try:
            node.physical_key = ctx.physical_key().getText()
        except AttributeError:
            pass

        self.qep.orig_nodes.append(node)
        
        return node


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = QueryPlanLexer(input_stream)
    stream = CommonTokenStream(lexer)
    
    parser = QueryPlanParser(stream)
    qep_parse_tree = parser.qep()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
        quit()

    visualizer = QueryPlanVisualizer()
    visualizer.visitQep(qep_parse_tree)
    qep = visualizer.qep
    print(qep)


if __name__ == '__main__':
    main(sys.argv)
