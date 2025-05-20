import typer
from core.commands import build, add, tests

app = typer.Typer()
app.add_typer(build.app, name="build")
app.add_typer(add.app, name="add")
app.add_typer(tests.app, name="tests")

if __name__ == "__main__":
    app()
