from openerp import models, fields


class Session(models.Model):
    _name = "openacademy.session"

    nom = fields.Char(Required = True, string="Nom")
    date_debut = fields.Date(string = "Debut")
    duree = fields.Integer(string="Duree")
    nb_place = fields.Integer(string="Places")

    course_id = fields.Many2one(comodel_name="openacademy.course", string="Course", required=True, ondelete = "set null")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Instructeur", ondelete = "set null")



