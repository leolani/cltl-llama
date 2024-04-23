import abc


class Llama(abc.ABC):
    def respond(self, statement: str) -> str:
        raise NotImplementedError("")
