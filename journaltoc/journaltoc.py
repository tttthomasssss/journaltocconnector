import sys

import requests

__ARTICLE_BASE_URL__ = 'http://www.journaltocs.ac.uk/api/articles/'

def _is_doi(search_term):
	search_term = search_term.lower()

	return (search_term.startswith('doi:') or search_term.startswith('10.') or 'doi.org/' in search_term)

def query_articles(search_term):
	params = {'doi': search_term} if _is_doi(search_term) else None

	url = '%s%s' % (__ARTICLE_BASE_URL__, search_term) if not params else __ARTICLE_BASE_URL__

	r = requests.get(url, params=params)

	# Raise if the request failed
	r.raise_for_status()

	return r.content

if (__name__ == '__main__'):
	term = 'deep learning' if len(sys.argv) <= 1 else sys.argv[1]
	print query_articles(term)
