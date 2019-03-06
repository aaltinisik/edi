# -*- encoding: utf-8 -*-
#
#Created on Dec 24, 2018
#
#@author: dogan
#

from odoo import models, fields, api


class EinvoiceProvider(models.Model):
    _name = 'account.einvoice.provider'
    
    type = fields.Selection([],string='Type')
    environment = fields.Selection([('test','TEST'),('prod','PRODUCTION')])
    name = fields.Char('Name')
    
    
    
    
    @api.multi
    def send(self, invoice):
        ''' Send e-invoice ubl to provider. Intended to be implemented by inheriting module
        '''
        pass
    
    
    @api.multi
    def get_registered_user(self, vat):
        ''' Get registration status of a vat from provider. Intended to be implemented by inheriting module
        '''
        pass
    
    @api.multi
    def get_pdf(self, uuid):
        ''' Get PDF document from provider. Intended to be implemented by inheriting module
        '''
        pass
    
    @api.multi
    def GetXML(self, invoice):
        ''' Get signed xml from provider. Intended to be implemented by inheriting module
        '''
        pass
    
    @api.multi
    def get_state(self, invoice):
        ''' Update invoice state from provider. Intended to be implemented by inheriting module
        '''
        pass
    
    @api.multi
    def cancel(self, invoice):
        ''' Update invoice state from provider. Intended to be implemented by inheriting module
        '''
        pass
    
   
    
    
    