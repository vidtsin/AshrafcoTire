# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date, datetime, time, timedelta


class StockMove(models.Model):
    _inherit = 'stock.move'

    part_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False,
                              related='picking_id.partner_id')

    @api.onchange('part_id')
    def onchange_part_id(self):
        return {
            'domain': {
                'product_id': [('partner_id', '=', self.part_id.id)]
            }
        }
