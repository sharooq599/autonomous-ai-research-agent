import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {

  // ============================================================
  // STATE
  // ============================================================

  const [conversations, setConversations] = useState([]);

  const [selectedConversation, setSelectedConversation] =
    useState(null);

  const [messages, setMessages] = useState([]);

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const [researchStep, setResearchStep] = useState(0);


  // ============================================================
  // RESEARCH STATUS
  // ============================================================

  const researchSteps = [
    {
      icon: "🔍",
      text: "Understanding your research question"
    },
    {
      icon: "🌐",
      text: "Searching the web for information"
    },
    {
      icon: "🧠",
      text: "Analyzing and comparing information"
    },
    {
      icon: "📝",
      text: "Generating your research report"
    }
  ];


  // ============================================================
  // LOAD CONVERSATIONS
  // ============================================================

  useEffect(() => {

    loadConversations();

  }, []);


  // ============================================================
  // RESEARCH STEP ANIMATION
  // ============================================================

  useEffect(() => {

    if (!loading) {

      setResearchStep(0);

      return;

    }


    setResearchStep(0);


    const interval = setInterval(() => {

      setResearchStep((previousStep) => {

        if (
          previousStep <
          researchSteps.length - 1
        ) {

          return previousStep + 1;

        }

        return previousStep;

      });

    }, 2500);


    return () => clearInterval(interval);

  }, [loading]);


  // ============================================================
  // GET ALL CONVERSATIONS
  // ============================================================

  const loadConversations = async () => {

    try {

      const response = await fetch(
        `${API_URL}/api/conversations`
      );

      const data = await response.json();

      setConversations(
        data.conversations || []
      );

    } catch (error) {

      console.error(
        "Failed to load conversations:",
        error
      );

    }

  };


  // ============================================================
  // LOAD CONVERSATION
  // ============================================================

  const loadConversation = async (
    conversationId
  ) => {

    try {

      setSelectedConversation(
        conversationId
      );

      const response = await fetch(
        `${API_URL}/api/conversations/${conversationId}`
      );

      const data = await response.json();

      setMessages(
        data.messages || []
      );

    } catch (error) {

      console.error(
        "Failed to load conversation:",
        error
      );

    }

  };


  // ============================================================
  // SEND RESEARCH QUESTION
  // ============================================================

  const sendResearch = async () => {

    if (
      !question.trim() ||
      loading
    ) {

      return;

    }


    setLoading(true);

    setResearchStep(0);


    try {

      const response = await fetch(
        `${API_URL}/api/research`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            question: question,

            conversation_id:
              selectedConversation

          })

        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Research failed"
        );

      }


      // --------------------------------------------------------
      // Save conversation ID
      // --------------------------------------------------------

      setSelectedConversation(
        data.conversation_id
      );


      // --------------------------------------------------------
      // Reload conversations
      // --------------------------------------------------------

      await loadConversations();


      // --------------------------------------------------------
      // Load complete conversation
      // --------------------------------------------------------

      await loadConversation(
        data.conversation_id
      );


      // --------------------------------------------------------
      // Clear input
      // --------------------------------------------------------

      setQuestion("");


    } catch (error) {

      console.error(
        "Research error:",
        error
      );

      alert(
        "Something went wrong. Check the backend terminal."
      );

    } finally {

      setLoading(false);

    }

  };


  // ============================================================
  // NEW RESEARCH
  // ============================================================

  const newResearch = () => {

    setSelectedConversation(null);

    setMessages([]);

    setQuestion("");

    setLoading(false);

  };


  // ============================================================
  // ENTER KEY
  // ============================================================

  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      sendResearch();

    }

  };


  // ============================================================
  // UI
  // ============================================================

  return (

    <div className="flex h-screen bg-slate-950 text-white">


      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="w-72 shrink-0 border-r border-white/10 bg-slate-900/80 p-5">

        {/* Logo */}

        <div className="mb-8 flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 text-xl shadow-lg shadow-blue-500/20">

            🤖

          </div>

          <div>

            <h2 className="text-lg font-bold">
              Research Agent
            </h2>

            <p className="text-xs text-slate-400">
              AI Research Assistant
            </p>

          </div>

        </div>


        {/* New Research */}

        <button
          onClick={newResearch}
          disabled={loading}
          className="mb-8 w-full rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 font-semibold shadow-lg shadow-blue-500/20 transition hover:scale-[1.02] hover:from-blue-500 hover:to-purple-500 disabled:cursor-not-allowed disabled:opacity-50"
        >

          + New Research

        </button>


        {/* Conversations */}

        <div>

          <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-slate-500">

            Conversations

          </h3>


          {conversations.length === 0 ? (

            <p className="text-sm text-slate-500">

              No conversations yet

            </p>

          ) : (

            <div className="space-y-2">

              {conversations.map(
                (conversation) => (

                  <button
                    key={conversation.id}
                    onClick={() =>
                      loadConversation(
                        conversation.id
                      )
                    }
                    disabled={loading}
                    className={`w-full rounded-lg px-3 py-3 text-left text-sm transition ${
                      selectedConversation ===
                      conversation.id

                        ? "bg-blue-600/20 text-blue-300"

                        : "text-slate-300 hover:bg-white/5"
                    }`}
                  >

                    <div className="truncate">

                      {conversation.title ||
                        `Conversation #${conversation.id}`}

                    </div>

                  </button>

                )
              )}

            </div>

          )}

        </div>

      </aside>


      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="flex min-w-0 flex-1 flex-col">


        {/* ==================================================
            HEADER
        ================================================== */}

        <header className="border-b border-white/10 px-8 py-6">

          <h1 className="text-2xl font-bold">

            Autonomous AI Research Agent

          </h1>

          <p className="mt-1 text-sm text-slate-400">

            Research complex topics with AI-powered web search

          </p>

        </header>


        {/* ==================================================
            CHAT AREA
        ================================================== */}

        <section className="relative flex flex-1 flex-col overflow-hidden">


          {/* ==================================================
              MESSAGES
          ================================================== */}

          <div className="flex-1 overflow-y-auto px-8 py-8">


            {messages.length === 0 && !loading ? (

              /* =================================================
                 WELCOME
              ================================================= */

              <div className="flex h-full flex-col items-center justify-center text-center">

                <div className="mb-6 text-6xl">

                  🤖

                </div>

                <h2 className="text-3xl font-bold">

                  What would you like me to research?

                </h2>

                <p className="mt-4 max-w-xl text-slate-400">

                  Ask a question and I'll research the web,
                  analyze the information, and generate a
                  detailed report.

                </p>

              </div>

            ) : (

              /* =================================================
                 MESSAGES
              ================================================= */

              <div className="mx-auto max-w-4xl space-y-6">

                {messages.map(
                  (message, index) => (

                    <div
                      key={index}
                      className={
                        message.role === "user"
                          ? "flex justify-end"
                          : "flex justify-start"
                      }
                    >

                      <div
                        className={
                          message.role === "user"

                            ? "max-w-[80%] rounded-2xl rounded-br-md bg-blue-600 px-5 py-4 shadow-lg"

                            : "max-w-[90%] rounded-2xl rounded-bl-md border border-white/10 bg-slate-900 px-5 py-4 shadow-lg"
                        }
                      >

                        <div className="mb-2 text-xs font-semibold text-slate-400">

                          {message.role === "user"
                            ? "You"
                            : "🤖 Research Agent"}

                        </div>

                        <div className="whitespace-pre-wrap text-sm leading-7">

                          {message.content}

                        </div>

                      </div>

                    </div>

                  )
                )}


                {/* =================================================
                   RESEARCHING ANIMATION
                ================================================= */}

                {loading && (

                  <div className="flex justify-start">

                    <div className="w-full max-w-2xl rounded-2xl border border-blue-500/20 bg-slate-900/80 p-6 shadow-xl shadow-blue-500/5">


                      {/* Agent Header */}

                      <div className="mb-5 flex items-center gap-4">

                        <div className="relative flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 text-xl shadow-lg shadow-blue-500/30">

                          🤖

                          <span className="absolute inset-0 animate-ping rounded-full bg-blue-500/20"></span>

                        </div>


                        <div>

                          <h3 className="font-semibold">

                            Research Agent is working

                          </h3>

                          <p className="text-sm text-slate-400">

                            Please wait while I research your question...

                          </p>

                        </div>

                      </div>


                      {/* Progress Bar */}

                      <div className="mb-6 h-2 overflow-hidden rounded-full bg-slate-800">

                        <div
                          className="h-full rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-1000"
                          style={{
                            width: `${(
                              (researchStep + 1) /
                              researchSteps.length
                            ) * 100}%`
                          }}
                        />

                      </div>


                      {/* Steps */}

                      <div className="space-y-4">

                        {researchSteps.map(
                          (step, index) => {

                            const completed =
                              index <
                              researchStep;

                            const active =
                              index ===
                              researchStep;


                            return (

                              <div
                                key={index}
                                className={`flex items-center gap-4 transition-all duration-500 ${
                                  index >
                                  researchStep
                                    ? "opacity-40"
                                    : "opacity-100"
                                }`}
                              >

                                {/* Status Circle */}

                                <div
                                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full ${
                                    completed
                                      ? "bg-green-500/20 text-green-400"

                                      : active
                                      ? "bg-blue-500/20 text-blue-400"

                                      : "bg-slate-800 text-slate-500"
                                  }`}
                                >

                                  {completed ? (

                                    "✓"

                                  ) : active ? (

                                    <span className="animate-spin">

                                      ⟳

                                    </span>

                                  ) : (

                                    step.icon

                                  )}

                                </div>


                                {/* Step Text */}

                                <div className="flex-1">

                                  <p
                                    className={`text-sm ${
                                      active
                                        ? "font-semibold text-white"
                                        : completed
                                        ? "text-green-400"
                                        : "text-slate-500"
                                    }`}
                                  >

                                    {step.text}

                                  </p>

                                </div>


                                {/* Active Indicator */}

                                {active && (

                                  <div className="flex gap-1">

                                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-blue-400"></span>

                                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-blue-400 [animation-delay:150ms]"></span>

                                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-blue-400 [animation-delay:300ms]"></span>

                                  </div>

                                )}

                              </div>

                            );

                          }
                        )}

                      </div>


                      {/* Bottom Message */}

                      <div className="mt-6 rounded-lg border border-blue-500/10 bg-blue-500/5 px-4 py-3 text-center text-xs text-slate-400">

                        🔎 Searching → 🧠 Analyzing → 📝 Writing report

                      </div>

                    </div>

                  </div>

                )}

              </div>

            )}

          </div>


          {/* ==================================================
              INPUT AREA
          ================================================== */}

          <div className="border-t border-white/10 bg-slate-950/90 px-8 py-5">

            <div className="mx-auto max-w-4xl">


              <div className="relative rounded-2xl border border-white/10 bg-slate-900 p-3 shadow-xl">


                <textarea
                  value={question}
                  onChange={(event) =>
                    setQuestion(
                      event.target.value
                    )
                  }
                  onKeyDown={handleKeyDown}
                  placeholder={
                    loading
                      ? "Researching your question..."
                      : "Ask a research question..."
                  }
                  rows="3"
                  disabled={loading}
                  className="w-full resize-none bg-transparent px-3 py-2 text-sm text-white outline-none placeholder:text-slate-500 disabled:cursor-not-allowed"
                />


                <div className="flex items-center justify-between px-2 pt-2">


                  <p className="text-xs text-slate-500">

                    Press Enter to send · Shift + Enter for a new line

                  </p>


                  <button
                    onClick={sendResearch}
                    disabled={
                      loading ||
                      !question.trim()
                    }
                    className="rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 text-sm font-semibold shadow-lg shadow-blue-500/20 transition hover:scale-105 hover:from-blue-500 hover:to-purple-500 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:scale-100"
                  >

                    {loading ? (

                      <span className="flex items-center gap-2">

                        <span className="animate-spin">

                          ⟳

                        </span>

                        Researching...

                      </span>

                    ) : (

                      "Send 🚀"

                    )}

                  </button>


                </div>

              </div>

            </div>

          </div>

        </section>

      </main>

    </div>

  );

}

export default App;