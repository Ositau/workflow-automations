"""Remove a published video package from the handoff folder.

Deletes <slug>.mp4, <slug>.png and <slug>.json. n8n calls this after a
successful upload, so the same video is never picked up and uploaded twice.

Prints one line of JSON:
    {"ok": true, "slug": ..., "removed": [...]}
or  {"ok": false, "error": ...}

Usage:  python mark_done.py <slug> [handoff_folder]
The folder can also be set with the HANDOFF_DIR environment variable.
"""
import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: mark_done.py <slug> [handoff_folder]"}))
        return
    slug = os.path.basename(sys.argv[1])  # a slug is a file name, never a path
    folder = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("HANDOFF_DIR", "")
    if not folder or not os.path.isdir(folder):
        print(json.dumps({"ok": False, "slug": slug, "error": f"handoff folder not found: {folder}"}))
        return
    removed = []
    for ext in (".mp4", ".png", ".json"):
        path = os.path.join(folder, slug + ext)
        if os.path.exists(path):
            try:
                os.remove(path)
                removed.append(slug + ext)
            except Exception as e:
                print(json.dumps({"ok": False, "slug": slug, "error": str(e)}))
                return
    print(json.dumps({"ok": True, "slug": slug, "removed": removed}))


if __name__ == "__main__":
    main()
