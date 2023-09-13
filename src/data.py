from typing import List, Dict

import requests


def get_solved_algorithms() -> List[str]:
    solved = []
    url = "https://api.github.com/repos/ne0hack/algos/git/trees/main"
    params = {"recursive": 1}

    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        data = response.json()
        for file in data["tree"]:
            if "leetcode/" in file["path"] and ".md" in file["path"]:
                title = file["path"].replace("leetcode/", "").replace(".md", "").strip()
                solved.append(title)

    return solved


def get_unsolved_algorithms(solved_algorithms: List[str]) -> Dict[str, list]:
    status_codes = {1: "easy", 2: "medium", 3: "hard"}
    unsolved = {"easy": [], "medium": [], "hard": []}
    url = "https://leetcode.com/api/problems/all/"

    response = requests.get(url=url)

    if response.status_code == 200:
        data = response.json()
        for algorithm in data["stat_status_pairs"]:
            if not algorithm["paid_only"]:
                title = str(algorithm["stat"]["frontend_question_id"]) + ". " + algorithm["stat"]["question__title"].strip()
                status = status_codes[int(algorithm["difficulty"]["level"])]
                link = "https://leetcode.com/problems/" + algorithm["stat"]["question__title_slug"].strip()

                if title not in solved_algorithms:
                    unsolved[status].append({"title": title, "link": link})
        unsolved["easy"] = unsolved["easy"][::-1]
        unsolved["medium"] = unsolved["medium"][::-1]
        unsolved["hard"] = unsolved["hard"][::-1]

    return unsolved
