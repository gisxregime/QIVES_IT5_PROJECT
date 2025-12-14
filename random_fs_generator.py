from random import Random
from auth import register_evidence
from config import DIRS_MIN, DIRS_MAX, FILES_MIN
from story import STORY_CHUNKS

def generate_name(rng, kind):
    words = ["old", "meta", "anon", "sys", "log", "temp", "dump", "trace"]

    if kind == "file":
        ext = rng.choice([".txt", ".log", ".dat"])
        return f"{rng.choice(words)}_{rng.randint(100, 999)}{ext}"

    return f"{rng.choice(words)}_{rng.randint(10, 99)}"

def generate_fake_content(rng):
    data = [
        "System log corrupted",
        "User session expired",
        "Trace ID: " + hex(rng.getrandbits(64)),
        "Cache entry missing",
    ]

    if rng.random() < 0.15:
        return "HINT: inspect unusual folders"

    return rng.choice(data)


def build_fs(user_id, chapter, seed, FILES_MAX = 40, HINT_FOLDER_TEPLATES=None):
    rng = Random(seed)
    filesystem = {}

    folder_count = rng.randint(DIRS_MIN, DIRS_MAX)
    folders = set()

    common_folders = ["logs", "history", "backups", "configs"]

    for name in common_folders:
        if len(folders) < folder_count and rng.random() < 0.7:
            folders.add(name)

    while len(folders) < folder_count:
        folders.add(generate_name(rng, "dir"))

    for f in folders:
        filesystem[f] = {}

    filesystem["root_files"] = {}

    total_files = rng.randint(FILES_MIN, FILES_MAX)

    for _ in range(total_files):
        file_name = generate_name(rng, "file")
        folder = rng.choice(list(filesystem.keys()))
        filesystem[folder][file_name] = generate_fake_content(rng)

    for folder in rng.sample(list(filesystem.keys()), min(3, len(filesystem))):
        if rng.random() < 0.5:
            subfolder = generate_name(rng, "dir")
            filesystem[folder][subfolder] = {}
            filesystem[folder][subfolder][generate_name(rng, "file")] = generate_fake_content(rng)

    possible_names = (HINT_FOLDER_TEPLATES or {}).get(
        chapter, ["case", "proof", "clue"]
    )

    hint_folder = rng.choice(possible_names) + "_" + str(rng.randint(100, 999))


    if rng.random() < 0.6:
        parent = rng.choice([f for f in filesystem if f != "root_files"])
        filesystem[parent][hint_folder] = {}
        filesystem[parent][hint_folder]["next.txt"] = STORY_CHUNKS.get(chapter, "NO STORY")
        path = f"/root/{parent}/{hint_folder}/next.txt"
    else:
        filesystem[hint_folder] = {}
        filesystem[hint_folder]["next.txt"] = STORY_CHUNKS.get(chapter, "NO STORY")
        path = f"/root/{hint_folder}/next.txt"

    register_evidence(user_id, chapter, path)

    return {"root": filesystem}

