# 搜索 API 集成项目

本项目集成了 Tavily 和腾讯云搜索 API，提供统一的搜索接口。

## 快速开始

### 1. 环境配置

首先复制环境变量示例文件：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的 API 密钥：

```env
# Tavily API 密钥
TAVILY_API_KEY=your_tavily_api_key_here

# 腾讯云密钥
TENCENT_SECRET_ID=your_tencent_secret_id_here
TENCENT_SECRET_KEY=your_tencent_secret_key_here
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 项目结构

```
.
├── .env                # 环境变量配置文件（需自行创建）
├── .env.example        # 环境变量示例文件
├── config.py           # 配置文件，从 .env 读取环境变量
├── tavily_search.py    # Tavily 搜索 API 封装
├── tencent.py          # 腾讯云搜索 API 封装
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明文档
```

## 使用说明

### Tavily 搜索

[Tavily API Platform](https://app.tavily.com/home)

```python
import tavily_search

# 执行搜索
result = tavily_search.search(
    query="Python 最佳实践",
    max_results=5,
    include_answer="advanced"
)
```

### 腾讯云搜索

[联网搜索API 联网搜索API_腾讯云](https://cloud.tencent.com/document/product/1806/121811)

```python
from tencent import TencentSearchAPI

# 初始化
tencent = TencentSearchAPI()

# 执行搜索
result = tencent.search(
    query="人工智能发展趋势",
    mode=0,
    cnt=10
)
```

## API 说明

### tavily_search.search()

执行 Tavily 搜索

参数：

- `query`: 搜索关键词
- `max_results`: 返回结果数量，默认 5
- `include_answer`: 是否包含 AI 生成的答案，默认 "advanced"

返回：搜索结果字典

### TencentSearchAPI

- `search(query, mode=0, site=None, from_time=None, to_time=None, cnt=None, industry=None)`: 执行搜索
  - `query`: 搜索关键词
  - `mode`: 搜索模式
  - `site`: 指定站点
  - `from_time`: 开始时间
  - `to_time`: 结束时间
  - `cnt`: 返回结果数量
  - `industry`: 行业分类

## 注意事项

- 请妥善保管 `.env` 文件中的 API 密钥，不要提交到版本控制系统
- `.env` 文件已在 `.gitignore` 中忽略（建议添加）
- 使用前请确保已获取相应的 API 密钥

## 获取 API 密钥

- Tavily API: https://tavily.com/
- 腾讯云 API: https://console.cloud.tencent.com/

## License

MIT
