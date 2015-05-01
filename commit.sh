#!/bin/bash
python ./cleaner.py
echo "Enter commit message:"
read commitmsg
echo "Enter branch name:"
read branch

git add .
git commit -m "$commitmsg"
git push origin "$branch"
