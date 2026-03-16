"""
newd2p - Start FastAPI Server
"""

import uvicorn
from src.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║            newd2p                        ║
    ║     Document → Narrative PPT             ║
    ║                                          ║
    ║  API:  http://localhost:8000             ║
    ║  Docs: http://localhost:8000/docs        ║
    ╚══════════════════════════════════════════╝
    """)

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )