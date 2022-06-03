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
    # Generate custom css according to selected colors
    site_custom_css = ''
    primary = config.get('primary_color')
    secondary = config.get('secondary_color')
    tertiary = config.get('tertiary_color')
    quaternary = config.get('quaternary_color')
    extra_light = config.get('extra_light_color')


    site_custom_css += '.bg-primary { background-color: ' +  primary + ' !important;} '
    site_custom_css += '.bg-secondary { background-color: ' +  secondary + ' !important;} '
    site_custom_css += '.bg-tertiary { background-color: ' +  tertiary + ' !important;} '
    site_custom_css += '.bg-quaternary { background-color: ' +  quaternary + ' !important;} '
    site_custom_css += '.bg-extra-light { background-color: ' +  extra_light + ' !important;} '

    #header
    site_custom_css += '.masthead { background: ' +  primary + ' !important;} '
    site_custom_css += '.account-masthead { background: ' +  primary + ' !important;} '
    site_custom_css += '.account-masthead .account ul li a:hover, .account-masthead .account ul li a:active { background: ' +  quaternary + ' !important;} '
    site_custom_css += '.masthead .navigation .nav-pills li.active a { background: ' +  quaternary + ' !important;} '
    site_custom_css += '.masthead .navigation .nav-pills li a:hover, .masthead .navigation .nav-pills li a:focus { background: ' +  quaternary + ' !important;} '

    # a
    site_custom_css += 'a { color: ' +  primary + ';}'

    # hero hedding
    site_custom_css += '.hero .page-heading { color: ' +  primary + ';}'

    # discover data active
    site_custom_css += '.group-container .toggle-section .active { border-bottom: 4px solid' +  secondary + ';}'
    site_custom_css += '.group-container .toggle-section .active .toggle-view { color: ' +  secondary + ';}'

    # stats
    site_custom_css += '.homepage .stats ul li a { color: ' +  secondary + ' !important;} '

    # featured
    site_custom_css += '.featured-item:hover { background-color: ' +  secondary + ' !important;} '

    # breadcrump
    site_custom_css += '.toolbar .breadcrumb li.active > a { color: ' +  primary + ' !important;} '
    
    # Stats amplus
    site_custom_css += '.oval { color: ' +  secondary + ' !important;} '

    # Footer nav
    site_custom_css += '.footer-nav-title { color: ' +  secondary + ' !important;} '

    # h
    site_custom_css += '.module-heading { color: ' +  primary + ' !important;} '
    site_custom_css += 'h1 { color: ' +  primary + ' !important;} '

    # buttons
    site_custom_css += '.btn-primary { background-color: ' +  primary + ' !important;} '

    return site_custom_css


def set_default_colors():
    # Set the initial colors
    colors = {}

    colors['primary_color'] = '#6033A7'
    colors['secondary_color'] = '#9F1A86'
    colors['tertiary_color'] = '#DE0064'
    colors['quaternary_color'] = '#7A64A6'
    colors['extra_light_color'] = '#EBD3E6'

    return colors


class ConfigViewAmplus(MethodView):
    def get(self):
        items = _get_config_options_amplus()
        schema = logic.schema.update_configuration_schema()
        data = {}

        # set colors defaults
        colors = set_default_colors()

        for item in colors:
            show_value = logic.get_action(u'config_option_show')({}, {'key': item})
            if show_value == '':
                config[item] = colors[item]

        for key in schema:
            if key == 'ckan.site_custom_css':
                custom_css = create_custom_css(config)
                data[key] = custom_css
            else:
                data[key] = config.get(key)

        vars = dict(data=data, errors={}, **items)

        return base.render(u'admin/config.html', extra_vars=vars)

    def post(self):
        try:
            req = request.form.copy()
            req.update(request.files.to_dict())
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