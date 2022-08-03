import json


def add_score(username: str, score: int):

    print(score)

    with open("res/data/data.json", "r+") as file:
        data = json.load(file)
        nb_score = 0

        for feur in data["scores"]:
            nb_score += 1

        print(nb_score)

        data["scores"][f"score{nb_score+1}"] = {"username": username, "score": score}
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
        nb_score = 0
