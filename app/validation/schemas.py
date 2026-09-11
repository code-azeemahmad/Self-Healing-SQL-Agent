from pydantic import BaseModel, ConfigDict, Field


class SQLGeneration(BaseModel):
    """
    Structured SQL generated from the user's request.
    """

    model_config = ConfigDict(extra="forbid")

    sql: str = Field(
        min_length=1,
        max_length=20_000,
        description="A single PostgreSQL SELECT statement.",
    )


class SQLRepair(BaseModel):
    """
    Structured output produced when repairing a failed SQL query.
    """

    model_config = ConfigDict(extra="forbid")

    corrected_sql: str = Field(
        min_length=1,
        max_length=20_000,
        description="The corrected PostgreSQL SELECT statement.",
    )

    diagnosis: str = Field(
        min_length=1,
        max_length=2_000,
        description="Concise explanation of the SQL failure.",
    )

    repair_reason: str = Field(
        min_length=1,
        max_length=2_000,
        description="What was changed to repair the SQL.",
    )


class ValidatedSQL(BaseModel):
    """
    SQL that passed application-level safety validation.
    """

    model_config = ConfigDict(extra="forbid")

    sql: str = Field(
        min_length=1,
        max_length=20_000,
    )