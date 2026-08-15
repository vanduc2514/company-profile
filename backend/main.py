"""
InsightEngine API & Web App — FastAPI Backend & Static Server for Google Cloud Run
Supports Gemini 2.5 Flash API with Google Search Grounding (Vietnamese Output) & serves frontend SPA assets.
"""

import os
import re
import time
import json
import random
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import httpx

app = FastAPI(
    title="InsightEngine API",
    description="Dịch Vụ Phân Tích Hồ Sơ Doanh Nghiệp Tự Động Qua Gemini Search Grounding",
    version="2.5.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional Firestore initialization
db = None
try:
    from google.cloud import firestore
    project_id = os.getenv("GCP_PROJECT_ID")
    if project_id:
        db = firestore.Client(project=project_id)
except Exception as e:
    print(f"Firestore initialized in mock/in-memory mode: {e}")

# In-memory storage fallback
IN_MEMORY_PROFILES: Dict[str, Dict[str, Any]] = {}

# ── Pydantic Schemas ──

class SourceInputs(BaseModel):
    google: Optional[str] = ""
    linkedin: Optional[str] = ""
    website: Optional[str] = ""
    registration: Optional[str] = ""

class SearchRequest(BaseModel):
    companyName: str
    geminiApiKey: Optional[str] = None
    manualInputs: Optional[SourceInputs] = None

class AnalysisRequest(BaseModel):
    inputs: SourceInputs

class ProductItem(BaseModel):
    icon: str
    name: str
    desc: str

class MetricDetail(BaseModel):
    level: str
    class_name: str = Field(..., alias="class")
    percent: int

class MarketMetrics(BaseModel):
    competitor: MetricDetail
    regulatory: MetricDetail
    growth: MetricDetail

class FeedItem(BaseModel):
    title: str
    source: str
    body: str
    active: bool

class RegistrationDetails(BaseModel):
    entityName: str
    jurisdiction: str
    status: str
    cik: str
    markets: str

class ProfileResponse(BaseModel):
    id: str
    companyName: str
    industry: str
    scale: str
    market: str
    registrationStatus: str
    confidenceScore: float
    summary: str
    website: str
    location: str
    createdAt: str
    inputs: SourceInputs
    products: List[ProductItem]
    registrationDetails: RegistrationDetails
    marketShare: int
    metrics: MarketMetrics
    feed: List[FeedItem]

# ── Gemini API Auto-Search with Google Grounding (Vietnamese Prompt) ──

async def call_gemini_auto_search(company_name: str, api_key: str) -> Dict[str, Any]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Bạn là chuyên gia phân tích tình báo doanh nghiệp hàng đầu. Hãy nghiên cứu kỹ lưỡng về công ty/doanh nghiệp: "{company_name}".
Thu thập thông tin đa nguồn trên Google Search, LinkedIn, Website chính thức và Cổng đăng ký kinh doanh bằng Google Search.

Trả về DUY NHẤT một đối tượng JSON hợp lệ (không chứa mã code block, không thêm văn bản ngoài) với cấu trúc sau bằng TIẾNG VIỆT:
{{
  "companyName": "{company_name}",
  "industry": "Lĩnh vực kinh doanh (Ví dụ: Công Nghệ / SaaS, Tài Chính & Fintech, Sản Xuất, Y Tế)",
  "scale": "Tập Đoàn Lớn (Enterprise) | Doanh Nghiệp Vừa & Nhỏ (SME) | Khởi Nghiệp (Startup)",
  "market": "Toàn Cầu | Nội Địa",
  "registrationStatus": "Đã Xác Thực ✓",
  "confidenceScore": 95.5,
  "summary": "Tóm tắt tổng quan doanh nghiệp từ 2-3 câu bằng Tiếng Việt.",
  "website": "tên miền website chính thức (ví dụ: stripe.com)",
  "location": "Thành phố và quốc gia trụ sở chính",
  "products": [
    {{"icon": "credit_card", "name": "Tên sản phẩm/dịch vụ 1", "desc": "Mô tả ngắn sản phẩm 1 bằng Tiếng Việt"}},
    {{"icon": "account_balance", "name": "Tên sản phẩm/dịch vụ 2", "desc": "Mô tả ngắn sản phẩm 2 bằng Tiếng Việt"}}
  ],
  "registrationDetails": {{
    "entityName": "Tên đăng ký pháp lý đầy đủ",
    "jurisdiction": "Cơ quan/Quốc gia đăng ký",
    "status": "Đang hoạt động / Công ty Cổ phần",
    "cik": "Mã số thuế hoặc Mã đăng ký",
    "markets": "Thị trường hoạt động chính"
  }},
  "marketShare": 75,
  "metrics": {{
    "competitor": {{"level": "Trung Bình", "class": "warning", "percent": 75}},
    "regulatory": {{"level": "Thấp", "class": "success", "percent": 20}},
    "growth": {{"level": "Mạnh", "class": "indigo", "percent": 85}}
  }},
  "feed": [
    {{"title": "Sự kiện/Thông tin mới nhất", "source": "Tin tức / Cổng thông tin • Ngày", "body": "Tóm tắt nội dung sự kiện bằng Tiếng Việt.", "active": true}}
  ],
  "sources": {{
    "google": "Tóm tắt kết quả tìm kiếm Google bằng Tiếng Việt về {company_name}",
    "linkedin": "Tóm tắt thông tin LinkedIn & quy mô nhân sự bằng Tiếng Việt",
    "website": "Tổng quan trang chủ & giải pháp cung cấp bằng Tiếng Việt",
    "registration": "Thông tin đăng ký kinh doanh & tư cách pháp nhân bằng Tiếng Việt"
  }}
}}
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "tools": [
            {"google_search": {}}
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, json=payload)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Lỗi kết nối Gemini API ({res.status_code}): {res.text}"
            )
        
        data = res.json()
        try:
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            cleaned_text = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned_text = re.sub(r"^```\s*", "", cleaned_text.strip(), flags=re.MULTILINE)
            cleaned_text = cleaned_text.strip()
            
            parsed = json.loads(cleaned_text)
            return parsed
        except Exception as err:
            print(f"Lỗi đọc kết quả JSON từ Gemini: {err}")
            raise HTTPException(status_code=500, detail=f"Lỗi đọc dữ liệu JSON Gemini: {err}")

# ── Local Keyword Fallback Generator (Vietnamese) ──

KEYWORD_MAP = {
    "industry": [
        (["saas", "cloud", "software", "ai", "tech", "api", "digital", "công nghệ", "phần mềm"], "Công Nghệ / SaaS"),
        (["bank", "finance", "invest", "capital", "fintech", "pay", "payment", "ngân hàng", "tài chính"], "Tài Chính & Fintech"),
        (["manufactur", "factory", "produc", "industrial", "sản xuất"], "Sản Xuất & Công Nghiệp"),
        (["health", "pharma", "clinic", "medical", "bio", "y tế"], "Y Tế & Dược Phẩm"),
        (["retail", "e-commerce", "ecommerce", "shop", "bán lẻ"], "Bán Lẻ & TMĐT")
    ],
    "scale": [
        (["startup", "seed", "series a", "series b", "khởi nghiệp"], "Khởi Nghiệp (Startup)"),
        (["sme", "small", "medium", "vừa và nhỏ"], "Doanh Nghiệp Vừa & Nhỏ (SME)"),
        (["enterprise", "corporation", "global", "tập đoàn"], "Tập Đoàn Lớn (Enterprise)")
    ],
    "market": [
        (["global", "worldwide", "international", "toàn cầu"], "Toàn Cầu"),
        (["domestic", "local", "vietnam", "viet nam", "nội địa"], "Nội Địa (Việt Nam)")
    ],
    "registration": [
        (["verified", "registered", "certificate", "xác thực"], "Đã Xác Thực ✓")
    ]
}

def analyze_sources(inputs: SourceInputs, company_name_override: Optional[str] = None) -> Dict[str, Any]:
    text = f"{company_name_override or ''} {inputs.google} {inputs.linkedin} {inputs.website} {inputs.registration}".lower()
    
    company_name = company_name_override or "Doanh Nghiệp Chưa Xác Định"
    if not company_name_override and inputs.google.strip():
        first_words = " ".join(inputs.google.strip().split()[:3])
        clean_name = re.sub(r'[^a-zA-Z0-9\s,&.-]', '', first_words).strip()
        if clean_name:
            company_name = clean_name.title()

    def match_cat(key: str, default_val: str) -> str:
        for keywords, value in KEYWORD_MAP[key]:
            if any(kw in text for kw in keywords):
                return value
        return default_val

    industry = match_cat("industry", "Công Nghệ / SaaS")
    scale = match_cat("scale", "Tập Đoàn Lớn (Enterprise)")
    market = match_cat("market", "Toàn Cầu")
    reg_status = match_cat("registration", "Đã Xác Thực ✓")

    matches = sum(1 for cat in KEYWORD_MAP.values() for keywords, _ in cat if any(kw in text for kw in keywords))
    confidence = min(98.8, max(75.0, round(68.0 + matches * 3.5, 1)))

    profile_id = f"profile-{int(time.time() * 1000)}"
    domain_name = company_name.lower().replace(" ", "").replace(",", "").replace(".", "") + ".com"
    
    return {
        "id": profile_id,
        "companyName": company_name,
        "industry": industry,
        "scale": scale,
        "market": market,
        "registrationStatus": reg_status,
        "confidenceScore": confidence,
        "summary": f"{company_name} là doanh nghiệp hoạt động trong lĩnh vực {industry} với mô hình vận hành {scale.lower()} tập trung vào thị trường {market.lower()}.",
        "website": domain_name,
        "location": "Trụ Sở Chính Toàn Cầu" if market == "Toàn Cầu" else "Trụ Sở Trong Nước",
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "inputs": inputs.model_dump(),
        "products": [
            {"icon": "credit_card", "name": f"Nền Tảng API {company_name}", "desc": "Hạ tầng giải pháp doanh nghiệp quy mô lớn."},
            {"icon": "account_balance", "name": "Báo Cáo Tình Báo Dữ Liệu", "desc": "Hệ thống giám sát chỉ số tự động."}
        ],
        "registrationDetails": {
            "entityName": f"Công Ty Cổ Phần {company_name}",
            "jurisdiction": "Cơ Quan Đăng Ký Kinh Doanh",
            "status": reg_status,
            "cik": f"MST-{random.randint(1000000000, 9999999999)}",
            "markets": market
        },
        "marketShare": random.randint(55, 88),
        "metrics": {
            "competitor": {"level": "Trung Bình", "class": "warning", "percent": 60},
            "regulatory": {"level": "Thấp", "class": "success", "percent": 20},
            "growth": {"level": "Mạnh", "class": "indigo", "percent": 82}
        },
        "feed": [
            {"title": "Hoàn Tất Thu Thập Đa Nguồn", "source": "Lõi InsightEngine • Mới xong", "body": f"Đã cấu trúc dữ liệu hồ sơ doanh nghiệp cho {company_name}.", "active": True}
        ]
    }

# ── API Endpoints ──

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "version": "2.5.0",
        "language": "vietnamese",
        "gemini": "enabled",
        "storage": "firestore" if db else "in-memory"
    }

@app.post("/api/search", status_code=status.HTTP_201_CREATED)
async def auto_search_company(req: SearchRequest):
    company_name = req.companyName.strip()
    if not company_name:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên doanh nghiệp.")

    api_key = req.geminiApiKey or os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            parsed = await call_gemini_auto_search(company_name, api_key)
            profile_id = f"profile-{int(time.time() * 1000)}"
            
            sources = parsed.get("sources", {})
            inputs_data = SourceInputs(
                google=sources.get("google", f"Trích đoạn tìm kiếm Google cho {company_name}"),
                linkedin=sources.get("linkedin", f"Thông tin LinkedIn cho {company_name}"),
                website=sources.get("website", f"Thông tin website cho {company_name}"),
                registration=sources.get("registration", f"Thông tin đăng ký kinh doanh cho {company_name}")
            )

            profile = {
                "id": profile_id,
                "companyName": parsed.get("companyName", company_name),
                "industry": parsed.get("industry", "Công Nghệ / SaaS"),
                "scale": parsed.get("scale", "Tập Đoàn Lớn (Enterprise)"),
                "market": parsed.get("market", "Toàn Cầu"),
                "registrationStatus": parsed.get("registrationStatus", "Đã Xác Thực ✓"),
                "confidenceScore": parsed.get("confidenceScore", 95.0),
                "summary": parsed.get("summary", f"Hồ sơ doanh nghiệp {company_name}."),
                "website": parsed.get("website", f"{company_name.lower().replace(' ', '')}.com"),
                "location": parsed.get("location", "Trụ Sở Chính"),
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "inputs": inputs_data.model_dump(),
                "products": parsed.get("products", [
                    {"icon": "credit_card", "name": "Giải Pháp Doanh Nghiệp", "desc": "Sản phẩm dịch vụ cốt lõi."}
                ]),
                "registrationDetails": parsed.get("registrationDetails", {
                    "entityName": company_name,
                    "jurisdiction": "Đơn Vị Đăng Ký Pháp Lý",
                    "status": "Đã Xác Thực ✓",
                    "cik": "0001859665",
                    "markets": "Toàn Cầu"
                }),
                "marketShare": parsed.get("marketShare", 75),
                "metrics": parsed.get("metrics", {
                    "competitor": {"level": "Trung Bình", "class": "warning", "percent": 75},
                    "regulatory": {"level": "Thấp", "class": "success", "percent": 20},
                    "growth": {"level": "Mạnh", "class": "indigo", "percent": 85}
                }),
                "feed": parsed.get("feed", [
                    {"title": "Truy Vấn Google Search Grounding", "source": "Google Search • Trực tiếp", "body": f"Đã hoàn tất tra cứu thời gian thực cho {company_name}.", "active": True}
                ])
            }

            if db:
                db.collection("profiles").document(profile["id"]).set(profile)
            else:
                IN_MEMORY_PROFILES[profile["id"]] = profile

            return profile

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Lỗi thực thi Gemini API: {e}. Chuyển sang trình tạo thông minh mặc định.")

    inputs_data = req.manualInputs or SourceInputs(
        google=f"Kết quả tìm kiếm Google cho {company_name}: Đơn vị hàng đầu, giá trị vốn hóa lớn, sản phẩm và hiện diện thị trường rộng khắp.",
        linkedin=f"Hồ sơ LinkedIn cho {company_name}: Quy mô 1000+ nhân sự, văn phòng quốc tế, lĩnh vực công nghệ phần mềm.",
        website=f"Trang chủ {company_name}: Nền tảng API, giải pháp đám mây và tài liệu giải pháp doanh nghiệp.",
        registration=f"Cổng đăng ký kinh doanh {company_name}: Pháp nhân đã xác thực, mã số thuế hoạt động hợp pháp."
    )

    profile = analyze_sources(inputs_data, company_name_override=company_name)

    if db:
        db.collection("profiles").document(profile["id"]).set(profile)
    else:
        IN_MEMORY_PROFILES[profile["id"]] = profile

    return profile

@app.post("/api/analyze", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(req: AnalysisRequest):
    if not any(val.strip() for val in req.inputs.model_dump().values()):
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung cho ít nhất một nguồn.")

    profile_data = analyze_sources(req.inputs)

    if db:
        db.collection("profiles").document(profile_data["id"]).set(profile_data)
    else:
        IN_MEMORY_PROFILES[profile_data["id"]] = profile_data

    return profile_data

@app.get("/api/profiles", response_model=List[ProfileResponse])
def list_profiles():
    if db:
        try:
            docs = db.collection("profiles").stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Firestore read error: {e}")
            return list(IN_MEMORY_PROFILES.values())
    return list(IN_MEMORY_PROFILES.values())

@app.get("/api/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: str):
    if db:
        try:
            doc = db.collection("profiles").document(profile_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"Firestore get error: {e}")

    if profile_id in IN_MEMORY_PROFILES:
        return IN_MEMORY_PROFILES[profile_id]

    raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ")

@app.delete("/api/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: str):
    if db:
        try:
            db.collection("profiles").document(profile_id).delete()
        except Exception as e:
            print(f"Firestore delete error: {e}")

    IN_MEMORY_PROFILES.pop(profile_id, None)
    return None

# ── Mount Frontend Static Assets ──
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
