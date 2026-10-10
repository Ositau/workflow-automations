"""Pick the next finished video package from the handoff folder.

A package is three files that share a name:
    <slug>.mp4   the video
    <slug>.png   the thumbnail (optional)
    <slug>.json  the details: slug, title, description, tags

The .json file is written last by whatever produces the video, so if it
exists the package is complete. A half-copied video is never picked up.

Prints one line of JSON for n8n to read:
    {"found": true, "slug": ..., "title": ..., "description": ..., "tags": ...,
     "mp4": <path>, "thumbnail": <path or "">}
or  {"found": false}

Usage:  python pick_next.py [handoff_folder]
The folder can also be set with the HANDOFF_DIR environment variable.
"""
import glob
import json
import os
import sys


def handoff_dir():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.environ.get("HANDOFF_DIR", "")


def main():
    folder = handoff_dir()
    if not folder or not os.path.isdir(folder):
        print(json.dumps({"found": False, "error": f"handoff folder not found: {folder}"}))
        return
    for meta_path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            slug = meta["slug"]
        except Exception:
            continue  # unreadable or incomplete details file: skip it
        mp4 = os.path.join(folder, meta.get("mp4_name", slug + ".mp4"))
        thumb = os.path.join(folder, meta.get("thumb_name", slug + ".png"))
        if not os.path.exists(mp4):
            continue
        print(json.dumps({
            "found": True,
            "slug": slug,
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "mp4": mp4,
            "thumbnail": thumb if os.path.exists(thumb) else "",
        }))
        return
    print(json.dumps({"found": False}))


if __name__ == "__main__":
    main()
