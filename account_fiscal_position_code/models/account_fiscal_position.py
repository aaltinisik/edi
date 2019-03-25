# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015, Eska Yazılım ve Danışmanlık A.Ş.
#    http://www.eskayazilim.com.tr
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


from odoo import models, fields, api


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    code = fields.Char(string='Code')

    @api.one
    def name_get(self):
        if self.code:
            return self.id, '[%s] %s' % (self.code, self.name)
        else:
            return self.id, self.name

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

