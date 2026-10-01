#!/bin/sh
# upall.sh <page-id-urlencoded> : POSTs builder, tokens, components, then screens to the UUIDs in urls.txt
cd "$(dirname "$0")"
files="builder.data.png out/tokens.data.png out/components.data.png $(ls out/[HE]*.data.png | tr '\n' ' ')"
i=1; for f in $files; do u=$(sed -n "${i}p" urls.txt); [ -z "$u" ] && break; r=$(curl -s -F "file=@$f;type=image/png" "https://mcp.figma.com/mcp/upload/$u/submit?scaleMode=FILL&currentPageId=$1"); echo "$(basename $f .data.png) $(echo "$r" | sed -n 's/.*"imageHash":"\([^"]*\)".*/\1/p')"; i=$((i+1)); done > out/hashes.txt
cat out/hashes.txt
