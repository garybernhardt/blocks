from ast import parse, NodeTransformer
from blockfunctioncreator import BLOCK_FUNCTION_NAME


class FunctionPredefiner:
    def __init__(self, node):
        self.node = node

    def transform(self):
        return PredefinitionTransformer().visit(self.node)


class PredefinitionTransformer(NodeTransformer):
    def visit_Expr(self, node):
        self.block_function_call_expr = node
        return None

    def visit_FunctionDef(self, node):
        return self._definition_before_call(node)

    def _definition_before_call(self, definition_node):
        return (definition_node, self.block_function_call_expr)

