# -*- coding: utf-8 -*-
{
    'name': 'Biometric Device Integration',
    'version': '12.0.1.0.0',
    'summary': """Integrating Biometric Device With HR Attendance""",
    'description': 'This module integrates Odoo with the biometric device(Model: ZKteco K30)',
    'category': 'Generic Modules/Human Resources',
    'author': 'iSky Development',
    'company': 'iSky Development',
    'website': "https://www.iskydev.com",
    'depends': ['base', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/generate_attendance.xml',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        'data/biometric_device_auto_integration.xml',
    ],
    'license': 'AGPL-3',
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
