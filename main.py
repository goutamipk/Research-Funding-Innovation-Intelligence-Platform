import time
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logger import logger
from app.core.middleware import setup_middleware
from app.datasets.dataset_loader import dataset_loader
from app.services.grant_service import grant_service
from app.services.statistics_service import statistics_service
from app.services.patent_service import patent_service
from app.services.recommendation_service import recommendation_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events handler.
    Loads datasets ONCE during startup and initializes all services.
    """
    logger.info(f"Initializing {settings.APP_NAME}...")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")

    # Load grants dataset ONCE during startup
    start_time = time.time()
    logger.info("Loading grants dataset...")
    try:
        df = dataset_loader.load_grants(settings.DATASET_PATH)
        elapsed_seconds = time.time() - start_time
        mem_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
        logger.info(
            f"Grants dataset loaded successfully | "
            f"Rows: {len(df):,} | Columns: {len(df.columns)} | "
            f"Load Time: {elapsed_seconds:.2f}s | Memory: {mem_mb:.2f} MB"
        )

        # Initialize shared services with the loaded DataFrame
        grant_service.initialize(df=df)
        statistics_service.initialize(df=df)
        recommendation_service.initialize_recommender()
    except Exception as e:
        logger.critical(f"Failed to load grants dataset during startup: {str(e)}", exc_info=True)
        raise RuntimeError(f"Startup initialization failed: Could not load grants dataset from '{settings.DATASET_PATH}': {str(e)}") from e

    # Note: PatentService connects directly to data/patents.db SQLite database
    logger.info("PatentService SQLite data-access layer ready.")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}...")


def create_application() -> FastAPI:
    """
    FastAPI Application Factory.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Production-ready FastAPI backend for an AI-powered Research Funding & Patent Intelligence Platform.",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # 1. Setup CORS & Operational Middlewares
    setup_middleware(app)

    # 2. Register Global Exception Handlers
    register_exception_handlers(app)

    # 3. Mount API v1 Router
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # 4. Root & Top-Level Alias Endpoints
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
    async def top_level_health():
        """
        Top-level health check endpoint redirecting to API v1 health handler.
        """
        from app.api.v1.endpoints.health import check_health
        return await check_health()

    return app


app = create_application()

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}...")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
    )
