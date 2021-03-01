"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Account_move(models.Model):
    """Inherit Partner Model."""

    _inherit = 'account.move'

    voyage_id = fields.Many2one("cps.voyage", string='Voyage')

