"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResPartner(models.Model):
    """Inherit Partner Model."""

    _inherit = 'fleet.vehicle'

    soustraitant_id = fields.Many2one("res.partner", string='Sous-traitant', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', True),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])

