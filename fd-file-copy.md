# Shortcut to copy the contents of frontend and backend source files to clipboard

by exclusive

```sh
txt1=$(echo frontend\\n---) ; txt2=$(fd . frontend/src --type f --exclude "*.json" | xargs cat) ; txt3=$(echo backend\\n---) ; txt4=$(fd . backend/src  --type f --exclude "*.json" | xargs cat); echo $txt1\\n\`\`\`tsx\\n$txt2\\n\`\`\`\\n\\n$txt3\\n\`\`\`python\\n$txt4\\n\`\`\` | pbcopy
```

by file type

```sh
txt1=$(echo frontend\\n---) ; txt2=$(fd . frontend/src --type f -e tsx -e ts | xargs cat) ; txt3=$(echo backend\\n---) ; txt4=$(fd . backend/src  --type f -e py | xargs cat); echo $txt1\\n\`\`\`tsx\\n$txt2\\n\`\`\`\\n\\n$txt3\\n\`\`\`python\\n$txt4\\n\`\`\` | pbcopy
```
