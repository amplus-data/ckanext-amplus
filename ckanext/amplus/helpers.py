"""amplus custom helpers.
"""
import os
import json

from ckan.plugins import toolkit
from ckan.lib import search, i18n
from datetime import datetime
from ckan.common import config
from logging import getLogger

log = getLogger(__name__)


def _get_action(action, context_dict, data_dict):
    return toolkit.get_action(action)(context_dict, data_dict)


def get_recently_updated_datasets(limit=5):
    '''
     Returns recent created or updated datasets.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :returns: a list of recently created or updated datasets
    :rtype: list
    '''
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']

    except (toolkit.ValidationError, search.SearchError):
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = (datetime.now() - modified).days
            pkgs.append(package)
        return pkgs