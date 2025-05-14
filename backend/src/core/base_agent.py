class BaseAgent:
    async def initialize(self):
        pass

    async def process(self, input_data):
        raise NotImplementedError("Subclasses must implement process method")

    async def cleanup(self):
        pass 