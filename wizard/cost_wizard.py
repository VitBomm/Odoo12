from odoo import models, fields, api

class CostWizard(models.TransientModel):
    _name = "hhd.cost.recovery.wizard"
    _description = "Thêm Note"

    cost_id = fields.Many2one('hhd.cost.recovery', string="Chi Phí", default=default_cost)
    field_note = fields.Text()

    def default_cost(self):
        return self.env['hhd.cost.recovery'].browse(self._context.get('note_field'))

    @api.multi
    def change_field(self):
        self.cost_id.note_field = self.field_note
        self.cost_id.state = 'draft'
