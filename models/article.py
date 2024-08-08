from odoo import api, fields, models, _

class Articles(models.Model):
    _name = 'article.article'
    _description = 'Articles'

    def get_reader_status(self):
        return self.env.user.has_group('article_manager.group_article_reader')
    
    def get_manager_status(self):
        return self.env.user.has_group('article_manager.group_article_manager')

    name = fields.Char()
    author = fields.Many2one('res.partner', string='Author', default=lambda self: self.env.user.partner_id.id)
    assigned_to = fields.Many2one('res.partner', string='Assigned To')
    content = fields.Char(string='Content')
    title = fields.Char(string='Title')
    start_date = fields.Date(string='Start Date')
    publish_date = fields.Date('Publish Date')
    finished_date = fields.Date('Finished Date')
    is_article_manager = fields.Boolean('Manager', store=False, default=lambda self: self.get_manager_status())
    is_article_reader = fields.Boolean('Reader', store=False, default=lambda self: self.get_reader_status())
    deadline = fields.Date('Deadline')
    image = fields.Binary(string='Image')
    state = fields.Selection([('open', 'Open'), ('reading', 'reading'), ('read', 'read'), ('abandoned', 'abandoned')], default='open')

    def action_reading(self):
        self.write({'state':'reading'})
        date = fields.Date.today()
        self.write({'start_date' : date})

    def action_read(self):
        self.write({'state':'read'})
        date = fields.Date.today()
        self.write({'finished_date' : date})
    
    def action_abandoned(self):
        self.write({'state':'abandoned'})

    
    @api.model_create_multi
    def create(self, values):
        for val in values:
            val['name'] = val['title']
        return super().create(values)
