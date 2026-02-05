def query_router(query:str):
    q=query.lower()
    scores = {
        "nutrition": 0,
        "nutrition100g": 0,
        "exercise": 0,
        "workout": 0,
        "compendium": 0,
        "guidelines": 0,
    }

    if q in ["hi", "hey", "hello"]:
        return (
            "👋 **Hello! I'm ATLAS**\n\n"
            "Your AI-powered fitness & nutrition advisor.\n"
            "Ask me about diet plans, workouts, or nutrition facts."
        )
    if any(w in q for w in ["your name", "who are you", "what is your name", "what's your name"]):
        return (
            "## About Me\n"
            "• **Name:** ATLAS\n"
            "• **Role:** AI Fitness & Nutrition Advisor\n"
        )

    if any(w in q for w in ["eat", "meal", "diet", "pre workout", "post workout"]):
        scores["nutrition"] += 2

    if any(w in q for w in ["per 100g", "calories", "protein", "carbs", "fat", "grams"]):
        scores["nutrition100g"] += 3

    if any(w in q for w in ["exercise", "how to", "form", "sit up", "push up", "squat"]):
        scores["exercise"] += 2

    if any(w in q for w in ["workout", "routine", "split", "plan"]):
        scores["workout"] += 2

    if any(w in q for w in ["met", "burn", "calories burned", "energy expenditure"]):
        scores["compendium"] += 3

    if any(w in q for w in ["safe", "avoid", "injury", "recommend"]):
        scores["guidelines"] += 2

    
    selected = [k for k, v in scores.items() if v > 0]


    if not selected:
        return ["exercise", "nutrition"]

    selected.sort(key=lambda x: scores[x], reverse=True)
    return selected


