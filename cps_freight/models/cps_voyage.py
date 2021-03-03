"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError

class CpsVoyage(models.Model):

    _name = 'cps.voyage'
    _description = "Liste des voyages"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    progress = fields.Float("Progression", compute='compute_progress_state', store=True, group_operator="avg", help="Display progress of current task.")

    state_national = fields.Selection([('pret','Pret'), ('encours','En cours'), ('attente_chargement','Att. Char.'), ('attente_doc','Att. doc.'), ('charge','Chargé'), ('route','En route'), ('attente_liv','Att. livr.'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_cch = fields.Selection([('pret','Pret'), ('encours','En cours'), ('attente_chargement','Att. Char.'), ('attente_doc','Att. doc.'), ('charge','Chargé'), ('route','En route'), ('dedouanement','Dédouanement'), ('handling','Handling'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_dap = fields.Selection([('pret','Pret'),('attente_doc','Att. Doc.'), ('echange','En echange'),  ('dedouanement','Dédouanement'), ('attente_chargement','Att. Char.'), ('charge','Chargé'), ('route','En route'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_fret = fields.Selection([('pret','Pret'),('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('landing','Landing'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_obc = fields.Selection([('pret','Pret'),('encours','En cours'), ('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('route','En route'), ('dedouanement','Dédouanement'),('en_board','En board'),('take_off','Take off'),('landed','Landed'),('route_2','En Route'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_charter_dtd = fields.Selection([('pret','Pret'),('encours','En cours'), ('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('route','En route'), ('dedouanement','Dédouanement'),('en_board','En board'),('take_off','Take off'),('landed','Landed'),('released','Released'),('route_2','En Route'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_routier = fields.Selection([('pret','Pret'),('encours','En cours'), ('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('dedouanement_zf','Dédouanement ZF'), ('route','En route'), ('dedouanement','Dédouanement'),('scanner','En Scanner'),('on_board','On board'),('amarrage','Amarage'),('route_2','En Route'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_routier_transbordement = fields.Selection([('pret','Pret'),('encours','En cours'), ('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('dedouanement_zf','Dédouanement ZF'), ('route','En route'), ('dedouanement','Dédouanement'),('scanner','En Scanner'),('on_board','On board'),('amarrage','Amarage'),('transbordement','Transbordement'),('route_2','En Route'), ('livre','Livré'), ('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    state_general =  fields.Selection([('pret','Pret'),('encours','En cours'), ('attente_chargement','Att. Char.'),('attente_doc','Att. Doc.'), ('dedouanement_zf','Dédouanement ZF'), ('route','En route'), ('dedouanement','Dédouanement'),('scanner','En Scanner'),('on_board','On board'),('amarrage','Amarage'),('transbordement','Transbordement'),('route_2','En Route'), ('livre','Livré'),('charge','Chargé'), ('attente_liv','Att. Liv.'),('handling','Handling'),('echange','Echange'),('landing','Landing'),('en_board','On board'),('take_off','Take off'),('landed','Landed'),('released','Released'),('annule','Annulé'), ('bloque','BLoqué')], string='Etat', default='pret')
    priorite = fields.Selection([('faible','Faible'),('moyen','Moyen'),('eleve','Elevé'), ('prioritaire','Prioritaire')], string='Priorité', default='faible')
    tracking_ids = fields.One2many('cps.voyage.tracking', 'voyage_id', string='Tracking du voyage')
    resume_ids = fields.One2many('cps.voyage.resume', 'voyage_id', string='Résumé du voyage')
    date= fields.Datetime(string="Date")
    default_code = fields.Char("N° Voyage")
    client_id = fields.Many2one("res.partner", string='Client', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 0),('is_company', '=', True)])
    ref_client = fields.Char("Référence Client")
    type_ramassage = fields.Selection([('ftl','F.T.L.'), ('groupage','Groupage')], string='Type ramassage', default='ftl')
    colisage_ids = fields.One2many('cps.colisage', 'voyage_id', string='Liste des colis')
    facture_achat_ids = fields.One2many('account.move', 'voyage_id', domain=[('move_type', '=', 'in_invoice')], string="Factures d'achat")
    total_facture_achats = fields.Float('Factures achats', compute="compute_facture_achat_amount")
    facture_vente_ids = fields.One2many('account.move', 'voyage_id', domain=[('move_type', '=', 'out_invoice')], string="Factures de vente")
    total_facture_vente = fields.Float('Factures achats', compute="compute_facture_vente_amount")
    type_voyage  = fields.Selection([('national','National'), ('international','International')], string='Type', default='national')
    type_trajet = fields.Selection([('import','Import'), ('export','Export')], string='Direction', default='export')
    type_operation = fields.Selection([('cch','CCH'), ('dap','DAP'), ('fret','Fret Aerien'), ('obc','OBC'), ('charter','Charter'), ('dtd','DTD'), ('routier','Routier'), ('routier-trans','Routier avec Transbordement')], string='Transport', default='cch')
    ton = fields.Char("TON")
    ref_tmc = fields.Char("Ref TMC")
    # prestation_id = fields.Many2one("cps.prestation", string='Type préstation')
    name = fields.Char('Nom du voyage', compute='compute_name', store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(related="company_id.currency_id", string="devise")

    trajet_id = fields.Many2one('cps.trajet', 'Trajet')
    cout_trajet = fields.Float( related='trajet_id.cout', string="Cout du trajet", store=True)
    cout_total = fields.Monetary( compute='compute_cout', string="Cout total", store=True)
    marge = fields.Float('Marge (%)')
    prix = fields.Monetary(string="Prix de vente", store=True)
    sous_traitance_1 = fields.Boolean('Sous-traitance ?')
    vehicule_parc_1 = fields.Many2one('fleet.vehicle', 'Vehicule parc', domain=[('soustraitant_id', '=', False)])
    mat_vehicule_parc_1 = fields.Char('Matricule', related='vehicule_parc_1.license_plate')
    vehicule_sous_traitant_1 = fields.Many2one('cps.soustraitant', 'Vehicule sous-traitant')
    cout_sous_traitant_1 = fields.Monetary(string="Cout")
    mat_vehicule_sous_traitant_1 = fields.Char('Matricule', related='vehicule_sous_traitant_1.vehicule_id.license_plate')
    # ----CCH fields--------
    dedouanement_1 = fields.Many2one("res.partner", string='Transitaire', domain=[('is_transitaire', '=', True),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_transitaire_1 = fields.Monetary(string="Cout")
    handling = fields.Many2one("res.partner", string='Handling', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', True),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_handling = fields.Monetary(string="Cout")
    porteur = fields.Monetary(string="Porteurs")

    #-----DAP------------
    n_lta = fields.Char(string='N° LTA')
    echange= fields.Many2one("res.partner", string='Echange', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', True),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_echange = fields.Monetary(string="Cout")


    #--------- FRET--------------
    fret = fields.Many2one("res.partner", string='Fret', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', True),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_fret = fields.Monetary(string="Cout fret")

    #OBC
    cout_bagage = fields.Monetary(string="Excédent bagage")
    frais_divers = fields.Monetary(string="Frais divers")
    dedouanement_2 = fields.Many2one("res.partner", string='Transitaire', domain=[('is_transitaire', '=', True),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_transitaire_2 = fields.Monetary(string="Cout")
    sous_traitance_2 = fields.Boolean('Sous-traitance ?')
    vehicule_parc_2 = fields.Many2one('fleet.vehicle', 'Vehicule parc', domain=[('soustraitant_id', '=', False)])
    mat_vehicule_parc_2 = fields.Char('Matricule', related='vehicule_parc_2.license_plate')
    vehicule_sous_traitant_2 = fields.Many2one('cps.soustraitant', 'Vehicule sous_traitant')
    mat_vehicule_sous_traitant_2 = fields.Char('Matricule', related='vehicule_sous_traitant_2.vehicule_id.license_plate')
    cout_sous_traitant_2 = fields.Monetary(string="Cout")


    #INTER-ROUTIER
    bateau = fields.Many2one("res.partner", string='Bateau', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', True),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_bateau = fields.Monetary(string="Cout")
    dedouanement_zf = fields.Many2one("res.partner", string='Transitaire ZF', domain=[('is_transitaire', '=', True),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', False),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_transitaire_zf = fields.Monetary(string="Cout")

    #INTER-ROUTIER TRANSBORDEMENT
    transbordement = fields.Many2one("res.partner", string='Transbordement', domain=[('is_transitaire', '=', False),('is_soutraitant', '=', False),('is_compagnie_aerienne', '=', False),('is_compagnie_maritine', '=', False),('is_compagnie_magasinnage', '=', True),('supplier_rank', '=', 1),('is_company', '=', True)])
    cout_transbordement = fields.Monetary(string="Cout")

    @api.onchange('vehicule_sous_traitant_1')
    def onchange_vehicule_soustraitant(self):
        vehicule_sous_traitant = self.env['cps.soustraitant.price'].search([('trajet_id', '=', self.trajet_id.id),('vehicule_sous_traitant_1', '=', self.vehicule_sous_traitant_1.id)],order='id desc', limit=1)
        self.cout_sous_traitant_1 = vehicule_sous_traitant.price
        if self.type_voyage=='national':
            self.cout_trajet = self.cout_sous_traitant_1

    @api.model
    def create (self, vals):
        vals['default_code'] = self.env['ir.sequence'].next_by_code('cps.voyage')
        result = super ( CpsVoyage, self).create(vals)
        self.env['cps.voyage.tracking'].create({'voyage_id': result.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_national'].selection).get(self.state_national)})
        result.calculer_resume()
        return result

    def write(self, values):
        voyage = super(CpsVoyage, self).write(values)
        self.calculer_resume()
        self.compute_state(values)
        return voyage

    @api.depends('state_national','state_cch','state_dap','state_fret','state_charter_dtd','state_routier','state_routier_transbordement')
    def compute_progress_state(self):
        i=0
        progress=0
        for s in self:
            if s.type_voyage=='national':
                if s.state_national!="pret" and s.state_national!="bloque" and  s.state_national!="annule" :
                    for state in dict(s._fields['state_national'].selection).keys():
                        i+=1
                        if state==s.state_national:
                            progress=i / (len(dict(s._fields['state_national'].selection))-2)*100
            if s.type_operation=="cch":
                if s.state_cch!="pret" and s.state_cch!="bloque" and  s.state_cch!="annule" :
                    for state in dict(s._fields['state_cch'].selection).keys():
                        i+=1
                        if state==s.state_cch:
                            progress=i / (len(dict(s._fields['state_cch'].selection))-2)*100
            if s.type_operation=="dap":
                if s.state_dap!="pret" and s.state_dap!="bloque" and  s.state_dap!="annule" :
                    for state in dict(s._fields['state_dap'].selection).keys():
                        i+=1
                        if state==s.state_dap:
                            progress=i / (len(dict(s._fields['state_dap'].selection))-2)*100
            if s.type_operation=="fret":
                if s.state_fret!="pret" and s.state_fret!="bloque" and  s.state_fret!="annule" :
                    for state in dict(s._fields['state_fret'].selection).keys():
                        i+=1
                        if state==s.state_fret:
                            progress=i / (len(dict(s._fields['state_fret'].selection))-2)*100
            if s.type_operation=="charter" or s.type_operation=="dtd":
                if s.state_charter_dtd!="pret" and s.state_charter_dtd!="bloque" and  s.state_charter_dtd!="annule" :
                    for state in dict(s._fields['state_charter_dtd'].selection).keys():
                        i+=1
                        if state==s.state_charter_dtd:
                            progress=i / (len(dict(s._fields['state_charter_dtd'].selection))-2)*100
            if s.type_operation=="routier":
                if s.state_routier!="pret" and s.state_routier!="bloque" and  s.state_routier!="annule" :
                    for state in dict(s._fields['state_routier'].selection).keys():
                        i+=1
                        if state==s.state_routier:
                            progress=i / (len(dict(s._fields['state_routier'].selection))-2)*100
            if s.type_operation=="routier_transbordement-trans":
                if s.state_routier_transbordement!="pret" and s.state_routier_transbordement!="bloque" and  s.state_routier_transbordement!="annule" :
                    for state in dict(s._fields['state_routier_transbordement'].selection).keys():
                        i+=1
                        if state==s.state_routier_transbordement:
                            progress=i / (len(dict(s._fields['state_routier_transbordement'].selection))-2)*100
            s.progress = progress

    def compute_state(self, values):
        last_tracking = self.env['cps.voyage.tracking'].search([('voyage_id', '=', self.id)],order='id desc', limit=1)
        time_elapsed=0
        if len(last_tracking)>0:
            time_elapsed = (fields.Datetime.now()-last_tracking.date_tracking).total_seconds() / 60.0
        last_tracking.duree = time_elapsed
        if 'state_national' in values:
            if values['state_national']:
                self.env['cps.voyage.tracking'].create({'voyage_id': self.id,'date_tracking':fields.Datetime.now(),'description': dict(self._fields['state_national'].selection).get(self.state_national)})
                self.state_general = self.state_national
        elif 'state_cch' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_cch'].selection).get(self.state_cch)})
            self.state_general = self.state_cch
        elif 'state_dap' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_dap'].selection).get(self.state_dap)})
            self.state_general = self.state_dap
        elif 'state_fret' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_fret'].selection).get(self.state_fret)})
            self.state_general = self.state_fret
        elif 'state_obc' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_obc'].selection).get(self.state_obc)})
            self.state_general = self.state_obc
        elif 'state_charter_dtd' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_charter_dtd'].selection).get(self.state_charter_dtd)})
            self.state_general = self.state_charter_dtd
        elif 'state_routier' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_routier'].selection).get(self.state_routier)})
            self.state_general = self.state_routier
        elif 'state_routier_transbordement' in values:
            self.env['cps.voyage.tracking'].create({'voyage_id': self.id, 'date_tracking': fields.Datetime.now(), 'description': dict(self._fields['state_routier_transbordement'].selection).get(self.state_routier_transbordement)})
            self.state_general = self.state_routier_transbordement

    def calculer_resume(self):
        self.resume_ids.unlink()
        if self.cout_trajet > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description': "Cout du voyage ", 'cout': self.cout_trajet})
        if self.cout_sous_traitant_1 > 0:
            if len(self.vehicule_sous_traitant_1)>0:
                self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Sous-traitance véhicule " + self.vehicule_sous_traitant_1.vehicule_id.name , 'type_prestataire':'sous-traitant', 'client_id': self.vehicule_sous_traitant_1.soustraitant_id.id, 'cout': self.cout_sous_traitant_1})
        if self.cout_transitaire_1 > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de transit " , 'type_prestataire':'transit', 'client_id': self.dedouanement_1.id, 'cout': self.cout_transitaire_1})
        if self.cout_handling > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de handling " , 'type_prestataire':'aerienne', 'client_id': self.handling.id, 'cout': self.cout_handling})
        if self.cout_echange > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais d'échange " , 'type_prestataire':'aerienne', 'client_id': self.echange.id, 'cout': self.cout_echange})
        if self.cout_fret > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de fret " , 'type_prestataire':'aerienne', 'client_id': self.fret.id, 'cout': self.cout_fret})
        if self.cout_bagage > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais d'excedent de bagage' " , 'type_prestataire':'aerienne', 'client_id': self.fret.id, 'cout': self.cout_bagage})
        if self.frais_divers > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais divers' " , 'type_prestataire':'autre', 'cout': self.frais_divers})
        if self.cout_transitaire_2 > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de transit " , 'type_prestataire':'transit', 'client_id': self.dedouanement_2.id, 'cout': self.cout_transitaire_2})
        if self.cout_sous_traitant_2 > 0:
            if len(self.vehicule_sous_traitant_2)>0:
                self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Sous-traitance véhicule " + self.vehicule_sous_traitant_2.name , 'type_prestataire':'sous-traitant', 'client_id': self.vehicule_sous_traitant_2.soustraitant_id.id, 'cout': self.cout_sous_traitant_2})
        if self.cout_bateau > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de bateau " , 'type_prestataire':'maritine', 'client_id': self.bateau.id, 'cout': self.cout_bateau})
        if self.cout_transitaire_zf > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de transit en Z.F. ", 'type_prestataire':'transit', 'client_id': self.dedouanement_zf.id, 'cout': self.cout_transitaire_zf})
        if self.cout_transbordement > 0:
            self.env['cps.voyage.resume'].create({'voyage_id': self.id, 'description':"Frais de transbordement ", 'type_prestataire':'magasinnage', 'client_id': self.transbordement.id, 'cout': self.cout_transbordement})

    def action_generate_bill(self):
        # "creating cps facture"
        account_revenue = self.env['account.account'].search([('code', '=', '612630')])
        for p in self.resume_ids:
            if len(p.client_id) > 0:
                account_journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
                invoice = self.env['account.move'].create({
                    'partner_id': p.client_id.id,
                    'partner_shipping_id': p.client_id.id,
                    'journal_id': account_journal.id,
                    'move_type': 'in_invoice',
                    'invoice_date': fields.Datetime.now(),
                    'invoice_payment_term_id': p.client_id.property_supplier_payment_term_id.id,
                    'currency_id': self.currency_id.id,
                    'name': '/',
                    'voyage_id' : self.id,
                    'invoice_line_ids' : [],
                    'state': 'draft',

                })
                invoice_line = []
                invoice_line.append((0, 0, {
                                                'quantity': 1,
                                                'price_unit': p.cout,
                                                'name': p.description,
                                                'account_id': account_revenue.id,
                                                # 'tax_ids': [(6, 0, sol.tax_id.ids if tax_id is not False else [])],
                                                'sale_line_ids': [],
                                                # 'facturation_line_id': facture_line.id
                                            }),
                                    )
                invoice.write({'invoice_line_ids': invoice_line})

    def action_generate_invoice(self):
        # "creating cps facture"
        account_revenue = self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)], limit=1)
        if self.client_id is not False:
            account_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            invoice = self.env['account.move'].create({
                'partner_id': self.client_id.id,
                'partner_shipping_id': self.client_id.id,
                'journal_id': account_journal.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Datetime.now(),
                'invoice_payment_term_id': self.client_id.property_payment_term_id.id,
                'currency_id': self.currency_id.id,
                'voyage_id': self.id,
                'name': '/',
                'invoice_line_ids': [],
                'state': 'draft',

            })
            invoice_line = []
            invoice_line.append((0, 0, {
                'quantity': 1,
                'price_unit': self.prix,
                'name': self.trajet_id.name,
                'account_id': account_revenue.id,
                # 'tax_ids': [(6, 0, sol.tax_id.ids if tax_id is not False else [])],
                'sale_line_ids': [],
                # 'facturation_line_id': facture_line.id
            }),
                                )
            invoice.write({'invoice_line_ids': invoice_line})

    def compute_facture_achat_amount(self):
        total=0
        for f in self.facture_achat_ids:
            total+=f.amount_untaxed_signed
        self.total_facture_achats = -total

    def action_view_factures_achat(self):
        if len(self.facture_achat_ids) > 0:
            result = {
                'name': "Liste des factures d'achat",
                'res_model': 'account.move',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.facture_achat_ids.ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
            return result
        else :
            raise UserError(_("Aucune facture n'est encore disponible"))

    def compute_facture_vente_amount(self):
        total=0
        for f in self.facture_vente_ids:
            total+=f.amount_untaxed_signed
        self.total_facture_vente = total

    def action_view_factures_vente(self):
        if len(self.facture_achat_ids) > 0:
            result = {
                'name': "Liste des factures de vente",
                'res_model': 'account.move',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.facture_vente_ids.ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
            return result
        else :
            raise UserError(_("Aucune facture n'est encore disponible"))

    def action_view_vehicule_parc_1(self):
        result = {
            'name': "Liste des vehicules",
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', '=', self.vehicule_parc_1.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return result

    def action_view_vehicule_parc_2(self):
        result = {
            'name': "Liste des vehicules",
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', '=', self.vehicule_parc_2.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return result

    def action_view_vehicule_soustraitant_1(self):
        result = {
            'name': "Liste des vehicules",
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', '=', self.vehicule_sous_traitant_1.vehicule_id.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return result

    def action_view_vehicule_soustraitant_2(self):
        result = {
            'name': "Liste des vehicules",
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', '=', self.vehicule_sous_traitant_2.vehicule_id.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return result

    @api.depends('cout_trajet','cout_sous_traitant_1','cout_transitaire_1','cout_handling','cout_echange','cout_fret','cout_bagage','frais_divers','cout_transitaire_2','cout_sous_traitant_2','cout_bateau','cout_transitaire_zf','cout_transbordement')
    def compute_cout(self):
        for p in self:
            p.cout_total= p.cout_trajet+p.cout_sous_traitant_1+p.cout_transitaire_1+p.cout_handling+p.cout_echange + p.cout_fret + p.cout_bagage+ p.frais_divers+ p.cout_transitaire_2+ p.cout_sous_traitant_2+ p.cout_bateau+ p.cout_transitaire_zf+ p.cout_transbordement

    def set_price(self):
        for p in self:
            p.prix=p.cout_total+((p.cout_total*p.marge)/100)

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            res.append((rec.id, name))
        return res

    # def get_name(self):
    #     for s in self:
    #         name = ""
    #         if s.default_code is not False:
    #             name = name + s.default_code
    #         if s.trajet_id is not False:
    #             name += " / " + s.trajet_id.name
    #         return name

    @api.depends('trajet_id','default_code')
    def compute_name(self):
        for s in self:
            name = ""
            print('s.default_code-----------------------',s.default_code)
            print('s.trajet_id-----------------------',s.trajet_id)
            if s.default_code is not False:
                name = name + s.default_code
            if len(s.trajet_id)>0:
                name += " / " + str(s.trajet_id.name)
            s.name = name

    @api.onchange('type_voyage')
    def on_change_type_voyage(self):
        self.type_operation=""