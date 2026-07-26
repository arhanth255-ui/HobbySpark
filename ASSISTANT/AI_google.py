from google import genai
import os

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

response = client.chats.create(
    model="gemini-2.5-flash"
)
res = response.send_message("""Make a proffesional docstring for the following. Follow a pattern like:
                1.Prints the given arg(string) to the serial moniter.
                2.Takes input from the serial moniter, returning a string.
            Do not show arguments make the docstrings one line docstrings.""")
print("RES= ", res.text)
while True:
    a = input("PROMPT-> ")
    res = response.send_message(a)
    print("GEMINI->",res.text)

