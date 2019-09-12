# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date, datetime, time, timedelta


class ProductTemplae(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
