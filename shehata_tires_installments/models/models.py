import datetime

from addons.calendar.models import calendar
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta


class ShehataInheritInstallments(models.Model):
    _inherit = 'account.payment.term.line'
    value = fields.Selection([
        ('balance', 'Balance'),
        ('percent', 'Percent'),
        ('fixed', 'Fixed Amount'),
        ('installment', 'Installment')
    ], string='Type', required=True, default='balance',
        help="Select here the kind of valuation related to this payment terms line.")

    no_months = fields.Integer(string='Number Of Months',  help="For installments enter a number of months.")
    value_amount = fields.Float(store=True,string='Value', digits=dp.get_precision('Payment Terms'), help="For percent enter a ratio between 0-100.")
    is_installment = fields.Boolean(string='Is Installment',default=True)

    @api.constrains('no_months')
    def _check_no_months(self):
        for rec in self:
            if rec.value == 'installment':
                if rec.no_months<=0:
                    raise UserError(_('If DueType equal Installment,The Number Of Months or Installments	Should be > 0'))

class ShehataInheritInstallmentsPayementTerm(models.Model):
    _inherit = 'account.payment.term'

    def _default_line_ids(self):
        return [(0, 0, {'value': 'balance', 'value_amount': 0.0, 'sequence': 9, 'days': 0, 'option': 'day_after_invoice_date','no_months': 10})]

    @api.one
    def compute(self, value, date_ref=False):
        date_ref = date_ref or fields.Date.today()
        amount = value
        sign = value < 0 and -1 or 1
        result = []
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        for line in self.line_ids:
            if line.value == 'fixed':
                amt = sign * currency.round(line.value_amount)
            elif line.value == 'percent':
                amt = currency.round(value * (line.value_amount / 100.0))
            elif line.value == 'balance':
                amt = currency.round(amount)
            #
            elif line.value == 'installment':
                amt = currency.round(amount)
            #
            if amt:
                next_date = fields.Date.from_string(date_ref)
                if line.option == 'day_after_invoice_date':
                    next_date += relativedelta(days=line.days)
                    if line.day_of_the_month > 0:
                        months_delta = (line.day_of_the_month < next_date.day) and 1 or 0
                        next_date += relativedelta(day=line.day_of_the_month, months=months_delta)
                elif line.option == 'after_invoice_month':
                    next_first_date = next_date + relativedelta(day=1, months=1)  # Getting 1st of next month
                    next_date = next_first_date + relativedelta(days=line.days - 1)
                elif line.option == 'day_following_month':
                    next_date += relativedelta(day=line.days, months=1)
                elif line.option == 'day_current_month':
                    next_date += relativedelta(day=line.days, months=0)
                    #
                if line.value == 'installment':
                    if line.no_months>0:
                        uniqe_amt = amt / line.no_months
                    else:
                        uniqe_amt = amt
                    inst_amt = uniqe_amt
                    for x in range(0, line.no_months):
                        result.append((fields.Date.to_string(next_date), inst_amt))
                        next_date += relativedelta(months=1)
                else:
                    result.append((fields.Date.to_string(next_date), amt))
                    #
                amount -= amt
        amount = sum(amt for _, amt in result)
        dist = currency.round(value - amount)
        if dist:
            last_date = result and result[-1][0] or fields.Date.today()
            result.append((last_date, dist))
        return result

    @api.constrains('line_ids')
    def _check_lines(self):

        payment_term_lines = self.line_ids.sorted()
        if payment_term_lines and payment_term_lines[-1].value != 'installment':
            if payment_term_lines and payment_term_lines[-1].value != 'balance':
                raise ValidationError(_('The last line of a Payment Term should have the Balance type Or installment.'))
        lines = self.line_ids.filtered(lambda r: r.value == 'installment')
        if len(lines) > 1:
             raise ValidationError(_('A Payment Term should have only one line of type Balance or installment.'))




