## ClassDef Embedding
**Embedding**: Embedding的功能是计算文本嵌入向量之间的余弦相似度，并找到与目标消息最相似的消息及其相似度。

**attributes**:
- embedding1: 第一个文本嵌入向量
- embedding2: 第二个文本嵌入向量
- target_message: 目标消息
- data: 包含消息和对应嵌入向量的数据列表
- top_n: 返回的最相似消息数量，默认为5

**Code Description**:
Embedding类包含两个静态方法。calculate_cosine_similarity方法用于计算两个文本嵌入向量之间的余弦相似度。find_top_similar_messages方法用于找到与目标消息最相似的top_n个消息及其相似度。在find_top_similar_messages方法中，首先获取目标消息的嵌入向量，然后计算目标消息与其他消息的相似度，最后根据相似度排序并返回top_n个最相似的消息及其相似度。

在项目中，Embedding类被用于处理文本数据，通过计算余弦相似度来寻找与目标消息最相似的消息。这有助于在文本数据中进行相似性分析和推荐相关消息。

**Note**:
- 确保传入的数据格式正确，包含所需的消息和对应的嵌入向量。
- 在调用find_top_similar_messages方法时，确保目标消息在数据中存在，否则会引发ValueError异常。

**Output Example**:
[('相似消息1', 0.85), ('相似消息2', 0.78), ('相似消息3', 0.72), ('相似消息4', 0.68), ('相似消息5', 0.61)]
### FunctionDef __init__(self)
**__init__**: __init__的功能是初始化对象。

**参数**：这个函数没有参数。

**代码描述**：这个函数是一个构造函数，用于初始化对象。在这个特定的例子中，函数体内没有具体的操作，只有一个占位符pass语句。在实际应用中，可以在这个函数中进行对象的属性初始化或其他必要的操作。

**注意**：在编写类时，__init__函数是一个特殊的函数，用于在创建对象时进行初始化操作。通常情况下，我们会在这个函数中设置对象的初始状态，以确保对象在创建后处于正确的状态。
***
### FunctionDef calculate_cosine_similarity(embedding1, embedding2)
**calculate_cosine_similarity**: calculate_cosine_similarity函数的作用是计算余弦相似度。

**参数**:
· embedding1: 第一个嵌入向量，类型为List[float]。
· embedding2: 第二个嵌入向量，类型为List[float]。

**代码描述**:
calculate_cosine_similarity函数实现了计算两个嵌入向量之间的余弦相似度。函数内部调用了名为cosine的函数，通过计算1减去两个嵌入向量的余弦值来得到余弦相似度。

在项目中，calculate_cosine_similarity函数被find_top_similar_messages函数调用。find_top_similar_messages函数的作用是找到与目标消息最相似的top_n个消息及其相似度。在该函数中，首先获取目标消息的嵌入向量，然后通过调用calculate_cosine_similarity函数计算目标消息与其他消息的相似度，最终返回相似度排名前top_n的消息及其相似度。

**注意**: 在使用calculate_cosine_similarity函数时，需要传入两个嵌入向量作为参数，并且这两个向量需要是浮点数列表。函数返回一个浮点数，代表计算得到的余弦相似度。

**输出示例**:
0.85
***
### FunctionDef find_top_similar_messages(target_message, data, top_n)
**find_top_similar_messages**: find_top_similar_messages函数的作用是找到与目标消息最相似的top_n个消息及其相似度。

**参数**:
· target_message: 目标消息，类型为str。
· data: 包含消息和嵌入向量的数据列表，类型为List[dict]。
· top_n: 返回相似度排名前top_n的消息数量，默认为5，类型为int。

**代码描述**:
find_top_similar_messages函数首先在给定的数据列表中查找目标消息的嵌入向量，然后计算目标消息与其他消息的相似度。相似度通过调用Embedding.calculate_cosine_similarity函数计算得出，最终返回相似度排名前top_n的消息及其相似度。

在项目中，find_top_similar_messages函数与calculate_cosine_similarity函数相关联。calculate_cosine_similarity函数用于计算两个嵌入向量之间的余弦相似度，而find_top_similar_messages函数则利用该相似度找到最相似的消息。

**注意**: 在使用find_top_similar_messages函数时，需要传入目标消息、数据列表以及top_n参数。数据列表中的每个元素应包含'message'和'embedding'字段，且embedding字段为嵌入向量。

**输出示例**:
[('相似消息1', 0.85), ('相似消息2', 0.82), ('相似消息3', 0.78), ('相似消息4', 0.75), ('相似消息5', 0.72)]
***
