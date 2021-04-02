from odoo import fields, models, _, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # ------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------
    is_approved = fields.Boolean('Is approved')
    is_rejected = fields.Boolean('Is rejected')
    sequence = fields.Integer('Sequence', related='stage_id.sequence')
    # ------------------------------------------------------------
    # Methodes
    # ------------------------------------------------------------
    def action_approve(self):
        """Set task to approve."""
        self.ensure_one()
        self.is_approved = True
        self.is_rejected = False

    def action_rejected(self):
        """Set task to rejected."""
        self.ensure_one()
        self.is_rejected = True
        self.is_approved = False

