from ckan.common import g, config
import ckan.lib.helpers as h
from flask import Blueprint
import ckan.logic as logic
from ckan.common import g, _, config, request
import ckan.lib.base as base
from flask.views import MethodView
import ckan.lib.navl.dictization_functions as dict_fns
from ckan.views.home import CACHE_PARAMETERS


amplus = Blueprint('amplus', __name__)


def _get_config_options_amplus():
    styles = [{
        u'text': u'Default',
        u'value': u'/base/css/main.css'
    }, {
        u'text': u'Red',
        u'value': u'/base/css/red.css'
    }, {
        u'text': u'Green',
        u'value': u'/base/css/green.css'
    }, {
        u'text': u'Maroon',
        u'value': u'/base/css/maroon.css'
    }, {
        u'text': u'Fuchsia',
        u'value': u'/base/css/fuchsia.css'
    }]

    homepages = [{
        u'value': u'1',
        u'text': u'Amplus'
    }, {
        u'value': u'2',
        u'text': (u'Introductory area, search, featured'
                  u' group and featured organization')
    }, {
        u'value': u'3',
        u'text': (u'Search, stats, introductory area, '
                  u'featured organization and featured group')
    }, {
        u'value': u'4',
        u'text': u'Search, introductory area and stats'
    }]

    return dict(styles=styles, homepages=homepages)

def create_custom_css(config):
    header = config.get('header_color')
    footer = config.get('footer_color')
    admin_header_color = config.get('admin_header_color')
    oval = config.get('oval')
    footer_nav_title = config.get('footer_nav_title')
    footer_nav_links = config.get('footer_nav_links')

    # buttons
    btn_primary_color = config.get('btn_primary_color')
    btn_danger_color = config.get('btn_danger_color')
    btn_default_color = config.get('btn_default_color')

    # headiing
    module_heading = config.get('module_heading')
    h1_color = config.get('h1_color')

    # links
    link_color = config.get('link_color')
    link_hover_color = config.get('link_hover_color')
    link_active_color = config.get('link_active_color')

    site_custom_css = '.masthead { background: ' +  header + ';} ' 
    site_custom_css += '.site-footer { background: ' +  footer + ';}'
    site_custom_css += '.account-masthead { background: ' +  admin_header_color + ';}'
    site_custom_css += '.stat-content .oval { color: ' +  oval + ';}'
    site_custom_css += '.footer-nav-title  { color: ' +   footer_nav_title + ';}'
    site_custom_css += '.footer-links ul li a  { color: ' +   footer_nav_links + ';}'
    

    # buttons
    site_custom_css += '.btn-primary { background: ' +  btn_primary_color + ';}'
    site_custom_css += '.btn-default { background: ' +  btn_default_color + ';}'
    site_custom_css += '.form-actions .btn-danger { background: ' +  btn_danger_color + ';}'

    # heading
    site_custom_css += '.module-heading { color: ' +  module_heading + ';}'
    # h1 
    # think how we can devide the different h1
    site_custom_css += '.primary .search-form > h1, .primary .search-form > .h1 { color: ' +  h1_color + ';}'

    # link color
    site_custom_css += 'a { color: ' +  link_color + ';}'
    site_custom_css += '.masthead .navigation .nav-pills li a:hover { background: ' +  link_hover_color + ';}'
    site_custom_css += '.masthead .navigation .nav-pills li.active a { background: ' +  link_active_color + ';}'

    


    return site_custom_css 


class ConfigViewAmplus(MethodView):
    def get(self):
        items = _get_config_options_amplus()
        schema = logic.schema.update_configuration_schema()
        data = {}
        
        for key in schema:
            if key == 'ckan.site_custom_css':
                custom_css = create_custom_css(config)
                data[key] = custom_css
            else:
                data[key] = config.get(key)

        vars = dict(data=data, errors={}, **items)

        return base.render(u'admin/config.html', extra_vars=vars)

    def post(self):
        print ("POSTT")
        try:
            req = request.form.copy()
            req.update(request.files.to_dict())
            print (req['ckan.site_custom_css'])
            # update ckan.site_custom_css
            custom_css = create_custom_css(req)
            req['ckan.site_custom_css'] = custom_css

            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(req,
                                           ignore_keys=CACHE_PARAMETERS))))

            del data_dict['save']
            data = logic.get_action(u'config_option_update')({
                u'user': g.user
            }, data_dict)

        except logic.ValidationError as e:
            items = _get_config_options_amplus()
            data = request.form
            errors = e.error_dict
            error_summary = e.error_summary
            vars = dict(data=data,
                        errors=errors,
                        error_summary=error_summary,
                        form_items=items,
                        **items)
            return base.render(u'admin/config.html', extra_vars=vars)

        return h.redirect_to(u'admin.config')


amplus.add_url_rule(u'/ckan-admin/config', view_func=ConfigViewAmplus.as_view(str(u'config')))