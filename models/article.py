from odoo import fields, models, _


class Articles(models.Model):
    _name = 'article.article'
    _description = 'Articles'
    _inherit = ['portal.mixin', 'mail.thread',
        'mail.activity.mixin']
    _rec_name = 'title'

    author = fields.Many2one('res.partner', string='Author', default=lambda self: self.env.user.partner_id.id)
    assigned_to = fields.Many2one('res.partner', string='Assigned To')
    content = fields.Char(string='Content')
    title = fields.Char(string='Title')
    start_date = fields.Date(string='Start Date')
    publish_date = fields.Date('Publish Date')
    finished_date = fields.Date('Finished Date')
    is_article_manager = fields.Boolean('Manager', compute='_compute_is_article_manager')
    is_article_reader = fields.Boolean('Reader', compute='_compute_is_article_reader')
    deadline = fields.Date('Deadline')
    image = fields.Binary(string='Image')
    state = fields.Selection([('open', 'Open'), ('reading', 'reading'), ('read', 'read'), ('abandoned', 'abandoned')], default='open')

    def _compute_is_article_manager(self):
        for record in self:
            record.is_article_manager = self.env.user.has_group('content_manager.group_article_manager')
    
    def _compute_is_article_reader(self):
        for record in self:
            record.is_article_reader = self.env.user.has_group('content_manager.group_article_reader')

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'reading':
            vals['start_date'] = fields.Date.today()

        elif 'state' in vals and vals['state'] == 'read':
            author = self.author
            email_values = {'title': self.title, 'reader': self.assigned_to.name}

            template_id = self.env.ref('content_manager.article_mail_template').id
            template = self.env['mail.template'].browse(template_id)
            template.with_context(email_values).sudo().send_mail(author.id, force_send=True)

            vals['finished_date'] = fields.Date.today()

        res = super().write(vals)
        return res


    def action_reading(self):
        date = fields.Date.today()
        update_data = {
            'state':'reading',
            'start_date': date
        }
        self.write(update_data)

    def action_read(self):
        date = fields.Date.today()
        update_data = {
            'state': 'read',
            'finished_date': date
        }
        self.write(update_data)
    
    def action_abandoned(self):
        self.write({'state':'abandoned'})
