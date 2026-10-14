"""Resolve the maintainer-approved organization rename without rewriting evidence."""
import re

CURRENT_ORGANIZATION = 'eyleme-dev'
HISTORICAL_ORGANIZATION = 'eylema-dev'
REPOSITORIES = {'devguide', '.github', 'eylema-docs-en', 'eylema-docs-tr',
                'eylema-examples', 'eylema-evals', 'eylema-models', 'eylema-training',
                'eylemadotdev'}
ALIASES = {organization + '/' + name: CURRENT_ORGANIZATION + '/' + name
           for organization in (CURRENT_ORGANIZATION, HISTORICAL_ORGANIZATION)
           for name in REPOSITORIES}
ALIASES.update({'eylema-dev/eylema': 'eyleme-dev/eyleme',
                'eyleme-dev/eylema': 'eyleme-dev/eyleme',
                'eyleme-dev/eyleme': 'eyleme-dev/eyleme'})


def canonical_repository(value):
    """Accept only an exact managed repository in the current or historical org."""
    if not isinstance(value, str) or value not in ALIASES:
        raise ValueError('Repository is outside the approved organization migration')
    return ALIASES[value]


def canonical_url(value):
    """Normalize only a verified GitHub repository URL; keep all remaining bytes."""
    match = re.fullmatch(r'https://github\.com/([^/]+/[^/]+)(/.*)?', value)
    if not match:
        raise ValueError('Expected a canonical GitHub repository URL')
    return 'https://github.com/' + canonical_repository(match[1]) + (match[2] or '')


def canonical_endpoint(value):
    """Map a fixed repository GET endpoint to the renamed org before network access."""
    match = re.fullmatch(r'repos/([^/]+/[^/]+)(/[^?#\s]*)?(\?[^\s]*)?', value)
    if not match or any(part in {'.', '..'} for part in (match[2] or '').split('/')):
        raise ValueError('Expected an allowlisted GitHub repository endpoint')
    return 'repos/' + canonical_repository(match[1]) + (match[2] or '') + (match[3] or '')
