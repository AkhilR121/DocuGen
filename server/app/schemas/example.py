from pydantic import BaseModel


class ExampleBase(BaseModel):
    title: str
    description: str | None = None


class ExampleCreate(ExampleBase):
    pass


class ExampleUpdate(ExampleBase):
    title: str | None = None


class ExampleInDBBase(ExampleBase):
    id: int

    class Config:
        from_attributes = True


class Example(ExampleInDBBase):
    pass
