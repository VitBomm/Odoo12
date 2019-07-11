from odoo import models, api, fields,exceptions

class Add_Invoice_Wizard(models.TransientModel):
    _name= "hhd.add.invoice.wizard"

    chiphi_id = fields.Many2many(comodel_name="hhd.cost.recovery", relation="chiphi_addvoice", string="Chi Phí của nhân viên", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Nhân Viên")
    customer_id = fields.Many2one(comodel_name="res.partner", string="Khách Hàng", default=lambda self: self.env['account.invoice'].browse(self.env.context.get('active_id')).partner_id, readonly=True)

    @api.onchange('user_id')
    @api.multi
    def on_change_partner(self):
        if self.user_id:
            return {'domain': {'chiphi_id': ['&', ('user_id', '=', self.user_id.id), ('state', '=', 'approve'), ('partner_id.id', '=', self.customer_id.id)]}}
    
    @api.multi
    def auto_add_product(self):
        description = '--'.join(self.chiphi_id.mapped('name'))
        tongtien = sum(self.chiphi_id.mapped('tongtien'))
        temp = self.env.context.get('active_id')
        invoice = self.env['account.invoice'].browse(temp)
        for r in self.chiphi_id:
            invoice.cost_id = [(4, r.id, 0)]
        invoice.invoice_line_ids = [(0, 0, {'name': description, 'price_unit': tongtien, 'account_id': self.user_id.id})]
        # self.env['account.invoice.line'].write({'name':'Test1213123','invoice_id':temp1.id})
        #invoice.cost_id.create({'invoice':})