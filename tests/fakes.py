class FakeSQLGenerator:
    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, *args, **kwargs) -> str:
        self.calls += 1

        if self.calls == 1:
            return "SELECT customer_name FROM customers"

        return "SELECT name FROM customers"