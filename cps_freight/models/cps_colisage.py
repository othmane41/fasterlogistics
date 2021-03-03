"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class CpsColisage(models.Model):

    _name = 'cps.colisage'
    _description = "Liste des colis"

    voyage_id = fields.Many2one("cps.voyage", string='Voyage')
    type_colis = fields.Selection([('colis','Colis'), ('palette','Palette')], string='Type', default='colis')
    qte_colis = fields.Integer("Quantité")


