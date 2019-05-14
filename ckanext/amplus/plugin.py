import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.amplus.helpers as helpers


class AmplusPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'amplus')

    def get_helpers(self):
        return {
            'amplus_get_recently_updated_datasets':
                helpers.get_recently_updated_datasets
        }