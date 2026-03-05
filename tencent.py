import json
import hmac
import hashlib
import time
from datetime import datetime
from typing import Optional, Dict, Any
import requests
from config import settings


class TencentSearchAPI:
    
    def __init__(self):
        self.secret_id = settings.TENCENT_SECRET_ID
        self.secret_key = settings.TENCENT_SECRET_KEY
        self.endpoint = "wsa.tencentcloudapi.com"
        self.service = "wsa"
        self.version = "2025-05-08"
        self.action = "SearchPro"
        
    def _sign(self, params: Dict[str, Any], timestamp: int) -> str:
        date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        canonical_headers = f"content-type:application/json\nhost:{self.endpoint}\n"
        signed_headers = "content-type;host"
        payload = json.dumps(params)
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (
            http_request_method + "\n" +
            canonical_uri + "\n" +
            canonical_querystring + "\n" +
            canonical_headers + "\n" +
            signed_headers + "\n" +
            hashed_request_payload
        )
        
        credential_scope = f"{date}/{self.service}/tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (
            "TC3-HMAC-SHA256" + "\n" +
            str(timestamp) + "\n" +
            credential_scope + "\n" +
            hashed_canonical_request
        )
        
        def _sign_str(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
        
        secret_date = _sign_str(("TC3" + self.secret_key).encode("utf-8"), date)
        secret_service = _sign_str(secret_date, self.service)
        secret_signing = _sign_str(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        
        authorization = (
            "TC3-HMAC-SHA256" + " " +
            "Credential=" + self.secret_id + "/" + credential_scope + ", " +
            "SignedHeaders=" + signed_headers + ", " +
            "Signature=" + signature
        )
        
        return authorization

    def search(
        self,
        query: str,
        mode: int = 0,
        site: Optional[str] = None,
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
        cnt: Optional[int] = None,
        industry: Optional[str] = None
    ) -> Dict[str, Any]:
        timestamp = int(time.time())
        
        params = {
            "Query": query,
        }
        
        if mode is not None:
            params["Mode"] = mode
        if site:
            params["Site"] = site
        if from_time:
            params["FromTime"] = from_time
        if to_time:
            params["ToTime"] = to_time
        if cnt:
            params["Cnt"] = cnt
        if industry:
            params["Industry"] = industry
        
        authorization = self._sign(params, timestamp)
        
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Host": self.endpoint,
            "X-TC-Action": self.action,
            "X-TC-Version": self.version,
            "X-TC-Timestamp": str(timestamp),
        }
        
        url = f"https://{self.endpoint}"
        response = requests.post(url, headers=headers, json=params)
        result = response.json()
        
        if "Response" in result and "Error" in result["Response"]:
            error = result["Response"]["Error"]
            raise Exception(f"API错误 [{error['Code']}]: {error['Message']}")
        
        if "Response" not in result:
            return result
        
        resp = result["Response"]
        pages = resp.get("Pages", [])
        
        results = []
        for page_str in pages:
            try:
                page_data = json.loads(page_str)
                results.append({
                    "title": page_data.get("title", ""),
                    "url": page_data.get("url", ""),
                    "passage": page_data.get("passage", ""),
                    "content": page_data.get("content", ""),
                    "date": page_data.get("date", ""),
                    "site": page_data.get("site", ""),
                    "score": page_data.get("score", 0.0),
                    "images": page_data.get("images", []),
                    "favicon": page_data.get("favicon", ""),
                })
            except json.JSONDecodeError:
                continue
        
        print(f"\n解析结果 (共{len(results)}条):")
        for i, res in enumerate(results, 1):
            print(f"\n--- 结果 {i} ---")
            print(f"标题: {res['title']}")
            print(f"来源: {res['site']}")
            print(f"URL: {res['url']}")
            print(f"日期: {res['date']}")
            print(f"相关性: {res['score']:.4f}")
            print(f"摘要: {res['passage'][:200]}...")
        
        return result
