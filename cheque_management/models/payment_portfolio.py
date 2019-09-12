# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PaymentPortfolio(models.Model):
    _name = 'payment.portfolio'
    _description = 'Payment Portfolio'

    seq = fields.Char(string="Sequence",
                      default=lambda self: self.env['ir.sequence'].next_by_code('Payment_Portfolio_seq_increment'), readonly=True)
    date = fields.Date("Issue Date")
    # partner_id = fields.Many2one('res.partner', string="Receiving From", required=True)
    desc = fields.Text('Description')

    IssueCheque_ids = fields.One2many('issue.cheque', 'PaymentPortfolio_id', string='Cheques')

    @api.multi
    def post_cheques(self):
        for rec in self:
            for line in rec.IssueCheque_ids:
                line.post_cheque()

