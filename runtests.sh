#!/bin/zsh
echo
echo
echo
echo
echo

for test in `ls blocks/tests | cut -d '.' -f 1`; do
    python -c "import blocks.tests.$test"
done
