import json
import zipfile
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from typing import Annotated, Any, Final, Optional

import requests
import typer
from rich import print
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from slugify import slugify
from typer import Argument, Option, Typer

# The Typer application
app: Final[Typer] = typer.Typer()

# The default Minecraft version
DEFAULT_MC_VERSION: Final[str] = "1.20"
# The default output directory for generated packs
DEFAULT_PACK_DIR: Final[Path] = Path("./packs/")


@app.command()
def generate(
    packs: Annotated[
        list[str],
        Argument(
            metavar="📦 PACKS...",
            help="Vanilla Tweaks pack names in format 'Category/Pack Name'.",
            show_default=False,
        ),
    ],
    mc_version: Annotated[str, Option(help="The Minecraft version.")] = DEFAULT_MC_VERSION,
    outdir: Annotated[Optional[Path], Option(help="The pack output directory.")] = DEFAULT_PACK_DIR,
) -> None:
    """Download Vanilla Tweaks packs into separate Minecraft resource packs."""

    print(f"\n:package: Requested [blue bold]{len(packs)}[/blue bold] Vanilla Tweaks pack/s\n")

    outdir.mkdir(exist_ok=True)

    # Fetch pack definitions
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TaskProgressColumn(),
        transient=True,
    ) as progress:
        # Fetch pack definitions
        task = progress.add_task("Fetching pack definitions", total=0)
        res = requests.get(f"https://vanillatweaks.net/assets/resources/json/{mc_version}/rpcategories.json")
        res.raise_for_status()
        metadata: dict[str, Any] = res.json()
        categories: dict[str, dict[str, Any]] = {  # {category: {pack: {...}, ...}, ...}
            entry["category"]: {item["display"]: item for item in entry["packs"]} for entry in metadata["categories"]
        }
        progress.remove_task(task)

        # Validate requested packs
        task = progress.add_task("Validating requested packs...", total=len(packs))
        chosen_packs: dict[str, dict[str, Any]] = {}  # {category: {pack: {...}, ...}, ...}
        for category, items in groupby([pack.split("/", 1) for pack in packs], itemgetter(0)):
            if category in categories:
                chosen_packs[category] = {}
                for _, item in items:
                    if item in categories[category]:
                        chosen_packs[category][item] = categories[category][item]
                        progress.advance(task, 1)
                    else:
                        print(f"[red]Unknown pack:[/red] [dim]{category} »[/dim] {item}")
                        exit(1)
            else:
                print(f"[red]Unknown category:[/red] {category}")
                exit(1)

    # Download and adjust each pack
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:

        def process(category: str, pack: dict[str, Any]) -> None:
            # Track the task progress
            category_slug: str = slugify(category)
            task = progress.add_task(f"[dim]{category} »[/dim] {pack['display']}", total=4)

            # Generate the pack archive
            res = requests.post(
                "https://vanillatweaks.net/assets/server/zipresourcepacks.php",
                data={"version": mc_version, "packs": json.dumps({category_slug: [pack["name"]]})},
            )
            res.raise_for_status()
            progress.advance(task, 1)

            # Download the archived pack
            res = requests.get(f"https://vanillatweaks.net/{res.json()['link']}")
            res.raise_for_status()
            pack_content: BytesIO = BytesIO(res.content)
            progress.advance(task, 1)

            # Fetch the actual pack image
            res = requests.get(
                f"https://vanillatweaks.net/assets/resources/icons/resourcepacks/{mc_version}/{pack['name']}.png?v1"
            )
            res.raise_for_status()
            img: bytes = res.content
            progress.advance(task, 1)

            # Modify the archived pack
            with zipfile.ZipFile(pack_content, "r") as original, zipfile.ZipFile(
                outdir / f"Vanilla Tweaks - {pack['display']}.zip", mode="w"
            ) as archive:
                # Load the pack metadata
                with original.open("pack.mcmeta", "r") as file:
                    content: dict[str, Any] = json.loads(file.read())
                # Update the pack description
                with archive.open("pack.mcmeta", "w") as file:
                    content["pack"]["description"] = f"{pack['display']}\nvanillatweaks.net"
                    file.write(json.dumps(content, indent=2).encode())
                # Update the pack image
                archive.writestr("pack.png", img)
                # Copy remaining files
                for file in original.filelist:
                    if file.filename not in ("pack.mcmeta", "pack.png"):
                        archive.writestr(file, original.read(file))
            progress.advance(task, 1)

        with ThreadPoolExecutor(max_workers=5) as pool:
            for category_name, entries in chosen_packs.items():
                for pack_data in entries.values():
                    pool.submit(process, category=category_name, pack=pack_data)

    print(f"\n:tada: [green]Success![/green] [link={outdir.absolute()}]{outdir.absolute()}[/link]")


if __name__ == "__main__":
    app()
