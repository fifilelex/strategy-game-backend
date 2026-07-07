from pydantic import BaseModel, Field


class IncomeSource(BaseModel):
    id_gamestate: int = Field(..., ge=0)
    id: int = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    income: int = Field(..., gt=0)
    cost: int = Field(..., gt=0)
    description: str = ""


class IncomeSourceCreate(BaseModel, extra="forbid"):

    name: str = Field(..., min_length=1)
    income: int = Field(..., gt=0)
    cost: int = Field(..., gt=0)
    description: str = ""


class IncomeSourceUpdate(BaseModel, extra="forbid"):

    name: str | None = Field(default=None, min_length=1)
    income: int | None = Field(default=None, gt=0)
    cost: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1)


class GameState(BaseModel):
    uid: int = Field(..., ge=0)
    username: str = Field(..., min_length=1)
    turn: int = Field(..., gt=0)
    money: int = Field(..., ge=0)
    income: int = Field(..., ge=0)
    is_active: bool = Field(...)

    def get_state(self):
        return self.turn, self.money, self.income


class GameStateCreate(BaseModel):

    username: str = Field(..., min_length=1)
    turn: int = Field(..., gt=0)
    money: int = Field(..., ge=0)
    income: int = Field(..., ge=0)
    is_active: bool = Field(...)


class GameStateUpdate(BaseModel):

    username: str | None = Field(default=None, min_length=1)
    turn: int | None = Field(default=None, gt=0)
    money: int | None = Field(default=None, ge=0)
    income: int | None = Field(default=None, ge=0)
    is_active: bool | None = Field(default=None)
