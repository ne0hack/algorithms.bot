from typing import List, Dict
from urllib.parse import urlencode
import http.client
import json


def get_solved_algorithms() -> List[str]:
    """
    Fetches a list of solved algorithm problems from a specific GitHub repository.

    Returns:
        List[str]: A list of titles representing solved algorithm problems.
    """

    solved = []

    conn = http.client.HTTPSConnection("api.github.com")

    headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0"}
    payload = ""
    params = {"recursive": 1}
    params_string = urlencode(params)

    conn.request("GET", "/repos/ne0hack/algos/git/trees/main?" + params_string, payload, headers)
    response = conn.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode("utf-8"))
        for file in data["tree"]:
            if "leetcode/" in file["path"] and ".md" in file["path"]:
                title = " ".join(file["path"].replace("leetcode/", "").replace(".md", "").strip().split())
                solved.append(title)

    return solved


def get_unsolved_algorithms(solved_algorithms: List[str]) -> Dict[str, list]:
    """
    Fetches unsolved algorithm problems from LeetCode and categorizes them by difficulty.

    Parameters:
    - solved_algorithms (List[str]): A list of titles of algorithm
      problems that have already been solved.

    Returns:
    - Dict[str, list]: A dictionary with keys 'easy', 'medium', and 'hard'. Each key maps to
      a list of dictionaries, where each dictionary represents an unsolved problem
      with 'title' and 'link' keys.
    """

    status_codes = {1: "easy", 2: "medium", 3: "hard"}
    unsolved = {"easy": [], "medium": [], "hard": []}

    conn = http.client.HTTPSConnection("leetcode.com")

    headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0"}
    payload = ""

    conn.request("GET", "/api/problems/all/", payload, headers)
    response = conn.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode("utf-8"))
        for algorithm in data["stat_status_pairs"]:
            if not algorithm["paid_only"]:
                title = " ".join(
                    (
                        str(algorithm["stat"]["frontend_question_id"])
                        + ". "
                        + algorithm["stat"]["question__title"].strip()
                    ).split()
                )
                status = status_codes[int(algorithm["difficulty"]["level"])]
                link = "https://leetcode.com/problems/" + algorithm["stat"]["question__title_slug"].strip()

                if title not in solved_algorithms:
                    unsolved[status].append({"title": title, "link": link})
        unsolved["easy"] = unsolved["easy"][::-1]
        unsolved["medium"] = unsolved["medium"][::-1]
        unsolved["hard"] = unsolved["hard"][::-1]

    return unsolved
