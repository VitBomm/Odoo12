# -*- coding: utf-8 -*-
from odoo import http

# class HhdCostRecovery(http.Controller):
#     @http.route('/hhd_cost_recovery/hhd_cost_recovery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hhd_cost_recovery/hhd_cost_recovery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hhd_cost_recovery.listing', {
#             'root': '/hhd_cost_recovery/hhd_cost_recovery',
#             'objects': http.request.env['hhd_cost_recovery.hhd_cost_recovery'].search([]),
#         })

#     @http.route('/hhd_cost_recovery/hhd_cost_recovery/objects/<model("hhd_cost_recovery.hhd_cost_recovery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hhd_cost_recovery.object', {
#             'object': obj
#         })