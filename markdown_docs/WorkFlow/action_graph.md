## ClassDef ActionGraph
Doc is waiting to be generated...
### FunctionDef __init__(self)
**__init__**: __init__函数的功能是初始化ActionGraph对象的属性。

**参数**:
· 无参数

**代码描述**:
在这个函数中，初始化了ActionGraph对象的三个属性：nodes，edges和execution_order。其中，nodes是一个空字典，用于存储图中的节点；edges也是一个空字典，用于存储图中的边；execution_order是一个空列表，用于存储节点的执行顺序。

**注意**:
在使用ActionGraph对象时，可以通过调用__init__函数来初始化对象的属性，以便后续对图的操作和处理。
***
### FunctionDef add_node(self, node)
**add_node**: add_node函数的功能是将一个节点添加到图中。
**parameters**:
· node: 要添加到图中的节点对象。
**Code Description**:
这个add_node函数接受一个节点对象作为参数，并将该节点添加到图中。在函数内部，通过节点的key作为键，将节点对象存储在self.nodes字典中。这样可以方便地通过节点的key来访问和操作节点对象。
**Note**:
- 在调用add_node函数时，确保传入的参数是一个有效的节点对象。
- 添加节点后，可以通过self.nodes来访问和管理已添加的节点。
***
### FunctionDef add_edge(self, from_node, to_node)
**add_edge**: add_edge函数的作用是向图中添加一条边。
**parameters**:
· from_node: 表示边的起始节点，类型为ActionNode。
· to_node: 表示边的结束节点，类型为ActionNode。
**Code Description**:
如果from_node的key不在self.edges中，则将from_node的key添加到self.edges中，并将to_node的key添加到from_node对应的值中。然后调用from_node的add_next方法，将to_node添加为from_node的下一个节点。最后调用to_node的add_prev方法，将from_node添加为to_node的前一个节点。
**Note**: 请确保from_node和to_node参数的类型为ActionNode类的实例。
***
### FunctionDef topological_sort(self)
**topological_sort**: topological_sort函数的功能是对图进行拓扑排序。

**parameters**:
· 无参数

**Code Description**:
该函数实现了对图进行拓扑排序的操作。首先，创建了一个空集合visited用于存储已访问过的节点，以及一个空栈stack用于存储排序后的节点。接着定义了内部函数visit(k)，用于递归访问节点k及其相邻节点。在visit函数中，首先检查节点k是否已经访问过，若未访问过，则将其加入visited集合中，并递归访问k的相邻节点。最后，将节点k插入到stack的首位，实现逆序排列。接着，对图中的每个节点依次调用visit函数，完成整个图的拓扑排序。最终，将排序后的节点顺序存储在对象的execution_order属性中。

**Note**:
- 在调用topological_sort函数前，需要确保图的节点和边已经正确设置。
- 该函数实现了拓扑排序算法，适用于有向无环图（DAG）。
#### FunctionDef visit(k)
**visit**: visit函数的功能是执行拓扑排序中的访问操作。

**parameters**:
· k: 表示当前访问的节点。

**Code Description**:
visit函数实现了拓扑排序中对节点的访问操作。首先，函数会检查当前节点k是否已经被访问过，如果没有被访问过，则将其添加到已访问的节点集合中。接着，如果当前节点k存在于图中的边中，函数会递归地对当前节点的邻居节点进行访问操作。最后，函数会将当前节点k插入到栈中，以确保拓扑排序的正确顺序。

**Note**:
- 在调用visit函数时，需要确保传入的参数k是图中的有效节点。
- visit函数实现了深度优先搜索（DFS）的思想，通过递归地访问节点来完成拓扑排序的过程。
***
***
