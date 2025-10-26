import random
import requests

# ==================== CODEFORCES API CLASS ====================

class CodeForcesAPI:
    """Class to handle all interactions with the Codeforces API"""

    BASE_URL = "https://codeforces.com/api/problemset.problems"

    def __init__(self):
        self.recent_problems = []
        self.max_recent = 30

    def get_random_problem(self, min_rating, max_rating):
        """
        Gets a random Codeforces problem within the given rating range.

        Args:
            min_rating (int): Minimum problem rating
            max_rating (int): Maximum problem rating

        Returns:
            dict: Dictionary with problem information or None if error
        """
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            data = response.json()

            if data["status"] != "OK":
                return None

            problems = data["result"]["problems"]

            # Filter by rating
            filtered = [
                p for p in problems
                if "rating" in p and min_rating <= p["rating"] <= max_rating
            ]

            # Avoid repeating recent problems
            filtered = [
                p for p in filtered
                if p["name"] not in self.recent_problems
            ]

            if not filtered:
                return None

            problem = random.choice(filtered)

            # Save to recent problems
            self._add_recent_problem(problem["name"])

            return problem

        except requests.RequestException as e:
            print(f"Error getting problem: {e}")
            return None

    def _add_recent_problem(self, problem_name):
        """
        Adds a problem to the recent problems list
        """
        self.recent_problems.append(problem_name)
        if len(self.recent_problems) > self.max_recent:
            self.recent_problems.pop(0)

    def get_problem_url(self, contest_id, index):
        """
        Generates the problem URL
        """
        return f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

    def format_problem_data(self, problem):
        """
        Formats the problem data for sending

        Returns:
            dict: Dictionary with formatted data
        """
        if problem is None:
            return None

        return {
            "contest_id": problem["contestId"],
            "index": problem["index"],
            "name": problem["name"],
            "rating": problem.get("rating", "N/A"),
            "url": self.get_problem_url(problem["contestId"], problem["index"])
        }