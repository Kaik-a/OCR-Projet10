"""Command to empty the default database"""
import logging

from django.core.management.base import BaseCommand, CommandError

from catalog.models import Category, Favorite, Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command empty_database"""

    help = "Empty the database"

    def add_arguments(self, parser):
        """Add an argument"""
        parser.add_argument("emptydb", nargs="+", type=bool)

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """Action to do when using command"""
        if options["emptydb"]:
            try:
                Category.objects.all().delete()
                Product.objects.all().delete()
                Favorite.objects.all().delete()
                logger.info("Database correctly emptied")
            except Exception as error:
                message = f"Error while emptying database - {error}"
                logger.error(message)
                raise CommandError(message) from error
