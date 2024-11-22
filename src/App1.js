
import React, { useState, useEffect } from "react";
import "./App.css";

const Loader = () => (
  <div className="loader-container">
    <div className="loader-text">Drinks Handing Bot</div>
  </div>
);

const App = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [listening, setListening] = useState(false);
  const [messages, setMessages] = useState([]);

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  const synth = window.speechSynthesis; // Setup Speech Synthesis

  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  const startListening = () => {
    setListening(true);
    recognition.start();
  };

  const stopListening = () => {
    setListening(false);
    recognition.stop();
  };

  recognition.onresult = (event) => {
    const transcriptMessage = event.results[0][0].transcript;
    setMessage(transcriptMessage);
    stopListening();
    handleMessage(transcriptMessage);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    stopListening();
  };

  const handleMessage = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, user: true },
    ]);

    // Check for "hello" in the message
    if (message.toLowerCase().includes("take") || message.toLowerCase().includes("give")) {
      callFlaskApp();
    }

    setTimeout(() => {
      const botReply = "Sure will do the same!";
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: botReply, user: false },
      ]);

      // Text-to-Speech for bot reply
      speakText(botReply);
    }, 500);
  };

  const callFlaskApp = () => {
    fetch("http://localhost:8000/run-server", {
      method: "GET",
    })
      .then(response => response.text())
      .then(data => {
        console.log("Response from Flask app: ", data);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: data, user: false },
        ]);

        // Optionally, speak out the response
        speakText(data);
      })
      .catch(error => console.error("Error calling Flask app: ", error));
  };

  const speakText = (text) => {
    if (synth.speaking) {
      console.error("SpeechSynthesis.speaking");
      return;
    }
    const utterThis = new SpeechSynthesisUtterance(text);
    utterThis.onend = () => {
      console.log("SpeechSynthesisUtterance.onend");
    };
    utterThis.onerror = (event) => {
      console.error("SpeechSynthesisUtterance.onerror", event);
    };
    synth.speak(utterThis);
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      handleMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <>
      {isLoading && <Loader />}
      <div className={`container ${!isLoading ? "visible" : ""}`}>
        <h1>Drinks Handing Bot</h1>
        <div className="chat-container">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.user ? "user-message" : "bot-message"}`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            onKeyDown={handleKeyDown} // Add onKeyDown handler
          />
          <button className="btn" onClick={handleSendMessage}>
            Send
          </button>
          <button className="btn" onClick={startListening} disabled={listening}>
            {listening ? "Listening..." : "Speak"}
          </button>
          <button className="btn" onClick={stopListening} disabled={!listening}>
            Stop
          </button>
        </div>
      </div>
    </>
  );
};

export default App;