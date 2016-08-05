from openerp import models, fields, api


class Course(models.Model):
    _name = "openacademy.course"

    _rec_name="titre"
    # les champs de la table course
    titre = fields.Char(Required = True, string="Titre")
    description = fields.Text(string="Description")

    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sessions",
                                  required=False, ondelete = "set null")
    user_id = fields.Many2one(comodel_name="res.users", string="Responsable", ondelete = "set null")

    # Permet de dupliquer le cours ????
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('titre', '=like', u"Copy of {}%".format(self.titre))])
        if not copied_count:
            new_titre = u"Copy of {}".format(self.titre)
        else:
            new_titre = u"Copy of {} ({})".format(self.titre, copied_count)

        default['titre'] = new_titre
        return super(Course, self).copy(default)



    _sql_constraints = [
        (
            'titre_description_check',
            'CHECK titre != description',
            "le nom et la description du cours doivent etre differents"
        ),
        (
            'titre_unique_check',
            'unique(titre)',
            "Le titre du cours doit etre unique"
        ),
    ]

