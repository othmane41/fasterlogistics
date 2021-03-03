"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class CpsTrajet(models.Model):

    _name = 'cps.trajet'
    _description = "Lignes des trajets"

    voyage_ids = fields.One2many("cps.voyage", 'trajet_id', string="Liste des voyages")

    lieu_ramassage = fields.Many2one("res.partner", string='Lieu de ramassage', domain=[('type','=', 'delivery')], required=True)
    lieu_livraison = fields.Many2one("res.partner", string='Lieu de livraison', domain=[('type','=', 'delivery')], required=True)
    ville_ramassage = fields.Char(related='lieu_ramassage.city', string='Ville ramassage')
    ville_livraison = fields.Char(related='lieu_livraison.city', string='Ville livraison')
    cout = fields.Float(string="Cout")
    name = fields.Char('Nom', compute="compute_name")
    currency_id = fields.Many2one('res.currency', string='Devise')
    partner_price_ids = fields.One2many('cps.soustraitant.price', 'trajet_id', string='Fournisseurs')
    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            res.append((rec.id, name))
        return res

    def get_name(self):
        for p in self:
            name = ""
            if p.lieu_ramassage is not False and p.lieu_livraison is not False :
                name = name + str(p.lieu_ramassage) + " - " + str(p.lieu_livraison)
            return name

    @api.depends('lieu_ramassage','lieu_livraison')
    def compute_name(self):
        for p in self:
            name = ""
            if p.lieu_ramassage is not False and p.lieu_livraison is not False :
                name = name + str(p.ville_ramassage) + "/" + str(p.lieu_ramassage.name)  + " -> " + str(p.ville_livraison) + "/" + str(p.lieu_livraison.name)
            p.name =  name
