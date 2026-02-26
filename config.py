# config.py

# Architecture, Hardware, Performance, AI 분야 집중 키워드
KEYWORDS = [
    # 1. Computer Architecture & Hardware
    "architecture", "microarchitecture", "isa", "risc-v", "arm", "x86",
    "processor", "cpu", "gpu", "tpu", "npu", "fpga", "asic",
    "memory", "dram", "hbm", "cxl", "pim", "processing-in-memory",
    "cache", "interconnect", "chiplet", "wafer", "semiconductor",
    
    # 2. Systems for AI (AI Infra & Optimization)
    "llm inference", "model serving", "training system", "distributed learning",
    "cuda", "rocm", "kernel optimization", "quantization", "model compression",
    "ai accelerator", "machine learning system", "mlsys", "hpc",
    
    # 3. Performance & Optimization
    "performance", "latency", "throughput", "bandwidth", "bottleneck",
    "optimization", "profiling", "parallelism", "concurrency",
    "compiler", "llvm", "simd", "vectorization"
]

RSS_SOURCES = [
    {"name": "GeekNews", "url": "https://news.hada.io/rss"},
    {"name": "Phoronix", "url": "https://www.phoronix.com/rss.php"},
]

GEMINI_MODEL = 'gemini-2.5-flash'

GEMINI_PROMPT_TEMPLATE = """
당신은 Computer Architecture, Hardware, AI System 분야의 전문 연구원입니다.
아래 뉴스 내용을 동료 대학원생에게 브리핑하기 위해, 
'시스템 및 하드웨어 관점'에서 성능 영향, 아키텍처 변화, 기술적 특징 위주로 **3줄 이내로 한글 요약**해주세요.

제목: {title}
내용: {content}
""".strip()
