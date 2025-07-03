# 🤖 Small Talk AI Chatbot with Dialogflow ES + FastAPI

This is a production-ready small talk AI chatbot that uses **Dialogflow ES**, **FastAPI**, and **live external APIs** to handle engaging conversations. The bot is built to impress companies like **Google**, with fully custom intents, clean API architecture, and conversational polish.

## 🔧 Tech Stack

* **Dialogflow ES**: NLU platform to handle intent classification
* **FastAPI**: Async webhook backend to handle logic and API calls
* **httpx**: Async HTTP client to call public APIs
* **ngrok**: For local webhook testing

## 🌟 Features (Custom Intents with APIs)

| Intent Name                        | API Used                          | Description                           |
| ---------------------------------- | --------------------------------- | ------------------------------------- |
| `custom.smalltalk.weather`         | weatherapi.com (requires API key) | Get live weather by city              |
| `custom.smalltalk.joke`            | jokeapi.dev                       | Fetch a random joke                   |
| `custom.smalltalk.quote`           | quotable.io                       | Get a motivational quote              |
| `custom.smalltalk.time`            | worldtimeapi.org                  | Show current time in India            |
| `custom.smalltalk.fun_fact`        | uselessfacts.jsph.pl              | Share a fun fact                      |
| `custom.smalltalk.ask_advice`      | api.adviceslip.com                | Get a random life advice              |
| `custom.smalltalk.compliment_user` | complimentr.com                   | Generate a nice compliment            |
| `custom.smalltalk.quiz`            | opentdb.com                       | Trivia quiz question                  |
| `custom.smalltalk.travel`          | restcountries.com                 | Capital and population of any country |

## 🚀 How It Works

1. **User says**: "Tell me a joke"
2. **Dialogflow** matches `custom.smalltalk.joke`
3. Dialogflow sends a **POST webhook** to FastAPI
4. FastAPI calls `https://v2.jokeapi.dev/...`, returns a joke
5. Joke is sent back to user via Dialogflow `fulfillmentText`

## 📁 Project Structure

```
smalltalk-chatbot/
├── main.py              # FastAPI webhook
├── requirements.txt     # Python dependencies
└── README.md            # Project overview
```

## 🧠 Key Concepts

* Full custom intent naming (no prebuilt smalltalk)
* Parameter extraction via Dialogflow (e.g. geo-city, geo-country)
* Async API requests using httpx
* Deployable on **Google Cloud Run** or **Cloud Functions**

## 🧪 Testing with ngrok

```bash
uvicorn main:app --reload --port 8000
ngrok http 8000
```

Set the **ngrok URL** as your Dialogflow webhook.

## 🔒 Environment Setup

Create a `.env` or replace directly in `main.py`:

```python
WEATHER_API_KEY = "your_weatherapi_key_here"
```

## 🌍 Deploy to Google Cloud (Optional)

* Create a GCP project
* Use Cloud Run for containerized deployment
* OR use Cloud Functions for webhook logic only

## 📌 Why This Project Stands Out

* ✅ All intents are custom-built
* ✅ API-rich conversations (not hardcoded)
* ✅ Fully asynchronous, production ready
* ✅ Clean and scalable codebase
* ✅ Excellent for Conversational AI interviews

## 👀 Sample Responses

* *"The weather in Mumbai is Sunny with 32°C. Feels like 36°C."*
* *"Here's a quote: 'The only way to do great work is to love what you do.' — Steve Jobs"*
* *"Compliment: You're more helpful than Google Search itself."*

## 📮 Contact

For collaboration or questions, reach out on [LinkedIn](https://www.linkedin.com).
