"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class CpsPrestation(models.Model):

    _name = 'cps.prestation'
    _description = "Liste des prestations"

    # name = fields.Char(string='Nom de la préstation')
    # liste_voyage = fields.One2many('cps.voyage', 'prestation_id', string='Liste des voyages')


