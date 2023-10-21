from __future__ import annotations

import json
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from typing import Final, Any, Optional

import requests
import typer
from rich.progress import SpinnerColumn, Progress, TextColumn, TaskProgressColumn, TaskID
from typer import Typer

# The Typer application
app: Final[Typer] = typer.Typer()


@app.command()
def generate(packs: list[str], mc_version: str = "1.20", outdir: Optional[Path] = None) -> None:
    """Download Vanilla Tweaks packs into separate Minecraft resource packs."""

    if not outdir:
        outdir = Path("./packs")
    outdir.mkdir(exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TaskProgressColumn(),
    ) as progress:
        def process(category: str, pack: str):
            # Track the task progress
            category_display: str = re.sub(r"(\w)([A-Z])", r"\1 \2", category).title()
            pack_display: str = re.sub(r"(\w)([A-Z])", r"\1 \2", pack).title()
            task = progress.add_task(f"[gray]{category_display} »[/gray] {pack_display}", total=4)

            # Generate the pack archive
            res = requests.post(
                "https://vanillatweaks.net/assets/server/zipresourcepacks.php",
                data={"version": mc_version, "packs": json.dumps({category: [pack]})},
            )
            res.raise_for_status()
            progress.advance(task, 1)

            # Download the archived pack
            res = requests.get(f"https://vanillatweaks.net/{res.json()['link']}")
            res.raise_for_status()
            pack_content: BytesIO = BytesIO(res.content)
            progress.advance(task, 1)

            # Fetch the actual pack image
            res = requests.get(f"https://vanillatweaks.net/assets/resources/icons/resourcepacks/{mc_version}/{pack}.png?v1")
            res.raise_for_status()
            img: bytes = res.content
            progress.advance(task, 1)

            # Modify the archived pack
            with zipfile.ZipFile(pack_content, "r") as original:
                with zipfile.ZipFile(outdir / f"Vanilla Tweaks - {pack_display}.zip", mode="w") as archive:
                    # Load the pack metadata
                    with original.open("pack.mcmeta", "r") as file:
                        content: dict[str, Any] = json.loads(file.read())
                    # Update the pack description
                    with archive.open("pack.mcmeta", "w") as file:
                        content["pack"]["description"] = f"{category_display} / {pack_display}\nvanillatweaks.net"
                        file.write(json.dumps(content, indent=2).encode())
                    # Update the pack image
                    archive.writestr("pack.png", img)
                    # Copy remaining files
                    for file in original.filelist:
                        if file.filename not in ("pack.mcmeta", "pack.png"):
                            archive.writestr(file, original.read(file))
            progress.advance(task, 1)

        with ThreadPoolExecutor(max_workers=3) as pool:
            for item in packs:
                category_name, pack_name = item.split("/", 1)
                pool.submit(process, category=category_name, pack=pack_name)


if __name__ == "__main__":
    app()
