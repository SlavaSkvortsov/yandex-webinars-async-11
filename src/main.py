import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='app_settings.app_title',
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
    )
