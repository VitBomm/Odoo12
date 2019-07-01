from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class ReportWizard(models.TransientModel):
    
    _name='hhd.cost.recovery.report.wizard'
    _description='Report theo điều kiện'

    date_from = fields.Date(string="Start Date",required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required =True, default=fields.Date.today)

    # user_id = fields.Many2one('hhd.cost.recovery',on_delete="set null", string="Nhân Viên")
    # partner_id = fields.Many2one('res.partner',on_delete="set null", string="Nhân Viên")
    # state = fields.Selection()
    
    @api.multi
    def get_report(self):
        data = {
            'ids' : self.ids,
            'model' : self._name,
            'form' :
            {
                'date_from' : self.date_from,
                'date_end' : self.date_end,
            },
        }
        return self.env.ref('hhd_cost_recovery.recap_report').report_action(self, data=data)

    # @api.multi
    # def get_report_xlsx(self):

class ReportCostRecap(models.AbstractModel):
    _name = 'report.hhd_cost_recovery.cost_recap_report_view'

    @api.model
    def _get_report_values(self, docids,data=None):
        date_from = data['form']['date_from']
        date_end = data['form']['date_end']
        date_from_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        
        docs = []
        costs = self.env['hhd.cost.recovery'].search([],order='name asc')
        for cost in costs:
            if cost.date_start >= date_from_obj.date() and cost.end_date <= date_end_obj.date():
                docs.append(
                    {
                        'cost_name': cost.name,
                        'tongtien': cost.tongtien,
                        'user_id' : cost.user_id,
                        'expired': cost.expired,
                        'partner_id': cost.partner_id,
                    }
                )   
        print(docs)
        return 
        {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'date_from': date_from,
                'date_end': date_end,
                'docs': docs,
        }

