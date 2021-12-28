'''Module containing all tokens and classes needed to tokenize expressions.

:data TOKEN_REGEX: Regular Expression used for extracting specific token characters.
:type TOKEN_REGEX: Pattern'''

import re
from abc import ABC, abstractmethod
from typing import List, Pattern
from math import e, pi, sin, cos, tan, log

class Token(ABC):

    '''Token Abstract Base Class.'''

    def __init__(self, stack: List):
        self._stack = stack

    @abstractmethod
    def execute(self):
        '''Execute the function.'''
        pass

    @property
    def precedence(self):
        '''Precedence of a token.'''
        try:
            return self.__class__.PRECEDENCE
        except NameError: # If value isn't set
            return -1

class VariableToken(Token):

    '''Variable token.'''

    def execute(self, value: float):
        '''Push given value to top of stack.

        :param value: What value to push.
        :type value: float'''
        self._stack.append(value)

class ValueToken(Token):

    '''Token representing a number.'''

    def __init__(self, stack: List, value: float):
        super().__init__(stack)
        self.__value = value

    def execute(self):
        '''Push value to top of stack.'''
        self._stack.append(self.__value)

class PiToken(ValueToken):

    '''Token for the number pi.'''

    def __init__(self, stack: List):
        super().__init__(stack, pi)

class EulerToken(ValueToken):

    '''Token for the number e.'''

    def __init__(self, stack: List):
        super().__init__(stack, e)

class BinaryToken(Token):

    '''Binary Operation token.'''

    @abstractmethod
    def operation(self, a, b):
        '''What operation to execute.'''
        pass

    def execute(self):
        '''Pop two items from the stack, run an operation on them,\
            and push the result to the stack.'''
        b = self._stack.pop()
        a = self._stack.pop()
        result = self.operation(a, b)
        self._stack.append(result)

class AddToken(BinaryToken):

    '''Addition token.'''

    PRECEDENCE = 1

    def operation(self, a, b):
        '''Add a and b'''
        return a + b

class SubtractToken(BinaryToken):

    '''Subtraction token.'''

    PRECEDENCE = 1

    def operation(self, a, b):
        '''Subtract a and'''
        return a - b

class MultiplyToken(BinaryToken):

    '''Multiplication token.'''

    PRECEDENCE = 2

    def operation(self, a, b):
        '''Multiply a and b'''
        return a * b

class DivideToken(BinaryToken):

    '''Division token.'''

    PRECEDENCE = 2

    def operation(self, a, b):
        '''Divide a and b.'''
        return a / b

class PowerToken(BinaryToken):

    '''Exponation token.'''

    PRECEDENCE = 3

    def operation(self, a, b):
        '''Exponate a to the power of b'''
        return a ** b

class FunctionToken(Token):

    '''Token representing a unary function.'''

    @abstractmethod
    def operation(self, a):
        pass

    def execute(self):
        '''Pop an item from the stack, run a function on it,\
            and push the result to the stack.'''
        a = self._stack.pop()
        result = self.operation(a)
        self._stack.append(result)

class SinToken(FunctionToken):

    '''Sine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run sin'''
        return sin(a)

class CosToken(FunctionToken):

    '''Cosine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run cosine'''
        return cos(a)

class TanToken(FunctionToken):

    '''Tangent token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run tangent'''
        return tan(a)

class LogToken(FunctionToken):

    '''Logarithm token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run logarithm base 10.'''
        return log(a)

class TokenBuilder:

    '''Build tokens.'''

    def __init__(self, stack: List):
        self._stack = stack

    def build_value(self, value: float):
        '''Build a value token.'''
        return ValueToken(self._stack, value)

    def build_add(self):
        '''Build an add token.'''
        return AddToken(self._stack)

    def build_subtract(self):
        '''Build a subtract token.'''
        return SubtractToken(self._stack)

    def build_multiply(self):
        '''Build a multiply token.'''
        return MultiplyToken(self._stack)

    def build_divide(self):
        '''Build a divide token.'''
        return DivideToken(self._stack)

    def build_power(self):
        '''Build a power token.'''
        return PowerToken(self._stack)

    def build_pi(self):
        '''Build a pi token.'''
        return PiToken(self._stack)

    def build_e(self):
        '''Build an e token.'''
        return EulerToken(self._stack)

    def build_sin(self):
        '''Build a sin token.'''
        return SinToken(self._stack)

    def build_cos(self):
        '''Build a cos token.'''
        return CosToken(self._stack)

    def build_tan(self):
        '''Build a tan token.'''
        return TanToken(self._stack)

    def build_log(self):
        '''Build a log token.'''
        return LogToken(self._stack)

    def build_x(self):
        '''Build a variable token.'''
        return VariableToken(self._stack)

TOKEN_REGEX:Pattern[str] = re.compile(r"\d+\.?\d*|\+|-|\*|/|\)|\^|tan\(|cos\(|sin\(|log\(|pi|e|x|\(")

class TokenStream:

    '''A read-only representation of a stream of strings representing individual tokens.

    :property text: The infix represenetation of the full expression.
    :type text: str'''

    def __init__(self, expression: str):
        self.__expression: List[str] = TOKEN_REGEX.findall(expression)
        self.__iteration = 0

    @property
    def text(self) -> str:
        '''The infix representation of the full expression.'''
        return "".join(self.__expression)

    def reset(self):
        '''Reset the stream to the beginning.'''
        self.__iteration = 0

    def __iter__(self): 
        return self

    def __next__(self):
        if self.__iteration < len(self.__expression):
            value = self.__expression[self.__iteration]
            self.__iteration += 1
            return value
        raise StopIteration

    def __str__(self):
        return self.text