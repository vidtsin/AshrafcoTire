# -*- coding: utf-8 -*-
###################################
# ENG-Mahmoud Ramadan             #
# Odoo Developer                  #
# Email:mramadan271193@gmail.com  #
# Version: Odoo 12 .              #
###################################

{
    'name': "POS Product Quantity",

    'summary': """Show Product Quantity in All Warehouses On POS.""",

    'description': """""",

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0.5',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/p_quantity.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
