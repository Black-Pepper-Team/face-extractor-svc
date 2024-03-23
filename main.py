# API + CLI imports
import logging
import typer
from typing_extensions import Annotated
from pathlib import Path

# Internal imports
import debug
import src.api.main as api
import src.model.claim as claim_db

app = typer.Typer(help="Face recognition API for the Black Pepper Team")

# --- Debugging commands ---
@app.command()
def debug_embeddings(
        img_1_path: Annotated[Path, typer.Option(help='Path to image 1')] = 'test/anton_1.jpg',
        img_2_path: Annotated[Path, typer.Option(help='Path to image 2')] = 'test/ivan_1.jpg',
    ) -> None:
    debug.debug_embeddings(img_1_path, img_2_path)
    
@app.command()
def debug_discrete_embeddings(
        img_1_path: Annotated[Path, typer.Option(help='Path to image 1')] = 'test/ivan_1.jpg',
        img_2_path: Annotated[Path, typer.Option(help='Path to image 2')] = 'test/ivan_2.jpg',
    ) -> None:
    debug.debug_discrete_embeddings(img_1_path, img_2_path)
    
@app.command()
def debug_encode(img_path: Annotated[Path, typer.Argument(help='Path to image')]) -> None:
    debug.debug_encode(img_path=img_path)
    
@app.command()
def debug_show_npy_img(img_path: Annotated[Path, typer.Argument(help='Path to image')]) -> None:
    debug.debug_show_npy_img(img_path=img_path)
    
@app.command()
def debug_embeddings(
        img_1_path: Annotated[Path, typer.Option(help='Path to image 1')] = 'test/anton_1.jpg',
        img_2_path: Annotated[Path, typer.Option(help='Path to image 2')] = 'test/ivan_1.jpg',
    ) -> None:
    debug.debug_embeddings(img_1_path, img_2_path)
    
# --- Actually useful commands ---

@app.command()
def run_api() -> None:
    """Runs the service API"""
    
    api.run_api()
    
@app.command()
def migrate_up() -> None:
    """
    Migrates the database up
    """

    try:
        claim_db.migrate_up()
        print('Database migrated up')
    except Exception as e:
        logging.error(f'Error while migrating up: {e}')
    
@app.command()
def migrate_down() -> None:
    """
    Migrates the database down
    """
    
    try:
        claim_db.migrate_down()
        print('Database migrated down')
    except Exception as e:
        logging.error(f'Error while migrating down: {e}')

if __name__ == '__main__':
    app()
    