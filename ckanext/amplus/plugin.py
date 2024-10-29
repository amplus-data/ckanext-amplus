import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.amplus.helpers as helpers


class AmplusPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    # IConfigurer

    def update_config(self, config_):
        ckan_version = helpers.get_ckan_version()
        if (ckan_version.startswith('2.9')):
            toolkit.add_template_directory(config_, 'templates')
        else:
            toolkit.add_template_directory(config_, 'templates-2-10')

        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'amplus')

    def get_helpers(self):
        return {
            'amplus_get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,
            'amplus_get_site_statistics':
                helpers.get_site_statistics,
            'get_ckan_version':
                helpers.get_ckan_version
        }

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        validators = [ignore_missing, ignore_missing]
        validators = [ignore_missing, ignore_missing]

        schema.update({
            'homepage_blogs': validators,
            'footer_links': validators,
            'social_media_links': validators,
        })

        return schema
