import time
from database import get_db_conn


# SCORE ENGINE
class ScoreTracker:
    def __init__(self, user_id, chapter, time_limit=300):
        self.user_id = user_id
        self.chapter = chapter
        self.time_limit = time_limit  # seconds
        self.start_time = None
        self.command_count = 0

    def start(self):
        self.start_time = time.time()

    def record_command(self):
        self.command_count += 1

    def time_elapsed(self):
        if not self.start_time:
            return 0
        return int(time.time() - self.start_time)

    def is_time_up(self):
        return self.start_time and self.time_elapsed() >= self.time_limit

    def calculate_score(self):
        """
        Scoring rules:
        - Base score: 1000
        - Time penalty: 1 point per second
        - Command penalty: 2 points per command
        - Minimum score: 50 (if chapter completed)
        """

        time_penalty = self.time_elapsed() * 1
        command_penalty = self.command_count * 2

        score = 1000 - time_penalty - command_penalty

        if score < 50:
            score = 50

        return score


# DATABASE HELPERS
def save_score(user_id, chapter, score):
    """
    Save the user's score if it doesn't exist,
    or update only if the new score is higher than previous.
    """
    conn = get_db_conn()
    c = conn.cursor()

    # Check if user already has a score for this chapter
    c.execute(
        "SELECT score FROM score WHERE user_id = ? AND chapter = ?",
        (user_id, chapter)
    )
    row = c.fetchone()

    if row:
        # Update only if new score is higher
        if score > row["score"]:
            c.execute(
                "UPDATE score SET score = ? WHERE user_id = ? AND chapter = ?",
                (score, user_id, chapter)
            )
    else:
        # Insert new score
        c.execute(
            "INSERT INTO score (user_id, chapter, score) VALUES (?, ?, ?)",
            (user_id, chapter, score)
        )

    conn.commit()
    conn.close()


def get_best_score(chapter):
    """
    Returns the highest score for a chapter and the username of the record holder.
    Returns None if no scores exist yet.
    """
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("""
              SELECT u.username, s.score
              FROM score s
                       JOIN users u ON u.id = s.user_id
              WHERE s.chapter = ?
              ORDER BY s.score DESC LIMIT 1
              """, (chapter,))
    row = c.fetchone()
    conn.close()
    return row
