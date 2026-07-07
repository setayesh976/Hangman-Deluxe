"""
Hangman Deluxe - Single File Version
All modules combined: display, words, scores, game engine, menu.
"""

import os
import sys
import time
import json
import random
import platform
from datetime import datetime
from typing import List, Dict, Any

# ══════════════════════════════════════════════════════════════════════════════
# COLORS & DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_banner():
    print(f"""
{Color.CYAN}{Color.BOLD}
 ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
 ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
 ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
 ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
 ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Color.RESET}
{Color.YELLOW}                 ✦  D E L U X E  E D I T I O N  ✦{Color.RESET}
""")


HANGMAN_STAGES = [
    f"\n{Color.GREEN}\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.GREEN}\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.YELLOW}\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.YELLOW}\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.YELLOW}\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.RED}\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.RED}\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.RED}{Color.BOLD}\n  +---+\n  |   |\n [O]  |\n /|\\  |\n / \\  |\n      |\n=========\n{Color.RESET}",
    f"\n{Color.RED}{Color.BOLD}\n  +---+\n  |   |\n [X]  |\n /|\\  |\n / \\  |\n      |\n=========  GAME OVER\n{Color.RESET}",
]


def get_hangman(wrong_count: int, max_lives: int) -> str:
    total  = len(HANGMAN_STAGES)
    index  = min(int(wrong_count * (total - 1) / max(max_lives, 1)), total - 1)
    return HANGMAN_STAGES[index]


def print_word_display(word: str, guessed: set) -> str:
    display = ""
    for ch in word:
        if ch in guessed:
            display += f"{Color.GREEN}{Color.BOLD} {ch.upper()} {Color.RESET}"
        else:
            display += f"{Color.DIM} _ {Color.RESET}"
    return display


def print_lives_bar(lives_left: int, max_lives: int) -> str:
    hearts = f"{Color.RED}♥{Color.RESET}" * lives_left
    empty  = f"{Color.DIM}♡{Color.RESET}" * (max_lives - lives_left)
    return f"  Lives: {hearts}{empty}  ({lives_left}/{max_lives})"


def print_guessed_letters(wrong_guesses: set) -> str:
    if not wrong_guesses:
        return f"  {Color.DIM}No wrong guesses yet{Color.RESET}"
    letters = "  ".join(
        f"{Color.RED}{Color.BOLD}{ch.upper()}{Color.RESET}" for ch in sorted(wrong_guesses)
    )
    return f"  Wrong: {letters}"


def divider(width: int = 50) -> str:
    return f"{Color.DIM}{'─' * width}{Color.RESET}"


# ══════════════════════════════════════════════════════════════════════════════
# WORD BANK
# ══════════════════════════════════════════════════════════════════════════════

WORD_BANK = {
    "easy": [
        {"word": "python",   "hint": "A popular programming language named after a snake", "category": "Technology"},
        {"word": "cloud",    "hint": "Where modern data is often stored remotely",          "category": "Technology"},
        {"word": "music",    "hint": "Art form using sound and rhythm",                     "category": "Arts"},
        {"word": "ocean",    "hint": "Vast body of salt water covering most of Earth",      "category": "Nature"},
        {"word": "bridge",   "hint": "Structure built to cross an obstacle",                "category": "Architecture"},
        {"word": "robot",    "hint": "Machine programmed to perform tasks automatically",   "category": "Technology"},
        {"word": "tiger",    "hint": "Largest wild cat with orange and black stripes",      "category": "Animals"},
        {"word": "pizza",    "hint": "Italian dish with dough, sauce, and toppings",        "category": "Food"},
        {"word": "space",    "hint": "The universe beyond Earth's atmosphere",              "category": "Science"},
        {"word": "chess",    "hint": "Strategic board game with kings and queens",          "category": "Games"},
        {"word": "novel",    "hint": "Long-form fictional narrative in book form",          "category": "Arts"},
        {"word": "coral",    "hint": "Marine organism that builds underwater reefs",        "category": "Nature"},
        {"word": "laser",    "hint": "Focused beam of coherent light",                     "category": "Science"},
        {"word": "globe",    "hint": "Spherical model representing planet Earth",           "category": "Geography"},
        {"word": "flame",    "hint": "Visible part of a fire",                             "category": "Science"},
    ],
    "medium": [
        {"word": "algorithm", "hint": "Step-by-step procedure for solving a problem",       "category": "Technology"},
        {"word": "quantum",   "hint": "Smallest discrete unit of a physical quantity",      "category": "Science"},
        {"word": "symphony",  "hint": "Complex musical composition for a full orchestra",   "category": "Arts"},
        {"word": "eclipse",   "hint": "When one celestial body blocks another's light",     "category": "Astronomy"},
        {"word": "photon",    "hint": "Elementary particle representing a quantum of light","category": "Science"},
        {"word": "voltage",   "hint": "Electric potential difference measured in volts",    "category": "Physics"},
        {"word": "fractal",   "hint": "Self-similar mathematical pattern at every scale",   "category": "Mathematics"},
        {"word": "glacier",   "hint": "Slow-moving mass of ice formed from compressed snow","category": "Nature"},
        {"word": "protein",   "hint": "Large biomolecule made of amino acid chains",        "category": "Biology"},
        {"word": "encrypt",   "hint": "To convert data into a coded form for security",    "category": "Technology"},
        {"word": "paradox",   "hint": "Statement that contradicts itself yet may be true",  "category": "Philosophy"},
        {"word": "turbine",   "hint": "Rotary machine converting fluid energy to mechanical","category": "Engineering"},
        {"word": "scaffold",  "hint": "Temporary structure supporting workers on buildings","category": "Architecture"},
        {"word": "dialect",   "hint": "Regional variety of a language",                    "category": "Linguistics"},
        {"word": "mandate",   "hint": "Official order or commission to carry out a task",   "category": "Politics"},
    ],
    "hard": [
        {"word": "cryptography",   "hint": "Science of secure communication through codes",     "category": "Technology"},
        {"word": "metamorphosis",  "hint": "Process of transformation, as in a caterpillar",    "category": "Biology"},
        {"word": "perpendicular",  "hint": "At a 90-degree angle to a given line or plane",     "category": "Mathematics"},
        {"word": "thermodynamics", "hint": "Branch of physics dealing with heat and energy",     "category": "Physics"},
        {"word": "infrastructure", "hint": "Basic physical systems of a society",                "category": "Engineering"},
        {"word": "bioluminescence","hint": "Production of light by living organisms",            "category": "Biology"},
        {"word": "photosynthesis", "hint": "Plants converting sunlight into chemical energy",    "category": "Biology"},
        {"word": "consciousness",  "hint": "State of being aware of one's own existence",       "category": "Philosophy"},
        {"word": "juxtaposition",  "hint": "Placing two contrasting elements side by side",     "category": "Literature"},
        {"word": "anachronism",    "hint": "Something out of its proper historical time period", "category": "History"},
        {"word": "serendipity",    "hint": "Finding something valuable by happy accident",       "category": "Language"},
        {"word": "palindrome",     "hint": "Word that reads the same forwards and backwards",    "category": "Linguistics"},
        {"word": "archipelago",    "hint": "Group or chain of islands",                         "category": "Geography"},
        {"word": "onomatopoeia",   "hint": "Word that phonetically imitates its sound",         "category": "Linguistics"},
        {"word": "electromagnetic","hint": "Relating to electric and magnetic interaction",      "category": "Physics"},
    ],
}

DIFFICULTY_CONFIG = {
    "easy":   {"lives": 8, "hint_cost": 10, "base_score": 50},
    "medium": {"lives": 6, "hint_cost": 20, "base_score": 100},
    "hard":   {"lives": 5, "hint_cost": 30, "base_score": 200},
}

# ══════════════════════════════════════════════════════════════════════════════
# SCORES & RECORDS
# ══════════════════════════════════════════════════════════════════════════════

RECORDS_FILE = "records.json"


def _load_records() -> Dict[str, Any]:
    if not os.path.exists(RECORDS_FILE):
        return {"leaderboard": [], "stats": {"total_games": 0, "wins": 0, "losses": 0,
                                              "total_score": 0, "difficulty_counts": {}}}
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"leaderboard": [], "stats": {}}


def _save_records(data: Dict[str, Any]):
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def calculate_score(word, difficulty, lives_left, max_lives, elapsed, used_hint):
    base        = {"easy": 50, "medium": 100, "hard": 200}.get(difficulty, 50)
    length_bonus = len(word) * 5
    life_bonus   = (lives_left / max_lives) * base
    time_bonus   = max(0, int(60 - elapsed)) * 2
    hint_penalty = 30 if used_hint else 0
    return max(int(base + length_bonus + life_bonus + time_bonus - hint_penalty), 1)


def save_game_result(player_name, word, difficulty, score, won, elapsed, used_hint):
    data  = _load_records()
    entry = {
        "name": player_name, "word": word, "difficulty": difficulty,
        "score": score, "won": won, "time": round(elapsed, 1),
        "hint_used": used_hint, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    if won:
        data["leaderboard"].append(entry)
        data["leaderboard"] = sorted(data["leaderboard"], key=lambda x: x["score"], reverse=True)[:10]
    s = data.setdefault("stats", {"total_games": 0, "wins": 0, "losses": 0,
                                   "total_score": 0, "difficulty_counts": {}})
    s["total_games"] = s.get("total_games", 0) + 1
    if won:
        s["wins"]        = s.get("wins", 0) + 1
        s["total_score"] = s.get("total_score", 0) + score
    else:
        s["losses"] = s.get("losses", 0) + 1
    dc = s.setdefault("difficulty_counts", {})
    dc[difficulty] = dc.get(difficulty, 0) + 1
    _save_records(data)


def get_leaderboard() -> List[Dict]:
    return _load_records().get("leaderboard", [])


def get_stats() -> Dict:
    return _load_records().get("stats", {})


# ══════════════════════════════════════════════════════════════════════════════
# GAME ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class HangmanGame:
    def __init__(self, difficulty: str, player_name: str):
        self.difficulty  = difficulty
        self.player_name = player_name
        self.config      = DIFFICULTY_CONFIG[difficulty]
        self.max_lives   = self.config["lives"]
        entry            = random.choice(WORD_BANK[difficulty])
        self.word        = entry["word"].lower()
        self.hint        = entry["hint"]
        self.category    = entry["category"]
        self.guessed_correct: set = set()
        self.guessed_wrong:   set = set()
        self.lives_left  = self.max_lives
        self.score       = 0
        self.hint_used   = False
        self.start_time  = time.time()
        self.finished    = False
        self.won         = False

    @property
    def wrong_count(self): return len(self.guessed_wrong)

    @property
    def all_guessed(self): return set(self.word) <= self.guessed_correct

    @property
    def elapsed(self): return time.time() - self.start_time

    def _render(self):
        clear_screen()
        diff_color = {"easy": Color.GREEN, "medium": Color.YELLOW, "hard": Color.RED}[self.difficulty]
        print(f"\n{diff_color}{Color.BOLD}  ◈ {self.difficulty.upper()} MODE  │  Category: {self.category}{Color.RESET}")
        print(divider())
        print(get_hangman(self.wrong_count, self.max_lives))
        print(f"\n  {print_word_display(self.word, self.guessed_correct)}\n")
        print(print_lives_bar(self.lives_left, self.max_lives))
        print(print_guessed_letters(self.guessed_wrong))
        print(f"{Color.YELLOW}  Score: {self.score:,}{Color.RESET}")
        print(divider())

    def _use_hint(self):
        if self.hint_used:
            print(f"\n{Color.YELLOW}  Hint already used!{Color.RESET}")
        else:
            self.hint_used = True
            self.score = max(0, self.score - self.config["hint_cost"])
            print(f"\n{Color.CYAN}  💡 HINT: {self.hint}{Color.RESET}")
        input(f"\n{Color.DIM}  Press Enter to continue...{Color.RESET}")

    def _process_guess(self, letter: str) -> str:
        if letter in self.guessed_correct or letter in self.guessed_wrong:
            return "already_guessed"
        if letter in self.word:
            self.guessed_correct.add(letter)
            self.score += self.word.count(letter) * 10
            return "correct"
        else:
            self.guessed_wrong.add(letter)
            self.lives_left -= 1
            return "wrong"

    def play(self) -> dict:
        while not self.finished:
            self._render()
            if self.all_guessed:
                self._end_win(); break
            if self.lives_left <= 0:
                self._end_loss(); break
            print(f"\n  {Color.BOLD}Enter a letter{Color.RESET} or {Color.CYAN}[H]{Color.RESET}int / {Color.RED}[Q]{Color.RESET}uit: ", end="")
            raw = input().strip().lower()
            if raw == "q":
                self._end_quit(); break
            elif raw == "h":
                self._use_hint()
            elif len(raw) == 1 and raw.isalpha():
                result = self._process_guess(raw)
                self._render()
                if result == "already_guessed":
                    print(f"\n{Color.YELLOW}  ⚠  Already guessed '{raw.upper()}'!{Color.RESET}")
                    time.sleep(1)
                elif result == "wrong":
                    print(f"\n{Color.RED}  ✗  '{raw.upper()}' is not in the word!{Color.RESET}")
                    time.sleep(0.8)
                else:
                    print(f"\n{Color.GREEN}  ✓  Great guess!{Color.RESET}")
                    time.sleep(0.5)
            else:
                print(f"\n{Color.RED}  Invalid input. Enter a single letter.{Color.RESET}")
                time.sleep(0.8)
        return {"won": self.won, "score": self.score, "word": self.word}

    def _end_win(self):
        self.won    = True
        self.finished = True
        elapsed     = self.elapsed
        final_score = calculate_score(self.word, self.difficulty, self.lives_left,
                                      self.max_lives, elapsed, self.hint_used)
        self.score  = final_score
        save_game_result(self.player_name, self.word, self.difficulty,
                         final_score, True, elapsed, self.hint_used)
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}")
        print("  ╔══════════════════════════════╗")
        print("  ║    🎉  YOU WON!  🎉          ║")
        print(f"  ║  Word: {self.word.upper():<21}║")
        print(f"  ║  Score: {final_score:<20}║")
        print(f"  ║  Time:  {elapsed:.1f}s{' '*(19-len(f'{elapsed:.1f}s'))}║")
        print("  ╚══════════════════════════════╝")
        print(Color.RESET)
        input(f"  {Color.DIM}Press Enter to continue...{Color.RESET}")

    def _end_loss(self):
        self.won      = False
        self.finished = True
        save_game_result(self.player_name, self.word, self.difficulty,
                         0, False, self.elapsed, self.hint_used)
        clear_screen()
        print(get_hangman(self.max_lives, self.max_lives))
        print(f"\n{Color.RED}{Color.BOLD}")
        print("  ╔══════════════════════════════╗")
        print("  ║    💀  GAME OVER  💀          ║")
        print(f"  ║  Word was: {self.word.upper():<18}║")
        print("  ╚══════════════════════════════╝")
        print(Color.RESET)
        input(f"  {Color.DIM}Press Enter to continue...{Color.RESET}")

    def _end_quit(self):
        self.won = False; self.finished = True
        print(f"\n{Color.YELLOW}  Game quit. The word was: {Color.BOLD}{self.word.upper()}{Color.RESET}")
        time.sleep(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════

class MainMenu:
    def __init__(self):
        self.player_name = ""

    def _get_player_name(self) -> str:
        clear_screen(); print_banner()
        print(f"  {Color.CYAN}Enter your name (or press Enter for 'Player'):{Color.RESET} ", end="")
        name = input().strip()
        return name if name else "Player"

    def _pick_difficulty(self):
        clear_screen()
        print(f"\n{Color.BOLD}  ◈ SELECT DIFFICULTY{Color.RESET}\n")
        print(f"  {Color.GREEN}[1]{Color.RESET}  Easy    — 8 lives  │  Short common words")
        print(f"  {Color.YELLOW}[2]{Color.RESET}  Medium  — 6 lives  │  Intermediate vocabulary")
        print(f"  {Color.RED}[3]{Color.RESET}  Hard    — 5 lives  │  Complex & technical terms")
        print(f"  {Color.DIM}[4]  Back{Color.RESET}\n")
        print(f"  {Color.DIM}Choice: {Color.RESET}", end="")
        return {"1": "easy", "2": "medium", "3": "hard", "4": None}.get(input().strip())

    def _show_leaderboard(self):
        clear_screen()
        board = get_leaderboard()
        print(f"\n{Color.YELLOW}{Color.BOLD}  🏆  TOP 10 LEADERBOARD{Color.RESET}\n")
        print(divider())
        if not board:
            print(f"\n  {Color.DIM}No records yet. Play a game!{Color.RESET}\n")
        else:
            print(f"  {'#':<4} {'Name':<15} {'Score':>7}  {'Difficulty':<8}  {'Word':<15}  {'Time':>6}")
            print(divider())
            for i, e in enumerate(board, 1):
                medal = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"  {i}."
                print(f"  {medal:<4} {e['name']:<15} {e['score']:>7,}  {e['difficulty']:<8}  {e['word']:<15}  {e['time']:>5.1f}s")
        print(divider())
        input(f"\n  {Color.DIM}Press Enter to go back...{Color.RESET}")

    def _show_stats(self):
        clear_screen()
        s      = get_stats()
        total  = s.get("total_games", 0)
        wins   = s.get("wins", 0)
        losses = s.get("losses", 0)
        tscore = s.get("total_score", 0)
        dc     = s.get("difficulty_counts", {})
        wr     = f"{wins/total*100:.1f}%" if total else "N/A"
        print(f"\n{Color.CYAN}{Color.BOLD}  📊  GAME STATISTICS{Color.RESET}\n")
        print(divider())
        print(f"  Total games : {Color.BOLD}{total}{Color.RESET}")
        print(f"  Wins        : {Color.GREEN}{wins}{Color.RESET}")
        print(f"  Losses      : {Color.RED}{losses}{Color.RESET}")
        print(f"  Win rate    : {Color.YELLOW}{wr}{Color.RESET}")
        print(f"  Total score : {Color.YELLOW}{tscore:,}{Color.RESET}")
        print(divider())
        for diff, color in [("easy", Color.GREEN), ("medium", Color.YELLOW), ("hard", Color.RED)]:
            count = dc.get(diff, 0)
            bar   = "█" * count + "░" * max(0, 10 - count)
            print(f"  {color}{diff.capitalize():<8}{Color.RESET}  {bar}  {count}")
        print()
        input(f"  {Color.DIM}Press Enter to go back...{Color.RESET}")

    def run(self):
        self.player_name = self._get_player_name()
        while True:
            clear_screen(); print_banner()
            print(f"  {Color.CYAN}Welcome, {Color.BOLD}{self.player_name}{Color.RESET}!\n")
            print(f"  {Color.GREEN}[1]{Color.RESET}  🎮  New Game")
            print(f"  {Color.YELLOW}[2]{Color.RESET}  🏆  Leaderboard")
            print(f"  {Color.CYAN}[3]{Color.RESET}  📊  Statistics")
            print(f"  {Color.MAGENTA}[4]{Color.RESET}  👤  Change Name")
            print(f"  {Color.RED}[5]{Color.RESET}  🚪  Quit\n")
            print(f"  {Color.DIM}Choice: {Color.RESET}", end="")
            choice = input().strip()
            if choice == "1":
                diff = self._pick_difficulty()
                if diff:
                    HangmanGame(diff, self.player_name).play()
            elif choice == "2": self._show_leaderboard()
            elif choice == "3": self._show_stats()
            elif choice == "4": self.player_name = self._get_player_name()
            elif choice == "5":
                print(f"\n{Color.CYAN}  Goodbye, {self.player_name}! 👋{Color.RESET}\n")
                break


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    try:
        clear_screen()
        print_banner()
        MainMenu().run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing Hangman Deluxe! Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
