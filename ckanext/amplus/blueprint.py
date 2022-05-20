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


class ConfigViewAmplus(MethodView):
    def get(self):
        items = _get_config_options_amplus()
        schema = logic.schema.update_configuration_schema()
        data = {}
        for key in schema:
            data[key] = config.get(key)

        vars = dict(data=data, errors={}, **items)

        return base.render(u'admin/config.html', extra_vars=vars)

    def post(self):
        try:
            req = request.form.copy()
            req.update(request.files.to_dict())
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