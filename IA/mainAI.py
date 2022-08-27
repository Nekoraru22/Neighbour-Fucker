import openai, re

class AI:
    """A library to connect with GPT-3 AI"""

    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key
        open("IA/temp.txt", "w+").write(open("IA/prompt.txt", "r").read())

    def get(self, string: str) -> str:
        """Gathers an answer to the question"""

        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=open("IA/temp.txt", "r").read(),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Stranger:", " Me:"]
        )

        if "This model's maximum context length is 2049 tokens" in response:
            self.clear()
            open("IA/temp.txt", "a").write(f"{string}\nAI:")
            return self.get(string)

        if "You exceeded your current quota" in response: return
        return response

    def clear(self) -> None:
        open("IA/temp.txt", "w+").write(open("IA/prompt.txt", "r").read())

    def question(self, ans: str) -> str:
        """Receives the question and processes it"""

        open("IA/temp.txt", "a").write(f"{ans}\nAI:")
        
        out = self.get(ans)["choices"][0]["text"]
        fin = re.sub(r"^([\n]+)|([\n]+)$", "", str(out), 0, re.MULTILINE)
        
        open("IA/temp.txt", "a").write(f" {fin}\n\nHuman: ")
        return fin