from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError

class ShehataInheritProductProduct(models.Model):
    _inherit = 'product.template'

    length = fields.Char(string='Length')
    width = fields.Char(string='Width')
    height = fields.Char(string='Height')
    weight = fields.Char(string='Weight')
    car_dimensions = fields.Many2many('car.dimension',string='Car_dimensions')
    ginet_dimensions= fields.Many2many('gient.dimension',string='Ginet_dimensions')

    size = fields.Many2one('product.size')
    brand = fields.Many2one('product.brand')
    model = fields.Many2one('product.model')
    pattern = fields.Many2one('product.pattern')
    extra = fields.Many2one('product.extra')

    size_code = fields.Char(string='Size Code',compute='_compute_codes',default=0)
    brand_code = fields.Char(string='Brand Code',compute='_compute_codes',default=0)
    model_code = fields.Char(string='Model Code',compute='_compute_codes',default=0)
    pattern_code = fields.Char(string='Pattern Code',compute='_compute_codes',default=0)
    extra_code = fields.Char(string='Extra Code',compute='_compute_codes',default=0)



    internal_ref_copy = fields.Char(string='Internal Reference',compute='_compute_internal_ref',readonly='True')


    _sql_constraints = [
        ('internal_reference_unique', 'unique(default_code)', "Internal Reference Already Exists It Must Be Unique !"),
    ]

    default_code = fields.Char(
        'Internal Reference', default='', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
    @api.depends('size.code', 'brand.code', 'model.code','pattern.code','extra.code')
    def _compute_codes(self):

        self.size_code  = self.size.code
        self.brand_code = self.brand.code
        self.model_code = self.model.code
        self.pattern_code = self.pattern.code
        self.extra_code = self.extra.code

    # @api.onchange('job_id')
    @api.depends('size_code', 'brand_code','model_code','pattern_code','extra_code')
    def _compute_default_code(self):

        if self.size_code and self.brand_code and self.model_code and self.pattern_code and self.extra_code !=0:

          self.default_code = (
                    str(self.size_code) + str(self.brand_code) + str(self.model_code) + str(self.pattern_code) + str(
                self.extra_code))


        elif self.size_code and self.brand_code and self.model_code and self.pattern_code !=0:

                  self.default_code =(str(self.size_code)+str(self.brand_code)+str(self.model_code)+str(self.pattern_code))


        elif self.extra_code and self.brand_code and self.model_code and self.pattern_code !=0:

                  self.default_code =(str(self.extra_code)+str(self.brand_code)+str(self.model_code)+str(self.pattern_code))
        elif self.size_code and self.extra_code and self.model_code and self.pattern_code !=0:

                  self.default_code =(str(self.size_code)+str(self.extra_code)+str(self.model_code)+str(self.pattern_code))
        elif self.size_code and self.brand_code and self.extra_code and self.pattern_code !=0:

                  self.default_code =(str(self.size_code)+str(self.brand_code)+str(self.extra_code)+str(self.pattern_code))
        elif self.size_code and self.brand_code and self.model_code and self.extra_code !=0:

                  self.default_code =(str(self.size_code)+str(self.brand_code)+str(self.model_code)+str(self.extra_code))












        elif self.size_code and self.model_code and self.brand_code !=0:
            self.default_code = (str(self.size_code) +str(self.model_code)+str(self.brand_code))



        elif self.pattern_code and self.model_code and self.brand_code != 0:
            self.default_code = (str(self.pattern_code) + str(self.model_code) + str(self.brand_code))


        elif self.pattern_code and self.model_code and self.size_code != 0:
            self.default_code = (str(self.pattern_code) + str(self.model_code) + str(self.size_code))


        elif self.pattern_code and self.brand_code and self.size_code != 0:
            self.default_code = (str(self.pattern_code) + str(self.brand_code) + str(self.size_code))





        elif self.size_code and self.extra_code and self.brand_code !=0:
            self.default_code = (str(self.size_code) +str(self.extra_code)+str(self.brand_code))



        elif self.extra_code and self.model_code and self.brand_code != 0:
            self.default_code = (str(self.extra_code) + str(self.model_code) + str(self.brand_code))


        elif self.extra_code and self.model_code and self.size_code != 0:
            self.default_code = (str(self.extra_code) + str(self.model_code) + str(self.size_code))


        elif self.pattern_code and self.extra_code and self.size_code != 0:
            self.default_code = (str(self.pattern_code) + str(self.extra_code) + str(self.size_code))


        elif self.pattern_code and self.model_code and self.extra_code !=0:
            self.default_code = (str(self.pattern_code) +str(self.model_code)+str(self.extra_code))



        elif self.pattern_code and self.extra_code and self.brand_code != 0:
            self.default_code = (str(self.pattern_code) + str(self.extra_code) + str(self.brand_code))










        elif  self.size_code and self.brand_code !=0:
            self.default_code = (str(self.size_code) + str(self.brand_code))



        elif self.size_code and self.model_code !=0:
            self.default_code = (str(self.size_code) +str(self.model_code))


        elif self.size_code and self.pattern_code !=0:
            self.default_code = (str(self.size_code) +str(self.pattern_code))



        elif self.brand_code and self.model_code !=0:
            self.default_code = (str(self.brand_code) + str(self.model_code))


        elif self.brand_code and self.pattern_code !=0:
            self.default_code = (str(self.brand_code) + str(self.pattern_code))



        elif self.pattern_code and self.model_code !=0:
            self.default_code = (str(self.pattern_code) +str(self.model_code))


        elif self.extra_code and self.model_code !=0:
            self.default_code = (str(self.extra_code) +str(self.model_code))
        elif self.pattern_code and self.extra_code !=0:
            self.default_code = (str(self.pattern_code) +str(self.extra_code))
        elif self.brand_code and self.extra_code !=0:
            self.default_code = (str(self.brand_code) +str(self.extra_code))
        elif self.size_code and self.extra_code !=0:
            self.default_code = (str(self.size_code) +str(self.extra_code))






        elif self.extra_code !=0:
            self.default_code = str(self.extra_code)
        elif self.brand_code !=0:
            self.default_code = str(self.brand_code)

        elif self.model_code !=0:
            self.default_code = str(self.model_code)

        elif self.size_code  !=0:
            self.default_code = str(self.size_code)


        elif self.pattern_code !=0:
            self.default_code = str(self.pattern_code)



        else:

         self.default_code = " "








    #
        #
        # if self.size_code and self.brand_code and self.model_code and self.pattern_code !=0:
        #
        #           self.default_code =(str(self.size_code)+str(self.brand_code)+str(self.model_code)+str(self.pattern_code))
        #
        #
        #
        # elif self.size_code and self.model_code and self.brand_code !=0:
        #     self.default_code = (str(self.size_code) +str(self.model_code)+str(self.brand_code))
        #
        #
        #
        # elif self.pattern_code and self.model_code and self.brand_code != 0:
        #     self.default_code = (str(self.pattern_code) + str(self.model_code) + str(self.brand_code))
        #
        #
        # elif self.pattern_code and self.model_code and self.size_code != 0:
        #     self.default_code = (str(self.pattern_code) + str(self.model_code) + str(self.size_code))
        #
        #
        # elif self.pattern_code and self.brand_code and self.size_code != 0:
        #     self.default_code = (str(self.pattern_code) + str(self.brand_code) + str(self.size_code))
        #
        #
        #
        #
        # elif  self.size_code and self.brand_code !=0:
        #     self.default_code = (str(self.size_code) + str(self.brand_code))
        #
        #
        #
        # elif self.size_code and self.model_code !=0:
        #     self.default_code = (str(self.size_code) +str(self.model_code))
        #
        #
        # elif self.size_code and self.pattern_code !=0:
        #     self.default_code = (str(self.size_code) +str(self.pattern_code))
        #
        #
        #
        # elif self.brand_code and self.model_code !=0:
        #     self.default_code = (str(self.brand_code) + str(self.model_code))
        #
        #
        # elif self.brand_code and self.pattern_code !=0:
        #     self.default_code = (str(self.brand_code) + str(self.pattern_code))
        #
        #
        #
        # elif self.pattern_code and self.model_code !=0:
        #     self.default_code = (str(self.pattern_code) +str(self.model_code))
        #
        #
        #
        #
        #
        #
        # elif self.brand_code !=0:
        #     self.default_code = str(self.brand_code)
        #
        # elif self.model_code !=0:
        #     self.default_code = str(self.model_code)
        #
        # elif self.size_code  !=0:
        #     self.default_code = str(self.size_code)
        #
        #
        # elif self.pattern_code !=0:
        #     self.default_code = str(self.pattern_code)
        #
        # else:
        #
        #  self.default_code = " "
        #




    @api.depends('default_code')
    def _compute_internal_ref(self):
        if self.default_code:
            self.internal_ref_copy = self.default_code
        else:

         self.internal_ref_copy = " "




class ShehataSize(models.Model):
    _name = 'product.size'
    _rec_name = 'size'

    size = fields.Char(string='Size')
    code = fields.Char(string='Code')


class ShehataBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')


class ShehataModel(models.Model):
    _name = 'product.model'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')



class ShehataPattern(models.Model):
    _name = 'product.pattern'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')


class ShehataExtra(models.Model):
    _name = 'product.extra'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')




class ShehataGientDimension(models.Model):
    _name = 'gient.dimension'

    name = fields.Char(string='Name')



class ShehataCarDimension(models.Model):
    _name = 'car.dimension'

    name = fields.Char(string='Name')



class ResPartnerInheritMobile(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('mobile_no_unique', 'unique(mobile)', "Mobile Already Exists It Must Be Unique !"),
    ]

    mobile = fields.Char(string='Mobile')
