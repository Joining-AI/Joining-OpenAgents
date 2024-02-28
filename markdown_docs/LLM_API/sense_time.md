## ClassDef AuthenticatedRequestSender
**AuthenticatedRequestSender**: AuthenticatedRequestSender的功能是处理身份验证并发送请求。

**attributes**:
- base_url: API的基础URL
- ak: 从环境变量获取的AK
- sk: 从环境变量获取的SK
- authorization: 授权信息
- refresh_interval: 刷新token的时间间隔
- timer: 定时器
- lock: 线程锁

**Code Description**:
AuthenticatedRequestSender类包含了处理身份验证并发送请求的方法。在初始化时，会设置基础URL、AK、SK等属性，并调用refresh_token方法刷新token。generate_jwt_token方法用于生成JWT token，refresh_token方法定时刷新token。send_get_request方法发送GET请求，ask_once方法发送POST请求并处理响应，embed方法发送POST请求并处理嵌入式响应。在对象销毁时，会取消定时器。

在项目中，AuthenticatedRequestSender类被Tools模块中的FunctionManager类调用。FunctionManager根据服务类型选择使用AuthenticatedRequestSender类或其他服务类进行实例化，以处理不同的服务请求。

**Note**: 
- 在使用AuthenticatedRequestSender类时，需要确保环境变量中设置了SENSETIME_AK和SENSETIME_SK。
- 调用ask_once和embed方法时，可以处理身份验证失败的情况并进行重试。

**Output Example**:
```json
{
    "message": "请求成功"
}
```
### FunctionDef __init__(self, refresh_interval)
**__init__**: \_\_init\_\_函数的功能是初始化AuthenticatedRequestSender类的实例。

**参数**:
· refresh_interval: 刷新间隔时间，默认值为1700。

**代码描述**:
\_\_init\_\_函数用于初始化AuthenticatedRequestSender类的实例。在函数内部，它设置了base_url为"https://api.sensenova.cn/v1/llm"，并从环境变量中获取SENSETIME_AK和SENSETIME_SK作为ak和sk参数。此外，它初始化了authorization为None，refresh_interval为传入的refresh_interval参数值，timer和lock为None和threading.Lock()的实例。最后，它调用refresh_token函数来刷新JWT令牌。

在项目中，\_\_init\_\_函数是AuthenticatedRequestSender类的构造函数，用于初始化类的实例并设置必要的属性。它确保在创建AuthenticatedRequestSender实例时，相关的属性和参数已经设置好，以便后续的请求和操作能够顺利进行。

**注意**:
在使用\_\_init\_\_函数时，可以通过传入refresh_interval参数来设置JWT令牌的刷新间隔时间。确保在实例化AuthenticatedRequestSender类时，已经设置了正确的环境变量SENSETIME_AK和SENSETIME_SK，以便成功获取AK和SK参数。

refresh_token函数被\_\_init\_\_函数调用，用于在初始化AuthenticatedRequestSender实例时立即刷新JWT令牌，以确保实例化后即可使用有效的令牌进行请求。
***
### FunctionDef generate_jwt_token(self)
**generate_jwt_token**: generate_jwt_token函数的功能是生成JWT令牌。

**参数**：此函数无参数。

**代码描述**：generate_jwt_token函数首先创建了headers和payload两个字典，分别用于指定JWT的头部和载荷内容。其中，头部包含了算法和类型信息，载荷包含了签发者、过期时间和生效时间等信息。接着，利用jwt库的encode方法生成JWT令牌，使用指定的算法和密钥对载荷进行加密。最后，返回生成的JWT令牌。

在项目中，generate_jwt_token函数被AuthenticatedRequestSender类中的refresh_token函数调用。refresh_token函数在获取新的JWT令牌前会调用generate_jwt_token函数生成新的令牌，并在一定时间间隔后再次调用refresh_token函数以更新JWT令牌。

**注意**：在使用generate_jwt_token函数时，确保提供正确的ak和sk参数以生成有效的JWT令牌。

**输出示例**：示例JWT令牌：eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhZG1pbiIsImV4cCI6MTYyMzUwNzY4MCwibmJmIjoxNjIzNTA3NjYxfQ.5r5y4v9e4J8G1K7y0KvK8Rb2z4v8J7e4v8J7e4v8J7e
***
### FunctionDef refresh_token(self)
**refresh_token**: refresh_token函数的功能是刷新JWT令牌。

**参数**：此函数无参数。

**代码描述**：refresh_token函数通过获取新的JWT令牌来刷新现有的令牌。在函数内部，它首先使用线程锁确保安全地生成新的JWT令牌，然后取消之前的定时器（如果存在），创建一个新的定时器以在指定的刷新间隔后再次调用refresh_token函数。最后，启动新的定时器以开始刷新JWT令牌的过程。

在项目中，refresh_token函数被AuthenticatedRequestSender类中的其他函数调用，以确保在需要时始终具有有效的JWT令牌。

**注意**：在使用refresh_token函数时，确保已正确初始化ak和sk参数，并了解刷新间隔的设置以便及时更新JWT令牌。

**输出示例**：无。
***
### FunctionDef send_get_request(self)
**send_get_request**: send_get_request函数的功能是向指定的URL发送GET请求并返回响应结果。

**参数**:
· 无参数

**代码描述**:
该函数首先构建了一个指向"https://api.sensenova.cn/v1/llm/models"的URL，并设置了包含Authorization和Content-Type的headers。然后，使用requests库发送GET请求到指定的URL，并携带headers。最后，将获取到的响应结果以JSON格式打印输出。

**注意**:
在使用该函数之前，确保已经设置了self.authorization的值，以便在headers中正确添加Authorization信息。

**输出示例**:
{
    "key1": "value1",
    "key2": "value2",
    ...
}
***
### FunctionDef ask_once(self, messages, know_ids, max_new_tokens, model, n, repetition_penalty, stream, temperature, top_p, user, knowledge_config, plugins, retry_count)
**ask_once**: ask_once函数的功能是向服务器发送一次请求以获取聊天完成的消息。

**参数**:
- messages: 要发送的消息内容。
- know_ids: 知识库的ID。
- max_new_tokens: 生成消息的最大标记数。
- model: 使用的模型名称。
- n: 生成的消息数量。
- repetition_penalty: 重复惩罚值。
- stream: 是否流式传输。
- temperature: 温度值。
- top_p: 顶部p值。
- user: 用户信息。
- knowledge_config: 知识配置。
- plugins: 插件信息。
- retry_count: 重试次数。

**代码描述**:
ask_once函数通过构建请求payload并向服务器发送POST请求来获取聊天完成的消息。在函数内部，首先构建请求的URL和headers，然后构建请求的payload数据。接着，使用requests库向服务器发送POST请求，并解析响应数据以获取消息内容。如果响应状态码为200，则返回消息内容；如果状态码为401，则根据重试次数判断是否刷新token并重新发送请求；其他状态码则直接返回状态码。

**注意**:
在使用ask_once函数时，确保传入必要的参数以正确发送请求并处理响应。
如果遇到401状态码，函数会尝试最多3次刷新token并重新发送请求。
了解各参数的含义和取值范围，以便正确配置请求。

**输出示例**:
{"message": "这是一个聊天完成的消息内容。"}
***
### FunctionDef embed(self, input_text, model, retry_count)
**embed**: embed函数的功能是将输入文本嵌入到指定的模型中，并返回嵌入结果。

**参数**:
· input_text: 输入的文本内容，默认为None。
· model: 指定的嵌入模型，默认为'nova-embedding-stable'。
· retry_count: 重试次数，默认为0。

**代码描述**:
embed函数首先构建请求的URL和headers，然后将输入文本和模型信息作为payload发送POST请求。根据响应的状态码进行不同的处理：若状态码为200，则解析响应数据并返回第一个嵌入结果；若状态码为401，则尝试刷新令牌并重新调用embed函数，最多重试3次；其他状态码则返回相应的错误信息。

在功能上，embed函数依赖于refresh_token函数来确保在需要时刷新JWT令牌，以维持有效的身份验证状态。

**注意**:
在使用embed函数前，请确保已正确初始化base_url和authorization参数。
若遇到身份验证失败的情况，函数会尝试最多3次刷新令牌。
根据实际情况，可根据业务需求调整模型参数。

**输出示例**:
{"embedding": [0.1, 0.2, ..., 0.9]}
***
### FunctionDef __del__(self)
**__del__**: __del__函数的功能是取消计时器。

**参数**:
· self: 表示类的实例本身。

**代码描述**:
在__del__函数中，首先使用了self.lock来确保线程安全。然后检查self.timer是否存在，如果存在则调用cancel()方法来取消计时器。

**注意**:
在Python中，__del__方法是一个特殊方法，用于在对象被销毁时执行清理操作。在这里，__del__方法用于取消计时器，确保资源的正确释放。
***
