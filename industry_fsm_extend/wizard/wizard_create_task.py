from odoo import fields, models, _
from odoo.exceptions import ValidationError


class WizardCreateTask(models.TransientModel):
    _name = 'wizard.create.task'

    user_id = fields.Many2one('res.users', string='Assigned To')
    date_installation = fields.Date('Date of installation')
    name = fields.Char('Name')

    def create_task(self):
        """Create installation task from production task."""
        context = self.env.context or {}
        for wizard in self:
            if context.get('active_id', False) and context.get('active_model', False):
                model_obj = self.env[context.get('active_model')]
                task = model_obj.browse(context.get('active_id'))
                task_install = task.copy()
                task_install.name = wizard.name
                task_install.parent_id = task
                task_install.date_installation = wizard.date_installation
                task_install.user_id = wizard.user_id
                task_install.is_install_task = True
                task_install.project_id = task.project_id.related_project_id
                task_install.is_approved = False
                task_install.fsm_done = False
                task_install.is_fsm = True
                task_install.planned_date_begin   = False
                task_install.planned_date_end = False
                if task_install.user_id and task_install.date_installation:
                    tasks = wizard.env['project.task'].search(
                        [('user_id', '=', task_install.user_id.id), ('date_installation', '=', task_install.date_installation),
                         ('is_closed', '=', False), ('is_fsm', '=', True)])
                    if len(tasks) > 1:
                        raise ValidationError(
                            _("User can only have one task at a time!")
                        )
