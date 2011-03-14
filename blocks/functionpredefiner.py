from ast import parse, NodeTransformer
from blockfunctioncreator import BLOCK_FUNCTION_NAME


class FunctionPredefiner:
    def __init__(self, node):
        self.node = node

    def transform(self):
        return PredefinitionTransformer().visit(self.node)


class PredefinitionTransformer(NodeTransformer):
    def __init__(self, *args, **kwargs):
        self.block_function_call_expr = None
        super(PredefinitionTransformer, self).__init__(*args, **kwargs)

    def visit(self, node):
        return super(PredefinitionTransformer, self).visit(node)

    def visit_Expr(self, node):
        call_node = node.value
        is_a_block_call = call_node.args[0].id.startswith(BLOCK_FUNCTION_NAME)
        if is_a_block_call:
            self.block_function_call_expr = node
            return self.removed_node()
        else:
            return self.generic_visit(node)

    def removed_node(self):
        return None

    def visit_FunctionDef(self, node):
        if self.block_function_call_expr:
            new_node = self._definition_before_call(node)
            self.block_function_call_expr = None
            return new_node
        else:
            return self.generic_visit(node)

    def _definition_before_call(self, definition_node):
        call = self.block_function_call_expr.value
        return (PredefinitionTransformer().visit(definition_node),
                self.block_function_call_expr)

