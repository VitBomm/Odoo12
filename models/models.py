# -*- coding: utf-8 -*-
from datetime import timedelta
from datetime import date
from odoo import models, fields, api,exceptions

class Bill(models.Model):
    _name = 'hhd.cost.recovery.category'
    _description = 'Hoá Đơn'

    name = fields.Char(string='Tên Hoá Đơn')
    cost_id = fields.Many2one(comodel_name='hhd.cost.recovery', ondelete='cascade', string="Chi Phí", required=True)
    date_start = fields.Date(string='Ngày Làm Hoá Đơn', default=fields.Date.today)
    user_id = fields.Many2one(comodel_name='res.users', on_delete='set null', default=lambda self: self.env.user, string="Nhân Viên", index=True)
    tien_bill = fields.Float('Giá Tiền', digits=(7, 2))

    _sql_constraints = [
        (
            'name_unique_bill',
            'unique(name)',
            'name must be unique',
        )
    ]
    @api.constrains('date_start')
    def check_date_validate(self):
        if self.cost_id.date_start < self.date_start:
            raise exceptions.ValidationError('Ngày Của Hoá Đơn Không Thể Nhỏ Hơn Ngày Của Chi Phí')


class Cost(models.Model):
    _name = 'hhd.cost.recovery'
    _inherit = ['mail.thread']
    _description = 'Chi Phí'

    name = fields.Char(String='Tên Chi Phí')
    tongtien = fields.Float(String='Tổng Tiền', digits=(10,2), compute="_all_money", store=True)
    description = fields.Text(string='Mô Tả')
    note_field = fields.Text(string='Ghi Chú')
    bill_ids = fields.One2many(comodel_name='hhd.cost.recovery.category', inverse_name='cost_id', string="Hoá Đơn")
    user_id = fields.Many2one(comodel_name='res.users', ondelete='set null', default=lambda self: self.env.user, string='Nhân Viên', index=True)
    manager_id = fields.Many2one(comodel_name='res.users', ondelete='set null', string='Quản lý', index=True)
    partner_id = fields.Many2one(comodel_name='res.partner', ondelete='set null', string='Đối Tác', index=True)
    date_start = fields.Date(string ="Ngày Lập Phiếu", default=fields.Date.today)
    duration = fields.Float(string="Số Ngày Cần Hoàn Tiền", digits=(6, 2), help="Duration in days")
    end_date = fields.Date(string="Ngày Hết Hạn", store=True, compute="_get_end_date", inverse="_set_end_date")
    expired = fields.Char(string='Hết Hạn', store=True, compute="_is_expired")
    state = fields.Selection(string='Tình Trạng', selection=[('draft', 'Draft'), ('submit', 'Submit'), ('approve', 'Approve'),
                                                             ('done', 'Done'), ('cancel', 'Cancel')], default="draft", track_visibility='onchange')
    invoice = fields.Many2one(comodel_name='account.invoice', ondelete='cascade', string='Hoá Đơn Cần Thanh Toán', index=True)

    @api.multi
    def submit_request(self):
        self.state = 'submit'

    @api.multi
    def approve_request(self):
        self.state = 'approve'

    @api.multi
    def done_request(self):
        self.state = 'done'

    @api.multi
    def cancel_request(self):

        self.state = 'draft'

    # @api.multi
    # def draft_request(self):
    #     self.state = 'draft'

    @api.onchange('manager_id')
    def _default_manager(self):
        if not self.manager_id:
            self.manager_id = self.env.user

    @api.constrains('user_id','manager_id')
    def _check_manager_not_in_user_id(self):
        for r in self:
            if r.user_id and r.user_id == r.manager_id:
                raise exceptions.ValidationError('Nhân viên mà đòi làm quản lý. haha')

    @api.depends('date_start', 'duration')
    def _get_end_date(self):
        for r in self:
            if not(r.date_start and r.duration):
                r.end_date = r.date_start
            else:
                r.end_date = r.date_start + timedelta(r.duration)

    @api.depends('date_start', 'duration')
    def _set_end_date(self):
        for r in self:
            if not(r.date_start and r.end_date):
                continue

            r.duration = (r.end_date - r.date_start).days + 1
    
    def _is_expired(self):
        for r in self.search([]):
            if r.state != 'done':
                if r.end_date < (date.today() + timedelta(1)):
                    r.expired = 'Hết Hạn'
                else:
                     r.expired = 'Còn '+ str((r.end_date - date.today() + timedelta(1)).days) + ' ngày nữa hết hạn'
            else:
                r.expired = 'Đã Thanh Toán'

    @api.depends('state')
    def _check_done(self):
        for r in self:
            if r.state == 'done':
                r.expired = 'Đã Thanh Toán'

    @api.depends('bill_ids.tien_bill')
    def _all_money(self):
        for r in self:
            r.tongtien = sum(r.bill_ids.mapped('tien_bill'))

    _sql_constraints = [

        ('cost_name_unique',

         'UNIQUE(name)',

         "The Name must be unique"),

    ]






