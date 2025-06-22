import tree_sitter_java
import tree_sitter_kotlin
from tree_sitter import Language, Parser

# 加载Language对象
Java_LANGAUGE = Language(tree_sitter_java.language())
KOTLIN_LANGAUGE = Language(tree_sitter_kotlin.language())

# 创建Parser并配置语言
java_parser = Parser(Java_LANGAUGE)
kotlin_parser = Parser(KOTLIN_LANGAUGE)

# 准备用于解析的代码段
java_code_snippet = '''
'''


# 进行解析
tree = java_parser.parse(
	bytes(
		java_code_snippet, "utf-8"
	)
)

# 获取AST的节点
root_node = tree.root_node

# 遍历AST
cursor = tree.walk()


def traverse(cursor):
    node = cursor.node
    # 处理当前节点
    print(node.type+" : "+ node.text.decode("utf-8"))

    # 如果有子节点，进入第一个子节点并递归遍历
    if cursor.goto_first_child():
        traverse(cursor)
        # 遍历完子节点后，返回父节点
        cursor.goto_parent()

    # 如果有兄弟节点，移动到下一个兄弟节点并递归遍历
    if cursor.goto_next_sibling():
        traverse(cursor)

traverse(cursor)
