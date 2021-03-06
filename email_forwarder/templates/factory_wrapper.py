"""
Wrapper for admin and users outbound templates module.
"""
import logging

from .outbound_factory import OutboundFactory


class FactoryWrapper:
    """
    Wrapper for admin and users outbound templates.
    Contains rules for getting outbound template by inbound.

    Args:
        - admin_templates -- admin templates factory
        - user_templates -- user templates factory
    """
    def __init__(self, admin_templates: OutboundFactory,
                 user_templates: OutboundFactory,
                 logs: logging.Logger):
        self.admin_templates = admin_templates
        self.user_templates = user_templates
        self.logs = logs

    def get_user_template(self, user: str, inbound_template_id: int):
        """
        Get template for user by inbound template.
        If exists personal return them. Otherway default from admin's list.

        Args:
            - user -- user's email
            - inbound_template_id -- inbound template identifier
        """
        self.logs.info(('Поиск шаблона для отправки '
                        'для отправителя %s и шаблона id:%s'),
                       user, inbound_template_id)
        template = self.user_templates.template_by_user(user,
                                                        inbound_template_id)
        if not template:
            self.logs.info(('Индивидуального шаблона для для отправителя %s '
                            'и шаблона id:%s найти не удалось'),
                           user, inbound_template_id)
            template = self.admin_templates.template_by_inbound_template(
                inbound_template_id)

        if not template:
            self.logs.info(('Общего шаблона для для отправителя %s '
                            'и шаблона id:%s найти не удалось'),
                           user, inbound_template_id)

        return template
