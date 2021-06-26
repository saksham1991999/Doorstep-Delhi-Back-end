from product.models import Category


def add_categories():
    Category.objects.bulk_create(
        [
            Category(name='Man', icon="shoe_1"),
            Category(name='Women', icon="shoe"),
            Category(name='Child', icon="baby_changing"),
            Category(name='Fourniture', icon="living_room"),
            Category(name='Watch', icon="watch"),
            Category(name='Media', icon="home_cinema"),
            Category(name='Sport', icon="sport"),
            Category(name='Travel', icon="sport"),
            Category(name='Tool', icon="tool"),
            Category(name='Game', icon="game"),
            Category(name='Home', icon="vacuum"),

        ]
    )
