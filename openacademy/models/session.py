from datetime import timedelta
from openerp import models, fields, api, exceptions
from dateutil import parser

class Session(models.Model):
    _name = "openacademy.session"

    nom = fields.Char(Required = True, string="Nom")
    date_debut = fields.Date(string = "Debut", default =fields.Date.today)
    duree = fields.Integer(string="Duree")
    nb_place = fields.Integer(string="Places")
    percent_place = fields.Float(string="Places occupees (%)",  compute='pourcentage',)
    active = fields.Boolean(string="Active", default=True)
    date_fin = fields.Date(string="Fin", compute='date_fin_session', )
    heure = fields.Float(string="Nombre heures",  compute='session_heures')
    nb_participant = fields.Integer(string="Nombre de participants", compute='total_participant')
    color = fields.Integer(string="Couleur")

    state = fields.Selection(string="Etat",
                             selection=[('draft', "Brouillon"), ('confirmed', 'Confirme'),('done', 'Termine')],
                             default='draft',
                             readonly=True)

    course_id = fields.Many2one(comodel_name="openacademy.course", string="Course", required=True, ondelete = "cascade")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Instructeur",
                                 domain=['|',('instructor', '=', True),('category_id.name', 'in',('Teacher Level 1','Teacher level 2'))],
                                 ondelete = "cascade")
    participant_ids = fields.Many2many(comodel_name="res.partner", relation="session_participant_rel",
                                       column1="participant_id", column2="session_id", string="Participant",
                                       ondelete = "cascade")

    # @api.depends() should contain all fields that will be used in the calculations.
    @api.one
    @api.depends('nb_place', 'participant_ids')
    def pourcentage(self):
        if self.nb_place > 0 :
            self.percent_place = len(self.participant_ids)*100/self.nb_place
        else:
            self.percent_place = 0

    @api.one
    @api.depends('date_debut','duree')
    def date_fin_session(self):
        if self.date_debut and self.duree:
            if self.duree <= 0:
                self.date_fin = self.date_debut
            else:
                self.date_fin = parser.parse(self.date_debut) + timedelta(days=int(self.duree))

    @api.one
    @api.depends('duree')
    def session_heures(self):
        if self.duree <= 0:
            self.heure = 0
        else:
            self.heure = self.duree*24

    @api.one
    @api.depends('participant_ids')
    def total_participant(self):
        for record in self:
            record.nb_participant=len(record.participant_ids)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'
        print "hommmaaaaaaaaa"

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.onchange('nb_place','participant_ids')
    def _onchange_nb_place(self):
        if self.nb_place < 0:
            return {
                'warning':{
                    'title': "Nombre negatif",
                    'message': "Le nombre de places ne peut pas etre negatif",
                }
            }
        if len(self.participant_ids)>self.nb_place:
            return {
                'warning': {
                    'title': "Limite du nombre de participants",
                    'message': "Le nombre de participants pour cette session ne peut pas etre depasse",
                }
            }

    @api.constrains('partner_id','participant_ids')
    def _check_partnerInparticipants(self):
        for record in self:
            if record.partner_id in record.participant_ids:
                raise exceptions.ValidationError("Un instructeur ne peut pas etre un participant dans sa propre session")

