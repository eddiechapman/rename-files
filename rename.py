import click
import csv
import pathlib


@click.command()
@click.argument("src", 
    type=click.Path(exists=True, dir_okay=True, path_type=pathlib.Path)
)
@click.option("-d", "--dest",
    type=click.Path(dir_okay=True, writable=True, path_type=pathlib.Path),
    help="Directory where files will copied to before renaming"
)
@click.option("-o", "--outfile",
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    default=pathlib.Path.cwd() / "filename_info.csv",
    help="Path to resulting CSV file containing filename analysis"
)
@click.option("-n", "--max_chars", 
    type=int,
    default=16,
    help="Maximum number of characters in filename stems"
)
def inspect(src, dest, outfile, max_chars):
    click.echo(f"Collecting filepaths for inspection...")
    filepaths = (p for p in src.rglob("*") if p.is_file())
    
    filepath_info = []
    click.echo(f"Inspecting filepaths from {click.style(src, fg='blue')}...")
    with click.progressbar(filepaths) as bar:
        for i, filepath in enumerate(bar, start=2):
            filepath_info.append({
                "src": src,
                "dest": dest,
                "path": filepath,
                "name": filepath.stem,
                "length": len(filepath.stem),
                "valid": len(filepath.stem) <= max_chars,
                "new name": filepath.stem,
                "new length": f"=LEN(G{i})",
                "new valid": f'=IF(H{i} < {max_chars + 1},"True","False")'
            })

    click.echo(f"Creating destination directory for renamed files: {click.style(dest, fg='blue')}...")
    dest.mkdir(exist_ok=True)

    click.echo(f"Writing results to outfile CSV: {click.style(outfile, fg='blue')}...")
    
    with outfile.open("w") as f:
        writer = csv.DictWriter(f, fieldnames=filepath_info[0].keys())
        writer.writeheader()
        writer.writerows(filepath_info)

    click.echo(f"Success. Results written to {click.style(outfile, fg='blue')}")
    click.echo(f"Edit the filenames in the `new name` column of {click.style(outfile, fg='blue')}")
    click.echo(f"When you are finished, run `python3 rename -f {outfile}` to move and rename the files")


@click.command()
@click.option("-f", "--infile",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    help="Path to CSV file containing file renaming info"
)
def rename(infile):
    click.echo(f"Renaming files using file info from {click.style(infile, fg='blue')}...")
    with infile.open("r") as f:
        reader = csv.DictReader(f)
        with click.progressbar(row for row in reader) as bar:
            for row in bar:
                src = pathlib.Path(row["src"])
                dest = pathlib.Path(row["dest"])
                file = pathlib.Path(row["path"])
                target = dest / file.relative_to(src).with_stem(row["new name"])
                target.parents[0].mkdir(parents=True, exist_ok=True)
                try:
                    file.rename(target)
                except FileNotFoundError as e:
                    file.print(e)

    click.echo(f"File renaming complete.")
