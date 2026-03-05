from typing import Dict, Any
from tavily import TavilyClient
from config import settings

def search(
    query: str,
    max_results: int = 5,
    include_answer: str = "advanced"
) -> Dict[str, Any]:
    """
    使用 Tavily API 进行搜索
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量，默认 5
        include_answer: 是否包含 AI 生成的答案，默认 "advanced"
    
    Returns:
        搜索结果字典
    """
    client = TavilyClient(settings.TAVILY_API_KEY)
    
    response = client.search(
        query=query,
        include_answer=include_answer,
        max_results=max_results
    )
    
    return response

if __name__ == '__main__':
    query = '鸣潮'
    response = search(query)

    answer = response.get('answer')
    results = response.get('results', [])
    
    print(f"\n答案: {answer}")
    print(f"\n解析结果 (共{len(results)}条):")
    
    for i, result in enumerate(results, 1):
        url = result.get('url', '')
        content = result.get('content', '')
        title = result.get('title', '')
        score = result.get('score', 0.0)
        
        print(f"\n--- 结果 {i} ---")
        print(f"标题: {title}")
        print(f"URL: {url}")
        print(f"相关性: {score:.4f}")
        print(f"内容: {content[:200]}...")