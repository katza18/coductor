import typer
from core.commands import build

app = typer.Typer()
app.add_typer(build.app, name="build")

if __name__ == "__main__":
    app()
