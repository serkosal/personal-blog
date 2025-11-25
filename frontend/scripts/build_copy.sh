#! /usr/bin/env bash

shopt -s nullglob # this makes *.js/*.css expand to nothing if no match

DJANGO_STATIC_BASE="../backend/blog/static/assets"
SCRIPTS_DEST="${DJANGO_STATIC_BASE}/scripts"
STYLES_DEST="${DJANGO_STATIC_BASE}/styles"

npm run build

mkdir -p $SCRIPTS_DEST
mkdir -p $STYLES_DEST

echo "deleting old files"
for f in "$SCRIPTS_DEST/*.js"; do
  [ -s "$f" ] && rm -f "$f"
done
for f in "$STYLES_DEST/*.css"; do
  [ -s "$f" ] && rm -f "$f"
done

echo "copying files"
for f in dist/assets/*.js; do
  if [ -s "$f" ] && grep -q '[^[:space:]]' "$f"; then
    cp "$f" "$SCRIPTS_DEST/"
  fi
done
for f in dist/assets/*.css; do
  if [ -s "$f" ] && grep -q '[^[:space:]]' "$f"; then
    cp "$f" "$STYLES_DEST/"
  fi
done

echo "done!"