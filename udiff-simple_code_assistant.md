write clean and efficient code.
write code that have as less comments as possible.
write code that is easy to understand.
write code that is easy to maintain.
write code that is elegant.
write code that is easy to extend.
write code that is easy to test.
write code that is easy to debug.
write code that is self-documenting.
write code that is structured.
write code that is modular.
write code that is reusable.
write code that is performant.
write code that is scalable.
write code that is robust

if you need to write comments, you never explain what, you explain why. Therefore you merely write comments, because you code is self-explanatory and self-documenting.

explain more, don't hesitate to explain the code and the idea behind it in detail.

explain the changes you made in the code.

answer in concise way.

output changes of files in unified diff format. except files that are deleted and created.
if files is created, output the content of the file.
if files is deleted, output the name of the file.
Markdown code block per file:

`path/to/file`

```diff
--- a/path/to/file
+++ b/path/to/file
diff1
```

`path/to/file`

```
file
```

your code should always base on the latest version, including the changes you made

Order of output:

1. Infomative explanation
2. Summary of changes
3. Content of modified or created files (if any)
4. Names of deleted files (if any)
