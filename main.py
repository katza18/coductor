import typer
from core.commands import build, scaffold, add_feature, todo, generate_tests, ask

app = typer.Typer()
app.add_typer(build.app, name="build")
app.add_typer(scaffold.app, name="scaffold")
app.add_typer(add_feature.app, name="feature")
app.add_typer(todo.app, name="todo")
app.add_typer(generate_tests.app, name="tests")
app.add_typer(ask.app, name="ask")

if __name__ == "__main__":
    app()
