import time

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.type}({self.value})"
        return f"{self.type}"

def is_digit(c):
    return c.isdigit() or c == '.'

def lex(input_str):
    tokens = []
    i = 0
    while i < len(input_str):
        c = input_str[i]

        if c.isspace():
            i += 1
        elif is_digit(c):
            num = c
            i += 1
            while i < len(input_str) and is_digit(input_str[i]):
                num += input_str[i]
                i += 1
            tokens.append(Token("Number", float(num)))
        else:
            if c == '+':
                tokens.append(Token("Plus"))
            elif c == '-':
                tokens.append(Token("Minus"))
            elif c == '*':
                tokens.append(Token("Multiply"))
            elif c == '/':
                tokens.append(Token("Divide"))
            elif c == '(':
                tokens.append(Token("LeftParenthesis"))
            elif c == ')':
                tokens.append(Token("RightParenthesis"))
            else:
                raise ValueError(f"Token inválido: {c}")
            i += 1

    return tokens



class ASTNode:
    pass

class BinOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

def parse(tokens):
    def expression():
        return additive_expression()

    def additive_expression():
        left = multiplicative_expression()
        while len(tokens) > 0 and tokens[0].type in ('Plus', 'Minus'):
            operator = tokens.pop(0)
            right = multiplicative_expression()
            left = BinOpNode(operator.type, left, right)
        return left

    def multiplicative_expression():
        left = primary_expression()
        while len(tokens) > 0 and tokens[0].type in ('Multiply', 'Divide'):
            operator = tokens.pop(0)
            right = primary_expression()
            left = BinOpNode(operator.type, left, right)
        return left

    def primary_expression():
        if tokens[0].type == 'Number':
            return NumberNode(tokens.pop(0).value)
        elif tokens[0].type == 'LeftParenthesis':
            tokens.pop(0)  # Consume the '('
            expression_node = expression()
            if tokens[0].type != 'RightParenthesis':
                raise ValueError("Expected ')'")
            tokens.pop(0)  # Consume the ')'
            return expression_node
        raise ValueError("Invalid expression")

    return expression()

def evaluate(node):
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, BinOpNode):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.operator == 'Plus':
            return left + right
        elif node.operator == 'Minus':
            return left - right
        elif node.operator == 'Multiply':
            return left * right
        elif node.operator == 'Divide':
            if right == 0:
                raise ValueError("Division by zero")
            return left / right

def evaluate_with_ast(input_str):
    tokens = lex(input_str)
    ast = parse(tokens)
    result = evaluate(ast)
    return result

# Função que realiza a operação diretamente em Python
def evaluate_directly(input_str):
    result = eval(input_str)  # Avaliação direta da expressão
    return result

def main():
  input_str = "3.14 + 42 - (8 * 2) / 4.0"

  # Medição do tempo para o parser AST
  start_time_ast = time.time()
  result_ast = evaluate_with_ast(input_str)
  end_time_ast = time.time()
  time_elapsed_ast = end_time_ast - start_time_ast

  # Medição do tempo para avaliação direta em Python
  start_time_direct = time.time()
  result_direct = evaluate_directly(input_str)
  end_time_direct = time.time()
  time_elapsed_direct = end_time_direct - start_time_direct

  # Resultados e comparação
  print(f"Resultado do parser AST: {result_ast}")
  print(f"Tempo gasto com parser AST: {time_elapsed_ast:.6f} segundos")

  print(f"Resultado da avaliação direta em Python: {result_direct}")
  print(f"Tempo gasto com avaliação direta em Python: {time_elapsed_direct:.6f} segundos")




if __name__ == "__main__":
    main()