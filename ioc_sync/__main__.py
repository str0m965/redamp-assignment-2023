import click

from .db import recreate_all
from .service import CommonService


@click.group()
def cli():
    pass


@click.command('list-sources')
def list_data_sources():
    """
    List all data sources in database
    """
    service = CommonService.get_instance()
    data_sources = service.get_data_sources()
    for data_source in data_sources:
        click.echo(f"{data_source.id} {data_source.url} {data_source.updated_at}")


@click.command('find-one-ip')
@click.argument('ip')
def find_one_ip(ip):
    """
    Find one ip ioc
    """
    service = CommonService.get_instance()
    ip_ioc = service.get_ip_ioc(ip)
    click.echo(ip_ioc)
    if ip_ioc:
        click.echo(f"{ip_ioc.id} | {ip_ioc.url} | {ip_ioc.data_source.url}")
    else:
        click.echo(f"{ip} not found")


@click.command('find-one-url')
@click.argument('url')
def find_one_url(url):
    """
    Find one url ioc
    """
    service = CommonService.get_instance()
    url_ioc = service.get_url_ioc(url)
    if url_ioc:
        click.echo(f"{url_ioc.id} | {url_ioc.url} | {url_ioc.data_source.url}")
    else:
        click.echo(f"{url} not found")


@click.command('update-all')
def sync_all():
    """
    Update all iocs from known data sources
    """
    service = CommonService.get_instance()
    service.sync_all_iocs()


@click.command('init-db')
def init_db():
    """
    Initialize database, remove all data
    :return:
    """
    recreate_all()


cli.add_command(list_data_sources)
cli.add_command(find_one_ip)
cli.add_command(find_one_url)
cli.add_command(sync_all)
cli.add_command(init_db)

if __name__ == '__main__':
    cli()
