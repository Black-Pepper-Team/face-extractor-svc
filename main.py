# API + CLI imports
import logging
import typer
from typing_extensions import Annotated
from pathlib import Path

# Internal imports
import debug
import src.api.main as api
import src.model.migrate as db
import face_recognition

from src.extractor.embedding import FeatureExtractor, FaceExtractionStatus
from src.contracts.oracle import ContestContract
from src.config.env import EnvConfig

logging.basicConfig(level=logging.INFO)

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

@app.command()
def create_contest(
    img_path: Annotated[Path, typer.Option(help='Path to image')] = 'test/ivan_1.jpg',
    duration: Annotated[int, typer.Option(help='Duration of contest')] = 60,
) -> None:
    img = face_recognition.load_image_file(img_path)
    extractor = FeatureExtractor(img)
    
    embedding, status = extractor.extract_discrete_features()
    match status:
        case FaceExtractionStatus.NO_FACE_FOUND:
            print("No face in image")
            exit(1)
        case FaceExtractionStatus.TOO_MANY_PEOPLE:
            print("too many people on image")
            exit(2)
    cfg = EnvConfig()
    contest = ContestContract(cfg.eth_provider, cfg.contest_address, cfg.private_key)

    txid = contest.createcontest(embedding, duration)
    print(f"Create contest {txid=}")

@app.command()
def finalize_contest() -> None:
    cfg = EnvConfig()
    contest = ContestContract(cfg.eth_provider, cfg.contest_address, cfg.private_key)

    contest_id = contest.latest_contest_id()

    txid = contest.finalizecontest(contest_id)
    print(txid.hex())
    
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
        db.migrate_up()
        print('Database migrated up')
    except Exception as e:
        logging.error(f'Error while migrating up: {e}')
    
@app.command()
def migrate_down() -> None:
    """
    Migrates the database down
    """
    
    try:
        db.migrate_down()
        print('Database migrated down')
    except Exception as e:
        logging.error(f'Error while migrating down: {e}')

if __name__ == '__main__':
    app()
    
