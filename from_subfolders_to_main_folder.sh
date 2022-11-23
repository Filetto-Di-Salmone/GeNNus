rm -vrf README.txt

rm -vrf checksums

find . -mindepth 2 -type f -print -exec mv {} . \;