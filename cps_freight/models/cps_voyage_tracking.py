"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class CpsVoyageTracking(models.Model):

    _name = 'cps.voyage.tracking'
    _description = "Tracking du voyage"

    voyage_id = fields.Many2one('cps.voyage', 'Voyage')

    date_tracking= fields.Datetime(string="Date")
    duree=fields.Float('Durée (min)')
    description = fields.Char('Déscription')

