def query_router(query: str):
    q = query.lower()
    scores = {
        "nutrition": 0,
        "nutrition100g": 0,
        "exercise": 0,
        "workout": 0,
        "compendium": 0,
        "guidelines": 0,
    }

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
        return []

    selected.sort(key=lambda x: scores[x], reverse=True)
    return selected