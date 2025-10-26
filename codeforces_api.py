# ==================== IMPORTS ====================

import random
import requests

# ==================== API CLASS DEFINITION ====================

class CodeForcesAPI:
    """
    Handles all interactions with the Codeforces API.
    Manages problem fetching, formatting, and recent problem tracking.
    """
    
    # API endpoint for problem set
    BASE_URL = "https://codeforces.com/api/problemset.problems"
    
    def __init__(self):
        """
        Initialize the Codeforces API handler with empty recent problems list.
        Sets up tracking for recently sent problems to avoid repetition.
        """
        self.recent_problems = []     # List to track recent problems
        self.max_recent = 30          # Maximum number of problems to track
    
    # ==================== PROBLEM FETCHING ====================
    
    def get_random_problem(self, min_rating, max_rating):
        """
        Fetches a random problem from Codeforces within a difficulty range.
        Ensures no recent problems are repeated.
        
        Args:
            min_rating (int): Minimum problem difficulty (e.g., 800)
            max_rating (int): Maximum problem difficulty (e.g., 3500)
            
        Returns:
            dict: Problem information dictionary containing:
                - contestId: ID of the contest
                - index: Problem index in contest
                - name: Problem name
                - rating: Difficulty rating
                - tags: Problem tags
            None: If an error occurs or no suitable problem is found
        """
        try:
            # Fetch problem set from Codeforces API
            response = requests.get(self.BASE_URL, timeout=10)
            data = response.json()
            
            # Validate API response
            if data["status"] != "OK":
                return None
            
            # Extract problems list
            problems = data["result"]["problems"]
            
            # Filter by rating range
            filtered = [
                p for p in problems 
                if "rating" in p and min_rating <= p["rating"] <= max_rating
            ]
            
            # Avoid recently sent problems
            filtered = [
                p for p in filtered 
                if p["name"] not in self.recent_problems
            ]
            
            if not filtered:
                return None
            
            problem = random.choice(filtered)
            self._add_recent_problem(problem["name"])
            
            return problem
            
        except requests.RequestException as e:
            print(f"❌ Error fetching problem from Codeforces: {e}")
            return None
    
    # ==================== UTILITY METHODS ====================
    
    def _add_recent_problem(self, problem_name):
        """
        Adds a problem to the recent list and maintains maximum size limit.
        Uses FIFO (First In, First Out) approach for problem rotation.
        
        Args:
            problem_name (str): Name of the problem to add to recent list
        """
        self.recent_problems.append(problem_name)
        if len(self.recent_problems) > self.max_recent:
            self.recent_problems.pop(0)
    
    def get_problem_url(self, contest_id, index):
        """
        Generates the full problem URL on Codeforces website.
        
        Args:
            contest_id (int): ID of the contest
            index (str): Problem index within contest
            
        Returns:
            str: Complete URL to the problem
        """
        return f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    
    def get_difficulty_bars(self, rating):
        """
        Generates visual representation of problem difficulty using green bars.
        Each 200 rating points equals one green bar.
        
        Args:
            rating (int): Problem difficulty rating
            
        Returns:
            str: String of green bar emojis representing difficulty
        """
        if rating == "N/A" or not isinstance(rating, int):
            return ""
        
        # Calculate number of bars (every 200 points = 1 bar)
        num_bars = (rating - 800) // 200 + 1
        num_bars = max(1, min(num_bars, 15))
        
        bars = "🟩" * num_bars
        
        return bars
    
    # ==================== DATA FORMATTING ====================
    
    def format_problem_data(self, problem):
        """
        Formats raw problem data for easy use in Discord messages.
        Adds additional formatting and safely handles missing fields.
        
        Args:
            problem (dict): Raw problem data from Codeforces API
            
        Returns:
            dict: Formatted data dictionary containing:
                - contest_id: Contest identifier
                - index: Problem index
                - name: Problem name
                - rating: Difficulty rating
                - difficulty_bars: Visual difficulty representation
                - tags: Problem topics/tags
                - url: Full problem URL
            None: If input problem is None
        """
        if problem is None:
            return None
        
        # Get and format difficulty information
        rating = problem.get("rating", "N/A")
        difficulty_bars = self.get_difficulty_bars(rating)
        
        # Build formatted data dictionary
        return {
            "contest_id": problem.get("contestId", "N/A"),
            "index": problem.get("index", "N/A"),
            "name": problem.get("name", "Untitled Problem"),
            "rating": rating,
            "difficulty_bars": difficulty_bars,
            "tags": problem.get("tags", []),
            "url": self.get_problem_url(
                problem.get("contestId", 0),
                problem.get("index", "A")
            )
        }