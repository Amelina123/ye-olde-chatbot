from chatbot import Chatbot

bot = Chatbot()


# encoded = bot.encode_prompt("Hello, how are you?")
# print(encoded)  

# reply = bot.decode_reply([15496, 703, 345, 30]) # Pass in a string of generated token IDs here from your tokenizer
# print(reply)

# prompt = "What is the weather like today?"
# reply = bot.generate_reply(prompt)
# print(f"Prompt: {prompt}")
# print(f"Reply: {reply}")

# prompts = [
#     "What's your name?",
#     "What do you think about AI?",
#     "Sorry, tell me your name again."
# ]

# for prompt in prompts:
#     reply = bot.generate_reply(prompt)
#     print(f"Prompt: {prompt}")
#     print(f"Reply: {reply}\n")

# bot.reset_history()

print(f" Hello, I am glad to talk to you.")
print("\n--- System prompt ---")
print(bot.system_prompt.strip())
print("---------------------\n")
print("Type :q or exit to leave.\n")
name = input("Enter your name:")
bot.history.append((f"My name is {name}.", "Nice to meet you!"))
print(f" Hello, {name}\n Enter your massege or question")
exit_conditions = (":q", "exit")
while True:
    prompt = input("User: ")
    if prompt.strip().lower() in exit_conditions:
        print("Goodbye!")
        break
    
    reply = bot.generate_reply(prompt)
    print(f"Chatbot: {reply}\n")
bot.reset_history()
