import { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const getIntentName = (message) => {
  const msg = message.toLowerCase();
  if (msg.includes("joke")) return "custom.smalltalk.joke";
  if (msg.includes("weather")) return "custom.smalltalk.weather";
  if (msg.includes("quote")) return "custom.smalltalk.quote";
  if (msg.includes("time")) return "custom.smalltalk.time";
  if (msg.includes("fact")) return "custom.smalltalk.fun_fact";
  if (msg.includes("advice")) return "custom.smalltalk.ask_advice";
  if (msg.includes("compliment")) return "custom.smalltalk.compliment_user";
  if (msg.includes("quiz")) return "custom.smalltalk.quiz";
  if (msg.includes("travel")) return "custom.smalltalk.travel";
  return "custom.smalltalk.joke"; // fallback
};


  const sendMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);

    const intent = detectIntent(message);
    const body = {
      queryResult: {
        intent: { displayName: intent },
        parameters: {
          "geo-city": "Delhi",
          "geo-country": "India"
        }
      }
    };

    try {
      const res = await fetch('https://dialogflow-test-464709.el.r.appspot.com/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setResponse(data.fulfillmentText || "No response");
    } catch (err) {
      console.error(err);
      setResponse("❌ Failed to fetch response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl p-8 rounded-xl max-w-md w-full space-y-4">
        <h1 className="text-2xl font-bold text-gray-800">🤖 SmallTalk Chatbot</h1>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask anything (e.g. Tell me a joke, Give me a fact)"
          className="w-full px-4 py-2 border rounded-lg focus:outline-none"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg w-full hover:bg-blue-700 transition"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
        {response && (
          <div className="bg-gray-100 p-3 rounded-lg text-gray-800">
            <strong>🤖 Response:</strong><br /> {response}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
