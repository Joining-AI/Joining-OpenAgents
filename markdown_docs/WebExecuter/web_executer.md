## ClassDef WebSearch
**WebSearch**: WebSearch的功能是根据指定的搜索引擎执行搜索操作。

**attributes**:
· search_engine: 搜索引擎类型，默认为'bing'。

**Code Description**:
WebSearch类包含一个构造函数__init__，用于初始化搜索引擎类型。search方法根据指定的搜索引擎类型执行搜索操作，支持Google和Bing搜索引擎。根据搜索结果，返回包含标题和链接的列表。

在项目中，WebSearch类用于执行Web搜索操作。通过调用WebExecuter模块中的其他功能，实现对指定搜索引擎的搜索功能。

**Note**:
对于不支持的搜索引擎类型，会引发ValueError异常。
在搜索过程中，如果发生异常，将打印错误信息并返回None。

**Output Example**:
(['Title1', 'Title2', ...], ['Link1', 'Link2', ...])
### FunctionDef __init__(self, search_engine)
**__init__**: __init__函数的功能是初始化WebSearch对象。

**参数**:
· search_engine: 搜索引擎的名称，默认为'bing'。

**代码描述**:
这个__init__函数是WebSearch对象的构造函数。它接受一个参数search_engine，用于指定搜索引擎的名称。如果没有提供搜索引擎的名称，默认将使用'bing'作为搜索引擎。在函数内部，将传入的search_engine参数赋值给对象的search_engine属性，以便在后续的搜索操作中使用。

**注意**:
在实例化WebSearch对象时，可以选择指定搜索引擎的名称，如果不指定将默认使用'bing'作为搜索引擎。
***
### FunctionDef search(self, query)
**search**: search函数的功能是根据指定的搜索引擎（Google或Bing）和查询内容执行搜索，并返回搜索结果的标题和链接。

**parameters**:
· self: 指向当前实例的引用。
· query: 要搜索的查询内容。

**Code Description**:
search函数根据self.search_engine的值选择使用Google还是Bing搜索引擎，并构建相应的搜索URL。然后，发送带有自定义User-Agent头的GET请求到搜索引擎的URL。接收到响应后，使用BeautifulSoup解析HTML内容，提取搜索结果的标题和链接信息。最多返回前10个搜索结果的标题和链接。

**Note**: 
- 当self.search_engine不是'google'或'bing'时，会引发ValueError异常。
- 如果发生任何异常，函数将返回(None, None)。

**Output Example**:
(['Title 1', 'Title 2', ...], ['Link 1', 'Link 2', ...])
***
## ClassDef BrowserExecute
Doc is waiting to be generated...
### FunctionDef __init__(self, driver_path)
**__init__**: 初始化函数的作用是初始化浏览器驱动和设置基本URL。

**参数**:
· driver_path: 浏览器驱动程序的路径。

**代码描述**:
在这个初始化函数中，首先通过传入的driver_path参数来设置Edge浏览器的服务。然后使用该服务来实例化一个Edge浏览器对象。最后，将基本URL设置为'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=%E6%81%92%E5%A4%A7'。

**注意**:
在使用该初始化函数时，需要确保传入正确的浏览器驱动程序的路径，以便成功初始化浏览器驱动。
***
### FunctionDef open_new_tab(self, url)
**open_new_tab**: open_new_tab函数的功能是打开一个新的标签页。

**parameters**:
· url: 新标签页要打开的URL地址。

**Code Description**:
打开新的标签页，首先通过执行JavaScript代码在浏览器中打开一个空白的新标签页。然后切换到新打开的标签页，通过获取浏览器当前所有标签页的句柄，选择最后一个句柄来切换到新标签页。最后在新标签页中加载指定的URL地址。

**Note**:
- 在调用该函数之前，确保已经实例化了浏览器对象并赋值给self.browser。
- 确保传入的url参数是一个有效的URL地址。
***
### FunctionDef close_current_tab(self)
**close_current_tab**: close_current_tab函数的作用是关闭当前的标签页。

**参数**:
· 无参数

**代码描述**:
该函数首先关闭当前的标签页，然后切换回主标签页。关闭当前标签页是通过self.browser.close()实现的，这会关闭当前正在浏览的标签页。接着，通过self.browser.switch_to.window(self.browser.window_handles[0])将焦点切换回主标签页，即浏览器窗口中的第一个标签页。

**注意**:
在调用该函数时，会关闭当前标签页并切换回主标签页。
***
### FunctionDef page_turn(self)
**page_turn**: page_turn函数的功能是执行网页翻页操作。

**参数**：该函数没有参数。

**代码描述**：page_turn函数首先通过time.sleep(1)等待1秒，然后查找页面中的下一页按钮。接着获取该按钮的disabled属性值，如果为True，则打印"无法翻页已经达到最后一页"并返回1；否则点击下一页按钮，再次等待1秒，获取当前页面的源代码，并返回该数据。在异常处理中，如果捕获到NoSuchElementException异常，则打印异常信息并返回None。

在项目中，page_turn函数被start_scraping函数调用。start_scraping函数首先打开浏览器并获取页面源代码，然后调用page_turn函数执行翻页操作，直到返回值为1时停止翻页并打印"爬取完毕"。

**注意**：在使用page_turn函数时，需要确保页面中存在下一页按钮，并且按钮未被禁用。

**输出示例**：假设成功执行翻页操作后，返回当前页面的源代码。
***
### FunctionDef search(self, data)
**search**: search函数的功能是解析网页数据，提取标题、网址和发布时间信息，并根据设定条件下载对应的PDF文件。

**参数**：此函数的参数。
· data: 表示要解析的网页数据，包含标题、网址和发布时间等信息。

**代码描述**：search函数首先通过正则表达式解析网页标题、网址和发布时间信息。然后，对每个网址进行清理和时间解析，确保时间格式正确。接着，判断时间是否在指定范围内，若符合条件则调用download_pdf函数下载对应的PDF文件。

在项目中，search函数被WebExecuter\web_executer.py/BrowserExecute/start_scraping对象调用。在start_scraping函数中，首先获取网页数据，然后调用search函数解析数据并下载PDF文件。若下载过程中出现异常，将捕获并打印错误信息，确保程序稳定可靠。

**注意**：在使用search函数时，需要传入正确的网页数据参数，以确保能够成功解析并下载PDF文件。
***
### FunctionDef download_pdf(self, url, title)
**download_pdf**: download_pdf函数的功能是下载指定URL的PDF文件。

**参数**：此函数的参数。
· url: 表示要下载的PDF文件的URL。
· title: 表示要保存的PDF文件的标题。

**代码描述**：download_pdf函数通过传入的URL和标题，尝试下载对应的PDF文件。首先，使用requests库发送GET请求获取文件内容，然后将内容写入以标题命名的PDF文件中。如果下载成功，将打印"下载成功: 文件名"；如果下载失败，将打印"下载失败: 错误信息"。

在项目中，download_pdf函数被WebExecuter\web_executer.py/BrowserExecute/search对象调用。在search函数中，通过解析网页数据获取到PDF文件的URL和标题后，调用download_pdf函数下载PDF文件。如果下载过程中出现异常，将捕获并打印错误信息，保证程序的稳定性和可靠性。

**注意**：在使用download_pdf函数时，需要确保传入正确的URL和标题参数，以确保能够成功下载PDF文件。
***
### FunctionDef start_scraping(self)
**start_scraping**: start_scraping函数的功能是打开浏览器并开始网页数据抓取操作。

**参数**：该函数没有参数。

**代码描述**：start_scraping函数首先使用浏览器打开指定的base_url，并等待1秒。然后获取当前页面的源代码，并调用search函数解析数据。接着进入一个无限循环，每次循环中调用page_turn函数执行翻页操作，直到page_turn函数返回值为1时，循环结束并打印"爬取完毕"。

在项目中，start_scraping函数是网页数据抓取的入口函数。通过打开浏览器、解析数据和执行翻页操作，实现了对网页内容的全面抓取。

**注意**：在使用start_scraping函数时，需要确保已设置base_url，并且页面中存在下一页按钮以支持翻页操作。
***
