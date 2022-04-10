# rename-files

> Move and rename contents of a directory according to values in a CSV file.

I use this tool to shorten names of audio sample files for my MPC1000, which can only accept filenames of 16 characters or less (not counting file extensions).

I find it easy to use find+replace (ctrl+h) within LibreOffice Calc to shorten filenames in bulk.

## Features

- specify new file names via CSV file
- CSV file contains formula columns to indicate if name exceeds maximum length
- files are copied recursively from `src` to `dest` directories, preserving inner structure
- `src` directory is not modified

## Installation

```
git clone https://github.com/eddiechapman/rename-files.git
cd rename-files
python3 -m venv venv
venv/bin/activate
pip install .
```

## Usage

Run `inspect` on a directory containing files you'd like to rename. Provide the maximum character length for filenames (optional), the directory where renamed files will be moved, and the name of the resulting CSV file.

```
inspect /mydir -d /newdir -o fileinfo.csv
```

Open the resulting `fileinfo.csv` to see the paths and filename lengths of each file in `mydir/`.

Change the values in the `new name` column of `fileinfo.csv` to your desired filenames.

Run `rename` with the location of `fileinfo.csv`, and the contents of `mydir/` will be moved to `newdir/` and renamed accordingly. 

```
rename -f fileinfo.csv
```
