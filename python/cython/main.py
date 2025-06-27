from dis import Bytecode

src = """\
22
333
__dataclass_fields__: ClassVar
"""

code = compile(src, "<string>", "exec")
print(code.co_consts)
annotate_code = code.co_consts[1]

for bc in Bytecode(annotate_code):
    print(bc.positions, bc.opname)