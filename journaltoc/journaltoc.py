import sys

import feedparser
import requests


__ARTICLE_BASE_URL__ = 'http://www.journaltocs.ac.uk/api/articles/'
__JOURNAL_BASE_URL__ = 'http://www.journaltocs.ac.uk/api/journals/'
__UESR_BASE_URL = 'http://www.journaltocs.ac.uk/api/user/'

def _is_doi(search_term):
	''' Test if argument is a DOI '''
    search_term = search_term.lower()

	return (search_term.startswith('doi:') or search_term.startswith('10.') or 'doi.org/' in search_term)

def _is_issn(val):
    ''' Test if argument is an ISSN number '''
    val = val.replace('-', '').replace(' ', '')
    if (len(val) != 8):
        return False
    r = sum([(8 - i) * (lambda x: if x != 'X' int(x) else 10) for i, x in enumerate(val)])
    return not (r % 11)

def _query_api(url, params):

	r = requests.get(url, params=params)

	# Raise if the request failed
	r.raise_for_status()

	return r.content

def query_articles(search_term, return_full_response=False):
	params = {'doi': search_term} if _is_doi(search_term) else None
	url = '%s%s' % (__ARTICLE_BASE_URL__, search_term) if not params else __ARTICLE_BASE_URL__

	response = _query_api(url=url, params=params)
	rssdoc = feedparser.parse(response)

	return rssdoc['entries'] if not return_full_response else rssdoc

def query_journals(search_term, user, output='articles', return_full_response=False):
	params = {
		'user': user,
		'output': output
	}

	url = '%s%s' % (__JOURNAL_BASE_URL__, search_term)

	response = _query_api(url=url, params=params)
	rssdoc = feedparser.parse(response)

	return rssdoc['entries'] if not return_full_response else rssdoc

def query_user(user, output='articles', return_full_response=False):
	params = {
		'output': output
	}

	url = '%s%s' % (__USER_BASE_URL__, user)

	response = _query_api(url=url, params=params)
	rssdoc = feedparser.parse(response)

	return rssdoc['entries'] if not return_full_response else rssdoc

if (__name__ == '__main__'):
	term = 'deep learning' if len(sys.argv) <= 1 else sys.argv[1]
	print query_articles(term)
