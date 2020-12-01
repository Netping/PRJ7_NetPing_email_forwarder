import logging
import re
import typing
import traceback

import flask
from waitress import serve

from email_forwarder.mails.mailbox import MailBox
from email_forwarder.templates.inbound_template import InboundTemplate
from email_forwarder.templates.outbound_template import OutboundTemplate
from email_forwarder.templates.outbound_factory import OutboundFactory


class WebServer:
    def __init__(self, host: str, port: int,
                 inbound_templates: typing.List[InboundTemplate],
                 outbound_admin_templates: typing.List[OutboundTemplate],
                 outbound_templates: OutboundFactory,
                 mailbox: MailBox, log: logging.Logger, errors: logging.Logger):
        self.host = host
        self.port = port
        self.inbound_templates = inbound_templates
        self.outbound_admin_templates = outbound_admin_templates
        self.outbound_templates = outbound_templates
        self.mailbox = mailbox
        self.log = log
        self.errors = errors

        self.app = flask.Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index,
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/<user>', 'user_page', self.user_page)
        self.app.add_url_rule('/<user>/<template_id>',
                              'edit_outbound_template',
                              self.edit_outbound_template,
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/favicon.ico', 'favicon', self.favicon)
    
    def favicon(self):
        flask.abort(404, description="Resource not found")

    def index(self):
        if flask.request.method == 'POST':
            try:
                user = flask.request.form.get('login', None)
                if not re.match(r'[^@]+@[^@]+\.[^@]+', user):
                    self.log.info('Попытка логина с некорретным email %s',
                                  user)
                    return flask.redirect(flask.url_for('index'))
                self.log.info('Перевод на страницу пользователя %s', user)
                if user:
                    return flask.redirect(
                        flask.url_for('user_page', user=user))
            except Exception as e:
                self.errors.error(
                    'Ошибка перевода на страницу пользователя: %s',
                    str(e))
                self.errors.error(traceback.format_exc())
                return flask.redirect(flask.url_for('index'))
        return flask.render_template('index.html')

    def user_page(self, user):
        self.log.info('Вошел %s', user)
        try:
            user_mails = self.mailbox.get_user_mails(user)
            errors = [
                {
                    'date': mail.receive_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'to': mail.receive_meta.get('To', ''),
                    'body': mail.body,
                } for mail in sorted(
                    user_mails, key=lambda m: m.receive_date,
                    reverse=True) if mail.inbound_template_id == -1
            ]
            stat = {
                'total': len(user_mails),
                'sent': len(user_mails) - len(errors),
                'errors': len(errors)
            }
        except Exception as e:
            self.errors.error(
                'Ошибка открытия страница пользователя: %s',
                str(e))
            self.errors.error(traceback.format_exc())
            return flask.redirect(flask.url_for('index'))
        return flask.render_template('user_page.html', stat=stat,
                                     user=user, errors=errors,
                                     templates=self.inbound_templates)

    def edit_outbound_template(self, user, template_id):
        template = [tmp for tmp in self.inbound_templates
                    if str(tmp.template_id) == str(template_id)]
        # admoin_outbound = [tmp for tmp in self.outbound_admin_templates
        #                    if str(tmp.inbound_template_id) == str(template_id)]
        if template:
            template = template[0]
        else:
            return flask.redirect(flask.url_for('index'))

        if flask.request.method == 'POST':
            self.log.info('Сохранение пользовательского шаблона:')
            self.log.info('user: %s', user)
            self.log.info('inbound_teplate_id: %s', template_id)
            try:
                name = flask.request.form.get('name', '')
                new_template = flask.request.form.get('template', None)
                self.log.info('name: %s', name)
                self.log.info('template: %s', new_template)
                outbound = self.outbound_templates.save_template_for_user(
                    user, int(template_id), name, new_template)
                action = 'Сохранено'
            except Exception as e:
                action = 'Ошибка сохранения'
                self.errors.error(
                    'Ошибка сохранения пользовательского шаблона: %s', str(e))
                self.errors.error(traceback.format_exc())
        else:
            self.log.info(
                ('Редактирование пользовательского шаблона: '
                 'user - %s, inbound_teplate_id - %s'), user, template_id)
            try:
                action = None
                outbound = self.outbound_templates.template_by_user(
                    user, template_id)
                if not outbound:
                    outbound = [tmp for tmp in self.outbound_admin_templates
                                if str(tmp.inbound_template_id) == str(
                                    template_id)]
                    if outbound:
                        outbound = outbound[0]
            except Exception as e:
                action = 'Ошибка редактирования'
                self.errors.error(
                    'Ошибка редактирования пользовательского шаблона: %s',
                    str(e))
                self.errors.error(traceback.format_exc())
                return flask.redirect(flask.url_for('index'))
        return flask.render_template('edit_template.html', user=user,
                                     template=template, outbound=outbound,
                                     action=action)

    def run(self):
        logging.getLogger('waitress').setLevel(logging.NOTSET)
        serve(self.app, host=self.host, port=self.port)
