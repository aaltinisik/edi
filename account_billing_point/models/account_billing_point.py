# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018, Kod Merkezi Yazılım LTD.
#    http://www.codequarters.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountBillingPoint(models.Model):
    _name = 'account.billing.point'
    _description = 'Billing Point'

    name = fields.Char(string='Name', required=True)

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'account.billing.point'))

    user_ids = fields.One2many('res.users', 'default_billing_point_id', string="Users")

    parent_id = fields.Many2one(string='Parent Billing Point', comodel_name='account.billing.point', index=True,
                                ondelete='restrict')
    child_ids = fields.One2many(string='Child Billing Points', comodel_name='account.billing.point',
                                inverse_name='parent_id')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        bps = self.search(args, limit=limit)
        return bps.name_get()

    @api.constrains("parent_id")
    def _check_recursion(self):
        if not super(AccountBillingPoint, self)._check_recursion():
            raise ValidationError(
                _("Error! Cannot create recursive cycle.")
            )
