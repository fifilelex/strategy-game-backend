# Strategy game

## What is the project?

This project is an economic simulation where the backend manages game state, calculations, and business rules. The client communicates with the backend through an API but does not directly control game data.

## What are main concepts?

The game is played in turns. During each turn, the player's money is updated based on their income sources. Income can either increase or decrease depending on current game conditions.

The player can increase their income by purchasing various income sources (called items). Items are stored and managed by the backend, which controls ownership and their effect on the player's economy.


# Architecture

Project is split into 4 main layers:

API
|
SERVICE
|
REPOSITORY
|
DATABASE

## Why does the separation exist?

The purpose of this separation is to isolate responsibilities:

- API does not contain business logic.
- Services do not know database implementation details.
- Repositories handle persistence only.

This makes the system easier to modify, test, and extend.

## API layer

Responsible for:

- HTTP endpoints
- Request handling and validation through schemas
- Converting requests into service calls
- Response formatting

## Service layer

Responsible for:

- Business rules
- Validation beyond schemas
- Coordinating repositories
- Containing game logic

## Repository layer

Responsible for:

- Database communication
- SQL queries
- Managing persistence operations

# Domain model

The domain represents an economic simulation where players manage their economy by acquiring income sources and progressing through turns.

## Player

A player represents a participant in the simulation.

The player has its own game state, including financial information and owned income sources.

Players do not directly modify their game data. All changes are performed through the backend, which validates actions and applies game rules.

## Game state

Game state represents the current progress of a player's simulation.

It stores information required to continue the game, such as current money, income, and progression.

Game state is modified during turns based on current player conditions.

## Turn

A turn represents one calculation cycle of the simulation.

During a turn:
- Player income is calculated.
- Money is updated based on current income sources.
- Game state is modified.

The backend is responsible for performing these calculations.

## Items / Income sources

Items represent assets that can be purchased by players.

Each item can affect the player's economy by increasing or decreasing income.

Ownership defines which income sources belong to a player.

## Relationships

Main relationships:

Player owns income sources.

Income sources affect the player's economic state.

Game state stores the current result of these interactions.

# Technological choices

## Tools

- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy


## Role in the system

### FastAPI

FastAPI provides the HTTP API layer and communication between the client and backend.

It also automatically generates API documentation, which simplified development and testing of endpoints.

### Pydantic

Pydantic defines data schemas used by the application.

It provides validation of incoming and outgoing data, making it easier to control what data can enter and leave the system.

### PostgreSQL

PostgreSQL stores persistent game state.

The backend controls all modifications, preventing clients from directly manipulating game data.

It also provides a relational database structure suitable for storing relations between players, items, and ownership.

### SQLAlchemy

SQLAlchemy provides database abstraction and object-relational mapping.

It reduces the amount of manual database handling and makes database operations easier to maintain.

It also simplified testing by allowing cleaner separation between application logic and database configuration.


# Development choices

## Formatting

### Black

Black automatically formats Python code to maintain consistent style.

### Ruff

Ruff detects common mistakes, unused code, and style issues.

It improves code readability and helps catch potential bugs earlier.


## Testing

### Pytest

Pytest provides a framework for automated testing.

Fixtures simplify preparing required test environments and database states.

It was especially useful during the SQLAlchemy migration because existing behavior could be verified automatically after major changes.