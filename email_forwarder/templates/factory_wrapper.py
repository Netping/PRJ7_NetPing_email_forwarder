"""
Wrapper for admin and users outbound templates module.
"""

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
                 user_templates: OutboundFactory):
        self.admin_templates = admin_templates
        self.user_templates = user_templates

    def get_user_template(self, user: str, inbound_template_id: int):
        """
        Get template for user by inbound template.
        If exists personal return them. Otherway default from admin's list.

        Args:
            - user -- user's email
            - inbound_template_id -- inbound template identifier
        """
        template = self.user_templates.template_by_user(user,
                                                        inbound_template_id)
        if not template:
            template = self.admin_templates.template_by_inbound_template(
                inbound_template_id)
        return template[0] if template else None
