# -*- coding: utf-8 -*-
{
    'name': "Field Service Ruku",
    'summary': "Schedule and track onsite operations, time and material",
    'description': """""",
    'category': 'Services/Field Service',
    'version': '1.0',
    'depends': ['industry_fsm_sale_report'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_create_task_views.xml',
        'views/project_task_views.xml',
        'views/project_project_views.xml',
    ],
    'application': True,
    'demo': [],
}
