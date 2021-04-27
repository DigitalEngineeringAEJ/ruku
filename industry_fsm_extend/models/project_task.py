from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # ------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------
    is_approved = fields.Boolean('Is approved')
    is_rejected = fields.Boolean('Is rejected')
    sequence = fields.Integer('Sequence', related='stage_id.sequence')
    number_cost_center = fields.Char('Number of cost center')
    date_installation = fields.Date('Date of installation')
    acronym_type_logistics_service = fields.Char(string="Acronym for type of logistics service")
    is_closed = fields.Boolean('Is Closed', related='stage_id.is_closed', store=True)
    related_task_id = fields.Many2one('project.task', string='Related Task')
    size = fields.Float('Size')
    wood_type = fields.Char('Wood Type')
    is_install_task = fields.Boolean('Is Install')

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

    def action_fsm_validate(self):
        """ Moves Task to next stage.
            If allow billable on task, timesheet product set on project and user has privileges :
            Create SO confirmed with time and material.
        """
        for task in self:
            super(ProjectTask, task).action_fsm_validate()

            if task.project_id.related_project_id:
                wizard = task.env['wizard.create.task'].create({'date_installation': task.date_installation, 'name': task.name})
                return {
                    'name': _('Assigned task'),
                    'res_model': 'wizard.create.task',
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'type': 'ir.actions.act_window',
                    'target': 'new'
                }

    # ------------------------------------------------------------
    # Onchange Methodes
    # ------------------------------------------------------------

    @api.onchange('user_id', 'date_installation', 'planned_date_begin', 'planned_date_end')
    def _onchange_user_id(self):
        if self.date_installation and self.planned_date_begin and self.planned_date_end:
            if self.is_install_task:
                if self.date_installation < self.planned_date_begin.date() or self.date_installation > self.planned_date_end.date():
                      raise ValidationError(
                        _("The date installation must be between date begin and date end!")
                    )
            else:
                if self.date_installation < self.planned_date_begin.date() or self.date_installation <= self.planned_date_end.date():
                      raise ValidationError(
                        _("The date installation must be greater than date begin and date end!")
                    )

        if self.is_install_task and self.user_id and self.date_installation:
                tasks = self.env['project.task'].search([('user_id', '=', self.user_id.id), ('date_installation', '=', self.date_installation), ('is_install_task', '=', True), ('is_fsm', '=', True)])
                if len(tasks) > 1:
                        raise ValidationError(
                                _("User can only have one task at a time!")
                            )

    @api.onchange('partner_id')
    def _onchange_customer(self):
        if self.partner_id:
            name = self.partner_id.name
            if self.partner_id.zip:
                name += '/' + self.partner_id.zip
            if self.partner_id.city:
                name += '/' + self.partner_id.city
            self.name = name
