from agno import Agent, AgentContext
from typing import Any, Dict, Optional

class BaseAgent(Agent):
    def __init__(self, context: Optional[AgentContext] = None):
        super().__init__(context)
        self.state: Dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize the agent with any necessary setup."""
        pass

    async def process(self, input_data: Any) -> Any:
        """Process input data and return a response."""
        raise NotImplementedError("Subclasses must implement process method")

    async def cleanup(self) -> None:
        """Clean up any resources used by the agent."""
        pass 