"""Command to populate the default database"""
import logging

from django.core.management.base import BaseCommand, CommandError

from catalog.models import Category
from catalog.populate import populate_categories, populate_product
from scrapping.categories import get_categories
from scrapping.products import get_products

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command populate_database"""

    help = "Populates the database"

    def add_arguments(self, parser):
        """Add argument populate"""
        parser.add_argument("populate", nargs="+", type=bool)

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """Action when using command"""
        if options["populate"]:

            try:
                categories = get_categories()
                logger.info("Categories downloaded")
            except Exception as error:
                message = f"Error while scrapping categories- {error}"
                logger.error(message)
                raise CommandError(message) from error

            try:
                populate_categories(categories)
                logger.info("Categories inserted in db")
            except Exception as error:
                message = f"Error while populating categories- {error}"
                logger.error(message)
                raise CommandError(message) from error

            try:
                products = get_products(
                    [category.name for category in Category.objects.all()]
                )
                logger.info("Products downloaded")
            except Exception as error:
                message = f"Error while scrapping products - {error}"
                logger.error(message)
                raise CommandError(message) from error

            try:
                populate_product(products)
                logger.info("Products inserted in db")
            except Exception as error:
                message = f"Error while populating products - {error}"
                logger.error(message)
                raise CommandError(message) from error
