#!/bin/bash

SUBMOD="ui-star-names"

CELESTIAL_BODIES_DIR="common/random_names/base"
CELESTIAL_BODIES_COUNT=$(cat $SUBMOD/$CELESTIAL_BODIES_DIR/* | sed 's/ //g' | sed '/^\s*$\|=\|}\|^#/d' | uniq | wc -l)

echo "Celestial bodies:" $CELESTIAL_BODIES_COUNT

