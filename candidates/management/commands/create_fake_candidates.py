from django.core.management import BaseCommand, base
from typing import Any

from candidates.utils import RandomUserDataCreator


class Command(BaseCommand):
    def add_arguments(self, parser: base.CommandParser) -> None:
        parser.add_argument('-q', '--quantity', type=int, help='The quantity of fake candidates.')

    def handle(self, **kwargs: Any) -> None:
        candidates_qty = kwargs.get('quantity')
        creator = RandomUserDataCreator(candidates_qty) if candidates_qty else RandomUserDataCreator()
        creator.run()
