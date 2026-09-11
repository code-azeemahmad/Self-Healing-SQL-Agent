from pydantic import BaseModel, ConfigDict, Field


class SQLGeneration(BaseModel):
    """
    Raw structured output produced by the LLM.
    This does not imply that the SQL is safe to execute.
    """

    model_config = ConfigDict(extra="forbid")

    sql: str = Field(
        min_length=1,
        max_length=20_000,
        description="A single PostgreSQL SELECT statement.",
    )


class ValidatedSQL(BaseModel):
    """
    SQL that has passed the application safety policy.
    """

    model_config = ConfigDict(extra="forbid")

    sql: str = Field(
        min_length=1,
        max_length=20_000,
    )