from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemAlreadyBoughtError,
    ItemDoesExistError,
    ItemDoesNotExistError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesExistError,
    UserDoesNotExistError,
)


def create_handlers(app):

    @app.exception_handler(ItemDoesExistError)
    def item_does_exist_handler(
        request: Request, exc: ItemDoesExistError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409, content={"error": "Item with such name already exists"}
        )

    @app.exception_handler(DatabaseError)
    def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"error": "Database error"})

    @app.exception_handler(FieldIsEmptyError)
    def field_is_empty_handler(
        request: Request, exc: FieldIsEmptyError
    ) -> JSONResponse:
        return JSONResponse(status_code=400, content={"error": "No fields to update"})

    @app.exception_handler(ItemAlreadyBoughtError)
    def item_already_bought_handler(
        request: Request, exc: ItemAlreadyBoughtError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"error": "Item already bought"})

    @app.exception_handler(ItemDoesNotExistError)
    def item_does_not_exist_handler(
        request: Request, exc: ItemDoesNotExistError
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": "Item not found"})

    @app.exception_handler(ItemNotOwnedError)
    def item_not_owned_handler(
        request: Request, exc: ItemNotOwnedError
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": "Item not owned"})

    @app.exception_handler(NotEnoughMoneyError)
    def not_enough_money_handler(
        request: Request, exc: NotEnoughMoneyError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409, content={"error": "User has not enough money"}
        )

    @app.exception_handler(UserDoesExistError)
    def user_does_exist_handler(
        request: Request, exc: UserDoesExistError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"error": "User already exists"})

    @app.exception_handler(UserDoesNotExistError)
    def user_does_not_exist_handler(
        request: Request, exc: UserDoesNotExistError
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": "User not found"})
