"""Commands for catalog"""
import ast
from datetime import datetime
from typing import Dict, List, Tuple
from uuid import UUID

from django.contrib.auth.models import User
from django.db import IntegrityError

from catalog.models import Favorite, Product
from catalog.populate import prepare_products


def get_better_products(base_product: Product) -> Tuple[List[Product], Product]:
    """
    Get a list of products with better nutriscore from a base product.

    :param Product base_product: product to compare
    :return: List[Product] list of better products
    """
    base_product = Product.objects.get(id=base_product)
    categories: List = ast.literal_eval(base_product.categories_tags)
    nutrition_grade: str = base_product.nutrition_grade_fr
    products: List[Product] = []

    # Find products with better nutrition grade for each category
    for category in categories:
        # pylint: disable=expression-not-assigned
        [
            products.append(product)
            for product in Product.objects.filter(
                categories_tags__contains=category,
                nutrition_grade_fr__cn=nutrition_grade,
            )
        ]

    products.sort(key=lambda x: x.nutrition_grade_fr)

    return products, base_product


def get_favorite_info(
    base_product: UUID, substitute_product: UUID, user: User
) -> Tuple[Favorite, Product]:
    """
    Get information on favorite.

    :param UUID base_product: product which needed to be replaced
    :param UUID substitute_product: replacement product
    :param User user: user who make the compare
    :return: Tuple[Favorite, Product]
    """

    base = Product.objects.get(id=base_product)
    substitute = Product.objects.get(id=substitute_product)

    return (
        Favorite(
            substitued=base, substitute=substitute, date=datetime.now(), user=user
        ),
        substitute,
    )


def get_delete_info(product_id: UUID, user: User) -> Tuple[Favorite, str]:
    """
    Get information to delete product in favorite.

    :param UUID product_id: product to delete
    :param User user: user owning the Favorite
    :return: Tuple[Favorite, product_name]
    """
    to_delete = Favorite.objects.get(substitute=product_id, user=user)

    product_name = Product.objects.get(id=product_id).product_name_fr

    return to_delete, product_name


def update_products(products: List) -> Dict:
    """
    Update the database's products

    ;param List products: list of products
    :return: Dict
    """
    list_product = prepare_products(products)
    added_products = 0
    updated_products = 0

    for product in list_product:
        if all(
            [
                product.brands,
                product.categories_tags,
                product.nutriments,
                product.nutrition_grade_fr,
                product.product_name_fr,
                product.image_url,
                product.url,
            ]
        ):
            try:
                product_db = Product.objects.get(
                    product_name_fr=product.product_name_fr
                )
            except Product.DoesNotExist:
                product_db = None

            if product_db:
                product_db.brands = product.brands
                product_db.categories_tags = product.categories_tags
                product_db.nutriments = product.categories_tags
                product_db.nutrition_grade_fr = product.nutrition_grade_fr
                product_db.image_url = product.image_url
                product_db.url = product.url

                try:
                    product_db.save()
                    updated_products += 1
                except IntegrityError:
                    continue
            else:
                try:
                    product.save()
                    added_products += 1
                except IntegrityError:
                    continue

    return {"updated": updated_products, "added": added_products}
