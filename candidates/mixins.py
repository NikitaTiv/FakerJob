from typing import Any

from candidates.models import Candidate


class HeaderMixin:
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, str | Candidate]:
        if not hasattr(self, 'header_name'):
            raise AttributeError('The header_name attribute should be specified.')
        context_data = super().get_context_data(**kwargs)
        context_data.update({'header': self.header_name})
        return context_data
