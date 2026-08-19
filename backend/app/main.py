from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.graph.workflow import research_graph

from app.memory.database import (
    create_tables,
    create_conversation,
    save_message,
    get_conversations,
    get_conversation_messages,
)


app = FastAPI(
    title="Autonomous AI Research Agent",
    description="AI-powered autonomous research system",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Schema
# ============================================================

class ResearchRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Research question asked by the user",
        examples=[
            "What is LangGraph?"
        ]
    )

    conversation_id: int | None = Field(
        default=None,
        description=(
            "Existing conversation ID. "
            "Leave empty to create a new conversation."
        ),
        examples=[
            None
        ]
    )


# ============================================================
# Startup
# ============================================================

@app.on_event("startup")
def startup():

    create_tables()


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Autonomous AI Research Agent API is running!"
    }


# ============================================================
# Get All Conversations
# ============================================================

@app.get("/api/conversations")
def conversations():

    try:

        return {
            "conversations": get_conversations()
        }

    except Exception as error:

        print(
            "Conversation loading error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to load conversations."
        )


# ============================================================
# Get Conversation History
# ============================================================

@app.get("/api/conversations/{conversation_id}")
def conversation_history(
    conversation_id: int
):

    try:

        messages = get_conversation_messages(
            conversation_id
        )

        return {
            "conversation_id": conversation_id,
            "messages": messages
        }

    except Exception as error:

        print(
            "Conversation history error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to load conversation history."
        )


# ============================================================
# Research
# ============================================================

@app.post("/api/research")
def research(
    request: ResearchRequest
):

    # ========================================================
    # 1. Validate question
    # ========================================================

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Research question cannot be empty."
        )


    # ========================================================
    # 2. Get existing conversation OR create new conversation
    # ========================================================

    try:

        if request.conversation_id is not None:

            conversation_id = request.conversation_id

        else:

            conversation_id = create_conversation()

    except Exception as error:

        print(
            "Conversation creation error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create conversation."
        )


    # ========================================================
    # 3. Load previous conversation history
    # ========================================================

    try:

        previous_messages = get_conversation_messages(
            conversation_id
        )

    except Exception as error:

        print(
            "Conversation history loading error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to load conversation history."
        )


    # ========================================================
    # 4. Convert database messages to LangChain messages
    # ========================================================

    messages = []

    for message in previous_messages:

        if message["role"] == "user":

            messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=message["content"]
                )
            )


    # ========================================================
    # 5. Add current user question
    # ========================================================

    messages.append(
        HumanMessage(
            content=question
        )
    )


    # ========================================================
    # 6. Save current user question
    # ========================================================

    try:

        save_message(
            conversation_id,
            "user",
            question
        )

    except Exception as error:

        print(
            "User message save error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to save your question."
        )


    # ========================================================
    # 7. Run LangGraph
    # ========================================================

    try:

        result = research_graph.invoke(
            {
                "question": question,
                "messages": messages
            }
        )

    except Exception as error:

        print(
            "Research workflow error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Research failed. "
                "Please try again."
            )
        )


    # ========================================================
    # 8. Validate final response
    # ========================================================

    try:

        result_messages = result.get(
            "messages",
            []
        )

        if not result_messages:

            raise ValueError(
                "No messages returned from research graph."
            )

        final_message = result_messages[-1]

        final_answer = final_message.content

        if not final_answer:

            raise ValueError(
                "Final research answer is empty."
            )

    except Exception as error:

        print(
            "Final response error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Research completed, "
                "but no final answer was generated."
            )
        )


    # ========================================================
    # 9. Save assistant answer
    # ========================================================

    try:

        save_message(
            conversation_id,
            "assistant",
            final_answer
        )

    except Exception as error:

        print(
            "Assistant message save error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Research completed, "
                "but the answer could not be saved."
            )
        )


    # ========================================================
    # 10. Return response
    # ========================================================

    return {

        "conversation_id": conversation_id,

        "question": question,

        "research_plan": result.get(
            "research_plan",
            []
        ),

        "research_results": result.get(
            "research_results",
            []
        ),

        "answer": final_answer
    }