#!/bin/bash

# Usage: if no args are given, print help and exit
if [ $# -lt 2 ]; then
  echo "Usage: $0 START_PAGE END_PAGE"
  echo
  echo "Example: $0 0 100"
  echo
  echo "Before running, edit this script and set:"
  echo "  isbn   (your book's ISBN)"
  echo "  cookie (your authentication cookie string)"
  exit 1
fi

# —————— User configuration ——————
isbn=""   # ← your own ISBN
cookie=""  # ← your full cookie here
# ——————————————————————————————

# sanity check: make sure required vars are not empty
if [ -z "$isbn" ] || [ -z "$cookie" ]; then
  echo "ERROR: You must set both 'isbn' and 'cookie' at the top of this script."
  exit 1
fi

# create directory if needed
if [ ! -d "$isbn" ]; then
  mkdir -p "$isbn"
fi

START_PAGE=$1
END_PAGE=$2

for (( i=START_PAGE; i<=END_PAGE; i++ )); do
  URL="https://jigsaw.vitalsource.com/books/${isbn}/images/${i}"
  FILENAME="${i}.jpg"
  OUTPATH="${isbn}/${FILENAME}"

  curl -s \
    -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0' \
    -H "${cookie}" \
    "$URL" -o "$OUTPATH"

  # small pause to let the file system catch up
  sleep 1

  # check in the isbn directory, not the current one
  if [ -f "$OUTPATH" ]; then
    echo "Downloaded page ${i} → ${OUTPATH}. waiting 2 seconds…"
    sleep 2
  else
    echo "Failed to download page ${i}"
    sleep 2
  fi
done
