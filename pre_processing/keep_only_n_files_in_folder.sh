cd Electronic

find . -maxdepth 1 -type f -name "*.mp3" -print0 | sort -z | head -z -n 2000 | xargs -0 rm
