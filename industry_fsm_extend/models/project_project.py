from odoo import fields, models


class ProjectProject(models.Model):
      _inherit = 'project.project'

      related_project_id = fields.Many2one('project.project', string='Related Project')
