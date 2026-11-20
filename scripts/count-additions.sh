#!/bin/bash
set -euo pipefail

readonly REPOSITORY_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SOURCE_NAMES_DIRECTORY="${REPOSITORY_DIRECTORY}/src/names"
readonly CATEGORY_TITLES=('Asteroid Postfixes' 'Asteroid Prefixes' 'Black Holes' 'Nebulae' 'Stars')
readonly CATEGORY_SUFFIXES=('asteroid_postfixes' 'asteroid_prefixes' 'black_holes' 'nebulae' 'stars')
readonly NAME_ENTRY_EXTRACTION='s/^[[:space:]]*"([^"]*)"[,]?[[:space:]]*$/\1/p'

count_unique_names() {
    local category_suffix="${1}"

    sed -nE "${NAME_ENTRY_EXTRACTION}" "${SOURCE_NAMES_DIRECTORY}/${category_suffix}"/*.json |
        sort -u |
        wc -l
}

for category_index in "${!CATEGORY_SUFFIXES[@]}"; do
    category_title="${CATEGORY_TITLES[${category_index}]}"
    category_suffix="${CATEGORY_SUFFIXES[${category_index}]}"

    echo " - ${category_title}: $(count_unique_names "${category_suffix}")"
done
