from fastapi import FastAPI, Request
import httpx
import traceback  # for logging errors

app = FastAPI()

WEATHER_API_KEY = "0739a5b0188843f4ada91007250307"

@app.post("/webhook")
async def webhook(request: Request):
    try:
        req_data = await request.json()
        print("🔍 Incoming request:")
        print(req_data)

        intent_name = req_data["queryResult"]["intent"]["displayName"]
        parameters = req_data["queryResult"].get("parameters", {})

        # your intent code remains unchanged
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

        elif intent_name == "custom.smalltalk.joke":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://v2.jokeapi.dev/joke/Any?format=txt&type=single")
            return {"fulfillmentText": res.text.strip()}

        elif intent_name == "custom.smalltalk.quote":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://zenquotes.io/api/random")
                data = res.json()

            quote = data[0]["q"]
            author = data[0]["a"]

            return {"fulfillmentText": f"\"{quote}\" – {author}"}


        elif intent_name == "custom.smalltalk.time":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata")
            data = res.json()

            time_only = data["time"]
            return {"fulfillmentText": f"The current time in India is {time_only}."}


        elif intent_name == "custom.smalltalk.fun_fact":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
                    data = res.json()

                fact = data.get("text", "Hmm... I couldn’t find a fun fact right now.")
                return {"fulfillmentText": f"🧠 Did you know? {fact}"}

            except Exception as e:
                return {"fulfillmentText": "Oops, I couldn't get a fun fact right now. Please try again later."}


        elif intent_name == "custom.smalltalk.ask_advice":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://api.adviceslip.com/advice")
                    data = res.json()

                advice = data["slip"]["advice"]
                return {"fulfillmentText": f"💡 Here's a tip: {advice}"}

            except Exception as e:
                return {"fulfillmentText": "Sorry, I couldn't fetch advice right now."}


        elif intent_name == "custom.smalltalk.compliment_user":
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get("https://complimentr.com/api")
                    data = res.json()

                compliment = data["compliment"].capitalize()
                return {"fulfillmentText": f"💬 {compliment}"}

            except Exception as e:
                return {"fulfillmentText": "You're amazing, even if I can't fetch a compliment right now!"}


        elif intent_name == "custom.smalltalk.quiz":
            async with httpx.AsyncClient() as client:
                res = await client.get("https://opentdb.com/api.php?amount=1&type=multiple")
                data = res.json()

            result = data["results"][0]
            question = result["question"]
            correct = result["correct_answer"]
            incorrect = result["incorrect_answers"]

            # Combine and shuffle answers
            import random, html
            all_answers = incorrect + [correct]
            random.shuffle(all_answers)

            # Decode HTML entities (important!)
            question_clean = html.unescape(question)
            options_clean = [html.unescape(opt) for opt in all_answers]

            # Build message
            options_text = "\n".join([f"- {opt}" for opt in options_clean])
            message = f"📚 {question_clean}\n{options_text}\n\n(Answer: {correct})"

            return {"fulfillmentText": message}


        elif intent_name == "custom.smalltalk.travel":
            country = parameters.get("geo-country", "India")
            async with httpx.AsyncClient() as client:
                res = await client.get(f"https://restcountries.com/v3.1/name/{country}")
            data = res.json()[0]
            capital = data["capital"][0]
            population = data["population"]
            return {"fulfillmentText": f"{country}'s capital is {capital} and it has a population of {population:,}."}

        return {"fulfillmentText": "Sorry, I couldn't process that request."}

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        traceback.print_exc()
        return {"fulfillmentText": "An error occurred on the server. Please try again."}
