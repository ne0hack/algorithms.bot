from typing import List, Dict

import requests
from fake_useragent import UserAgent


def get_solved_algorithms() -> List[str]:
    """
    Fetches a list of solved algorithm problems from a specific GitHub repository.

    Returns:
        List[str]: A list of titles representing solved algorithm problems.
    """
    solved = []

    url = "https://api.github.com/repos/ne0hack/algos/git/trees/main"
    user_agent = UserAgent()
    headers = {"Accept": "*/*", "User-Agent": user_agent.random}
    params = {"recursive": 1}
    timeout_seconds = 10

    response = requests.get(url=url, params=params, headers=headers, timeout=timeout_seconds)

    if response.status_code == 200:
        data = response.json()
        for file in data["tree"]:
            if "leetcode/" in file["path"] and ".md" in file["path"]:
                title = " ".join(file["path"].replace("leetcode/", "").replace(".md", "").strip().split())
                solved.append(title)
    else:
        raise UserWarning(f"An unknown github.com code arrived. (HTTP code: {response.status_code})")

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

    url = "https://leetcode.com/api/problems/all/"
    user_agent = UserAgent()
    headers = {"Accept": "*/*", "User-Agent": user_agent.random}
    timeout_seconds = 10

    response = requests.get(url=url, headers=headers, timeout=timeout_seconds)

    if response.status_code == 200:
        data = response.json()
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
    elif response.status_code == 403:
        raise PermissionError("Access to the resource is forbidden. (HTTP code: 403)")
    else:
        raise UserWarning(f"An unknown leetcode.com code arrived. (HTTP code: {response.status_code})")

    return unsolved
