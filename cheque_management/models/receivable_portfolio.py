# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ReceivablePortfolio(models.Model):
    _name = 'receivable.portfolio'
    _description = 'Receivable Portfolio'

    seq = fields.Char(string="Sequence",
                      default=lambda self: self.env['ir.sequence'].next_by_code('receivable_Portfolio_seq_increment'), readonly=True)
    date = fields.Date("Issue Date")
    desc = fields.Text('Description')

    receiveACheque_ids = fields.One2many('receive.cheque2', 'receivablePortfolio_id', string='Cheques')

    @api.multi
    def receive_cheques(self):
        for rec in self:
            for line in rec.receiveACheque_ids:
                line.receive_cheque()

