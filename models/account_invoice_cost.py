from odoo import models, api, fields

class Inherit_Invoice(models.Model):
    _inherit = 'account.invoice'
    
    cost_id = fields.One2many(comodel_name='hhd.cost.recovery', inverse_name='invoice', string="Chi Phí", index=True)
