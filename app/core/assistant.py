from abc import ABC, abstractmethod


class Assistant(ABC):
    @abstractmethod
    def get_response_for_prompt(self, prompt: str) -> str:
        pass
