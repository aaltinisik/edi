# -*- encoding: utf-8 -*-
#
#Created on Dec 21, 2018
#
#@author: dogan
#


from odoo import models, fields


class EinvoicePostbox(models.Model):
    _name = 'res.partner.einvoice.postbox'
    
    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one('res.partner','Partner', required=True, ondelete='cascade')
    