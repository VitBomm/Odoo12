from odoo import models, fields, api,exceptions

class Payment_Inherit(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def action_validate_invoice_payment(self):
        res = super(Payment_Inherit, self).action_validate_invoice_payment()
        temp = self.env.context.get('active_id')
        invoice = self.env['account.invoice'].browse(temp)
        for r in invoice.cost_id:
            r.state = 'done'
        if res:
            template = self.env.ref('hhd_cost_recovery.example_email_template')
            self.env['mail.template'].browse(template.id).send_mail(self.id)
        return res