"""Reusable Ollama agent wrapper."""

from typing import Any

from ollama import chat


class OllamaAgent:
    #"""An Ollama chat agent configured with a system prompt and tools."""

    def __init__(self, model: str) -> None:
        self.model = model
        self._System_Prompt = ""
        self._Tools_list: list[dict[str, Any]] = []

    @property
    def System_Prompt(self) -> str:
        #"""Return the system instruction sent with each request."""
        return self._System_Prompt

    @System_Prompt.setter
    def System_Prompt(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("System_Prompt must be a string.")
        self._System_Prompt = value

    @property
    def Tools_list(self) -> list[dict[str, Any]]:
       # """Return the Ollama tool definitions available to the agent."""
        return self._Tools_list

    @Tools_list.setter
    def Tools_list(self, value: list[dict[str, Any]]) -> None:
        if not isinstance(value, list) or not all(isinstance(tool, dict) for tool in value):
            raise TypeError("Tools_list must be a list of objects (dictionaries).")
        self._Tools_list = value

    def askAgent(self, question: str) -> str:
       # """Send a question to Ollama and return the agent's text response."""
        if not isinstance(question, str):
            raise TypeError("question must be a string.")

        messages = [
            {"role": "system", "content": self.System_Prompt},
            {"role": "user", "content": question},
        ]
        response = chat(
            model=self.model,
            messages=messages,
            tools=self.Tools_list or None,
        )
        return response.message.content or ""
