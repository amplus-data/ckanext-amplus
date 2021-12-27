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
        toolkit.add_resource('assets', 'amplus')

    def get_helpers(self):
        return {
            'amplus_get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,
            'amplus_get_site_statistics':
                helpers.get_site_statistics
        }

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        validators = [ignore_missing, str]

        schema.update({
            'homepage_blogs': validators,
            'footer_links': validators,
            'social_media_links': validators,
        })

        return schema
