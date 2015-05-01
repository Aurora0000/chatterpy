#!/bin/bash
echo "Enter category:"
read category
mkdir -p ./plugins/"$category"

echo "Enter plugin short name (usually in camelCase, NO spaces):"
read name
cp -r ./plugins/examplePlugin ./plugins/"$category"/"$name"

echo "Enter plugin full name (with spaces)"
read fullname

mv ./plugins/"$category"/"$name"/"examplePlugin.py" ./plugins/"$category"/"$name"/"$name.py"
mv ./plugins/"$category"/"$name"/"examplePlugin.chatterconf" ./plugins/"$category"/"$name"/"$name.chatterconf"
mv ./plugins/"$category"/"$name"/"examplePlugin.yapsy-plugin" ./plugins/"$category"/"$name"/"$name.yapsy-plugin"

sed -i -e "s/false/true/g" ./plugins/"$category"/"$name"/"$name.chatterconf"
sed -i -e "s/examplePlugin/$name/g" ./plugins/"$category"/"$name"/"$name.py"
sed -i -e "s/examplePlugin/$name/g" ./plugins/"$category"/"$name"/"$name.yapsy-plugin"
sed -i -e "s/Example Plugin/$fullname/g" ./plugins/"$category"/"$name"/"$name.yapsy-plugin"

echo "Your plugin is now available at ./plugins/$category/$name/"


