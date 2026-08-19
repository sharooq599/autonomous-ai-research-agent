const API_BASE_URL = "http://127.0.0.1:8000";


// ============================================================
// Research API
// ============================================================

export async function researchQuestion(
  question,
  conversationId = null
) {

  const response = await fetch(
    `${API_BASE_URL}/api/research`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question: question,
        conversation_id: conversationId,
      }),
    }
  );


  if (!response.ok) {

    const errorText = await response.text();

    throw new Error(
      `Research request failed: ${errorText}`
    );
  }


  return await response.json();
}


// ============================================================
// Get Conversations
// ============================================================

export async function getConversations() {

  const response = await fetch(
    `${API_BASE_URL}/api/conversations`
  );


  if (!response.ok) {

    throw new Error(
      "Failed to load conversations"
    );
  }


  return await response.json();
}


// ============================================================
// Get Conversation History
// ============================================================

export async function getConversationHistory(
  conversationId
) {

  const response = await fetch(
    `${API_BASE_URL}/api/conversations/${conversationId}`
  );


  if (!response.ok) {

    throw new Error(
      "Failed to load conversation history"
    );
  }


  return await response.json();
}