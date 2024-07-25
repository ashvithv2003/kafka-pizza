import random
from faker.providers import BaseProvider

class PizzaProvider(BaseProvider):
    def pizza_name(self):
        valid_pizza_names = [
            'Margherita',
            'Marinara',
            'Diavola',
            'Mari & Monti',
            'Salami',
            'Pepperoni'
        ]
        return valid_pizza_names[random.randint(0, len(valid_pizza_names) - 1)]

# Example usage
from faker import Faker

fake = Faker()
fake.add_provider(PizzaProvider)

for _ in range(5):
    print(fake.pizza_name())
