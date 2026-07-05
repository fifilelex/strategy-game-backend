from dataclasses import dataclass

from pydantic import BaseModel


class IncomeSource(BaseModel):
    id_gamestate: int
    id: int
    name: str
    income: int
    cost: int
    description: str = ""


class IncomeSourceCreate(BaseModel, extra="forbid"):

    name: str
    income: int
    cost: int
    description: str = ""


class IncomeSourceUpdate(BaseModel, extra="forbid"):

    name: str | None = None
    income: int | None = None
    cost: int | None = None
    description: str | None = None


@dataclass
class GameState:  # game_data
    uid: int
    username: str
    turn: int
    money: int
    income: int
    is_active: bool

    def get_state(self):
        return self.turn, self.money, self.income


class GameStateCreate(BaseModel):

    username: str
    turn: int
    money: int
    income: int
    is_active: bool


class GameStateUpdate(BaseModel):

    username: str | None = None
    turn: int | None = None
    money: int | None = None
    income: int | None = None
    is_active: bool | None = None
