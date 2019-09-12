# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    display_product_qty = fields.Boolean(string='Display Product Quantity')


class POSProductQty(models.Model):
    _name = 'pos.product.qty'
    _rec_name = 'name'
    _description = 'Pos Product Qty'

    name = fields.Char()

    def get_quantities(self, product_id, location_id):
        warehouses = self.env['stock.warehouse'].sudo().search([])
        location_id = self.env['stock.location'].search([('id','=',location_id)])
        current_warehouse = location_id.get_warehouse()
        vals = {}
        total_qty = 0
        for warehouse in warehouses:
            qty = self.get_quantity_in_location(warehouse.lot_stock_id, product_id)
            total_qty += qty
            vals.update({
                warehouse.id: {
                    'name': warehouse.name,
                    'quantity': qty,
                    'my_company': True if warehouse == current_warehouse else False
                }

            })
        final_values = {'warehouses': vals, 'total_qty': total_qty}
        return final_values

    def get_quantity_in_location(self, location, product_id):
        product_id = self.env['product.product'].sudo().browse(product_id)
        qty_onhand = sum(self.env['stock.quant'].sudo()._gather(product_id, location).mapped('quantity'))
        qty_reserved = sum(self.env['stock.quant'].sudo()._gather(product_id, location).mapped('reserved_quantity'))
        qty_available = qty_onhand - qty_reserved
        return qty_available
