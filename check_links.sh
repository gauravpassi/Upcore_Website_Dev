#!/bin/bash

echo "=== CHECKING ALL INTERNAL LINKS ==="
echo ""

# List all HTML files (exclude demos)
html_files=$(find . -type f -name "*.html" ! -path "./demos/*" | sort)

# Extract all unique internal links
all_links=$(grep -roh 'href="/[^"]*"\|src="/[^"]*"' --include="*.html" ! --include-dir=demos . | sed 's/href="\|src="\|"//g' | sort | uniq)

# Create list of existing resources
echo "Checking existence of resources..."

broken=""
for link in $all_links; do
  # Skip anchors (just check the base path)
  base_link="${link%#*}"
  
  # Skip external/data URLs
  if [[ "$base_link" =~ http|www\.|maps|googletagmanager ]]; then
    continue
  fi
  
  # Check if file exists (with or without .html)
  if [ "$base_link" = "/" ]; then
    # Root always exists
    continue
  elif [ -f ".${base_link}.html" ]; then
    # Has .html extension
    continue
  elif [ -f ".${base_link}/index.html" ]; then
    # Is a directory with index
    continue
  elif [ -f ".${base_link}" ]; then
    # File exists as-is
    continue
  else
    broken="$broken$link
"
  fi
done

if [ -n "$broken" ]; then
  echo "BROKEN LINKS/RESOURCES FOUND:"
  echo "$broken" | sort | uniq
else
  echo "No broken links found!"
fi
