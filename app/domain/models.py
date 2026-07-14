from pydantic import BaseModel, ConfigDict, Field


class IncomeSource(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_gamestate: int = Field(..., ge=0)
    item_id: int = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    income: int = Field(..., gt=0)
    cost: int = Field(..., gt=0)
    description: str = Field(default="", min_length=0)


class IncomeSourceRead(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_id: int = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    income: int = Field(..., gt=0)
    cost: int = Field(..., gt=0)
    description: str = Field(default="", min_length=0)


class IncomeSourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=1)
    income: int = Field(..., gt=0)
    cost: int = Field(..., gt=0)
    description: str = ""


class IncomeSourceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1)
    income: int | None = Field(default=None, gt=0)
    cost: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1)


class GameState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: int = Field(..., ge=0)
    username: str = Field(..., min_length=1)
    turn: int = Field(..., gt=0)
    money: int = Field(..., ge=0)
    income: int = Field(..., ge=0)
    is_active: bool = Field(...)


class GameStateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(..., min_length=1)
    turn: int = Field(..., gt=0)
    money: int = Field(..., ge=0)
    income: int = Field(..., ge=0)
    is_active: bool = Field(...)


class GameStateUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str | None = Field(default=None, min_length=1)
    turn: int | None = Field(default=None, gt=0)
    money: int | None = Field(default=None, ge=0)
    income: int | None = Field(default=None, ge=0)
    is_active: bool | None = Field(default=None)


class Ownership(BaseModel):
    user_id: int = Field(..., ge=0)
    item_id: int = Field(..., ge=0)
