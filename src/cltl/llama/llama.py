import random
import re
from openai import OpenAI

from cltl.llama.api import Llama

class LlamaImpl(Llama):
    def __init__(self, language="Dutch", port="9001"):
        self._language = language
        self._port = port
        url = "http://localhost:"+self._port+"/v1"
        self._client = OpenAI(base_url=url, api_key="not-needed")
        self._history = [
            {"role": "system", "content": "You are an intelligent assistant. \
            You always provide well-reasoned answers that are both correct and helpful. You give a concise and short answer only in the "+language+"."},
        ]
        self.started = False

    def _analyze(self, statement):
        self._history.append({"role": "user", "content": statement})

        completion = self._client.chat.completions.create(
            model="local-model",  # this field is currently unused
            messages=self._history,
            temperature=0.0,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}

        for chunk in completion:
            if chunk.choices[0].delta.content:
                #print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content
        self._history.append(new_message)
        return new_message["content"]




if __name__ == "__main__":
    language="Dutch"
    port = "9001"
    llama = LlamaImpl(language, port)
    userinput ="Wat zijn Schwartz waarden?"
    while not userinput.lower() in ["quit", "exit"]:
        response = llama._analyze(userinput)
        print(response['content'])
        userinput=input("> ")