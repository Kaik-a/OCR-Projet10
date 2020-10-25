"""Command to update the default database"""
import logging
from datetime import datetime
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError

from catalog.commands.commands import update_products
from catalog.models import Category
from scrapping.products import get_products

logging.basicConfig(filename="/home/mbi/logs/update.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command empty_database"""

    help = "update the database"

    def add_arguments(self, parser):
        """Add an argument"""
        parser.add_argument("updatedb", nargs="+", type=bool)

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """Action to do when using command"""
        if options["updatedb"]:
            try:
                self.stdout.write(f"Database update begins: {datetime.now()}")
                logger.info(f"Database update begin: {datetime.now()}")
                products: List = get_products(
                    [category.name for category in Category.objects.all()]
                )
                results: Dict = update_products(products)
                logger.info(
                    f"{datetime.now()}\n"
                    f"{results.get('updated')} products updated\n"
                    f"{results.get('added')} products added"
                )
                self.stdout.write(
                    f"{datetime.now()}\n"
                    f"{results.get('updated')} products updated\n"
                    f"{results.get('added')} products added"
                )
            except Exception as error:
                message = f"Error while updating database - {error}"
                logger.error(message)
                raise CommandError(message) from error

        self.stdout.write("Database correctly updated", ending="")
