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
            # You can also find the e-mail template like this:
            # template = self.env['ir.model.data'].get_object('mail_template_demo', 'example_email_template')
    
            # Send out the e-mail template to the user
            self.env['mail.template'].browse(template.id).send_mail(self.id)
        return res