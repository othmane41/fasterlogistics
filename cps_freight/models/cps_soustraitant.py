"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class CpsSousTraitant(models.Model):

    _name = 'cps.soustraitant'
    _description = "Vehicule des sous-traitant"

    soustraitant_id = fields.Many2one("res.partner", string='Sous-traitant', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', True),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)], required=True)
    vehicule_id = fields.Many2one('fleet.vehicle', 'Vehicule', domain=[('soustraitant_id', '!=', False)])
    name = fields.Char('Nom', compute="compute_name")

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            res.append((rec.id, name))
        return res

    def get_name(self):
        for p in self:
            name = ""
            if p.soustraitant_id is not False:
                name = name + p.soustraitant_id.name
            if p.vehicule_id is not False:
                name = name + " / " + p.vehicule_id.name
            return name

    @api.depends('soustraitant_id','vehicule_id')
    def compute_name(self):
        for p in self:
            name = ""
            if len(p.soustraitant_id)>0:
                name = name + p.soustraitant_id.name
            if len(p.vehicule_id) >0:
                name = name + " / " + p.vehicule_id.name
            p.name =  name


