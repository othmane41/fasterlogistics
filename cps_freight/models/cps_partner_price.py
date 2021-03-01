"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class CpsVoyageTracking(models.Model):

    _name = 'cps.soustraitant.price'
    _description = "Prix du voyage par fournisseur"

    trajet_id = fields.Many2one('cps.trajet', 'Voyage')
    vehicule_sous_traitant_1 = fields.Many2one('cps.soustraitant', 'Vehicule')
    price = fields.Float('Prix')

