start a neovim instance with a socket

```
nvim --listen /tmp/nvim.sock
```

then run the following command

```
python insert_to_file.py /tmp/nvim.sock --save
```
