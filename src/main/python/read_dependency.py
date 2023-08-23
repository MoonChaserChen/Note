import sys
import getopt
import os
import re
from typing import List


class Dependency:
    level = 0
    group = ""
    artifact = ""
    arti_type = ""
    version = ""
    scope = ""

    def __init__(self, level, group, artifact, arti_type, version, scope):
        # 依赖树层级，从0开始
        self.level = level
        self.group = group
        self.artifact = artifact
        self.arti_type = arti_type
        self.version = version
        self.scope = scope

    def __eq__(self, other):
        return self.group == other.group and self.artifact == other.artifact

    def __hash__(self):
        return hash((self.group, self.artifact))


class DependencyTree:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, from_: Dependency, to: Dependency):
        if from_ not in self.dependencies:
            self.dependencies[from_] = set()
        self.dependencies[from_].add(to)

    def remove_redundant_dependencies(self):
        """
        已知依赖树，需要移除依赖树中的多余部分。
        例如依赖树（A->B, B->C, A->C）中A->C就为多余部分，因为依赖具有传递性，知道了A->B及B->C就可推导出A->C。
        (A->B表示A依赖B)
        :return:
        """
        for from_ in self.dependencies:
            to_remove = set()
            for to in self.dependencies[from_]:
                # 如果从from_的其它子节点能到to，则表明当前from_到to是多余的
                other_nodes = self.dependencies[from_].copy()
                other_nodes.remove(to)
                for other_from in other_nodes:
                    if self.dfs(other_from, to, set()):
                        to_remove.add(to)
            self.dependencies[from_] -= to_remove

    def dfs(self, from_, target, visited):
        if from_ not in self.dependencies or from_ in visited:
            return False
        visited.add(from_)
        for to in self.dependencies[from_]:
            if to == target or self.dfs(to, target, visited):
                return True
        return False

    def print_dependencies(self):
        for from_ in self.dependencies:
            for to in self.dependencies[from_]:
                print(f'{from_.artifact} -> {to.artifact}')


def execute_mvn_command():
    """
    执行 mvn dependency:tree 命令获取依赖树
    :return: 以数组的形式保存每行的内容，每行的内容大致如下：
    [INFO] +- org.apereo.cas:cas-server-core-api-configuration-model:jar:6.6.9:compile
    """
    options, args = getopt.getopt(sys.argv[1:], "", ["grep="])
    grep_text = None
    for k, v in options:
        if k == "--grep":
            grep_text = v
    text = os.popen("mvn dependency:tree -Dverbose=true")
    result = []
    for line in text.readlines():
        if not grep_text or grep_text in line:
            result.append(line)
    return result


def parse_mvn_dependency(lines):
    """
    解析mvn依赖树，转换成Dependency对象
    :param lines: 以行形式保存的依赖树，可由executeMvnCommand方法生成
    :return: Dependency数组对象
    """
    reg = re.compile(r"(\[\w+\] )(.+ )\(?(.+):(.+):(.+):(.+):(\w+)")
    result = []
    for line in lines:
        m_r = reg.match(line)
        if m_r:
            dependency = Dependency(len(m_r.group(2)) // 3 - 1, m_r.group(3), m_r.group(4), m_r.group(5), m_r.group(6), m_r.group(7))
            result.append(dependency)
    return result


def gen_graphviz(dependencies: List[Dependency]):
    """
    将依赖树转换成graphviz内容
    :param dependencies: 依赖树对象，可由parseMvnDependency方法生成
    :return:
    """
    result = "digraph G {\n"
    for i in range(len(dependencies) - 1):
        for j in range(i + 1, len(dependencies)):
            if dependencies[i].level + 1 == dependencies[j].level:
                text = '\t"{}" -> "{}"\n'.format(dependencies[i].artifact, dependencies[j].artifact)
                result += text
            elif dependencies[i].level == dependencies[j].level:
                break
    result += "}"
    return result


def gen_purify_graphviz(dependencies: List[Dependency]):
    """
    将依赖树转换成graphviz内容（会移除冗余依赖）
    :param dependencies: 依赖树对象，可由parseMvnDependency方法生成
    :return:
    """

    # 有依赖的成树，输出成 A -> B 的形式
    tree = DependencyTree()
    # 没依赖的单独保存，直接输出成 A 的形式，在graphviz上呈现单独的节点
    single_dependencies = []
    for i in range(len(dependencies)):
        has_child = False
        for j in range(i + 1, len(dependencies)):
            if dependencies[i].level + 1 == dependencies[j].level:
                has_child = True
                tree.add_dependency(dependencies[i], dependencies[j])
            elif dependencies[i].level == dependencies[j].level:
                if dependencies[i].level == 0 and not has_child:
                    single_dependencies.append(dependencies[i])
                break
        if i == len(dependencies) - 1 and dependencies[i].level == 0:
            single_dependencies.append(dependencies[i])
    tree.remove_redundant_dependencies()

    result = "digraph G {\n"
    for node in single_dependencies:
        result += f'\t"{node.artifact}"\n'
    for node in tree.dependencies:
        for next_node in tree.dependencies[node]:
            text = f'\t"{node.artifact}" -> "{next_node.artifact}"\n'
            result += text
    result += "}"
    return result


# 将指定的项目依赖关系生成graphviz图像
# 命令示例：python /Users/akira/Desktop/read_dependency.py --grep=cas-server
d = parse_mvn_dependency(execute_mvn_command())
r = gen_purify_graphviz(d)
print(r)
