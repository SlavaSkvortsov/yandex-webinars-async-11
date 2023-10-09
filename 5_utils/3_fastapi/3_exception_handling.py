import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()



router = APIRouter()

@router.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException) -> JSONResponse:
    return JSONResponse(
        status_code=418,
        content={'message': f'Oops! {exc.name} did something. There goes a rainbow...'},
    )


@router.get('/unicorns/{name}')
async def read_unicorn(name: str) -> dict[str, str]:
    if name == 'yolo':
        raise UnicornException(name=name)
    return {'unicorn_name': name}


if __name__ == '__main__':
    uvicorn.run(app)
