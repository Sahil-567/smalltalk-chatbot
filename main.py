from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import traceback
import random
import html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can use ["http://localhost:5173"] for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... your webhook code continues here ...


WEATHER_API_KEY = "0739a5b0188843f4ada91007250307"

@app.post("/webhook")
async def webhook(request: Request):
    try:
        req_data = await request.json()
        print("🔍 Incoming request:")
        print(req_data)

        intent_name = req_data["queryResult"].get("intent", {}).get("displayName", "")
        parameters = req_data["queryResult"].get("parameters", {})

        # 1. 🌦️ Weather Intent
        if intent_name == "custom.smalltalk.weather":
            city = parameters.get("geo-city", "Delhi")
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
            async with httpx.AsyncClient() as client:
                res = await client.get(url)
                data = res.json()
            temp = data["current"]["temp_c"]
            feels = data["current"]["feelslike_c"]
            condition = data["current"]["condition"]["text"]
            return {"fulfillmentText": f"The current weather in {city} is {condition} with {temp}°C. It feels like {feels}°C."}

        # 2. 😂 Joke Intent
        elif intent_name == "custom.smalltalk.joke":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://v2.jokeapi.dev/joke/Any?format=txt&type=single")
            return {"fulfillmentText": res.text.strip()}

        # 3. 💬 Quote Intent
        elif intent_name == "custom.smalltalk.quote":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://zenquotes.io/api/random")
                data = res.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return {"fulfillmentText": f"\"{quote}\" – {author}"}

        # 4. 🕒 Time Intent
        elif intent_name == "custom.smalltalk.time":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata")
            data = res.json()
            time_only = data.get("time", "unknown")
            return {"fulfillmentText": f"The current time in India is {time_only}."}

        # 5. 💡 Fun Fact Intent
        elif intent_name == "custom.smalltalk.fun_fact":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
                    data = res.json()
                fact = data.get("text", "Hmm... I couldn’t find a fun fact right now.")
                return {"fulfillmentText": f"🧠 Did you know? {fact}"}
            except:
                return {"fulfillmentText": "Oops, I couldn't get a fun fact right now. Please try again later."}

        # 6. 🧠 Ask Advice Intent
        elif intent_name == "custom.smalltalk.ask_advice":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://api.adviceslip.com/advice")
                    data = res.json()
                advice = data["slip"]["advice"]
                return {"fulfillmentText": f"💡 Here's a tip: {advice}"}
            except:
                return {"fulfillmentText": "Sorry, I couldn't fetch advice right now."}

        # 7. 😊 Compliment User Intent
        elif intent_name == "custom.smalltalk.compliment_user":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://complimentr.com/api")
                    data = res.json()
                compliment = data["compliment"].capitalize()
                return {"fulfillmentText": f"💬 {compliment}"}
            except:
                return {"fulfillmentText": "You're amazing, even if I can't fetch a compliment right now!"}

        # 8. 📚 Quiz Intent
        elif intent_name == "custom.smalltalk.quiz":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://opentdb.com/api.php?amount=1&type=multiple")
                data = res.json()
            result = data["results"][0]
            question = html.unescape(result["question"])
            correct = html.unescape(result["correct_answer"])
            incorrect = [html.unescape(i) for i in result["incorrect_answers"]]
            all_answers = incorrect + [correct]
            random.shuffle(all_answers)
            options_text = "\n".join([f"- {opt}" for opt in all_answers])
            message = f"📚 {question}\n{options_text}\n\n(Answer: {correct})"
            return {"fulfillmentText": message}

        # 9. ✈️ Travel Intent
        elif intent_name == "custom.smalltalk.travel":
            country = parameters.get("geo-country", "India")
            async with httpx.AsyncClient() as client:
                res = await client.get(f"https://restcountries.com/v3.1/name/{country}")
            data = res.json()[0]
            capital = data["capital"][0]
            population = data["population"]
            return {"fulfillmentText": f"{country}'s capital is {capital} and it has a population of {population:,}."}

        # Default fallback
        return {"fulfillmentText": "Sorry, I couldn't process that request."}

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        traceback.print_exc()
        return {"fulfillmentText": "An error occurred on the server. Please try again."}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

