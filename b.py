from enum import IntEnum
class op(IntEnum):
	HALT = 0
	PUSH = 1
	ADD = 2
	SUB = 3
	MUL = 4
	DIV = 5
	STORE = 6
	LOAD = 7
	EQ = 8
	NEQ = 9
	GT = 10
	GTE = 11
	LT = 12
	LTE = 13
	JUMP = 14
	JUMP_IF_FALSE = 15
