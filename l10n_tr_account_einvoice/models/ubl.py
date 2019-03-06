# -*- coding: utf-8 -*-

from odoo import models, api, tools, _
from odoo.exceptions import UserError
from lxml import etree
import logging

logger = logging.getLogger(__name__)


class BaseUbl(models.AbstractModel):
    _inherit = 'base.ubl'

    @api.model
    def _ubl_check_xml_schema(self, xml_string, document, version='2.1'):
        '''Validate the XML file against the XSD'''
        xsd_file = 'l10n_tr_account_einvoice/data/xsd-%s/maindoc/UBL-%s-%s.xsd' % (
            version, document, version)
        xsd_etree_obj = etree.parse(tools.file_open(xsd_file))
        official_schema = etree.XMLSchema(xsd_etree_obj)
        '''
        try:
            t = etree.parse(StringIO(xml_string))
            official_schema.assertValid(t)
        except Exception, e:
            # if the validation of the XSD fails, we arrive here
            logger = logging.getLogger(__name__)
            logger.warning(
                "The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_string)
            logger.warning(e)
            raise UserError(_(
                "The UBL XML file is not valid against the official "
                "XML Schema Definition. The XML file and the "
                "full error have been written in the server logs. "
                "Here is the error, which may give you an idea on the "
                "cause of the problem : %s.")
                            % unicode(e))
        '''
        return True

    @api.model
    def _ubl_get_nsmap_namespace(self, doc_name, version='2.1'):
        nsmap = {
            None: 'urn:oasis:names:specification:ubl:schema:xsd:' + doc_name,
            'cac': 'urn:oasis:names:specification:ubl:'
                   'schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:'
                   'CommonBasicComponents-2',
            'ext': 'urn:oasis:names:specification:ubl:schema:xsd:'
                   'CommonExtensionComponents-2',
            'ubltr': 'urn:oasis:names:specification:ubl:schema:xsd:'
                     'TurkishCustomizationExtensionComponents',
            'udt': 'urn:un:unece:uncefact:data:specification:'
                   'UnqualifiedDataTypesSchemaModule:2',
            'qdt': 'urn:oasis:names:specification:ubl:schema:xsd:'
                   'QualifiedDatatypes-2',
            'ccts': 'urn:un:unece:uncefact:'
                    'documentation:2',
        }
        ns = {
            'cac': '{urn:oasis:names:specification:ubl:schema:xsd:'
                   'CommonAggregateComponents-2}',
            'cbc': '{urn:oasis:names:specification:ubl:schema:xsd:'
                   'CommonBasicComponents-2}',
            'ext': '{urn:oasis:names:specification:ubl:schema:xsd:'
                   'CommonExtensionComponents-2}',
            'ubltr': '{urn:oasis:names:specification:ubl:schema:xsd:'
                     'TurkishCustomizationExtensionComponents}',
            'udt': '{urn:un:unece:uncefact:data:specification:'
                   'UnqualifiedDataTypesSchemaModule:2}',
            'qdt': '{urn:oasis:names:specification:ubl:schema:xsd:'
                   'QualifiedDatatypes-2}',
            'ccts': '{urn:un:unece:uncefact:'
                    'documentation:2}',
        }
        return nsmap, ns

    @api.model
    def _ubl_get_party_identification(self, commercial_partner):
        '''This method is designed to be inherited in localisation modules
        Should return a dict with key=SchemeName, value=Identifier'''
        vat_no = "'CC##' (CC=Country Code, ##=VAT Number)"
        dict = {}
        if commercial_partner.vat:
            if len(commercial_partner.vat) == 12:
                dict["VKN"] = commercial_partner.vat[2:]
            elif len(commercial_partner.vat) == 13:
                dict["TCKN"] = commercial_partner.vat[2:]
            elif len(commercial_partner.vat) == 10:
                dict["VKN"] = commercial_partner.vat
            elif len(commercial_partner.vat) == 11:
                dict["TCKN"] = commercial_partner.vat
            else:
                raise UserError(_(
                    'The VAT number [%s] for partner [%s] does not seem to be valid. \nNote: the expected format is %s') % (
                                    commercial_partner.vat, commercial_partner.name, vat_no))
        else:
            dict["TCKN"] = "11111111111"
        if commercial_partner.commercial_id:
            dict["TICARETSICILNO"] = commercial_partner.commercial_id
        if commercial_partner.mersis:
            dict["MERSISNO"] = commercial_partner.mersis
 
        return dict
# 
# 
# 
# 

    @api.model
    def _ubl_add_address(
            self, partner, node_name, parent_node, ns, version='2.1'):
        address = etree.SubElement(parent_node, ns['cac'] + node_name)
        if partner.street:
            streetname = etree.SubElement(
                address, ns['cbc'] + 'StreetName')
        if hasattr(partner,'neighbour_id') and partner.neighbour_id:
            streetname.text = '  '+ partner.neighbour_id.name
        if partner.street:
            streetname.text  += partner.street
        etree.SubElement(address, ns['cbc'] + 'BuildingNumber')
        etree.SubElement(address, ns['cbc'] + 'CitySubdivisionName')
        if partner.street2:
            streetname.text += ' ' + partner.street2
        if hasattr(partner, 'street3') and partner.street3:
            blockname = etree.SubElement(
                address, ns['cbc'] + 'BlockName')
            blockname.text = partner.street3
        if partner.city or hasattr(partner,'district_id') and partner.district_id:
            city = etree.SubElement(address, ns['cbc'] + 'CityName')
            city.text = partner.city or partner.district_id.name
        if partner.zip:
            zip = etree.SubElement(address, ns['cbc'] + 'PostalZone')
            zip.text = partner.zip
        if partner.country_id:
            self._ubl_add_country(
                partner.country_id, address, ns, version=version)
        else:
            logger.warning('UBL: missing country on partner %s', partner.name)


