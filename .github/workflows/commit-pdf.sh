git checkout --orphan pdf
git rm -rf .
git add -f MastodonManual.pdf
git -c user.name='jyt' -c user.email='jyt' commit -m "Adding the manual pdf."
git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/$GITHUB_REPOSITORY pdf

