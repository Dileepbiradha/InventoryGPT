import { useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);

      const response = await api.post(
        "/ai-inventory/",
        {
          question
        }
      );

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);

      setAnswer(
        "Error contacting AI assistant."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div
        style={{
          padding: "30px",
          color: "white",
          background: "#0A0A0A",
          minHeight: "100vh"
        }}
      >
        <h1>AI Inventory Assistant</h1>

        <textarea
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask something about inventory..."
          style={{
            width: "100%",
            height: "120px",
            padding: "10px",
            marginTop: "20px",
            marginBottom: "20px"
          }}
        />

        <button
          onClick={askAI}
          style={{
            background: "#2563EB",
            color: "white",
            border: "none",
            padding: "12px 20px",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Ask AI
        </button>

        {loading && (
          <p style={{ marginTop: "20px" }}>
            Thinking...
          </p>
        )}

        {answer && (
          <div
            style={{
              marginTop: "30px",
              background: "#161616",
              padding: "20px",
              borderRadius: "10px"
            }}
          >
            <h3>Answer</h3>

            <p
              style={{
                whiteSpace: "pre-wrap"
              }}
            >
              {answer}
            </p>
          </div>
        )}
      </div>
    </>
  );
}

export default AIChat;