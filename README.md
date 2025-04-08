# coverdl
A command-line tool for downloading high quality album cover art.

# Installation

```
pip install coverdl
```

# Usage

Download cover art from album directory:

```
coverdl /artist/album/
```

Download cover art using track file:
```
coverdl "/artist/album/01 - Track Title.flac"
```

By default, the Apple Music and Deezer providers will be used to find cover art. You can specify a different provider like so:

```
coverdl -p itunes /artist/album
```

You can specify more than one provider by passing the `-p` option more than once:

```
coverdl -p applemusic -p itunes /artist/album
```

The order in which the providers are specified matters, as they will be used for priority ranking.

Click [here](https://github.com/viown/coverdl/blob/7d45d6f80a80ab45c87f80a924522ca4512c1347/coverdl/providers/source.py#L3) for a list of providers.

## Upgrading

> **Note:** The upgrading feature has not been implemented yet, below shows what it would look like.

coverdl will not download cover art for albums that already have them. Instead, you can upgrade them to a better quality version.

The `--upgrade` option allows you to upgrade your existing cover art to a better quality version (if found) by comparing the similarity of both images. This allows you to safely upgrade your existing cover art while being sure that a different version won't be downloaded by mistake:

```
coverdl --upgrade /artist/album/
```

Your old cover art will not be deleted, it will be renamed: e.g `cover.jpg` to `cover.jpg.bk`
To tell coverdl to delete it, pass the `--delete-old-covers` option.

In order for cover art to be considered an "upgrade," it must be larger in size. Use the `--max-size` option (in MBs) to prevent coverdl from exceeding a certain size. By default, this value is set to 10M.

## Downloading for an entire music library

If you have a large music library and you wish to download or upgrade cover art for all albums, use the `-r/--recursive` option while passing the path to your media library:

```
coverdl -r /music
```

The recursive option assumes the following directory structure in the `/music` directory:
```
/music/
├─ Artist Name One/
│  ├─ Album/
│  │  ├─ 01 - Track Title.flac
```

### When using --upgrade

Using `--upgrade` alongside `-r/--recursive` can be slow, and each run of the command will take the same length of time.

You can tell coverdl to skip already upgraded cover art on the next run by passing a cache file:
```
coverdl -r --upgrade /music --cache /PATH/TO/CACHE/cache.txt
```