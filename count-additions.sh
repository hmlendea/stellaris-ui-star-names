#!/bin/bash

CELESTIAL_BODIES_DIR="ui-star-names/common/random_names/base"

ASTEROID_POSTFIXES_COUNT=$(cat $CELESTIAL_BODIES_DIR/ui_asteroid-postfixes* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | sort | sed 's/\"//g' | uniq | wc -l)
ASTEROID_PREFIXES_COUNT=$(cat $CELESTIAL_BODIES_DIR/ui_asteroid-prefixes* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | sort | sed 's/\"//g' | uniq | wc -l)
BLACK_HOLES_COUNT=$(cat $CELESTIAL_BODIES_DIR/ui_black-holes* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | sort | sed 's/\"//g' | uniq | wc -l)
NEBULAS_COUNT=$(cat $CELESTIAL_BODIES_DIR/ui_nebulas* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | sort | sed 's/\"//g' | uniq | wc -l)
STARS_COUNT=$(cat $CELESTIAL_BODIES_DIR/ui_stars* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | sort | sed 's/\"//g' | uniq | wc -l)

echo " - Asteroid Postfixes:" $ASTEROID_POSTFIXES_COUNT
echo " - Asteroid Prefixes:" $ASTEROID_PREFIXES_COUNT
echo " - Black Holes:" $BLACK_HOLES_COUNT
echo " - Nebulas:" $NEBULAS_COUNT
echo " - Stars:" $STARS_COUNT
