from odoo import models, fields, api, _, exceptions
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class ReportWizard(models.TransientModel):
    
    _name='hhd.cost.recovery.report.wizard'
    _description='Report theo điều kiện'

    date_from = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required =True, default=fields.Date.today)
    user_id = fields.Many2one('res.users', ondelete='set null', string='Nhân Viên', index=True)
    partner_id = fields.Many2one('res.partner', on_delete="set null", string="Đối Tác", index=True)
    state = fields.Selection(String='Status', selection=[('draft', 'Draft'), ('submit', 'Submit'), ('approve', 'Approve'), ('done', 'Done')], default = "done")
    @api.constrains('date_from','date_end')
    def checkdate(self):
        if self.date_from and self.date_end and (self.date_from > self.date_end):
            raise exceptions.ValidationError('Ngày Kết Thúc Không Thể Ngắn Hơn Ngày Bắt Đầu')

    @api.multi
    def get_report(self):
        data = {
            'ids' : self.ids,
            'model' : self._name,
            'form' :
            {
                'date_from' : self.date_from,
                'date_end' : self.date_end,
                'user_selected': self.user_id.id,
                'partner_selected': self.partner_id.id,
                'state' : self.state,
            },
        }
        if self.env.context.get('report_type') == 'pdf':
            return self.env.ref('hhd_cost_recovery.recap_report').report_action(self, data=data)
        # else:
        #     return self.env.ref('hhd_cost_recovery.cost_xlsx').report_action(self, data=data)

class ReportCostRecap(models.AbstractModel):
    _name = 'report.hhd_cost_recovery.cost_recap_report_view'

    def docs_add(self, docs, temp):
        docs.append({
           'cost_name': temp.name,
            'tongtien': temp.tongtien,
            'user_id' : temp.user_id.name,
            'expired': temp.expired,
            'partner_id': temp.partner_id.name,
        })

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_end = data['form']['date_end']
        user_id = int(data['form']['user_selected'])
        partner_id = int(data['form']['partner_selected'])
        state = data['form']['state']
        date_from_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        
        docs = []
        costs = self.env['hhd.cost.recovery'].search([], order='name asc')
        for cost in costs:
            if cost.date_start >= date_from_obj.date() and cost.end_date <= date_end_obj.date():
                if state == False and partner_id == 0 == user_id:
                    self.docs_add(docs, cost)
                elif partner_id == 0 == user_id: 
                    if cost.state == state:
                        self.docs_add(docs, cost)
                elif partner_id== 0 and state== False:
                    if  cost.user_id.id == user_id:
                        self.docs_add(docs, cost)
                elif user_id == 0 and state== False:
                    if cost.partner.id == partner_id:
                        self.docs_add(docs, cost)
                elif state == False:
                    if cost.partner.id == partner_id and cost.user_id.id == user_id:
                        self.docs_add(docs, cost)
                elif user_id == 0:
                    if cost.partner_id.id == partner_id and cost.state == state:
                        self.docs_add(docs, cost)
                elif partner_id == 0:
                    if cost.user_id.id == user_id and cost.state == state:
                        self.docs_add(docs, cost)
                else:
                    if cost.user_id.id == user_id and cost.state == state and cost.partner_id.id == partner_id:
                        self.docs_add(docs, cost)

        return dict({
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
            'date_from': date_from,
            'date_end': date_end,
        })

