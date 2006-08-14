import compiler

from rope.pyobjects import *
import rope.codeanalyze


class ObjectInfer(object):

    def __init__(self):
        pass
    
    def _search_in_dictionary_for_attribute_list(self, names, attribute_list):
        pyobject = None
        if attribute_list[0] in names:
            pyobject = names.get(attribute_list[0]).get_object()
        if pyobject != None and len(attribute_list) > 1:
            for name in attribute_list[1:]:
                if name in pyobject.get_attributes():
                    pyobject = pyobject.get_attributes()[name].get_object()
                else:
                    pyobject = None
                    break
        return pyobject
        
    def infer_object(self, pyname):
        """Infers the `PyObject` this `PyName` references"""
        if not pyname.assigned_asts:
            return
        for assign_node in reversed(pyname.assigned_asts):
            try:
                lineno = assign_node.lineno
                if lineno is None:
                    lineno = 1
                holding_scope = pyname.module.get_scope().\
                                get_inner_scope_for_line(lineno)
                resulting_pyname = rope.codeanalyze.StatementEvaluator.\
                                   get_statement_result(holding_scope, assign_node)
                if resulting_pyname is None:
                    return None
                return resulting_pyname.get_object()
            except IsBeingInferredException:
                pass

