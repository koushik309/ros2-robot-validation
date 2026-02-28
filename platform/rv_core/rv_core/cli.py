import click
from .spec import TestSpec

@click.group()
def cli():
    pass

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
def run(spec_file):
    """Run a validation test from a YAML spec file."""
    spec = TestSpec.from_yaml(spec_file)
    click.echo(f"✅ Spec loaded: {spec.robot.name} in {spec.run.mode} mode")
    click.echo(f"   Duration: {spec.run.duration_s}s")
    click.echo(f"   Tests: {[t.id for t in spec.tests]}")
    # For now, just exit
    click.echo("🚀 Test execution not yet implemented. Stay tuned!")

def main():
    cli()

if __name__ == '__main__':
    main()