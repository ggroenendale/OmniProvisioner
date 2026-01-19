## Adding Zot registry to kubernetes setup

Install podman with crun

- I chose crun over runc because crun is written in C and is a smaller file size and lower in memory.

```bash
sudo pacman -S crun podman
```
