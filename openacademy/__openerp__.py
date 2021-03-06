# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """Training module""",

    'description': """This is a test module designed for training""",

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml',
        'workflows/session_workflow.xml',
        'security/groups.xml',

        'demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}