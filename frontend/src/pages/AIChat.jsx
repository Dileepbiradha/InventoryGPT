import { useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function AIChat() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askAI = async () => {

    try {

      console.log("Sending question:", question);

      const response = await api.post(
        "/ai-inventory",
        {
          question
        }
      );

      console.log("AI Response:", response.data);

      setAnswer(
        response.data.answer
      );

    } catch (error) {

      console.error("AI Error:", error);

      if (error.response) {

        setAnswer(
          error.response.data.error ||
          error.response.data.answer ||
          "Backend returned an error"
        );

      } else {

        setAnswer(
          "Cannot connect to backend server"
        );
      }
    }
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>

        <h1>Inventory AI Assistant</h1>

        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          style={{
            width: "500px",
            padding: "10px"
          }}
        />

        <button
          onClick={askAI}
          style={{
            marginLeft: "10px",
            padding: "10px"
          }}
        >
          Ask
        </button>

        <div
          style={{
            marginTop: "30px",
            border: "1px solid gray",
            padding: "20px"
          }}
        >
          <strong>Answer:</strong>
          <pre
            style={{
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            fontFamily: "inherit"
          }}
        >
          {answer}
        </pre>
        </div>

      </div>
    </>
  );
}

export default AIChat;