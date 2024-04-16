"""amplus custom helpers.
"""
from ckan import authz
from ckan.plugins import toolkit
from ckan.lib import search
from datetime import datetime
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


def get_site_statistics(user):
    """
    Count how many datasets, organizations and groups exist for particular user

    :param user: The username of the user
    :type user: str
    :returns: the dictionary containing number of datasets,
              organizations and groups

    :rtype: dict
    """

    stats = {}
    data_dict = {
        "rows": 1,
        'include_private': authz.is_sysadmin(user)
    }

    stats['dataset_count'] =\
        toolkit.get_action('package_search')({}, data_dict)['count']
    stats['group_count'] = len(toolkit.get_action('group_list')({}, {}))
    stats['organization_count'] =\
        len(toolkit.get_action('organization_list')({}, {}))

    return stats

def get_ckan_version():
    data = toolkit.get_action('status_show')({})
    print("++++++++++++++++++++++++++++++++++++++")
    print(data['ckan_version'])

    return data['ckan_version']
