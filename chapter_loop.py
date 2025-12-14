import secrets
import sys

from auth import get_seed, save_seed, log_action, set_user_progress
from random_fs_generator import build_fs
from score import ScoreTracker, save_score, get_best_score
from story import CHAPTER_GOALS
from util_dirs_file import is_dir, is_file


def run_chapter(user_id, username, chapter):
    best = get_best_score(chapter)
    if best:
        print(f"🏆 Best score for Chapter {chapter}: {best['score']}")
        print(f"👤 Record holder: {best['username']}")
    else:
        print("🏆 No record yet. Be the first!")
    tracker = ScoreTracker(user_id, chapter, time_limit=500)

    seed = get_seed(user_id, chapter)
    if seed is None:
        seed = secrets.randbelow(2**32)
        save_seed(user_id, chapter, seed)


    file_system = build_fs(user_id, chapter, seed)["root"]

    # Path works like: ["root", "folder", "subfolder"]
    current_path = ["root"]


    def get_current_folder():
        folder = file_system
        for name in current_path[1:]:
            folder = folder[name]
        return folder


    print("\n" + CHAPTER_GOALS.get(chapter, f"CHAPTER {chapter}"))

    print("\n⏳ Timer started. Good luck.\n")
    tracker.start()
    # MAIN COMMAND LOOP

    while True:
        # TIME CHECK
        if tracker.is_time_up():
            print("\n⏰ TIME UP!")
            score = tracker.calculate_score()
            save_score(user_id, chapter, score)
            print(f"Your score: {score}")
            return False

        prompt = "/" + "/".join(current_path[1:]) if len(current_path) > 1 else "/"

        try:
            command_input = input(f"{username}@qives:{prompt}$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nUse 'save' to store progress or 'exit' to quit.")
            continue

        if not command_input:
            continue

        tracker.record_command()

        parts = command_input.split()
        command = parts[0]
        current_folder = get_current_folder()

        # HELP!!!!!!!
        if command == "--help":
            print("""
Commands:
ls              Show files and folders
cd <dir>        Enter a folder
cd ..           Go back
pwd             Show current path
file <name>     Show file type
cat <file>      Show file content
save            Save progress
exit            Quit game
""")
            continue


        if command == "ls":
            print("  ".join(sorted(current_folder.keys())))
            log_action(user_id, f"ls @ {'/'.join(current_path)}")
            continue


        if command == "pwd":
            print(prompt)
            log_action(user_id, f"pwd @ {'/'.join(current_path)}")
            continue


        if command == "cd":
            if len(parts) < 2:
                print("cd: missing operand")
                continue

            target = parts[1]

            if target == "..":
                if len(current_path) > 1:
                    current_path.pop()
                else:
                    print("cd: already at root")
                log_action(user_id, "cd ..")
                continue

            if is_dir(current_folder, target):
                current_path.append(target)
                log_action(user_id, f"cd {target} @ {'/'.join(current_path)}")
            else:
                print("cd: no such directory")
            continue


        if command == "file":
            if len(parts) < 2:
                print("file: missing argument")
                continue

            name = parts[1]

            if is_dir(current_folder, name):
                print(f"{name}: directory")
            elif is_file(current_folder, name):
                preview = "\n".join(current_folder[name].splitlines()[:3])
                print(f"{name}: text file\n{preview}")
            else:
                print("file: no such file")

            log_action(user_id, f"file {name} @ {'/'.join(current_path)}")
            continue


        if command == "cat":
            if len(parts) < 2:
                print("cat: missing file")
                continue

            name = parts[1]

            if is_file(current_folder, name):
                print(current_folder[name])
                log_action(user_id, f"cat {name} @ {'/'.join(current_path)}")

                if name == "next.txt":
                    print("\n--- CHAPTER COMPLETE ---")
                    score = tracker.calculate_score()
                    save_score(user_id, chapter, score)
                    print(f"🏁 Final Score: {score}")
                    return True

            elif is_dir(current_folder, name):
                print(f"cat: {name}: is a directory")
            else:
                print("cat: cannot open file")
            continue

        if command == "save":
            score = tracker.calculate_score()
            save_score(user_id, chapter, score)
            set_user_progress(user_id, chapter)
            print(f"Progress saved. Score: {score}")
            log_action(user_id, "save")
            return False

        if command == "exit":
            score = tracker.calculate_score()
            save_score(user_id, chapter, score)
            set_user_progress(user_id, chapter)
            log_action(user_id, "exit")
            print("Game saved. Exiting...")
            sys.exit(0)


        print("Unknown command. Type --help.")
