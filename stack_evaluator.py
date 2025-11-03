# stack_evaluator.py
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b

def evaluate(expression):
    values = Stack()
    ops = Stack()
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] == '(':
            ops.push(expression[i])
        elif expression[i].isdigit():
            val = 0
            while i < len(expression) and expression[i].isdigit():
                val = (val * 10) + int(expression[i])
                i += 1
            values.push(val)
            i -= 1
        elif expression[i] == ')':
            while not ops.is_empty() and ops.peek() != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            ops.pop()
        else:
            while (not ops.is_empty() and precedence(ops.peek()) >= precedence(expression[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            ops.push(expression[i])
        i += 1
    while not ops.is_empty():
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.push(apply_op(val1, val2, op))
    return values.pop()

def process_files(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line == '-----':
                outfile.write('-----\n')
                continue
            if line:
                try:
                    result = evaluate(line)
                    outfile.write(str(int(result)) + '\n')
                except Exception:
                    outfile.write('Error evaluating expression\n')
