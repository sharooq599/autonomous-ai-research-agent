from app.memory.database import (
    create_tables,
    create_conversation,
    save_message,
    get_messages
)


print("Creating tables...")

create_tables()

print("✅ Tables created!")


print("Creating conversation...")

conversation_id = create_conversation()

print(
    f"✅ Conversation created: {conversation_id}"
)


save_message(
    conversation_id,
    "user",
    "What is LangGraph?"
)

save_message(
    conversation_id,
    "assistant",
    "LangGraph is a framework for building stateful AI workflows."
)


messages = get_messages(
    conversation_id
)


print("\nConversation history:")

for message in messages:

    print(
        f"{message['role']}: "
        f"{message['content']}"
    )