from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from replace_domain.controllers.books_controller import books_router
from replace_domain.controllers.authors_controller import authors_router
from replace_domain.exceptions import ModelNotFoundError, ResponseError


app = FastAPI(title='LMS', version='0.0.1')


@app.exception_handler(ModelNotFoundError)
async def handle_model_not_found(_: Request, exc: ModelNotFoundError) -> Response:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content=ResponseError(
                            title='Data not found',
                            detail=f'{exc.model} with id {exc.id} not found'))


app.include_router(books_router)
app.include_router(authors_router)
