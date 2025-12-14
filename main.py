import textwrap

from auth import get_user_progress, set_user_progress
from chapter_loop import run_chapter
from config import NUM_CHAPTERS
from database import init_db
from login import login, signup



def main():
    init_db()
    art = """  █████   ██▓ ██▒   █▓▓█████   ██████ 
▒██▓  ██▒▓██▒▓██░   █▒▓█   ▀ ▒██    ▒ 
▒██▒  ██░▒██▒ ▓██  █▒░▒███   ░ ▓██▄   
░██  █▀ ░░██░  ▒██ █░░▒▓█  ▄   ▒   ██▒
░▒███▒█▄ ░██░   ▒▀█░  ░▒████▒▒██████▒▒
░░ ▒▒░ ▒ ░▓     ░ ▐░  ░░ ▒░ ░▒ ▒▓▒ ▒ ░
 ░ ▒░  ░  ▒ ░   ░ ░░   ░ ░  ░░ ░▒  ░ ░
   ░   ░  ▒ ░     ░░     ░   ░  ░  ░  
    ░     ░        ░     ░  ░      ░  
                  ░                   """
    print(textwrap.indent(art, '          '))
    warn = "*** TRIGGER WARNING ***"
    print(textwrap.indent(warn, '                 '))
    print("This game contains themes of self-harm and emotional exhaustion.\n")

    while True:
        print("[1] Log In")
        print("[2] Sign Up")
        print("[3] Quit")
        sel = input("> ").strip()
        if sel == "1":
            uid, username = login()
            if uid:
                break
        elif sel == "2":
            uid, username = signup()
            if uid:
                break
        elif sel == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid option.")

    # main loop
    while True:
        chapter = get_user_progress(uid)
        if chapter > NUM_CHAPTERS:
            print("All chapters completed. Resetting progress to 1.")
            set_user_progress(uid, 1)
            chapter = 1

        print("\n================================================================")
        print("           W E L C O M E   T O   Q I V E S")
        print("================================================================")
        print("You are entering the classified digital archives for the case of Zae.\n")
        print("Type 'p' to proceed.")
        print("Type '--help' for game commands.\n")

        # --help behavior on proceed prompt
        while True:
            opt = input("> ").strip().lower()
            if opt == "p":
                break
            if opt == "--help":
                print("Commands inside the game:")
                print(f"{' ':<3}{'ls	             Show files/folders'}")
                print(f"{' ':<3}{'cd <dir>	         Go into a folder'}")
                print(f"{' ':<3}{'cd ..	         Go back one folder'}")
                print(f"{' ':<3}{'pwd	             Show current location'}")
                print(f"{' ':<3}{'file <name>	     Show file type'}")
                print(f"{' ':<3}{'cat <file>	     Show file content'}")
                print(f"{' ':<3}{'save	             Save the progress'}")
                print(f"{' ':<3}{'exit	             Exit the game'}")
                continue
            print("[!] Invalid. Type 'p' or '--help'.")

        finished = run_chapter(uid, username, chapter)
        if finished:

            if chapter == NUM_CHAPTERS:
                print(f"\nChapter {chapter} is complete.")
                print(f"\n=== ALL CHAPTERS COMPLETED ===")
                print("Case concluded. Thank you.")

                set_user_progress(uid, 1)
                return
            else:
                new_ch = chapter + 1
                set_user_progress(uid, new_ch)
                print(f"\nChapter {chapter} complete. Chapter {new_ch} unlocked.")
                cont = input("Proceed to next chapter? (y/N): ").strip().lower()
                if cont == "y":
                    continue
                else:
                    return
        else:
            return

if __name__ == "__main__":
    main()
