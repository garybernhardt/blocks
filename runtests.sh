#!/bin/zsh
echo
echo
echo
echo
echo

for test in `ls pyblocks/tests | cut -d '.' -f 1`; do
    python -c "import pyblocks.tests.$test"
done
