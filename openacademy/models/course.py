from openerp import models, fields


class Course(models.Model):
    _name = "openacademy.course"
    # les champs de la table course
    titre = fields.Char(Required = True, string="Titre")
    description = fields.Text(string="Description")

    #session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sessions", Sessionrequired=False, ondelete = "set null")
    user_id = fields.Many2one(comodel_name="res.users", string="Responsable", ondelete = "set null")
