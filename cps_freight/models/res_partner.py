"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResPartner(models.Model):
    """Inherit Partner Model."""

    _inherit = 'res.partner'

    liste_voyages = fields.One2many('cps.voyage', 'client_id', 'Liste des voyages')
    liste_vehicules = fields.One2many('fleet.vehicle', 'soustraitant_id', 'Liste des véhicules')

    is_transitaire = fields.Boolean(string="Est transitaire")
    is_soutraitant = fields.Boolean(string="Est sous-traitant")
    is_compagnie_aerienne = fields.Boolean(string="Est une compagnie aerienne")
    is_compagnie_maritine = fields.Boolean(string="Est une compagnie maritine")
    is_compagnie_magasinnage = fields.Boolean(string="Est une compagnie de magasinnage")

    numero_ice = fields.Char('ICE')
    numero_cnss = fields.Char('N° CNSS')
    numero_rc = fields.Char('N° RC')
    numero_if = fields.Char('N° IF')
    numero_tp = fields.Char('N° TP')
    classement = fields.Char('Classement')